# 🚀 SIMPLE DEPLOYMENT GUIDE

## Your Azure VM is Ready! ✅
- **IP Address:** `172.171.223.227`
- **Username:** `azureuser`
- **Status:** VM is accessible and ready for deployment

## 🎯 Step-by-Step Deployment

### Step 1: Connect to Your VM
Open PowerShell or Command Prompt and run:
```bash
ssh azureuser@172.171.223.227
```

### Step 2: Install Git (if needed)
```bash
sudo apt update
sudo apt install git -y
```

### Step 3: Clone Your GitHub Repository
Replace `YOUR_GITHUB_REPO_URL` with your actual repository URL:
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### Step 4: Install Dependencies Based on Your Project Type

#### For Python Projects:
```bash
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
```

#### For Node.js Projects:
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install
```

#### For Docker Projects:
```bash
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
docker-compose up -d
```

### Step 5: Run Your Application

#### For Python Flask/Django:
```bash
# Flask
python3 app.py

# Django
python3 manage.py runserver 0.0.0.0:80
```

#### For Node.js:
```bash
npm start
# or
node app.js
```

#### For Docker:
```bash
docker-compose up -d
```

## 🌐 Access Your Application

Once running, your application will be available at:
**http://172.171.223.227**

## 🔧 Common Commands

### Check if your app is running:
```bash
ps aux | grep python
# or
ps aux | grep node
```

### Check what's listening on port 80:
```bash
netstat -tlnp | grep :80
```

### View logs:
```bash
# For Python
tail -f app.log

# For Node.js
tail -f logs/app.log

# For Docker
docker-compose logs -f
```

### Stop your application:
```bash
# Find the process ID
ps aux | grep python

# Kill the process
kill [PID]

# For Docker
docker-compose down
```

## 🎯 Example: Deploy a Simple Python Flask App

### 1. Create a simple Flask app on your VM:
```bash
# Connect to VM
ssh azureuser@172.171.223.227

# Create a simple Flask app
cat > app.py << 'EOF'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Azure VM!</h1><p>Your app is running successfully!</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
EOF

# Install Flask
pip3 install flask

# Run the app
python3 app.py
```

### 2. Access your app:
Open your browser and go to: **http://172.171.223.227**

## 🎯 Example: Deploy a Node.js App

### 1. Create a simple Node.js app:
```bash
# Connect to VM
ssh azureuser@172.171.223.227

# Create package.json
cat > package.json << 'EOF'
{
  "name": "azure-app",
  "version": "1.0.0",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
EOF

# Create app.js
cat > app.js << 'EOF'
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('<h1>Hello from Azure VM!</h1><p>Your Node.js app is running!</p>');
});

app.listen(80, '0.0.0.0', () => {
  console.log('Server running on port 80');
});
EOF

# Install dependencies
npm install

# Run the app
npm start
```

## 🎯 Example: Deploy with Docker

### 1. Create Dockerfile:
```bash
# Connect to VM
ssh azureuser@172.171.223.227

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 80

CMD ["python", "app.py"]
EOF

# Create requirements.txt
echo "flask" > requirements.txt

# Create app.py
cat > app.py << 'EOF'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Docker on Azure!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
EOF

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:80"
    restart: unless-stopped
EOF

# Build and run
docker-compose up -d
```

## 🎉 Success!

Your application is now running on Azure! 🚀

**Next Steps:**
1. Set up a custom domain
2. Configure SSL certificate
3. Set up monitoring
4. Automate deployments with GitHub Actions


