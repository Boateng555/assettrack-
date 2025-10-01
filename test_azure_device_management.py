#!/usr/bin/env python
"""
Azure AD Device Management Test Script

This script demonstrates how to:
1. Add devices to Azure AD (simulated)
2. Assign devices to users
3. Sync devices to AssetTrack
4. Verify device assignments

Run this script to test your Azure AD device management setup.
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration
from assets.models import Employee, Asset
from django.contrib.auth.models import User

def test_azure_device_management():
    """Test Azure AD device management functionality"""
    
    print("🔧 Azure AD Device Management Test")
    print("=" * 50)
    
    # Initialize Azure AD integration
    azure_ad = AzureADIntegration()
    
    # Test 1: Check Azure AD connection
    print("\n1. Testing Azure AD Connection...")
    try:
        users = azure_ad.get_users()
        print(f"✅ Azure AD connection successful - Found {len(users)} users")
    except Exception as e:
        print(f"❌ Azure AD connection failed: {e}")
        return False
    
    # Test 2: Get devices from Azure AD
    print("\n2. Testing Device Retrieval...")
    try:
        devices = azure_ad.get_devices()
        print(f"✅ Found {len(devices)} devices in Azure AD")
        
        # Show device details
        for i, device in enumerate(devices[:3]):  # Show first 3 devices
            print(f"   Device {i+1}: {device.get('displayName', 'Unknown')} ({device.get('operatingSystem', 'Unknown OS')})")
    except Exception as e:
        print(f"❌ Device retrieval failed: {e}")
        return False
    
    # Test 3: Test user-device relationships
    print("\n3. Testing User-Device Relationships...")
    try:
        user_device_count = 0
        for user in users[:3]:  # Test first 3 users
            user_id = user.get('id')
            user_name = user.get('displayName', 'Unknown')
            user_devices = azure_ad.get_user_devices(user_id)
            user_device_count += len(user_devices)
            print(f"   {user_name}: {len(user_devices)} devices")
        
        print(f"✅ Total user devices found: {user_device_count}")
    except Exception as e:
        print(f"❌ User-device relationship test failed: {e}")
        return False
    
    # Test 4: Test device sync to AssetTrack
    print("\n4. Testing Device Sync to AssetTrack...")
    try:
        # Get current asset count
        current_assets = Asset.objects.count()
        azure_assets = Asset.objects.filter(azure_ad_id__isnull=False).count()
        
        print(f"   Current assets: {current_assets}")
        print(f"   Azure AD assets: {azure_assets}")
        
        # Run device sync
        device_synced, device_updated = azure_ad.sync_devices()
        print(f"✅ Device sync completed: {device_synced} new, {device_updated} updated")
        
        # Check updated counts
        new_assets = Asset.objects.count()
        new_azure_assets = Asset.objects.filter(azure_ad_id__isnull=False).count()
        
        print(f"   New total assets: {new_assets}")
        print(f"   New Azure AD assets: {new_azure_assets}")
        
    except Exception as e:
        print(f"❌ Device sync failed: {e}")
        return False
    
    # Test 5: Test device assignments
    print("\n5. Testing Device Assignments...")
    try:
        # Run full sync to get assignments
        sync_results = azure_ad.full_sync()
        
        print(f"✅ Full sync completed:")
        print(f"   Employees: {sync_results['employees_synced']} new, {sync_results['employees_updated']} updated")
        print(f"   User Devices: {sync_results['user_devices_synced']} synced, {sync_results['user_devices_assigned']} assigned")
        print(f"   Standalone Devices: {sync_results['standalone_devices_synced']} synced")
        print(f"   Assignments: {sync_results['assignments_updated']} updated")
        print(f"   Assets cleaned up: {sync_results['assets_cleaned_up']}")
        
    except Exception as e:
        print(f"❌ Device assignment test failed: {e}")
        return False
    
    # Test 6: Verify asset assignments
    print("\n6. Verifying Asset Assignments...")
    try:
        assigned_assets = Asset.objects.filter(assigned_to__isnull=False).count()
        azure_assigned_assets = Asset.objects.filter(
            assigned_to__isnull=False,
            azure_ad_id__isnull=False
        ).count()
        
        print(f"✅ Asset assignment verification:")
        print(f"   Total assigned assets: {assigned_assets}")
        print(f"   Azure AD assigned assets: {azure_assigned_assets}")
        
        # Show some assigned assets
        assigned_assets_list = Asset.objects.filter(
            assigned_to__isnull=False,
            azure_ad_id__isnull=False
        )[:5]
        
        print(f"   Sample assigned assets:")
        for asset in assigned_assets_list:
            print(f"     - {asset.name} → {asset.assigned_to.name} ({asset.asset_type})")
        
    except Exception as e:
        print(f"❌ Asset assignment verification failed: {e}")
        return False
    
    # Test 7: Generate sync summary
    print("\n7. Generating Sync Summary...")
    try:
        summary = azure_ad.get_sync_summary()
        
        print(f"✅ Sync Summary:")
        print(f"   Azure AD Users: {summary['azure_users']}")
        print(f"   Local Employees: {summary['local_employees']}")
        print(f"   Azure Synced Employees: {summary['azure_synced_employees']}")
        print(f"   Active Employees: {summary['active_employees']}")
        print(f"   Inactive Employees: {summary['inactive_employees']}")
        print(f"   Deleted Employees: {summary['deleted_employees']}")
        
    except Exception as e:
        print(f"❌ Sync summary generation failed: {e}")
        return False
    
    print("\n🎉 Azure AD Device Management Test Completed Successfully!")
    return True

def create_sample_devices():
    """Create sample devices for testing (if no real devices exist)"""
    
    print("\n📱 Creating Sample Devices for Testing...")
    
    # This would normally create devices in Azure AD
    # For testing purposes, we'll create local assets that simulate Azure AD devices
    
    sample_devices = [
        {
            'name': 'John\'s Laptop',
            'asset_type': 'laptop',
            'serial_number': 'TEST001',
            'manufacturer': 'Dell',
            'model': 'Latitude 5520',
            'operating_system': 'Windows',
            'os_version': '11.0',
            'azure_ad_id': 'test-device-001'
        },
        {
            'name': 'Jane\'s iPhone',
            'asset_type': 'phone',
            'serial_number': 'TEST002',
            'manufacturer': 'Apple',
            'model': 'iPhone 13',
            'operating_system': 'iOS',
            'os_version': '15.0',
            'azure_ad_id': 'test-device-002'
        },
        {
            'name': 'Bob\'s MacBook',
            'asset_type': 'laptop',
            'serial_number': 'TEST003',
            'manufacturer': 'Apple',
            'model': 'MacBook Pro',
            'operating_system': 'macOS',
            'os_version': '12.0',
            'azure_ad_id': 'test-device-003'
        }
    ]
    
    created_count = 0
    for device_data in sample_devices:
        try:
            # Check if device already exists
            existing = Asset.objects.filter(azure_ad_id=device_data['azure_ad_id']).first()
            if not existing:
                Asset.objects.create(**device_data)
                created_count += 1
                print(f"   ✅ Created: {device_data['name']}")
            else:
                print(f"   ⚠️  Already exists: {device_data['name']}")
        except Exception as e:
            print(f"   ❌ Failed to create {device_data['name']}: {e}")
    
    print(f"📱 Sample device creation completed: {created_count} devices created")
    return created_count

def show_device_management_commands():
    """Show useful commands for device management"""
    
    print("\n🛠️  Useful Device Management Commands:")
    print("=" * 50)
    
    print("\n1. Sync devices from Azure AD:")
    print("   python manage.py sync_azure_ad --devices-only")
    
    print("\n2. Sync employees with their devices:")
    print("   python manage.py sync_azure_ad --employees-only")
    
    print("\n3. Full sync (employees + devices + assignments):")
    print("   python manage.py sync_azure_ad")
    
    print("\n4. Check sync status:")
    print("   python manage.py sync_azure_ad --summary")
    
    print("\n5. Clean up orphaned assets:")
    print("   python manage.py sync_azure_ad --cleanup-only")
    
    print("\n6. View Azure AD sync status in web interface:")
    print("   http://localhost:8000/azure-sync/")
    
    print("\n7. Check asset assignments:")
    print("   python manage.py shell -c \"from assets.models import Asset; print(Asset.objects.filter(assigned_to__isnull=False).count())\"")

if __name__ == "__main__":
    print("🚀 Starting Azure AD Device Management Test")
    print("=" * 60)
    
    # Check if we have Azure AD credentials
    from django.conf import settings
    
    if not all([
        getattr(settings, 'AZURE_TENANT_ID', None),
        getattr(settings, 'AZURE_CLIENT_ID', None),
        getattr(settings, 'AZURE_CLIENT_SECRET', None)
    ]):
        print("⚠️  Azure AD credentials not configured. Creating sample devices for testing...")
        create_sample_devices()
        show_device_management_commands()
    else:
        # Run the full test
        success = test_azure_device_management()
        
        if success:
            show_device_management_commands()
        else:
            print("\n❌ Some tests failed. Check the error messages above.")
    
    print("\n📚 For more information, see: Azure_AD_Device_Management_Guide.md")
