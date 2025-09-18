# AssetTrack Deployment Setup

This guide covers the complete setup for deploying AssetTrack to Azure using GitHub Actions.

## Prerequisites

1. **Azure CLI** installed and configured
2. **Terraform** installed
3. **GitHub repository** with the following secrets configured:
   - `GHCR_TOKEN`: GitHub Container Registry token
   - `VM_HOST`: Azure VM public IP address
   - `VM_SSH_KEY`: Private SSH key for VM access
   - `VM_SSH_USER`: SSH username (default: azureuser)

## Infrastructure Setup

### 1. Deploy Infrastructure with Terraform

```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the infrastructure
terraform apply
```

### 2. Get VM IP Address

After successful deployment, get the VM IP:

```bash
terraform output vm_public_ip
```

### 3. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

- `GHCR_TOKEN`: Create a Personal Access Token with `write:packages` permission
- `VM_HOST`: The output from `terraform output vm_public_ip`
- `VM_SSH_KEY`: Your private SSH key content
- `VM_SSH_USER`: `azureuser`

### 4. Copy Deployment Files to VM

SSH into the VM and copy the deployment files:

```bash
# SSH into the VM
ssh azureuser@$(terraform output -raw vm_public_ip)

# Create app directory
mkdir -p /home/azureuser/app

# Copy deployment files (you'll need to do this manually or via scp)
# The deploy/ directory should be copied to /home/azureuser/app/
```

## Deployment Process

1. **Push to main branch**: The GitHub Action will automatically trigger
2. **Build & Push**: Docker image is built and pushed to GHCR
3. **Deploy**: The action SSH into the VM and deploys the new image
4. **Access**: Application will be available at `http://<VM_IP>`

## Manual Deployment Commands

If you need to deploy manually:

```bash
# SSH into VM
ssh azureuser@<VM_IP>

# Navigate to app directory
cd /home/azureuser/app

# Pull latest image
docker pull ghcr.io/<your-username>/<repo-name>:latest

# Deploy with docker-compose
GITHUB_REPOSITORY=<your-username>/<repo-name> docker-compose -f deploy/docker-compose.yml up -d
```

## Troubleshooting

### Check Application Status
```bash
# SSH into VM
ssh azureuser@<VM_IP>

# Check running containers
docker ps

# Check logs
docker-compose -f /home/azureuser/app/deploy/docker-compose.yml logs
```

### Restart Application
```bash
# SSH into VM
ssh azureuser@<VM_IP>

# Restart services
cd /home/azureuser/app
docker-compose -f deploy/docker-compose.yml restart
```

## Security Notes

- The VM is configured with SSH key authentication only
- HTTP and HTTPS ports are open for web traffic
- Consider setting up SSL/TLS certificates for production use
- Update `ALLOWED_HOSTS` in production settings with your actual domain
