#!/usr/bin/env python
"""
Remove Old Azure AD Configuration

This script safely removes old Azure AD synced data
so you can configure a new company Azure AD.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.models import Employee, Asset

def remove_old_azure_data():
    """Remove old Azure AD synced data"""
    
    print("🧹 REMOVING OLD AZURE AD DATA")
    print("=" * 35)
    
    # Count current Azure AD data
    old_azure_emps = Employee.objects.filter(azure_ad_id__isnull=False)
    old_azure_assets = Asset.objects.filter(azure_ad_id__isnull=False)
    
    print(f"Found {old_azure_emps.count()} Azure AD employees")
    print(f"Found {old_azure_assets.count()} Azure AD assets")
    
    if old_azure_emps.count() == 0 and old_azure_assets.count() == 0:
        print("✅ No Azure AD data found to remove")
        return True
    
    print("\n⚠️  WARNING: This will remove all Azure AD synced data!")
    print("⚠️  Make sure you have a backup!")
    
    # Remove Azure AD employees
    if old_azure_emps.count() > 0:
        print(f"\n🗑️  Removing {old_azure_emps.count()} Azure AD employees...")
        for emp in old_azure_emps:
            print(f"  - Removing: {emp.name} ({emp.email})")
            # Clear Azure AD fields but keep the employee
            emp.azure_ad_id = None
            emp.azure_ad_username = None
            emp.last_azure_sync = None
            emp.save()
        print("✅ Azure AD employees cleaned")
    
    # Remove Azure AD assets
    if old_azure_assets.count() > 0:
        print(f"\n🗑️  Removing {old_azure_assets.count()} Azure AD assets...")
        for asset in old_azure_assets:
            print(f"  - Removing: {asset.name} ({asset.asset_type})")
            # Clear Azure AD fields but keep the asset
            asset.azure_ad_id = None
            asset.last_azure_sync = None
            asset.save()
        print("✅ Azure AD assets cleaned")
    
    print("\n✅ Old Azure AD data removed successfully!")
    return True

def show_new_azure_setup():
    """Show instructions for setting up new Azure AD"""
    
    print("\n🔧 SETTING UP NEW COMPANY AZURE AD")
    print("=" * 40)
    
    print("Now you need to:")
    print()
    print("1. 🌐 Go to Azure Portal:")
    print("   https://portal.azure.com")
    print()
    print("2. 🔑 Create New App Registration:")
    print("   - Azure Active Directory → App registrations")
    print("   - New registration")
    print("   - Name: AssetTrack Company Integration")
    print("   - Supported account types: Accounts in this organizational directory only")
    print("   - Redirect URI: Web → https://yourdomain.com/accounts/microsoft/login/callback/")
    print()
    print("3. 🔐 Add API Permissions:")
    print("   - Microsoft Graph → Application permissions")
    print("   - Add: User.Read.All, Device.Read.All, Directory.Read.All")
    print("   - Grant admin consent")
    print()
    print("4. 🔒 Create Client Secret:")
    print("   - Certificates & secrets → New client secret")
    print("   - Copy the secret value")
    print()
    print("5. 📝 Update Environment Variables:")
    print("   Edit your .env file with new credentials:")
    print("   AZURE_TENANT_ID=your-company-tenant-id")
    print("   AZURE_CLIENT_ID=your-new-app-client-id")
    print("   AZURE_CLIENT_SECRET=your-new-app-client-secret")
    print()
    print("6. 🧪 Test New Connection:")
    print("   python setup_real_azure_ad.py --test")

def show_environment_template():
    """Show environment variables template"""
    
    print("\n📝 ENVIRONMENT VARIABLES TEMPLATE")
    print("=" * 40)
    
    print("Create/update your .env file with:")
    print()
    print("# Company Azure AD Configuration")
    print("AZURE_TENANT_ID=your-company-tenant-id")
    print("AZURE_CLIENT_ID=your-new-app-client-id")
    print("AZURE_CLIENT_SECRET=your-new-app-client-secret")
    print()
    print("Example:")
    print("AZURE_TENANT_ID=12345678-1234-1234-1234-123456789abc")
    print("AZURE_CLIENT_ID=87654321-4321-4321-4321-cba987654321")
    print("AZURE_CLIENT_SECRET=your-new-secret-value-here")
    print()
    print("⚠️  Keep these credentials secure!")
    print("⚠️  Never commit .env file to version control!")

if __name__ == "__main__":
    # Remove old Azure AD data
    success = remove_old_azure_data()
    
    if success:
        show_new_azure_setup()
        show_environment_template()
        
        print("\n🎯 NEXT STEPS:")
        print("1. Create new Azure AD app registration")
        print("2. Update your .env file with new credentials")
        print("3. Test the new connection")
        print("4. Sync with your company Azure AD")
