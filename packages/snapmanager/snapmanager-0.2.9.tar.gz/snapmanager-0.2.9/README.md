# SnapManager

A tool for managing VSS-enabled snapshots in Google Cloud Platform. Currently supports restoring VSS snapshots and creating bootable VM instances from them.

## Features

- Restore VSS-enabled snapshots to bootable VM instances
- Handles all the complexity of making Windows disks bootable
- Clean and user-friendly command-line interface
- Detailed progress tracking and error reporting

## Prerequisites

- Python 3.8 or higher
- Google Cloud SDK
- Google Cloud Service Account with the following permissions:
  - `roles/compute.instanceAdmin.v1`
  - `roles/compute.networkAdmin`
  - `roles/compute.securityAdmin`

## Authentication

SnapManager uses Google Cloud Application Default Credentials for authentication. You can set this up in one of two ways:

1. **Service Account Key File (Recommended for production)**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```

2. **User Credentials (Good for development)**:
   ```bash
   gcloud auth application-default login
   ```

## Installation

```bash
pip install snapmanager
```

## Usage

```bash
# Show help
snapmanager restore --help

# Restore a VSS snapshot
snapmanager restore \
  --project YOUR_PROJECT_ID \
  --zone ZONE \
  --vpc-network NETWORK_NAME \
  --subnet SUBNET_NAME \
  --snapshot SNAPSHOT_NAME
```

### Command Arguments

- `--project`: Google Cloud project ID where the snapshot and new VM will be created
- `--zone`: Google Cloud zone where the new VM will be created
- `--vpc-network`: VPC network to attach the new VM to
- `--subnet`: Subnet within the VPC network for the new VM
- `--snapshot`: Name of the VSS-enabled snapshot to restore from
- `--verbose`: Show detailed progress information for each step

## How It Works

1. Creates a temporary Windows Server VM in the specified VPC network and subnet
2. Creates a firewall rule to allow WinRM (port 5986) access to the temporary VM
3. Attaches the disk created from the VSS snapshot to the temporary VM
4. Configures Windows boot configuration using the temporary VM
5. Detaches the disk from the temporary VM
6. Deletes the temporary VM

## Example

```bash
snapmanager restore \
  --project my-project \
  --zone europe-west1-b \
  --vpc-network default \
  --subnet default \
  --snapshot my-windows-vss-snapshot
```

This will:
1. Create a new disk from the VSS snapshot
2. Create a temporary VM to make the disk bootable
3. Run necessary Windows boot configuration commands
4. Create a final VM with the bootable disk
5. Clean up temporary resources

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
