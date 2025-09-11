#!/usr/bin/env python
"""
Check Azure AD configuration
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from django.conf import settings

def check_config():
    """Check Azure AD configuration"""
    print("🔍 Checking Azure AD Configuration...")
    print("=" * 50)
    
    # Check environment variables
    print("Environment variables:")
    print(f"  AZURE_TENANT_ID: {os.getenv('AZURE_TENANT_ID')}")
    print(f"  AZURE_CLIENT_ID: {os.getenv('AZURE_CLIENT_ID')}")
    print(f"  AZURE_CLIENT_SECRET: {'Set' if os.getenv('AZURE_CLIENT_SECRET') else 'Not set'}")
    
    print("\nSettings:")
    print(f"  AZURE_TENANT_ID: {getattr(settings, 'AZURE_TENANT_ID', 'Not set')}")
    print(f"  AZURE_CLIENT_ID: {getattr(settings, 'AZURE_CLIENT_ID', 'Not set')}")
    print(f"  AZURE_CLIENT_SECRET: {'Set' if getattr(settings, 'AZURE_CLIENT_SECRET', None) else 'Not set'}")

if __name__ == '__main__':
    check_config()
