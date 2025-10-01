#!/usr/bin/env python
"""
Update Environment File

This script helps you update your .env file with the new Azure AD credentials.
"""

import os

def update_env_file():
    """Update .env file with new Azure AD credentials"""
    
    print("📝 UPDATING .env FILE WITH NEW AZURE AD CREDENTIALS")
    print("=" * 60)
    
    # Your credentials
    tenant_id = "50FADA20-1C23-45E6-9E98-0E55F3B03047"
    client_id = "5D3FC499-C87A-4982-A5C2-D3668C3B6CD6"
    
    print(f"✅ Tenant ID: {tenant_id}")
    print(f"✅ Client ID: {client_id}")
    print()
    print("🔒 Now you need to get the Client Secret from Azure Portal:")
    print("1. Go to your Azure AD app")
    print("2. Certificates & secrets → New client secret")
    print("3. Copy the Value (you won't see it again!)")
    print()
    
    # Get client secret from user
    client_secret = input("Enter your Client Secret value: ").strip()
    
    if not client_secret:
        print("❌ Client Secret is required!")
        return False
    
    # Create .env content
    env_content = f"""# Azure AD Configuration
AZURE_TENANT_ID={tenant_id}
AZURE_CLIENT_ID={client_id}
AZURE_CLIENT_SECRET={client_secret}
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file updated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def show_next_steps():
    """Show next steps after updating .env file"""
    
    print("\n🎯 NEXT STEPS:")
    print("=" * 20)
    print()
    print("1. 🧪 Test the connection:")
    print("   python setup_real_azure_ad.py --test")
    print()
    print("2. 🔄 Sync with Azure AD:")
    print("   python manage.py sync_azure_ad --summary")
    print("   python manage.py sync_azure_ad")
    print()
    print("3. 🌐 Use web interface:")
    print("   http://localhost:8000/azure-sync/")

if __name__ == "__main__":
    success = update_env_file()
    
    if success:
        show_next_steps()
    else:
        print("\n❌ Failed to update .env file. Please try again.")
