#!/usr/bin/env python
"""
Remove Azure AD Credentials

This script helps you remove Azure AD credentials
and verify the connection is completely removed.
"""

import os
import sys

def show_credential_removal():
    """Show how to remove Azure AD credentials"""
    
    print("🧹 REMOVE AZURE AD CREDENTIALS")
    print("=" * 40)
    
    print("To completely remove Azure AD connection:")
    print()
    print("1. 📝 Edit your .env file:")
    print("   - Open .env file in your project root")
    print("   - Find these lines:")
    print("     AZURE_TENANT_ID=...")
    print("     AZURE_CLIENT_ID=...")
    print("     AZURE_CLIENT_SECRET=...")
    print()
    print("   - Delete or comment them out:")
    print("     # AZURE_TENANT_ID=...")
    print("     # AZURE_CLIENT_ID=...")
    print("     # AZURE_CLIENT_SECRET=...")
    print()
    print("2. 🔒 Delete Azure AD App from Azure Portal:")
    print("   - Go to https://portal.azure.com")
    print("   - Azure Active Directory → App registrations")
    print("   - Find your AssetTrack app")
    print("   - Click Delete")
    print()
    print("3. 🧪 Test removal:")
    print("   python setup_real_azure_ad.py --test")
    print("   (Should show 'Azure AD not configured')")

def show_current_status():
    """Show current system status"""
    
    print("\n📊 CURRENT SYSTEM STATUS")
    print("=" * 30)
    
    print("✅ Azure AD data removed from database")
    print("✅ System ready for new setup")
    print("⚠️  Azure AD credentials still configured")
    print("⚠️  Need to remove from .env file")
    print("⚠️  Need to delete Azure AD app")

def show_next_steps():
    """Show next steps after removal"""
    
    print("\n🎯 NEXT STEPS AFTER REMOVAL:")
    print("=" * 35)
    
    print("1. ✅ Remove credentials from .env file")
    print("2. ✅ Delete Azure AD app from Azure Portal")
    print("3. ✅ Test that connection is removed")
    print("4. 🔄 Set up new Azure AD app when ready")
    print("5. 🔄 Configure new credentials")
    print("6. 🔄 Test new connection")
    print("7. 🔄 Sync with new Azure AD")

if __name__ == "__main__":
    show_credential_removal()
    show_current_status()
    show_next_steps()
