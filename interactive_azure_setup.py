#!/usr/bin/env python
"""
Interactive Azure AD Setup

This script guides you through setting up a new Azure AD app
and helps you configure everything step by step.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

def show_step_1():
    """Step 1: Access Azure Portal"""
    
    print("🔧 STEP 1: ACCESS AZURE PORTAL")
    print("=" * 40)
    print()
    print("1. 🌐 Go to: https://portal.azure.com")
    print("2. 🔐 Sign in with your Azure account")
    print("3. 📍 Navigate to: Azure Active Directory (left menu)")
    print()
    print("Press Enter when you're in Azure Active Directory...")
    input()

def show_step_2():
    """Step 2: Create App Registration"""
    
    print("🔑 STEP 2: CREATE APP REGISTRATION")
    print("=" * 40)
    print()
    print("1. 📱 Click: 'App registrations' (left menu)")
    print("2. ➕ Click: 'New registration' (top)")
    print("3. 📝 Fill in the details:")
    print("   - Name: AssetTrack Integration")
    print("   - Supported account types: Accounts in this organizational directory only")
    print("   - Redirect URI: Web → https://localhost:8000/accounts/microsoft/login/callback/")
    print("4. ✅ Click: 'Register'")
    print()
    print("Press Enter when you've created the app registration...")
    input()

def show_step_3():
    """Step 3: Get Credentials"""
    
    print("📋 STEP 3: GET YOUR CREDENTIALS")
    print("=" * 40)
    print()
    print("After registration, you'll see the Overview page:")
    print()
    print("📋 COPY THESE VALUES:")
    print("1. 🔑 Application (client) ID")
    print("2. 🏢 Directory (tenant) ID")
    print()
    print("Example:")
    print("- Application ID: 12345678-1234-1234-1234-123456789abc")
    print("- Directory ID: 87654321-4321-4321-4321-cba987654321")
    print()
    print("Press Enter when you've copied both values...")
    input()

def show_step_4():
    """Step 4: Add API Permissions"""
    
    print("🔐 STEP 4: ADD API PERMISSIONS")
    print("=" * 40)
    print()
    print("1. 📱 Click: 'API permissions' (left menu)")
    print("2. ➕ Click: 'Add a permission'")
    print("3. 🔍 Select: 'Microsoft Graph'")
    print("4. 🔍 Choose: 'Application permissions'")
    print("5. ✅ Add these permissions:")
    print("   - User.Read.All (Read all users)")
    print("   - Device.Read.All (Read all devices)")
    print("   - Directory.Read.All (Read directory data)")
    print("6. ✅ Click: 'Add permissions'")
    print("7. ⚠️  IMPORTANT: Click 'Grant admin consent' (required!)")
    print()
    print("Press Enter when you've added permissions and granted consent...")
    input()

def show_step_5():
    """Step 5: Create Client Secret"""
    
    print("🔒 STEP 5: CREATE CLIENT SECRET")
    print("=" * 40)
    print()
    print("1. 📱 Click: 'Certificates & secrets' (left menu)")
    print("2. ➕ Click: 'New client secret'")
    print("3. 📝 Add description: AssetTrack Integration Secret")
    print("4. ⏰ Expires: 24 months (recommended)")
    print("5. ✅ Click: 'Add'")
    print("6. ⚠️  IMPORTANT: Copy the Value immediately!")
    print("   (You won't see it again)")
    print()
    print("Press Enter when you've created the secret and copied the value...")
    input()

def show_step_6():
    """Step 6: Update Environment Variables"""
    
    print("📝 STEP 6: UPDATE ENVIRONMENT VARIABLES")
    print("=" * 45)
    print()
    print("Create or update your .env file with:")
    print()
    print("# New Azure AD Configuration")
    print("AZURE_TENANT_ID=your-directory-tenant-id")
    print("AZURE_CLIENT_ID=your-application-client-id")
    print("AZURE_CLIENT_SECRET=your-client-secret-value")
    print()
    print("Example:")
    print("AZURE_TENANT_ID=87654321-4321-4321-4321-cba987654321")
    print("AZURE_CLIENT_ID=12345678-1234-1234-1234-123456789abc")
    print("AZURE_CLIENT_SECRET=your-secret-value-here")
    print()
    print("Press Enter when you've updated your .env file...")
    input()

def show_step_7():
    """Step 7: Test Connection"""
    
    print("🧪 STEP 7: TEST CONNECTION")
    print("=" * 30)
    print()
    print("Run this command to test your connection:")
    print()
    print("python setup_real_azure_ad.py --test")
    print()
    print("Expected output:")
    print("✅ Connection successful!")
    print("📊 Found X users in Azure AD")
    print()
    print("Press Enter when you're ready to test...")
    input()

def show_step_8():
    """Step 8: Sync Data"""
    
    print("🔄 STEP 8: SYNC WITH AZURE AD")
    print("=" * 35)
    print()
    print("Once connection is working, sync your data:")
    print()
    print("# Check sync status")
    print("python manage.py sync_azure_ad --summary")
    print()
    print("# Full sync")
    print("python manage.py sync_azure_ad")
    print()
    print("Press Enter when you're ready to sync...")
    input()

def show_success():
    """Show success message"""
    
    print("🎉 SUCCESS! AZURE AD APP SET UP COMPLETE!")
    print("=" * 50)
    print()
    print("✅ Azure AD app registered")
    print("✅ Credentials configured")
    print("✅ API permissions added")
    print("✅ Admin consent granted")
    print("✅ Connection tested")
    print("✅ Ready to sync!")
    print()
    print("🚀 Your AssetTrack system is now connected to Azure AD!")

def main():
    """Main setup process"""
    
    print("🔧 AZURE AD APP SETUP GUIDE")
    print("=" * 30)
    print()
    print("This guide will help you set up a new Azure AD app")
    print("for your AssetTrack system step by step.")
    print()
    print("Press Enter to start...")
    input()
    
    show_step_1()
    show_step_2()
    show_step_3()
    show_step_4()
    show_step_5()
    show_step_6()
    show_step_7()
    show_step_8()
    show_success()

if __name__ == "__main__":
    main()
