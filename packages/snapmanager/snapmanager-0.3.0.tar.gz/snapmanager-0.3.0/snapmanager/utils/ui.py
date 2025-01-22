import time
import threading
import signal
import logging
import os
import sys
from typing import Optional, Dict, Any
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from rich import box
from snapmanager import __version__

console = Console()

class UIController:
    """Controls UI elements, state and user interactions."""
    
    def __init__(self):
        """Initialize UI controller."""
        self.current_step = ""
        self.original_step = ""
        self.current_message = ""
        self.message_time = 0
        self.current_stage = None
        self.current_substage = None
        self.substage_message = None
        self.substage_buffer = {}
        self.completed_stages = []
        self.stage_order = []
        self.spinner = Spinner("dots")
        self.dots_count = 0
        self.last_update = 0
        self.dot_interval = 0.5
        self.verbose = False
        self.live = Live("", console=console, refresh_per_second=4, transient=True)
        self._stop_thread = False
        self._spinner_thread = None
        
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def set_verbose(self, verbose: bool) -> None:
        """Set verbose mode."""
        self.verbose = verbose
    
    def start(self) -> None:
        """Start the UI controller."""
        if not self.verbose and not self.live.is_started:
            self.live.start()
            self._stop_thread = False
            self._spinner_thread = threading.Thread(target=self._update_spinner)
            self._spinner_thread.daemon = True
            self._spinner_thread.start()
    
    def stop(self) -> None:
        """Stop the UI controller."""
        self._stop_thread = True
        if self._spinner_thread:
            self._spinner_thread.join(timeout=0.2)
        if hasattr(self, 'live') and self.live.is_started:
            self.live.stop()
    
    def _cleanup(self):
        """Clean up resources."""
        self.stop()
    
    def _get_dots(self, now: float) -> str:
        """Animasyonlu nokta dizisi oluştur."""
        if now - self.last_update >= self.dot_interval:
            self.dots_count = (self.dots_count + 1) % 4
            self.last_update = now
        return "." * self.dots_count
    
    def _render_step(self) -> str:
        """Render current step."""
        output = []
        now = time.time()
        
        for stage in self.completed_stages:
            if isinstance(stage, list):
                output.extend(stage)
            else:
                output.append(stage)
        
        if self.current_step:
            dots = self._get_dots(now) if not self.verbose else ""
            current_line = f"[yellow]{self.spinner.render(now)}[/] [yellow]{self.original_step}[/]"
            if self.current_message:
                current_line += f": {self.current_message}{dots}"
            else:
                current_line += f"{dots}"
            output.append(current_line)
            
            if self.current_stage in self.substage_buffer:
                output.extend(self.substage_buffer[self.current_stage])
            
            if self.current_substage:
                substage_line = f"  [yellow]{self.spinner.render(now)}[/] [yellow]{self.current_substage}[/]"
                if self.substage_message:
                    substage_line += f": {self.substage_message}"
                output.append(substage_line)
        
        return "\n".join(output)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signal."""
        self._cleanup()
        sys.exit(1)
    
    def _update_spinner(self):
        """Update spinner in a separate thread."""
        while not self._stop_thread and self.live and self.live.is_started:
            self.live.update(self._render_step())
            time.sleep(0.1)
    
    def print_step_status(self, step_name: str, status: str = "pending", message: str = "") -> None:
        """Print step status with appropriate symbol."""
        if status == "pending":
            self.current_step = step_name
            self.original_step = step_name
            self.current_stage = step_name
            self.current_substage = None
            self.substage_message = None
            self.substage_buffer[step_name] = []
            if step_name not in self.stage_order:
                self.stage_order.append(step_name)
            
            if not self.verbose:
                if not self.live.is_started:
                    self.start()
            else:
                console.print(f"[yellow]⠋[/] [yellow]{step_name}[/]")
            
            if message:
                self.current_message = message
                self.message_time = time.time()
            return
        
        if status == "success":
            completed_output = [f"[green]✓[/] [green]{step_name}[/]"]
            if step_name in self.substage_buffer:
                completed_output.extend(self.substage_buffer[step_name])
                
            insert_pos = self.stage_order.index(step_name)
            
            if insert_pos < len(self.completed_stages):
                self.completed_stages = [stage for stage in self.completed_stages if 
                                      (isinstance(stage, list) and stage[0] != f"[green]✓[/] [green]{step_name}[/]") or
                                      (isinstance(stage, str) and stage != f"[green]✓[/] [green]{step_name}[/]")]
                self.completed_stages.insert(insert_pos, completed_output)
            else:
                self.completed_stages.append(completed_output)
                
        elif status == "error":
            error_msg = f"[red]✗[/] [red]{step_name}[/]" + (f": [red]{message}[/]" if message else "")
            
            if self.live and self.live.is_started:
                self.live.stop()
            
            console.print(f"\n{error_msg}")
        else:
            info_msg = f"[blue]ℹ[/] [blue]{step_name}[/]" + (f": [blue]{message}[/]" if message else "")
            insert_pos = self.stage_order.index(step_name)
            if insert_pos >= len(self.completed_stages):
                self.completed_stages.append([info_msg])
            else:
                self.completed_stages.insert(insert_pos, [info_msg])
        
        if step_name == self.current_step:
            if step_name == self.current_stage:
                self.current_stage = None
            self.current_step = ""
            self.current_message = ""
            self.original_step = ""
            self.current_substage = None
            self.substage_message = None
    
    def print_substage(self, stage_name: str, substage_name: str, status: str = "pending", message: Optional[str] = None):
        """Print a substage status."""
        if status == "pending":
            if self.current_stage != stage_name:
                self.current_stage = stage_name
                if stage_name not in self.substage_buffer:
                    self.substage_buffer[stage_name] = []
            
            self.current_substage = substage_name
            self.substage_message = message
            self.message_time = time.time()
            
            if not self.verbose:
                if not self.live.is_started:
                    self.start()
            else:
                console.print(f"  [yellow]⠋[/] [yellow]{substage_name}[/]")
        elif status == "success":
            if stage_name == self.current_stage:
                substage_line = f"  [green]✓[/] [green]{substage_name}[/]"
                if stage_name not in self.substage_buffer:
                    self.substage_buffer[stage_name] = []
                if substage_line not in self.substage_buffer[stage_name]:
                    self.substage_buffer[stage_name].append(substage_line)
                    if self.current_substage == substage_name:
                        self.current_substage = None
                        self.substage_message = None
                    
                    if self.verbose:
                        console.print(substage_line)
        elif status == "error":
            if stage_name == self.current_stage:
                substage_line = f"  [red]✗[/] [red]{substage_name}[/]" + (f": [red]{message}[/]" if message else "")
                if stage_name not in self.substage_buffer:
                    self.substage_buffer[stage_name] = []
                if substage_line not in self.substage_buffer[stage_name]:
                    self.substage_buffer[stage_name].append(substage_line)
                    if self.current_substage == substage_name:
                        self.current_substage = None
                        self.substage_message = None
                    
                    if self.verbose:
                        console.print(substage_line)
    
    def print_message(self, message: str):
        """Print a message in the current stage."""
        if not self.current_stage:
            return
            
        if not self.verbose:
            if self.live and self.live.is_started:
                self.current_message = message
                self.message_time = time.time()
        else:
            console.print(message)
    
    def print_banner(self) -> None:
        """Print application banner."""
        console.print()
        console.print("[bold magenta]SnapManager[/] [dim]v{}[/]".format(__version__))
        console.print("[dim]Makes VSS snapshot disks bootable in Google Cloud[/]")
        console.print()


    def print_operation_complete(self, duration: float, results: Optional[Dict[str, Any]] = None) -> None:
        """Print operation completion message with duration and optional results."""

        self._cleanup()
        
        for stage_output in self.completed_stages:
            console.print("\n".join(stage_output))
        
        minutes = int(duration / 60)
        seconds = int(duration % 60)
        
        console.print()
        if results and "Status" in results and results["Status"] == "Failed":
            console.print(Text("❌ Operation failed", style="red bold"))
            if "Error" in results:
                console.print(Text(f"Error: {results['Error']}", style="red"))
            if "Details" in results:
                console.print(Text(f"Details: {results['Details']}", style="red"))
        else:
            console.print(Text("Snapshot restored successfully", style="green bold"))
        
        console.print(Text(f"Duration: {minutes}m {seconds}s", style="white"))
        
        if results:
            console.print()
            for key, value in results.items():
                if key not in ["Error", "Details", "Status"]:
                    console.print(Text(f"{key}: ", style="cyan"), Text(str(value), style="white"))
    
    def print_results(self, results: Dict[str, Any]):
        """Print results in a table format."""
        with console.status("[bold green]Processing..."):
            for key, value in results.items():
                console.print(Text(f"{key}: ", style="cyan"), Text(str(value), style="white"))
    
    def __del__(self):
        """Ensure live display is stopped."""
        self._cleanup()


class UILogHandler(logging.Handler):
    """Handler for logging to UI."""
    
    def __init__(self, ui_controller, formatter=None):
        """Initialize UI log handler."""
        super().__init__()
        self.ui_controller = ui_controller
        if formatter:
            self.setFormatter(formatter)
    
    def emit(self, record):
        """Emit a log record."""
        try:
            if record.levelno >= logging.ERROR:
                msg = self.formatter.format(record) if self.formatter else record.getMessage()
                console.print(f"[red]{msg}[/red]")
                return
                
            if self.ui_controller.verbose:
                msg = self.formatter.format(record) if self.formatter else record.getMessage()
                console.print(msg)
            else:
                self.ui_controller.print_message(record.getMessage())
        except Exception:
            self.handleError(record)
