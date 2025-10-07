#!/bin/bash

# Fix Microsoft login by setting up social providers
echo "🔧 Fixing Microsoft login setup..."

# Navigate to project directory
cd /var/www/assettrack

# Activate virtual environment
source venv/bin/activate

# Run migrations to ensure all tables exist
python manage.py migrate

# Create the social providers
python setup_social_providers.py

# Create a superuser if it doesn't exist
echo "👤 Creating superuser (if needed)..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superuser created: admin / admin123")
else:
    print("✅ Superuser already exists")
EOF

# Collect static files
python manage.py collectstatic --noinput

# Set proper permissions
sudo chown -R www-data:www-data /var/www/assettrack
sudo chmod -R 755 /var/www/assettrack

# Restart services
sudo systemctl restart assettrack
sudo systemctl restart nginx

echo "✅ Microsoft login fix complete!"
echo "🌐 Test your application at: http://172.27.2.43"
echo "👤 Login with: admin / admin123"
