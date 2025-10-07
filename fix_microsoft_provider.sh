#!/bin/bash

# Fix Microsoft provider setup in database
echo "🔧 Fixing Microsoft provider setup..."

# Navigate to project directory
cd /var/www/assettrack

# Activate virtual environment
source venv/bin/activate

# Run the setup script to create social providers
python setup_social_providers.py

# Update the Microsoft social app with proper credentials
python manage.py shell << 'EOF'
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Get the site
site = Site.objects.get(domain='172.27.2.43')

# Update Microsoft social app
try:
    microsoft_app = SocialApp.objects.get(provider='microsoft')
    microsoft_app.client_id = 'your-client-id'  # Set your actual client ID
    microsoft_app.secret = 'your-client-secret'  # Set your actual client secret
    microsoft_app.save()
    print("✅ Microsoft social app updated")
except SocialApp.DoesNotExist:
    print("❌ Microsoft social app not found")
EOF

# Restart services
sudo systemctl restart assettrack
sudo systemctl restart nginx

echo "✅ Microsoft provider fix complete!"
echo "🌐 Test your application at: http://172.27.2.43"
