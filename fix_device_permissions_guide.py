#!/usr/bin/env python
"""
Fix Device Permissions Guide

This script provides step-by-step instructions to fix device permissions.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

def show_step_by_step_fix():
    """Show step-by-step instructions to fix device permissions"""
    
    print("🔧 FIX DEVICE PERMISSIONS - STEP BY STEP")
    print("=" * 45)
    print()
    print("The 403 Forbidden error means admin consent is not granted.")
    print("Follow these steps to fix it:")
    print()
    print("STEP 1: 🌐 GO TO AZURE PORTAL")
    print("=" * 30)
    print("1. Open: https://portal.azure.com")
    print("2. Sign in with your Azure account")
    print("3. Navigate to: Azure Active Directory")
    print()
    print("STEP 2: 📱 FIND YOUR APP")
    print("=" * 25)
    print("1. Click: 'App registrations' (left menu)")
    print("2. Find: 'AssetTrack Integration' (your app)")
    print("3. Click on it to open")
    print()
    print("STEP 3: 🔐 CHECK API PERMISSIONS")
    print("=" * 35)
    print("1. Click: 'API permissions' (left menu)")
    print("2. Look for: Microsoft Graph permissions")
    print("3. Check if you see:")
    print("   ✅ User.Read.All (should show 'Yes')")
    print("   ❓ Device.Read.All (check status)")
    print("   ✅ Directory.Read.All (should show 'Yes')")
    print()
    print("STEP 4: ⚠️  GRANT ADMIN CONSENT (CRITICAL!)")
    print("=" * 45)
    print("1. Look for: 'Grant admin consent for [Your Organization]' button")
    print("2. Click: 'Grant admin consent'")
    print("3. Confirm: The consent dialog")
    print("4. Wait: 5-10 minutes for permissions to propagate")
    print()
    print("STEP 5: 🔄 ADD ALTERNATIVE PERMISSIONS (if needed)")
    print("=" * 50)
    print("If Device.Read.All still doesn't work, try these:")
    print("1. Click: 'Add a permission'")
    print("2. Select: 'Microsoft Graph'")
    print("3. Choose: 'Application permissions'")
    print("4. Add these permissions:")
    print("   - DeviceManagement.Read.All")
    print("   - DeviceManagementConfiguration.Read.All")
    print("   - DeviceManagementApps.Read.All")
    print("5. Grant admin consent for these too")
    print()
    print("STEP 6: 🧪 TEST THE FIX")
    print("=" * 25)
    print("After granting consent, run:")
    print("python debug_device_permissions.py")
    print()
    print("Expected result:")
    print("✅ Device API call: 200 (success)")
    print("✅ Found X devices in Azure AD")

def show_troubleshooting():
    """Show troubleshooting for common issues"""
    
    print("\n🚨 TROUBLESHOOTING COMMON ISSUES")
    print("=" * 40)
    print()
    print("❌ ISSUE: 'Grant admin consent' button not visible")
    print("✅ SOLUTION:")
    print("   - You may not have admin rights")
    print("   - Contact your Azure AD administrator")
    print("   - Ask them to grant consent for your app")
    print()
    print("❌ ISSUE: Permission shows 'Yes' but still 403 error")
    print("✅ SOLUTION:")
    print("   - Wait 5-10 minutes for propagation")
    print("   - Try different device permissions")
    print("   - Check if your org restricts device access")
    print()
    print("❌ ISSUE: No devices found after fixing permissions")
    print("✅ SOLUTION:")
    print("   - Your org may not have devices registered")
    print("   - Add some test devices to Azure AD")
    print("   - Register devices for users")
    print()
    print("❌ ISSUE: Still getting 403 after admin consent")
    print("✅ SOLUTION:")
    print("   - Try alternative permissions:")
    print("     - DeviceManagement.Read.All")
    print("     - DeviceManagementConfiguration.Read.All")
    print("   - Contact Azure AD administrator")
    print("   - Check organization policies")

def show_expected_results():
    """Show what to expect after fixing"""
    
    print("\n🎯 EXPECTED RESULTS AFTER FIXING")
    print("=" * 40)
    print()
    print("✅ SUCCESS INDICATORS:")
    print("   - Device API call: 200 (success)")
    print("   - Found X devices in Azure AD")
    print("   - No more 403 Forbidden errors")
    print("   - Device sync works in AssetTrack")
    print()
    print("📊 WHAT YOU'LL SEE:")
    print("   - Devices appear in Azure AD sync")
    print("   - Devices automatically assigned to users")
    print("   - Asset types correctly determined")
    print("   - Complete device management")
    print()
    print("🚀 NEXT STEPS AFTER FIXING:")
    print("   1. Test device sync")
    print("   2. Add devices to Azure AD")
    print("   3. Sync devices to AssetTrack")
    print("   4. Verify device assignments")

if __name__ == "__main__":
    show_step_by_step_fix()
    show_troubleshooting()
    show_expected_results()
