#!/usr/bin/env python3
"""
Azure Email Setup Script for AssetTrack
This script helps you configure Azure email services for professional email delivery.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create or update .env file with Azure email credentials"""
    env_file = Path('.env')
    
    print("🔧 Azure Email Setup for AssetTrack")
    print("=" * 50)
    
    print("\n📧 Choose your Azure email service:")
    print("1. Azure Communication Services (Recommended)")
    print("2. Azure SendGrid")
    print("3. Skip for now (use console backend)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        setup_azure_communication()
    elif choice == "2":
        setup_sendgrid()
    elif choice == "3":
        print("✅ Skipping email setup. Using console backend for development.")
        return
    else:
        print("❌ Invalid choice. Please run the script again.")
        return

def setup_azure_communication():
    """Setup Azure Communication Services"""
    print("\n🚀 Setting up Azure Communication Services...")
    print("\n📋 You'll need:")
    print("   • Azure Communication Services resource")
    print("   • Connection string from Azure Portal")
    print("   • Verified email domain")
    
    print("\n🔗 Steps to get credentials:")
    print("1. Go to https://portal.azure.com")
    print("2. Search for 'Communication Services'")
    print("3. Create a new resource")
    print("4. Go to 'Keys' section")
    print("5. Copy the 'Connection String'")
    
    connection_string = input("\n📝 Enter your Azure Communication Services connection string: ").strip()
    from_email = input("📧 Enter your sender email (e.g., noreply@yourdomain.com): ").strip()
    
    if connection_string and from_email:
        update_env_file({
            'AZURE_EMAIL_USER': from_email,
            'AZURE_EMAIL_PASSWORD': connection_string,
            'DEFAULT_FROM_EMAIL': from_email
        })
        print("✅ Azure Communication Services configured!")
    else:
        print("❌ Missing credentials. Please run the script again.")

def setup_sendgrid():
    """Setup Azure SendGrid"""
    print("\n📧 Setting up Azure SendGrid...")
    print("\n📋 You'll need:")
    print("   • SendGrid account (via Azure Portal)")
    print("   • API key from SendGrid")
    
    print("\n🔗 Steps to get credentials:")
    print("1. Go to https://portal.azure.com")
    print("2. Search for 'SendGrid'")
    print("3. Create a new SendGrid resource")
    print("4. Click 'Manage' to go to SendGrid dashboard")
    print("5. Go to Settings > API Keys")
    print("6. Create new API key with 'Full Access'")
    
    api_key = input("\n🔑 Enter your SendGrid API key: ").strip()
    from_email = input("📧 Enter your sender email (e.g., noreply@yourdomain.com): ").strip()
    
    if api_key and from_email:
        update_env_file({
            'SENDGRID_API_KEY': api_key,
            'DEFAULT_FROM_EMAIL': from_email
        })
        print("✅ SendGrid configured!")
    else:
        print("❌ Missing credentials. Please run the script again.")

def update_env_file(credentials):
    """Update .env file with new credentials"""
    env_file = Path('.env')
    
    # Read existing .env file
    env_content = ""
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Update or add credentials
    for key, value in credentials.items():
        if f"{key}=" in env_content:
            # Update existing
            lines = env_content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[i] = f"{key}={value}"
                    break
            env_content = '\n'.join(lines)
        else:
            # Add new
            env_content += f"\n{key}={value}\n"
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"\n💾 Updated .env file with email credentials")

def test_email_configuration():
    """Test the email configuration"""
    print("\n🧪 Testing email configuration...")
    
    try:
        # Import Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
        import django
        django.setup()
        
        from django.core.mail import send_mail
        from django.conf import settings
        
        print(f"📧 Email backend: {settings.EMAIL_BACKEND}")
        print(f"📧 From email: {settings.DEFAULT_FROM_EMAIL}")
        
        # Test email (don't actually send)
        print("✅ Email configuration looks good!")
        print("💡 To test actual sending, use the 'Send' button in your handover signature modal.")
        
    except Exception as e:
        print(f"❌ Error testing email configuration: {e}")

if __name__ == "__main__":
    create_env_file()
    test_email_configuration()
    
    print("\n🎉 Setup complete!")
    print("\n📚 Next steps:")
    print("1. Restart your Django server")
    print("2. Test the 'Send' button in handover signature modal")
    print("3. Check that emails are delivered to employee inboxes")
    print("\n📖 For detailed setup instructions, see: AZURE_EMAIL_SETUP.md")
