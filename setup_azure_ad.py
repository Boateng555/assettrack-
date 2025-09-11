#!/usr/bin/env python
"""
Azure AD Setup Script
This script helps you configure Azure AD credentials for real-time testing
"""

import os
import sys

def setup_azure_credentials():
    """Interactive setup for Azure AD credentials"""
    
    print("🔗 Azure AD Integration Setup")
    print("=" * 50)
    print()
    print("This script will help you configure Azure AD credentials for real-time testing.")
    print("You'll need to get these values from the Azure Portal.")
    print()
    
    # Get credentials from user
    print("📋 Please enter your Azure AD credentials:")
    print()
    
    tenant_id = input("Enter your Azure AD Tenant ID: ").strip()
    client_id = input("Enter your Azure AD Client ID: ").strip()
    client_secret = input("Enter your Azure AD Client Secret: ").strip()
    
    if not all([tenant_id, client_id, client_secret]):
        print("❌ All credentials are required!")
        return False
    
    # Create settings configuration
    settings_content = f"""
# Azure AD Configuration - Added by setup script
AZURE_TENANT_ID = '{tenant_id}'
AZURE_CLIENT_ID = '{client_id}'
AZURE_CLIENT_SECRET = '{client_secret}'

# Optional: Configure sync settings
AZURE_SYNC_ENABLED = True
AZURE_SYNC_INTERVAL = 3600  # Sync every hour (in seconds)
"""
    
    # Update settings.py
    settings_file = 'assettrack_django/settings.py'
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Check if Azure AD settings already exist
        if 'AZURE_TENANT_ID' in content:
            print("⚠️  Azure AD settings already exist in settings.py")
            overwrite = input("Do you want to overwrite them? (y/N): ").strip().lower()
            if overwrite != 'y':
                print("Setup cancelled.")
                return False
            
            # Remove existing Azure AD settings
            lines = content.split('\n')
            new_lines = []
            skip_azure = False
            
            for line in lines:
                if line.strip().startswith('AZURE_'):
                    skip_azure = True
                    continue
                elif skip_azure and line.strip() == '':
                    skip_azure = False
                    continue
                elif skip_azure:
                    continue
                new_lines.append(line)
            
            content = '\n'.join(new_lines)
        
        # Add new Azure AD settings
        content += settings_content
        
        with open(settings_file, 'w') as f:
            f.write(content)
        
        print("✅ Azure AD credentials added to settings.py")
        print()
        
        # Create .env file for environment variables (optional)
        env_content = f"""# Azure AD Environment Variables
AZURE_TENANT_ID={tenant_id}
AZURE_CLIENT_ID={client_id}
AZURE_CLIENT_SECRET={client_secret}
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env file with environment variables")
        print()
        
        # Test the configuration
        print("🧪 Testing Azure AD configuration...")
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
            import django
            django.setup()
            
            from assets.azure_ad_integration import AzureADIntegration
            
            azure_ad = AzureADIntegration()
            token = azure_ad.get_access_token()
            
            if token:
                print("✅ Azure AD authentication successful!")
                print("🎉 Your Azure AD integration is ready for testing!")
            else:
                print("❌ Azure AD authentication failed!")
                print("Please check your credentials and permissions.")
                return False
                
        except Exception as e:
            print(f"❌ Error testing Azure AD configuration: {e}")
            return False
        
        print()
        print("🚀 Next steps:")
        print("1. Run: python manage.py sync_azure_ad")
        print("2. Visit: http://localhost:8000/azure-status/")
        print("3. Check your dashboard for synced employees and devices")
        print()
        print("📚 For more help, see: AZURE_AD_REAL_SETUP.md")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating settings: {e}")
        return False

def show_azure_portal_instructions():
    """Show instructions for getting Azure AD credentials"""
    
    print("📋 How to Get Azure AD Credentials")
    print("=" * 40)
    print()
    print("1. Go to Azure Portal: https://portal.azure.com")
    print("2. Navigate to: Azure Active Directory → App registrations")
    print("3. Click 'New registration'")
    print("4. Fill in:")
    print("   - Name: AssetTrack Integration")
    print("   - Supported account types: Accounts in this organizational directory only")
    print("   - Redirect URI: http://localhost:8000/")
    print("5. After registration, copy:")
    print("   - Application (client) ID → AZURE_CLIENT_ID")
    print("   - Directory (tenant) ID → AZURE_TENANT_ID")
    print("6. Go to Certificates & secrets")
    print("7. Create new client secret → AZURE_CLIENT_SECRET")
    print("8. Go to API permissions")
    print("9. Add Microsoft Graph permissions:")
    print("   - User.Read.All")
    print("   - Device.Read.All")
    print("   - Directory.Read.All")
    print("10. Grant admin consent")
    print()

def main():
    """Main setup function"""
    
    print("🔗 AssetTrack Azure AD Integration Setup")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        show_azure_portal_instructions()
        return
    
    print("Choose an option:")
    print("1. Setup Azure AD credentials")
    print("2. Show Azure Portal instructions")
    print("3. Exit")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        setup_azure_credentials()
    elif choice == '2':
        show_azure_portal_instructions()
    elif choice == '3':
        print("Setup cancelled.")
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()

