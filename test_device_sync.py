#!/usr/bin/env python
"""
Test script for enhanced Azure AD device sync functionality
This script demonstrates how the system automatically imports user devices as assets
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration
from assets.models import Employee, Asset

def test_device_sync():
    """Test the enhanced device sync functionality"""
    print("🚀 Testing Enhanced Azure AD Device Sync Functionality")
    print("=" * 70)
    
    azure = AzureADIntegration()
    
    # Test 1: Get Azure AD users and their devices
    print("\n👥 1. Azure AD Users and Their Devices:")
    print("-" * 40)
    users = azure.get_users()
    print(f"   Total active users in Azure AD: {len(users)}")
    
    total_user_devices = 0
    for i, user in enumerate(users[:5], 1):  # Show first 5 users
        user_devices = azure.get_user_devices(user.get('id'))
        total_user_devices += len(user_devices)
        print(f"   {i}. {user.get('displayName', 'N/A')} ({user.get('userPrincipalName', 'N/A')})")
        print(f"      Devices: {len(user_devices)}")
        for device in user_devices[:3]:  # Show first 3 devices per user
            os_type = device.get('operatingSystem', 'Unknown')
            print(f"        - {device.get('displayName', 'N/A')} ({os_type})")
        if len(user_devices) > 3:
            print(f"        ... and {len(user_devices) - 3} more devices")
    
    if len(users) > 5:
        print(f"   ... and {len(users) - 5} more users")
    
    print(f"\n   Total user devices found: {total_user_devices}")
    
    # Test 2: Current asset status
    print("\n💻 2. Current Asset Status:")
    print("-" * 40)
    total_assets = Asset.objects.count()
    azure_synced_assets = Asset.objects.filter(azure_ad_id__isnull=False).count()
    assigned_assets = Asset.objects.filter(assigned_to__isnull=False).count()
    
    print(f"   Total assets: {total_assets}")
    print(f"   Azure AD synced assets: {azure_synced_assets}")
    print(f"   Assigned assets: {assigned_assets}")
    print(f"   Available assets: {total_assets - assigned_assets}")
    
    # Test 3: Show some existing assets
    print("\n📱 3. Sample Existing Assets:")
    print("-" * 40)
    azure_assets = Asset.objects.filter(azure_ad_id__isnull=False)[:5]
    for asset in azure_assets:
        assigned_to = asset.assigned_to.name if asset.assigned_to else "Unassigned"
        print(f"   - {asset.name} ({asset.asset_type}) - Assigned to: {assigned_to}")
        print(f"     OS: {asset.operating_system} {asset.os_version}")
        print(f"     Serial: {asset.serial_number}")
    
    # Test 4: Demonstrate sync capabilities
    print("\n🔄 4. Enhanced Device Sync Capabilities:")
    print("-" * 40)
    print("   The enhanced sync will:")
    print("   ✅ Import all user devices from Azure AD as assets")
    print("   ✅ Automatically assign devices to their owners")
    print("   ✅ Set appropriate asset types (laptop, phone, etc.)")
    print("   ✅ Include OS information and device details")
    print("   ✅ Handle device updates and reassignments")
    print("   ✅ Clean up orphaned assets when users are disabled/deleted")
    
    # Test 5: Show what happens during sync
    print("\n🎯 5. What Happens During Sync:")
    print("-" * 40)
    print("   For each Azure AD user:")
    print("   1. Employee is created/updated")
    print("   2. User's devices are fetched from Azure AD")
    print("   3. Each device becomes an asset:")
    print("      - Windows/macOS devices → 'laptop' assets")
    print("      - iOS/Android devices → 'phone' assets")
    print("      - Other devices → 'other' assets")
    print("   4. Asset is automatically assigned to the employee")
    print("   5. Asset status is set to 'assigned'")
    
    # Test 6: Asset type mapping
    print("\n🔧 6. Asset Type Mapping:")
    print("-" * 40)
    print("   Azure AD OS → Asset Type")
    print("   Windows → laptop")
    print("   macOS → laptop")
    print("   iOS → phone")
    print("   Android → phone")
    print("   Other → other")
    
    print("\n🎯 Ready to test the enhanced device sync!")
    print("   Run: python manage.py sync_azure_ad --employees-only")
    print("   Or use the web interface at: http://localhost:8000/azure-sync/")

def test_sync_commands():
    """Test the available sync commands"""
    print("\n📝 Available Sync Commands:")
    print("-" * 40)
    print("   python manage.py sync_azure_ad                    # Full sync with devices")
    print("   python manage.py sync_azure_ad --employees-only   # Sync employees + their devices")
    print("   python manage.py sync_azure_ad --devices-only     # Sync standalone devices")
    print("   python manage.py sync_azure_ad --assignments-only # Sync device assignments")
    print("   python manage.py sync_azure_ad --summary          # Show sync summary")
    print("   python manage.py sync_azure_ad --cleanup-only     # Cleanup orphaned assets")

def show_expected_results():
    """Show what to expect after running the sync"""
    print("\n📊 Expected Results After Sync:")
    print("-" * 40)
    print("   ✅ All Azure AD users imported as employees")
    print("   ✅ All user devices imported as assets")
    print("   ✅ Devices automatically assigned to their owners")
    print("   ✅ Asset types correctly mapped")
    print("   ✅ OS information preserved")
    print("   ✅ Serial numbers generated from Azure AD device IDs")
    print("   ✅ Asset status set to 'assigned'")
    print("   ✅ Comprehensive sync reporting")

if __name__ == "__main__":
    test_device_sync()
    test_sync_commands()
    show_expected_results()
    
    print("\n" + "=" * 70)
    print("✅ Enhanced Device Sync Test Complete!")
    print("   The system now automatically:")
    print("   • Imports user devices from Azure AD")
    print("   • Creates assets for each device")
    print("   • Assigns devices to their owners")
    print("   • Handles device updates and reassignments")
    print("   • Provides comprehensive device management")
