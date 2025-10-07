#!/usr/bin/env python
"""
Setup script to create social account providers in the database
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/var/www/assettrack')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount import providers

def setup_social_providers():
    """Create social account providers in the database"""
    
    # Get or create the site
    site, created = Site.objects.get_or_create(
        domain='172.27.2.43',
        defaults={'name': 'AssetTrack'}
    )
    
    # Create Microsoft social app
    microsoft_app, created = SocialApp.objects.get_or_create(
        provider='microsoft',
        defaults={
            'name': 'Microsoft',
            'client_id': 'your-client-id',  # This will be set via environment
            'secret': 'your-client-secret',  # This will be set via environment
        }
    )
    
    # Add the site to the social app
    microsoft_app.sites.add(site)
    
    print(f"✅ Microsoft social app {'created' if created else 'updated'}")
    print(f"✅ Site: {site.domain}")
    print(f"✅ Social app: {microsoft_app.name}")

if __name__ == '__main__':
    setup_social_providers()
