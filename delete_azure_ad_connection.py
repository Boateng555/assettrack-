#!/usr/bin/env python
"""
Delete Azure AD Connection

This script completely removes the current Azure AD connection
and all associated data.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.models import Employee, Asset

def delete_azure_ad_connection():
    """Delete Azure AD connection and data"""
    
    print("🗑️ DELETING AZURE AD CONNECTION")
    print("=" * 40)
    
    # Check current Azure AD data
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False)
    azure_assets = Asset.objects.filter(azure_ad_id__isnull=False)
    
    print(f"Found {azure_employees.count()} Azure AD employees")
    print(f"Found {azure_assets.count()} Azure AD assets")
    
    if azure_employees.count() == 0 and azure_assets.count() == 0:
        print("✅ No Azure AD data found to delete")
        return True
    
    print("\n⚠️  WARNING: This will delete ALL Azure AD data!")
    print("⚠️  This action cannot be undone!")
    
    # Delete Azure AD employees
    if azure_employees.count() > 0:
        print(f"\n🗑️  Deleting {azure_employees.count()} Azure AD employees...")
        for emp in azure_employees:
            print(f"  - Deleting: {emp.name} ({emp.email})")
            emp.delete()
        print("✅ Azure AD employees deleted")
    
    # Delete Azure AD assets
    if azure_assets.count() > 0:
        print(f"\n🗑️  Deleting {azure_assets.count()} Azure AD assets...")
        for asset in azure_assets:
            print(f"  - Deleting: {asset.name} ({asset.asset_type})")
            asset.delete()
        print("✅ Azure AD assets deleted")
    
    print("\n✅ Azure AD connection and data deleted successfully!")
    return True

def show_cleanup_instructions():
    """Show instructions for cleaning up Azure AD credentials"""
    
    print("\n🧹 CLEAN UP AZURE AD CREDENTIALS")
    print("=" * 40)
    
    print("To completely remove Azure AD connection:")
    print()
    print("1. 📝 Remove from .env file:")
    print("   Delete or comment out these lines:")
    print("   # AZURE_TENANT_ID=...")
    print("   # AZURE_CLIENT_ID=...")
    print("   # AZURE_CLIENT_SECRET=...")
    print()
    print("2. 🔒 Remove from Azure Portal:")
    print("   - Go to Azure Portal → Azure Active Directory")
    print("   - Go to App registrations")
    print("   - Find your AssetTrack app")
    print("   - Click Delete")
    print()
    print("3. 🧪 Test removal:")
    print("   python setup_real_azure_ad.py --test")
    print("   (Should show 'Azure AD not configured')")

def show_final_status():
    """Show final status after deletion"""
    
    print("\n📊 FINAL STATUS")
    print("=" * 20)
    
    # Check remaining data
    total_employees = Employee.objects.count()
    total_assets = Asset.objects.count()
    
    print(f"Total Employees: {total_employees}")
    print(f"Total Assets: {total_assets}")
    print("✅ Azure AD connection removed")
    print("✅ System ready for new setup")

if __name__ == "__main__":
    # Delete Azure AD connection
    success = delete_azure_ad_connection()
    
    if success:
        show_cleanup_instructions()
        show_final_status()
        
        print("\n🎯 NEXT STEPS:")
        print("1. Remove Azure AD credentials from .env file")
        print("2. Delete Azure AD app from Azure Portal")
        print("3. Test that connection is removed")
        print("4. Set up new Azure AD app when ready")
