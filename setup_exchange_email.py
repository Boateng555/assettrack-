#!/usr/bin/env python3
"""
Microsoft Exchange Email Setup for AssetTrack
Configure: it-office-sal@harren-group.com
"""

import os
from pathlib import Path

def setup_exchange_email():
    """Setup Microsoft Exchange email for AssetTrack"""
    
    print("🏢 Microsoft Exchange Email Setup for AssetTrack")
    print("=" * 50)
    print("📧 Using: it-office-sal@harren-group.com")
    print("🌐 Server: Microsoft Exchange (Office 365)")
    
    print("\n📋 You'll need:")
    print("   • Your email password for it-office-sal@harren-group.com")
    print("   • OR an App Password (if 2FA is enabled)")
    
    print("\n🔧 Let's configure your Microsoft Exchange email:")
    
    # Get email password
    email_password = input("\n🔑 Enter password for it-office-sal@harren-group.com: ").strip()
    
    if email_password:
        # Create/update .env file
        env_file = Path('.env')
        env_content = ""
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_content = f.read()
        
        # Microsoft Exchange settings
        exchange_settings = {
            'EMAIL_HOST': 'smtp.office365.com',
            'EMAIL_PORT': '587',
            'EMAIL_HOST_USER': 'it-office-sal@harren-group.com',
            'EMAIL_HOST_PASSWORD': email_password,
            'EMAIL_DOMAIN': 'harren-group.com'
        }
        
        for key, value in exchange_settings.items():
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
        
        print("\n✅ Microsoft Exchange email configured!")
        print(f"📧 From: it-office-sal@harren-group.com")
        print(f"🌐 Server: smtp.office365.com:587")
        print(f"🔐 Authentication: TLS")
        
        # Test configuration
        test_exchange_config()
        
    else:
        print("❌ No password provided. Email will use console backend for development.")
        print("💡 You can run this script again later to configure email.")

def test_exchange_config():
    """Test the Microsoft Exchange configuration"""
    print("\n🧪 Testing Microsoft Exchange configuration...")
    
    try:
        # Import Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
        import django
        django.setup()
        
        from django.core.mail import send_mail
        from django.conf import settings
        
        print(f"📧 Email backend: {settings.EMAIL_BACKEND}")
        print(f"📧 From email: {settings.DEFAULT_FROM_EMAIL}")
        print(f"🌐 Email host: {settings.EMAIL_HOST}")
        print(f"🔌 Email port: {settings.EMAIL_PORT}")
        print(f"🔐 TLS enabled: {settings.EMAIL_USE_TLS}")
        
        print("✅ Microsoft Exchange configuration looks good!")
        print("\n💡 To test actual sending:")
        print("   1. Go to a handover in your AssetTrack app")
        print("   2. Click 'Employee Signature'")
        print("   3. Draw a signature and click 'Send'")
        print("   4. Check if email is sent from it-office-sal@harren-group.com")
        
    except Exception as e:
        print(f"❌ Error testing email configuration: {e}")

if __name__ == "__main__":
    setup_exchange_email()
    
    print("\n🎉 Setup complete!")
    print("\n📚 Next steps:")
    print("1. Restart your Django server: python manage.py runserver")
    print("2. Test the 'Send' button in handover signature modal")
    print("3. Check that emails are sent from it-office-sal@harren-group.com")
    print("\n💡 If you have 2FA enabled, you might need an App Password instead of your regular password.")
    print("📞 Contact your IT department if you need help with App Passwords.")
