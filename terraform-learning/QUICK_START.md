# 🚀 Quick Start: Deploy GitHub Code to Azure VM

## Your Azure VM Details
- **IP Address:** `172.171.223.227`
- **Username:** `azureuser`
- **SSH Command:** `ssh azureuser@172.171.223.227`

## 🎯 Method 1: Manual Deployment (Easiest)

### Step 1: Connect to Your VM
```bash
ssh azureuser@172.171.223.227
```

### Step 2: Clone Your GitHub Repository
```bash
# Replace with your actual GitHub repository URL
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### Step 3: Install Dependencies and Run
```bash
# For Python projects
pip3 install -r requirements.txt
python3 app.py

# For Node.js projects
npm install
npm start

# For Docker projects
docker-compose up -d
```

## 🎯 Method 2: Automated Deployment Script

### Using PowerShell (Windows):
```powershell
# Check if VM is ready
.\deploy.ps1 -CheckOnly

# Deploy your GitHub repository
.\deploy.ps1 -RepoUrl "https://github.com/yourusername/your-repo.git" -AppName "my-app"
```

### Using Bash (Linux/Mac):
```bash
# Check if VM is ready
./deploy.sh --check

# Deploy your GitHub repository
./deploy.sh --repo "https://github.com/yourusername/your-repo.git" --name "my-app"
```

## 🎯 Method 3: GitHub Actions (Advanced)

### Step 1: Create `.github/workflows/deploy.yml` in your repository:
```yaml
name: Deploy to Azure VM

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Deploy to Azure VM
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: 172.171.223.227
        username: azureuser
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /home/azureuser/your-app
          git pull origin main
          # Add your deployment commands here
```

### Step 2: Add SSH Private Key to GitHub Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add secret: `SSH_PRIVATE_KEY` with your private SSH key

## 🎯 Method 4: Docker Deployment

### Step 1: Create Dockerfile in your repository:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 80

CMD ["python", "app.py"]
```

### Step 2: Create docker-compose.yml:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:80"
    restart: unless-stopped
```

### Step 3: Deploy:
```bash
# On your Azure VM
git clone https://github.com/yourusername/your-repo.git
cd your-repo
docker-compose up -d
```

## 🔧 Common Application Types

### Python Django/Flask:
```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip -y

# Install dependencies
pip3 install -r requirements.txt

# Run Django
python3 manage.py runserver 0.0.0.0:80

# Run Flask
python3 app.py
```

### Node.js:
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install dependencies
npm install

# Run application
npm start
```

### React/Vue/Angular:
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Build and serve
npm install
npm run build
npx serve -s build -l 80
```

## 🌐 Access Your Application

Once deployed, your application will be accessible at:
- **HTTP:** `http://172.171.223.227`
- **SSH:** `ssh azureuser@172.171.223.227`

## 🔒 Security Notes

- Your VM has SSH access enabled (port 22)
- HTTP access is enabled (port 80)
- HTTPS access is enabled (port 443)
- Firewall rules are configured for these ports

## 🆘 Troubleshooting

### VM Not Accessible:
```bash
# Wait a few minutes for VM to fully start
# Check if VM is running in Azure portal
# Verify SSH key is correct
```

### Application Not Starting:
```bash
# Check logs
tail -f /var/log/syslog

# Check if port 80 is in use
netstat -tlnp | grep :80

# Check application status
ps aux | grep python
```

### Permission Issues:
```bash
# Make sure files are owned by azureuser
sudo chown -R azureuser:azureuser /home/azureuser/your-app
```

## 🎉 Success!

Your GitHub code is now running on your Azure VM! 🚀

**Next Steps:**
1. Set up a custom domain (optional)
2. Configure SSL certificate
3. Set up monitoring and logging
4. Automate deployments with CI/CD

