import logging
import random
import string
import time
from typing import Optional, Dict, Any, List

from google.cloud import compute_v1
from google.api_core import extended_operation

from snapmanager.core.types import StepResult
from snapmanager.utils.ui import UIController

logger = logging.getLogger(__name__)

def generate_strong_password(length: int = 16) -> str:
    """Generate a strong random password."""

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*"
    
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(length - 4))
    
    random.shuffle(password)
    return "".join(password)

class ComputeClient:
    """Client for Google Cloud Compute Engine operations."""
    
    def __init__(self, project: str, zone: str, ui_manager: Optional[UIController] = None):
        """Initialize compute client."""
        self.project = project
        self.zone = zone
        self.ui = ui_manager
        self.disks_client = compute_v1.DisksClient()
        self.zone_operations_client = compute_v1.ZoneOperationsClient()
        self.instances_client = compute_v1.InstancesClient()
        self.firewalls_client = compute_v1.FirewallsClient()
    
    def __del__(self):
        """Clean up resources."""
        pass
    
    def _handle_rate_limit(self, operation, max_attempts: int = 3, initial_delay: float = 5.0):
        """Rate limit'e takıldığında retry yap."""
        attempt = 0
        delay = initial_delay
        
        while attempt < max_attempts:
            try:
                return operation()
            except Exception as e:
                if "Operation rate exceeded" in str(e) and attempt < max_attempts - 1:
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                    attempt += 1
                    continue
                raise
        
        return operation()
    
    def create_disk_from_snapshot(self, disk_name: str, snapshot_name: str) -> Optional[compute_v1.Operation]:
        """Create a disk from a snapshot"""
        try:
            disk_size = self.get_snapshot_size(snapshot_name)
            if not disk_size:
                logger.error("Failed to get snapshot size")
                return None
                
            logger.info(f"Creating disk with size {disk_size}GB from snapshot")
            
            disk = compute_v1.Disk()
            disk.name = disk_name
            disk.size_gb = disk_size
            disk.source_snapshot = f"projects/{self.project}/global/snapshots/{snapshot_name}"
            disk.type_ = f"projects/{self.project}/zones/{self.zone}/diskTypes/pd-balanced"
            
            logger.info(f"Creating disk '{disk_name}' from snapshot '{snapshot_name}'")
            logger.debug(f"Disk config: {disk}")
            
            operation = self.disks_client.insert(
                project=self.project,
                zone=self.zone,
                disk_resource=disk
            )
            
            return operation
            
        except Exception as e:
            logger.error(f"Failed to create disk: {str(e)}")
            raise
    
    def create_temp_vm(self, name: str, machine_type: str, disk_name: str,
                   network: str, subnetwork: Optional[str] = None,
                   password: Optional[str] = None) -> Optional[compute_v1.Operation]:
        """Create a temporary VM with the specified disk attached"""
        try:
            logger.info(f"Creating VM {name} with disk {disk_name}")
            
            instance = compute_v1.Instance()
            instance.name = name
            instance.machine_type = f"projects/{self.project}/zones/{self.zone}/machineTypes/{machine_type}"
            
            instance.tags = compute_v1.Tags()
            instance.tags.items = ["allow-winrm"]
            
            boot_disk = compute_v1.AttachedDisk()
            boot_disk.auto_delete = True
            boot_disk.boot = True
            
            initialize_params = compute_v1.AttachedDiskInitializeParams()
            initialize_params.source_image = "projects/windows-cloud/global/images/windows-server-2019-dc-v20231011"
            initialize_params.disk_size_gb = 50
            boot_disk.initialize_params = initialize_params
            
            additional_disk = compute_v1.AttachedDisk()
            additional_disk.source = f"projects/{self.project}/zones/{self.zone}/disks/{disk_name}"
            additional_disk.auto_delete = False
            additional_disk.boot = False
            additional_disk.device_name = disk_name
            
            instance.disks = [boot_disk, additional_disk]
            
            network_interface = compute_v1.NetworkInterface()
            network_interface.network = f"projects/{self.project}/global/networks/{network}"
            if subnetwork:
                region = self.zone.rsplit("-", 1)[0]
                subnet_name = "k8s-subnet" if subnetwork == "k8s-net" else subnetwork
                network_interface.subnetwork = f"projects/{self.project}/regions/{region}/subnetworks/{subnet_name}"
            
            access_config = compute_v1.AccessConfig()
            access_config.name = "External NAT"
            access_config.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT.name
            network_interface.access_configs = [access_config]
        
            instance.network_interfaces = [network_interface]
            
            items = []
            if password:
                items.append(compute_v1.Items(
                    key="sysprep-specialize-script-ps1",
                    value=f"""$password = '{password}'
$admin = [ADSI]('WinNT://./Administrator')
$admin.SetPassword($password)
$admin.SetInfo()

$computer = [ADSI]"WinNT://."
$admin = $computer.Children.Find("Administrator")
$admin.UserFlags.value = $admin.UserFlags.value -band (-bnot 0x2)  # Remove ACCOUNTDISABLE flag
$admin.SetInfo()

net user Administrator /active:yes"""
                ))
            
            items.append(compute_v1.Items(
                key="windows-startup-script-ps1",
                value=r"""# Enable WinRM
Enable-PSRemoting -Force
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "*" -Force
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Open WinRM port
New-NetFirewallRule -Name "Allow WinRM HTTP" -DisplayName "Allow WinRM HTTP" -Protocol TCP -LocalPort 5985 -Action Allow -Direction Inbound

# Set execution policy
Set-ExecutionPolicy Unrestricted -Force"""
            ))
            
            metadata = compute_v1.Metadata()
            metadata.items = items
            instance.metadata = metadata
                
            logger.info(f"Creating VM '{name}' with disk '{disk_name}'")
            logger.debug(f"VM config: {instance}")
            
            operation = self.instances_client.insert(
                project=self.project,
                zone=self.zone,
                instance_resource=instance
            )
            
            return operation
            
        except Exception as e:
            logger.error(f"Failed to create VM: {str(e)}")
            raise
    
    def create_restored_vm(self, name: str, machine_type: str, boot_disk_name: str,
                      network: str, subnetwork: Optional[str] = None,
                      password: Optional[str] = None) -> Optional[compute_v1.Operation]:
        """Create the final restored VM with the bootable disk as boot disk"""
        try:
            logger.info(f"Creating restored VM {name} with boot disk {boot_disk_name}")
            
            instance = compute_v1.Instance()
            instance.name = name
            instance.machine_type = f"projects/{self.project}/zones/{self.zone}/machineTypes/{machine_type}"
            
            boot_disk = compute_v1.AttachedDisk()
            boot_disk.source = f"projects/{self.project}/zones/{self.zone}/disks/{boot_disk_name}"
            boot_disk.auto_delete = False
            boot_disk.boot = True
            boot_disk.device_name = boot_disk_name
            
            instance.disks = [boot_disk]
            
            network_interface = compute_v1.NetworkInterface()
            network_interface.network = f"projects/{self.project}/global/networks/{network}"
            if subnetwork:
                region = self.zone.rsplit("-", 1)[0]
                subnet_name = "k8s-subnet" if subnetwork == "k8s-net" else subnetwork
                network_interface.subnetwork = f"projects/{self.project}/regions/{region}/subnetworks/{subnet_name}"
            
            access_config = compute_v1.AccessConfig()
            access_config.name = "External NAT"
            access_config.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT.name
            network_interface.access_configs = [access_config]
        
            instance.network_interfaces = [network_interface]
                
            logger.info(f"Creating restored VM '{name}' with boot disk '{boot_disk_name}'")
            logger.debug(f"VM config: {instance}")
            
            operation = self.instances_client.insert(
                project=self.project,
                zone=self.zone,
                instance_resource=instance
            )
            
            return operation
            
        except Exception as e:
            logger.error(f"Failed to create restored VM: {str(e)}")
            raise
    
    def get_instance(self, instance_name: str) -> compute_v1.Instance:
        """Get instance by name."""
        try:
            logger.info(f"Getting instance {instance_name}")
            return self.instances_client.get(
                project=self.project,
                zone=self.zone,
                instance=instance_name
            )
        except Exception as e:
            logger.error(f"Failed to get instance {instance_name}: {str(e)}")
            raise
    
    def wait_for_operation(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Wait for a GCP operation to complete."""
        try:
            result = operation.result()
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_snapshot_size(self, snapshot_name: str) -> Optional[int]:
        """Get the size of a snapshot in GB."""
        try:
            logger.info(f"Getting size of snapshot {snapshot_name}")
            snapshots_client = compute_v1.SnapshotsClient()
            snapshot = snapshots_client.get(project=self.project, snapshot=snapshot_name)
            return snapshot.disk_size_gb
        except Exception as e:
            logger.error(f"Failed to get snapshot size: {str(e)}")
            raise

    def detach_disk(self, instance_name: str, disk_name: str) -> Optional[compute_v1.Operation]:
        """Detach a disk from an instance."""
        try:
            logger.info(f"Detaching disk '{disk_name}' from instance '{instance_name}'")
            
            request = compute_v1.DetachDiskInstanceRequest()
            request.project = self.project
            request.zone = self.zone
            request.instance = instance_name
            request.device_name = disk_name
            
            operation = self.instances_client.detach_disk(request)
            return operation
            
        except Exception as e:
            logger.error(f"Failed to detach disk: {str(e)}")
            raise

    def delete_instance(self, instance_name: str) -> Optional[compute_v1.Operation]:
        """Delete a compute instance."""
        try:
            request = compute_v1.DeleteInstanceRequest(
                project=self.project,
                zone=self.zone,
                instance=instance_name
            )
            return self.instances_client.delete(request)
        except Exception as e:
            logger.error(f"Failed to delete instance '{instance_name}': {str(e)}")
            return None

    def create_winrm_firewall_rule(self, network: str) -> Dict[str, Any]:
        """Create firewall rule for WinRM port.
        
        Args:
            network: VPC network name
            
        Returns:
            Operation result
        """
        try:
            firewall_rule_name = "allow-winrm"
            
            try:
                logger.info(f"Checking if firewall rule '{firewall_rule_name}' exists")
                self.firewalls_client.get(
                    project=self.project,
                    firewall=firewall_rule_name
                )
                logger.info(f"Firewall rule '{firewall_rule_name}' already exists")
                return {"success": True, "message": "Firewall rule already exists"}
            except Exception as e:
                logger.info(f"Firewall rule does not exist, will create: {str(e)}")
                pass
            
            logger.info("Creating firewall rule object")
            firewall_rule = compute_v1.Firewall()
            firewall_rule.name = firewall_rule_name
            firewall_rule.network = f'projects/{self.project}/global/networks/{network}'
            firewall_rule.direction = "INGRESS"
            
            allowed = compute_v1.Allowed()
            allowed.I_p_protocol = "tcp"
            allowed.ports = ["5985"]
            
            firewall_rule.allowed = [allowed]
            firewall_rule.source_ranges = ["0.0.0.0/0"]
            firewall_rule.target_tags = ["allow-winrm"]
            firewall_rule.description = "Allow WinRM HTTPS traffic"
            
            logger.debug(f"Inserting firewall rule with config: {firewall_rule}")
            operation = self.firewalls_client.insert(
                project=self.project,
                firewall_resource=firewall_rule
            )
            
            logger.info(f"Creating firewall rule '{firewall_rule_name}'")
            try:
                logger.info("Waiting for operation result")
                result = operation.result()
                logger.info("Firewall rule created successfully")
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Operation failed: {str(e)}", exc_info=True)
                return {"success": False, "error": str(e)}
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to create firewall rule: {error_msg}", exc_info=True)
            return {"success": False, "error": error_msg}

    def delete_winrm_firewall_rule(self) -> Dict[str, Any]:
        """Delete WinRM firewall rule.
        
        Returns:
            Operation result
        """
        try:
            firewall_rule_name = "allow-winrm"
            
            try:
                logger.info(f"Attempting to delete firewall rule: {firewall_rule_name}")
                operation = self.firewalls_client.delete(
                    project=self.project,
                    firewall=firewall_rule_name
                )
                
                logger.info(f"Deleting firewall rule '{firewall_rule_name}'")
                try:
                    logger.info("Waiting for operation result")
                    result = operation.result()
                    logger.info("Firewall rule deleted successfully")
                    return {"success": True, "result": result}
                except Exception as e:
                    logger.error(f"Operation failed: {str(e)}", exc_info=True)
                    return {"success": False, "error": str(e)}
                
            except Exception as e:
                if "not found" in str(e).lower():
                    logger.info(f"Firewall rule '{firewall_rule_name}' does not exist")
                    return {"success": True, "message": "Firewall rule does not exist"}
                logger.error(f"Failed to delete firewall rule: {str(e)}", exc_info=True)
                raise
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to delete firewall rule: {error_msg}", exc_info=True)
            return {"success": False, "error": error_msg}
