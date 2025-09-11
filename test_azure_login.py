#!/usr/bin/env python
"""
Test script to verify Azure AD login integration
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
# MicrosoftProvider import not needed for this test

def test_azure_ad_setup():
    """Test the Azure AD setup"""
    print("🔍 Testing Azure AD Integration Setup...")
    print("=" * 50)
    
    # Check if we have a site configured
    try:
        site = Site.objects.get(id=1)
        print(f"✅ Site configured: {site.domain} ({site.name})")
    except Site.DoesNotExist:
        print("❌ No site configured. Please run: python manage.py createsuperuser and configure the site in admin.")
        return False
    
    # Check if we have a social application configured
    try:
        social_app = SocialApp.objects.get(provider='microsoft')
        print(f"✅ Microsoft social app configured: {social_app.name}")
        print(f"   Client ID: {social_app.client_id}")
        print(f"   Secret configured: {'Yes' if social_app.secret else 'No'}")
    except SocialApp.DoesNotExist:
        print("❌ No Microsoft social app configured.")
        print("   Please go to /admin/ and create a social application:")
        print("   - Provider: Microsoft")
        print("   - Name: AssetTrack Microsoft")
        print("   - Client ID: dc7dc18b-b42b-469c-9a9b-a6387e2644b3")
        print("   - Secret: (your Azure client secret)")
        print("   - Sites: 127.0.0.1:8000")
        return False
    
    # Check environment variables
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    
    print(f"✅ Environment variables:")
    print(f"   AZURE_TENANT_ID: {tenant_id}")
    print(f"   AZURE_CLIENT_ID: {client_id}")
    print(f"   AZURE_CLIENT_SECRET: {'Set' if client_secret and client_secret != 'your-client-secret-here' else 'Not set'}")
    
    if client_secret == 'your-client-secret-here':
        print("⚠️  Warning: You need to set your actual Azure client secret in the .env file")
    
    print("\n🎯 Next Steps:")
    print("1. Set your Azure client secret in the .env file")
    print("2. Configure the redirect URI in Azure Portal:")
    print("   http://127.0.0.1:8000/accounts/microsoft/login/callback/")
    print("3. Visit http://127.0.0.1:8000/ to test the login")
    
    return True

if __name__ == '__main__':
    test_azure_ad_setup()
