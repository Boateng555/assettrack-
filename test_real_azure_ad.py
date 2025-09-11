#!/usr/bin/env python
"""
Test Real Azure AD Integration
This script tests the Azure AD integration with real tenant data
"""

import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration
from assets.models import Employee, Asset

def test_azure_ad_connection():
    """Test Azure AD connection and authentication"""
    
    print("🔗 Testing Azure AD Connection")
    print("=" * 40)
    
    try:
        azure_ad = AzureADIntegration()
        token = azure_ad.get_access_token()
        
        if token:
            print("✅ Azure AD authentication successful!")
            print(f"📝 Access token obtained: {token[:20]}...")
            return True
        else:
            print("❌ Azure AD authentication failed!")
            print("Please check your credentials in settings.py")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Azure AD: {e}")
        return False

def test_azure_ad_users():
    """Test fetching users from Azure AD"""
    
    print("\n👥 Testing Azure AD Users")
    print("=" * 30)
    
    try:
        azure_ad = AzureADIntegration()
        users = azure_ad.get_users()
        
        if users:
            print(f"✅ Found {len(users)} users in Azure AD")
            print()
            
            print("📋 Sample users:")
            for i, user in enumerate(users[:5]):  # Show first 5 users
                print(f"  {i+1}. {user.get('displayName', 'N/A')} ({user.get('department', 'N/A')})")
                print(f"      Email: {user.get('mail', 'N/A')}")
                print(f"      Job Title: {user.get('jobTitle', 'N/A')}")
                print()
            
            if len(users) > 5:
                print(f"  ... and {len(users) - 5} more users")
            
            return users
        else:
            print("⚠️  No users found in Azure AD")
            print("Make sure your Azure AD tenant has users and the app has proper permissions")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return []

def test_azure_ad_devices():
    """Test fetching devices from Azure AD"""
    
    print("\n💻 Testing Azure AD Devices")
    print("=" * 30)
    
    try:
        azure_ad = AzureADIntegration()
        devices = azure_ad.get_devices()
        
        if devices:
            print(f"✅ Found {len(devices)} devices in Azure AD")
            print()
            
            print("📋 Sample devices:")
            for i, device in enumerate(devices[:5]):  # Show first 5 devices
                print(f"  {i+1}. {device.get('displayName', 'N/A')}")
                print(f"      OS: {device.get('operatingSystem', 'N/A')} {device.get('operatingSystemVersion', '')}")
                print(f"      Manufacturer: {device.get('manufacturer', 'N/A')}")
                print(f"      Model: {device.get('model', 'N/A')}")
                print()
            
            if len(devices) > 5:
                print(f"  ... and {len(devices) - 5} more devices")
            
            return devices
        else:
            print("⚠️  No devices found in Azure AD")
            print("Make sure your Azure AD tenant has devices registered")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching devices: {e}")
        return []

def test_real_sync():
    """Test real Azure AD sync"""
    
    print("\n🔄 Testing Real Azure AD Sync")
    print("=" * 35)
    
    try:
        azure_ad = AzureADIntegration()
        
        print("📊 Current database state:")
        total_employees = Employee.objects.count()
        total_assets = Asset.objects.count()
        azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).count()
        azure_assets = Asset.objects.filter(azure_ad_id__isnull=False).count()
        
        print(f"  • Total employees: {total_employees}")
        print(f"  • Total assets: {total_assets}")
        print(f"  • Azure AD employees: {azure_employees}")
        print(f"  • Azure AD assets: {azure_assets}")
        print()
        
        print("🔄 Starting real Azure AD sync...")
        results = azure_ad.full_sync()
        
        print("✅ Sync completed!")
        print(f"  • Employees synced: {results['employees_synced']}")
        print(f"  • Employees updated: {results['employees_updated']}")
        print(f"  • Devices synced: {results['devices_synced']}")
        print(f"  • Devices updated: {results['devices_updated']}")
        print(f"  • Assignments updated: {results['assignments_updated']}")
        print()
        
        # Show updated database state
        print("📊 Updated database state:")
        total_employees = Employee.objects.count()
        total_assets = Asset.objects.count()
        azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).count()
        azure_assets = Asset.objects.filter(azure_ad_id__isnull=False).count()
        
        print(f"  • Total employees: {total_employees}")
        print(f"  • Total assets: {total_assets}")
        print(f"  • Azure AD employees: {azure_employees}")
        print(f"  • Azure AD assets: {azure_assets}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error during sync: {e}")
        return None

