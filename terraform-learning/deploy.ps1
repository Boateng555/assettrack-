# 🚀 PowerShell Deployment Script for Azure VM
# This script helps you deploy your GitHub code to your Azure VM

param(
    [Parameter(Mandatory=$false)]
    [string]$RepoUrl = "",
    
    [Parameter(Mandatory=$false)]
    [string]$AppName = "my-app",
    
    [Parameter(Mandatory=$false)]
    [switch]$CheckOnly
)

$VM_IP = "172.171.223.227"
$VM_USER = "azureuser"

Write-Host "🚀 Azure VM Deployment Script" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green
Write-Host "VM IP: $VM_IP" -ForegroundColor Yellow
Write-Host "VM User: $VM_USER" -ForegroundColor Yellow
Write-Host ""

# Function to check if VM is accessible
function Test-VMConnection {
    Write-Host "🔍 Checking VM connection..." -ForegroundColor Blue
    
    try {
        $result = ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$VM_USER@$VM_IP" "echo 'VM is accessible'" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ VM is accessible!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ VM is not accessible yet. Please wait a few minutes and try again." -ForegroundColor Red
            Write-Host "💡 The VM might still be starting up..." -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "❌ VM is not accessible yet. Please wait a few minutes and try again." -ForegroundColor Red
        Write-Host "💡 The VM might still be starting up..." -ForegroundColor Yellow
        return $false
    }
}

# Function to deploy a GitHub repository
function Deploy-GitHubRepo {
    param(
        [string]$RepoUrl,
        [string]$AppName
    )
    
    Write-Host "📦 Deploying $AppName from GitHub..." -ForegroundColor Blue
    
    # Create the deployment script
    $deployScript = @"
echo "🔄 Updating system packages..."
sudo apt update

echo "📥 Installing Git..."
sudo apt install git -y

echo "📂 Cloning repository..."
if [ -d "$AppName" ]; then
    echo "📁 Repository exists, updating..."
    cd $AppName
    git pull origin main
else
    echo "📁 Cloning new repository..."
    git clone $RepoUrl $AppName
    cd $AppName
fi

echo "🔧 Installing dependencies..."

# Check if it's a Python project
if [ -f "requirements.txt" ]; then
    echo "🐍 Python project detected..."
    sudo apt install python3 python3-pip -y
    pip3 install -r requirements.txt
fi

# Check if it's a Node.js project
if [ -f "package.json" ]; then
    echo "📦 Node.js project detected..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    npm install
fi

# Check if it's a Docker project
if [ -f "Dockerfile" ]; then
    echo "🐳 Docker project detected..."
    sudo apt install docker.io docker-compose -y
    sudo usermod -aG docker `$USER
    docker-compose up -d
fi

echo "✅ Deployment completed!"
echo "🌐 Your app should be accessible at: http://$VM_IP"
"@

    # Execute the deployment script on the VM
    $deployScript | ssh -o StrictHostKeyChecking=no "$VM_USER@$VM_IP" "bash"
}

# Function to show usage
function Show-Usage {
    Write-Host "Usage: .\deploy.ps1 [OPTIONS]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -RepoUrl URL        GitHub repository URL" -ForegroundColor White
    Write-Host "  -AppName NAME       Application name (default: 'my-app')" -ForegroundColor White
    Write-Host "  -CheckOnly          Just check VM connection" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\deploy.ps1 -RepoUrl 'https://github.com/username/my-app.git' -AppName 'my-app'" -ForegroundColor White
    Write-Host "  .\deploy.ps1 -CheckOnly" -ForegroundColor White
    Write-Host ""
}

# Main script logic
if ($CheckOnly) {
    if (Test-VMConnection) {
        Write-Host "🎉 VM is ready for deployment!" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "❌ VM is not ready yet." -ForegroundColor Red
        exit 1
    }
}

if ([string]::IsNullOrEmpty($RepoUrl)) {
    Write-Host "❌ Repository URL is required!" -ForegroundColor Red
    Show-Usage
    exit 1
}

# Check VM connection first
if (-not (Test-VMConnection)) {
    exit 1
}

# Deploy the repository
Deploy-GitHubRepo -RepoUrl $RepoUrl -AppName $AppName

Write-Host ""
Write-Host "🎉 Deployment completed!" -ForegroundColor Green
Write-Host "🌐 Access your application at: http://$VM_IP" -ForegroundColor Yellow
Write-Host "SSH into your VM: ssh $VM_USER@$VM_IP" -ForegroundColor Yellow
