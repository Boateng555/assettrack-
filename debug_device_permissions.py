#!/usr/bin/env python
"""
Debug Device Permissions

This script helps diagnose why device permissions aren't working.
"""

import os
import sys
import django
import requests

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration
from django.conf import settings

def debug_device_permissions():
    """Debug device permission issues"""
    
    print("🔍 DEBUGGING DEVICE PERMISSIONS")
    print("=" * 40)
    
    # Check Azure AD configuration
    tenant_id = getattr(settings, 'AZURE_TENANT_ID', None)
    client_id = getattr(settings, 'AZURE_CLIENT_ID', None)
    client_secret = getattr(settings, 'AZURE_CLIENT_SECRET', None)
    
    print(f"Tenant ID: {'✅ Set' if tenant_id else '❌ Not Set'}")
    print(f"Client ID: {'✅ Set' if client_id else '❌ Not Set'}")
    print(f"Client Secret: {'✅ Set' if client_secret else '❌ Not Set'}")
    
    if not all([tenant_id, client_id, client_secret]):
        print("❌ Azure AD credentials not configured!")
        return False
    
    # Test connection
    try:
        azure_ad = AzureADIntegration()
        print("\n🧪 Testing Azure AD connection...")
        
        # Test user access (this works)
        users = azure_ad.get_users()
        print(f"✅ Users access: {len(users)} users found")
        
        # Test device access with different approaches
        print("\n🔍 Testing device access...")
        
        # Method 1: Simple device query
        try:
            headers = azure_ad.get_headers()
            if headers:
                url = "https://graph.microsoft.com/v1.0/devices"
                response = requests.get(url, headers=headers)
                print(f"Method 1 - Simple devices query: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Found {len(data.get('value', []))} devices")
                else:
                    print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
        
        # Method 2: Device query with filter
        try:
            headers = azure_ad.get_headers()
            if headers:
                url = "https://graph.microsoft.com/v1.0/devices"
                params = {
                    '$select': 'id,displayName,deviceId',
                    '$top': 5
                }
                response = requests.get(url, headers=headers, params=params)
                print(f"Method 2 - Filtered devices query: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Found {len(data.get('value', []))} devices")
                else:
                    print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"❌ Method 2 failed: {e}")
        
        # Method 3: Check permissions
        try:
            headers = azure_ad.get_headers()
            if headers:
                url = "https://graph.microsoft.com/v1.0/me"
                response = requests.get(url, headers=headers)
                print(f"Method 3 - Me query: {response.status_code}")
                if response.status_code == 200:
                    print("✅ Basic Graph API access working")
                else:
                    print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"❌ Method 3 failed: {e}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    return True

def show_fix_instructions():
    """Show how to fix device permissions"""
    
    print("\n🔧 HOW TO FIX DEVICE PERMISSIONS")
    print("=" * 40)
    
    print("The 403 Forbidden error means device permissions aren't working.")
    print("Here's how to fix it:")
    print()
    print("1. 🌐 Go to Azure Portal:")
    print("   https://portal.azure.com")
    print()
    print("2. 📱 Navigate to your app:")
    print("   Azure Active Directory → App registrations → Your AssetTrack app")
    print()
    print("3. 🔐 Check API Permissions:")
    print("   - Click 'API permissions'")
    print("   - Look for 'Device.Read.All'")
    print("   - Make sure it shows 'Yes' status")
    print()
    print("4. ⚠️  GRANT ADMIN CONSENT:")
    print("   - Look for 'Grant admin consent' button")
    print("   - Click it and confirm")
    print("   - This is the most important step!")
    print()
    print("5. 🔄 Try Alternative Permissions:")
    print("   - Add 'DeviceManagement.Read.All'")
    print("   - Add 'DeviceManagementConfiguration.Read.All'")
    print("   - Grant admin consent for these too")
    print()
    print("6. ⏰ Wait 5-10 minutes:")
    print("   - Permissions can take time to propagate")
    print("   - Try again after waiting")

if __name__ == "__main__":
    success = debug_device_permissions()
    
    if not success:
        print("\n❌ Debug failed")
    else:
        show_fix_instructions()
