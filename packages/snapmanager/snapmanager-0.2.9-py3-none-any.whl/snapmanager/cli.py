"""Command line interface for VSS restore tool."""
import argparse
import logging
import os
import sys
from typing import Optional

from rich.console import Console

from snapmanager import __version__
from snapmanager.core.types import RestoreConfig
from snapmanager.core.manager import SnapManager
from snapmanager.utils.compute import generate_strong_password
from snapmanager.utils.ui import UILogHandler, UIController

logger = logging.getLogger(__name__)
console = Console()


def setup_logging(verbose: bool, ui_controller: UIController) -> None:
    """Configure logging settings."""
    log_format = '%(asctime)s|%(levelname)s|%(name)s|%(message)s'
    formatter = logging.Formatter(log_format)
    
    if not verbose:
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('urllib3.util').setLevel(logging.WARNING)
        logging.getLogger('urllib3.util.retry').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
        
        logging.getLogger('google').setLevel(logging.DEBUG)
        logging.getLogger('google.auth').setLevel(logging.WARNING)
        logging.getLogger('google.auth._default').setLevel(logging.WARNING)
        logging.getLogger('google.cloud').setLevel(logging.DEBUG)
    else:
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('urllib3.util').setLevel(logging.WARNING)
        logging.getLogger('urllib3.util.retry').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.DEBUG)
        
        logging.getLogger('google').setLevel(logging.DEBUG)
        logging.getLogger('google.auth').setLevel(logging.WARNING)
        logging.getLogger('google.auth._default').setLevel(logging.WARNING)
        logging.getLogger('google.cloud').setLevel(logging.DEBUG)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    ui_controller.set_verbose(verbose)
    
    ui_handler = UILogHandler(ui_controller, formatter=formatter)
    ui_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    root_logger.addHandler(ui_handler)
    
    log_file = os.path.expanduser('~/.snapmanager/snapmanager.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)


def restore_command(args: argparse.Namespace) -> None:
    """Restore a VSS snapshot disk and make it bootable."""
    try:
        ui_controller = UIController()
        setup_logging(args.verbose, ui_controller)
        
        # Fixed values
        machine_type = "n1-standard2"
        windows_password = generate_strong_password()

        config = RestoreConfig(
            project=args.project,
            zone=args.zone,
            snapshot_name=args.snapshot,
            vpc_network=args.vpc_network,
            subnet=args.subnet,
            machine_type=machine_type,
            windows_password=windows_password,
            verbose=args.verbose
        )
        
        manager = SnapManager(config, ui_controller=ui_controller)
        success = manager.run()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        sys.exit(1)


class UILogHandler(logging.Handler):
    """Custom logging handler that forwards messages to the UI controller."""
    
    def __init__(self, ui_controller: UIController, formatter: Optional[logging.Formatter] = None):
        super().__init__()
        self.ui = ui_controller
        if formatter:
            self.setFormatter(formatter)
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            if "Snapshot restore operation" in record.msg and "completed successfully" in record.msg:
                return
                
            if not self.ui.verbose:
                self.ui.print_message(record.msg)
            else:
                msg = self.format(record)
                self.ui.print_message(msg)
        except Exception:
            self.handleError(record)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SnapManager - Manage VSS snapshots in Google Cloud"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"SnapManager v{__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    restore_parser = subparsers.add_parser(
        "restore", 
        help="Restore a VSS snapshot disk and make it bootable",
        description="Restore a VSS snapshot disk and create a new bootable VM instance from it."
    )
    restore_parser.add_argument(
        "--project",
        required=True,
        help="Google Cloud project ID where the snapshot and new VM will be created"
    )
    restore_parser.add_argument(
        "--zone",
        required=True,
        help="Google Cloud zone where the new VM will be created"
    )
    restore_parser.add_argument(
        "--vpc-network",
        required=True,
        help="VPC network to attach the new VM to"
    )
    restore_parser.add_argument(
        "--subnet",
        required=True,
        help="Subnet within the VPC network for the new VM"
    )
    restore_parser.add_argument(
        "--snapshot",
        required=True,
        help="Name of the VSS-enabled snapshot to restore from"
    )
    restore_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.command == "restore":
        restore_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