def show_synced_data():
    """Show the synced data from Azure AD"""
    
    print("\n📋 Synced Azure AD Data")
    print("=" * 25)
    
    # Show Azure AD employees
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False)
    print(f"👥 Azure AD Employees ({azure_employees.count()}):")
    
    for emp in azure_employees:
        assigned_count = emp.assigned_assets.count()
        print(f"  • {emp.name} ({emp.department})")
        print(f"    Email: {emp.email}")
        print(f"    Job Title: {emp.job_title or 'N/A'}")
        print(f"    Assigned Assets: {assigned_count}")
        print(f"    Last Sync: {emp.last_azure_sync.strftime('%Y-%m-%d %H:%M:%S') if emp.last_azure_sync else 'Never'}")
        print()
    
    # Show Azure AD assets
    azure_assets = Asset.objects.filter(azure_ad_id__isnull=False)
    print(f"💻 Azure AD Assets ({azure_assets.count()}):")
    
    for asset in azure_assets:
        assigned_to = asset.assigned_to.name if asset.assigned_to else "Unassigned"
        print(f"  • {asset.name} ({asset.asset_type})")
        print(f"    OS: {asset.operating_system or 'N/A'} {asset.os_version or ''}")
        print(f"    Manufacturer: {asset.manufacturer or 'N/A'}")
        print(f"    Model: {asset.model or 'N/A'}")
        print(f"    Assigned To: {assigned_to}")
        print(f"    Status: {asset.status}")
        print(f"    Last Sync: {asset.last_azure_sync.strftime('%Y-%m-%d %H:%M:%S') if asset.last_azure_sync else 'Never'}")
        print()

def main():
    """Main test function"""
    
    print("🚀 Real Azure AD Integration Test")
    print("=" * 50)
    print()
    print("This script will test your Azure AD integration with real tenant data.")
    print("Make sure you have configured your Azure AD credentials in settings.py")
    print()
    
    # Test connection
    if not test_azure_ad_connection():
        print("\n❌ Cannot proceed without Azure AD connection.")
        print("Please check your credentials and run the setup script:")
        print("python setup_azure_ad.py")
        return
    
    # Test fetching data
    users = test_azure_ad_users()
    devices = test_azure_ad_devices()
    
    if not users and not devices:
        print("\n⚠️  No data found in Azure AD.")
        print("Make sure your tenant has users and devices, and the app has proper permissions.")
        return
    
    # Test real sync
    print("\n" + "="*50)
    print("🔄 READY TO SYNC REAL DATA FROM AZURE AD")
    print("="*50)
    
    confirm = input("\nDo you want to proceed with real Azure AD sync? (y/N): ").strip().lower()
    
    if confirm == 'y':
        results = test_real_sync()
        
        if results:
            show_synced_data()
            
            print("\n🎉 Real Azure AD Integration Test Completed!")
            print("\n📊 Summary:")
            print(f"  • {results['employees_synced']} new employees synced")
            print(f"  • {results['employees_updated']} employees updated")
            print(f"  • {results['devices_synced']} new devices synced")
            print(f"  • {results['devices_updated']} devices updated")
            print(f"  • {results['assignments_updated']} assignments updated")
            
            print("\n🌐 Next steps:")
            print("1. Visit: http://localhost:8000/azure-status/")
            print("2. Check your dashboard for the synced data")
            print("3. Run: python manage.py sync_azure_ad (for future syncs)")
        else:
            print("\n❌ Sync failed. Please check the error messages above.")
    else:
        print("\n⏸️  Sync cancelled. You can run it later with:")
        print("python manage.py sync_azure_ad")

if __name__ == "__main__":
    main()

