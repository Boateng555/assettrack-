#!/bin/bash

# Update script for Django AssetTrack on Linux server
# Run this script after git pull to update the server

echo "🔄 Updating Django AssetTrack on server..."

# Navigate to project directory
cd /var/www/assettrack

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Copy production environment file
cp env.production .env

# Set proper permissions
sudo chown -R www-data:www-data /var/www/assettrack
sudo chmod -R 755 /var/www/assettrack

# Restart services
sudo systemctl restart assettrack
sudo systemctl restart nginx

# Check service status
echo "📊 Checking service status..."
sudo systemctl status assettrack --no-pager
sudo systemctl status nginx --no-pager

echo "✅ Update complete!"
echo "🌐 Your application should be available at: http://172.27.2.43"
