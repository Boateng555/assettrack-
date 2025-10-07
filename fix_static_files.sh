#!/bin/bash

# Fix static files and deployment issues
echo "🔧 Fixing Django AssetTrack deployment issues..."

# Navigate to project directory
cd /var/www/assettrack

# Activate virtual environment
source venv/bin/activate

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Set proper permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data /var/www/assettrack
sudo chmod -R 755 /var/www/assettrack

# Create .env file with correct settings
echo "⚙️ Creating environment file..."
sudo tee /var/www/assettrack/.env > /dev/null << 'EOF'
SECRET_KEY=django-insecure-h-pd1d97vy_o%26m^#4s%@oao(*bpf6((i)ii@jfmbk90%_qqz
DEBUG=True
ALLOWED_HOSTS=172.27.2.43,localhost,127.0.0.1
EOF

# Set permissions for .env file
sudo chown www-data:www-data /var/www/assettrack/.env
sudo chmod 644 /var/www/assettrack/.env

# Restart services
echo "🔄 Restarting services..."
sudo systemctl restart assettrack
sudo systemctl restart nginx

# Check service status
echo "📊 Checking service status..."
sudo systemctl status assettrack --no-pager
sudo systemctl status nginx --no-pager

echo "✅ Fix complete!"
echo "🌐 Your application should now be available at: http://172.27.2.43"
