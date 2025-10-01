#!/usr/bin/env python
"""
Setup Real Azure AD Connection

This script helps you configure your real company Azure AD connection
and test it safely.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration

def check_current_azure_config():
    """Check current Azure AD configuration"""
    
    print("🔍 CURRENT AZURE AD CONFIGURATION")
    print("=" * 45)
    
    from django.conf import settings
    
    tenant_id = getattr(settings, 'AZURE_TENANT_ID', None)
    client_id = getattr(settings, 'AZURE_CLIENT_ID', None)
    client_secret = getattr(settings, 'AZURE_CLIENT_SECRET', None)
    
    print(f"Tenant ID: {'✅ Set' if tenant_id else '❌ Not Set'}")
    print(f"Client ID: {'✅ Set' if client_id else '❌ Not Set'}")
    print(f"Client Secret: {'✅ Set' if client_secret else '❌ Not Set'}")
    
    if not all([tenant_id, client_id, client_secret]):
        print("\n⚠️  Azure AD credentials not configured!")
        print("You need to set up your company Azure AD credentials.")
        return False
    
    return True

def test_azure_connection():
    """Test Azure AD connection"""
    
    print("\n🧪 TESTING AZURE AD CONNECTION")
    print("=" * 35)
    
    try:
        azure_ad = AzureADIntegration()
        
        # Test connection
        print("Testing connection...")
        users = azure_ad.get_users()
        print(f"✅ Connection successful!")
        print(f"📊 Found {len(users)} users in Azure AD")
        
        # Show sample users
        if users:
            print("\n👥 Sample users:")
            for user in users[:3]:
                print(f"  - {user.get('displayName', 'Unknown')} ({user.get('mail', 'No email')})")
        
        # Test devices
        devices = azure_ad.get_devices()
        print(f"\n🖥️  Found {len(devices)} devices in Azure AD")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def show_setup_instructions():
    """Show instructions for setting up Azure AD"""
    
    print("\n📋 AZURE AD SETUP INSTRUCTIONS")
    print("=" * 40)
    
    print("To connect to your company Azure AD, you need:")
    print()
    print("1. 🔑 AZURE AD APP REGISTRATION:")
    print("   - Go to Azure Portal → Azure Active Directory")
    print("   - Go to App registrations → New registration")
    print("   - Name: AssetTrack Integration")
    print("   - Supported account types: Accounts in this organizational directory only")
    print("   - Redirect URI: Web → https://yourdomain.com/accounts/microsoft/login/callback/")
    print()
    print("2. 🔐 API PERMISSIONS:")
    print("   - Microsoft Graph → Application permissions")
    print("   - Add: User.Read.All, Device.Read.All, Directory.Read.All")
    print("   - Grant admin consent")
    print()
    print("3. 🔒 CLIENT SECRET:")
    print("   - Go to Certificates & secrets")
    print("   - New client secret")
    print("   - Copy the secret value")
    print()
    print("4. 📝 ENVIRONMENT VARIABLES:")
    print("   Create a .env file with:")
    print("   AZURE_TENANT_ID=your-tenant-id")
    print("   AZURE_CLIENT_ID=your-client-id")
    print("   AZURE_CLIENT_SECRET=your-client-secret")
    print()
    print("5. 🧪 TEST CONNECTION:")
    print("   python setup_real_azure_ad.py --test")

def show_environment_setup():
    """Show how to set up environment variables"""
    
    print("\n🔧 ENVIRONMENT VARIABLES SETUP")
    print("=" * 35)
    
    print("Create a .env file in your project root:")
    print()
    print("AZURE_TENANT_ID=your-company-tenant-id")
    print("AZURE_CLIENT_ID=your-app-client-id")
    print("AZURE_CLIENT_SECRET=your-app-client-secret")
    print()
    print("Example:")
    print("AZURE_TENANT_ID=12345678-1234-1234-1234-123456789abc")
    print("AZURE_CLIENT_ID=87654321-4321-4321-4321-cba987654321")
    print("AZURE_CLIENT_SECRET=your-secret-value-here")
    print()
    print("⚠️  Keep these credentials secure!")
    print("⚠️  Never commit .env file to version control!")

def show_sync_instructions():
    """Show how to sync with real Azure AD"""
    
    print("\n🔄 SYNC WITH REAL AZURE AD")
    print("=" * 30)
    
    print("Once configured, you can sync:")
    print()
    print("1. 📊 Check sync status:")
    print("   python manage.py sync_azure_ad --summary")
    print()
    print("2. 👥 Sync employees:")
    print("   python manage.py sync_azure_ad --employees-only")
    print()
    print("3. 🖥️  Sync devices:")
    print("   python manage.py sync_azure_ad --devices-only")
    print()
    print("4. 🔄 Full sync:")
    print("   python manage.py sync_azure_ad")
    print()
    print("5. 🌐 Web interface:")
    print("   http://localhost:8000/azure-sync/")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test connection
        if check_current_azure_config():
            test_azure_connection()
        else:
            print("\n❌ Azure AD not configured. Please set up credentials first.")
    else:
        # Show setup instructions
        check_current_azure_config()
        show_setup_instructions()
        show_environment_setup()
        show_sync_instructions()
