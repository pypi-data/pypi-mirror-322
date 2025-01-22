import logging
import time
import socket
import base64
from dataclasses import dataclass
from typing import Optional

import winrm
from winrm.exceptions import WinRMOperationTimeoutError, WinRMTransportError

from snapmanager.core.types import StepResult
from snapmanager.utils.ui import UIController

logger = logging.getLogger(__name__)

@dataclass
class CommandResult:
    """Result of a command execution"""
    success: bool
    message: str = ""
    stdout: str = ""
    stderr: str = ""

def encode_powershell_command(command: str) -> str:
    """Encode PowerShell command in base64"""
    encoded = base64.b64encode(command.encode('utf-16-le')).decode('ascii')
    return encoded

class WinRMClient:
    """Client for Windows Remote Management operations"""
    
    def __init__(self, hostname: str, username: str, password: str, ui_manager: Optional[UIController] = None):
        """Initialize WinRM client."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ui = ui_manager
        self.session = None
        
        self.protocol = 'http'
        self.port = 5985
        self.timeout = 30
        self.max_retries = 30
        self.retry_delay = 15
        
        self.winrm_session = None
    
    def _create_session(self):
        """Create a new WinRM session"""
        if not self.session:
            self.session = winrm.Session(
                target=self.hostname,
                auth=(self.username, self.password),
                transport="ntlm",
                server_cert_validation="ignore"
            )
    
    def check_port_open(self, max_attempts: int = 30) -> bool:
        """Check if WinRM port is open using socket connection"""
        logger.info(f"Checking if WinRM port is open on {self.hostname}...")
        
        for attempt in range(max_attempts):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.hostname, 5985))
                sock.close()
                
                if result == 0:
                    logger.info("WinRM port is open")
                    return True
                    
                logger.debug(f"Waiting for WinRM port to open ({attempt + 1}/{max_attempts})")
                time.sleep(10)
                
            except Exception as e:
                logger.debug(f"Failed to connect to WinRM port ({attempt + 1}/{max_attempts}): {str(e)}")
                time.sleep(10)
                
        error_msg = "Timed out waiting for WinRM port to open"
        logger.error(error_msg)
        return False
    
    def wait_for_winrm(self, max_attempts: int = 30) -> bool:
        """Wait for WinRM to become available"""
        try:
            if not self.check_port_open():
                return False
                
            logger.info("Waiting for WinRM service to become available...")
            test_command = "Write-Host 'WinRM is ready'"
            
            for attempt in range(max_attempts):
                try:
                    result = self.run_command(test_command)
                    if result.success:
                        logger.info("WinRM service is now available")
                        return True
                        
                    logger.debug(f"Waiting for WinRM service ({attempt + 1}/{max_attempts})")
                    time.sleep(10)
                    
                except Exception as e:
                    logger.debug(f"Failed to connect to WinRM service ({attempt + 1}/{max_attempts}): {str(e)}")
                    time.sleep(10)
                    
            error_msg = "Timed out waiting for WinRM service"
            logger.error(error_msg)
            return False
            
        except Exception as e:
            error_msg = f"Error while waiting for WinRM: {str(e)}"
            logger.error(error_msg)
            return False
    
    def run_command(self, command: str, shell: str = "powershell") -> CommandResult:
        """Run a command using WinRM"""
        try:
            self._create_session()
            shell_id = self.session.protocol.open_shell()
            
            try:
                if shell == "powershell":
                    command = f"""
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
try {{
    {command}
}} catch {{
    Write-Error $_
    exit 1
}}
"""
                    encoded_command = encode_powershell_command(command)
                    command_id = self.session.protocol.run_command(
                        shell_id, 
                        'powershell.exe', 
                        ['-EncodedCommand', encoded_command]
                    )
                else:
                    command_id = self.session.protocol.run_command(shell_id, command)
                
                stdout, stderr, status_code = self.session.protocol.get_command_output(shell_id, command_id)
                self.session.protocol.cleanup_command(shell_id, command_id)
                
                success = status_code == 0
                stdout_str = stdout.decode('utf-8', errors='ignore')
                stderr_str = stderr.decode('utf-8', errors='ignore')
                
                if success:
                    logger.debug(f"Command succeeded with output: {stdout_str}")
                else:
                    logger.error(f"Command failed with error: {stderr_str}")
                    
                return CommandResult(
                    success=success,
                    message=stderr_str if not success else stdout_str,
                    stdout=stdout_str,
                    stderr=stderr_str
                )
                
            finally:
                self.session.protocol.close_shell(shell_id)
                
        except Exception as e:
            logger.error(f"Failed to execute command: {str(e)}")
            return CommandResult(
                success=False,
                message=str(e),
                stdout="",
                stderr=str(e)
            )

    def __del__(self):
        """Clean up resources."""
        pass
