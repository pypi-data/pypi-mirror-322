from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class StepResult:
    """Result of a restore step."""
    success: bool
    message: str = ""
    output: Optional[str] = None
    results: Optional[Dict[str, Any]] = None

class WindowsError(Exception):
    """Exception raised for Windows-specific errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

@dataclass
class RestoreConfig:
    """Configuration for restore operation."""
    project: str
    zone: str
    snapshot_name: str
    vpc_network: str
    subnet: Optional[str] = None
    machine_type: str = "e2-medium"
    windows_password: Optional[str] = None
    boot_disk_image: str = "projects/windows-cloud/global/images/windows-server-2019-dc-v20231011"
    verbose: bool = False
