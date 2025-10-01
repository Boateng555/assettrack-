#!/usr/bin/env python
"""
Test Device Permissions

This script tests if device permissions are working properly.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration

def test_device_permissions():
    """Test device permissions"""
    
    print("🧪 TESTING DEVICE PERMISSIONS")
    print("=" * 35)
    
    try:
        azure_ad = AzureADIntegration()
        
        # Test simple device query
        print("Testing simple device query...")
        devices = azure_ad.get_devices()
        print(f"✅ Devices found: {len(devices)}")
        
        if devices:
            print("\n📱 Sample devices:")
            for device in devices[:3]:
                print(f"  - {device.get('displayName', 'Unknown')} ({device.get('operatingSystem', 'Unknown OS')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Device query failed: {e}")
        return False

def show_troubleshooting():
    """Show troubleshooting steps"""
    
    print("\n🔧 TROUBLESHOOTING DEVICE PERMISSIONS")
    print("=" * 45)
    
    print("If device permissions are still not working:")
    print()
    print("1. 🔐 Check Admin Consent:")
    print("   - Go to Azure Portal → Your app → API permissions")
    print("   - Look for 'Grant admin consent' button")
    print("   - Click it and confirm")
    print()
    print("2. ⏰ Wait for Propagation:")
    print("   - Permissions can take 5-10 minutes to propagate")
    print("   - Try again after waiting")
    print()
    print("3. 🔍 Check Permission Details:")
    print("   - Make sure Device.Read.All shows 'Yes' status")
    print("   - Verify it's an Application permission (not Delegated)")
    print()
    print("4. 🧪 Test Alternative Permissions:")
    print("   - Try adding DeviceManagement.Read.All")
    print("   - Or DeviceManagementConfiguration.Read.All")
    print()
    print("5. 📞 Contact Admin:")
    print("   - Your Azure AD admin may need to grant consent")
    print("   - Some organizations restrict device access")

if __name__ == "__main__":
    success = test_device_permissions()
    
    if not success:
        show_troubleshooting()
    else:
        print("\n🎉 Device permissions are working!")
        print("You can now sync devices from Azure AD.")
