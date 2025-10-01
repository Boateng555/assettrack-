#!/usr/bin/env python3
"""
Harren Group Email Setup for AssetTrack
Configure your business email: sal-it-office@harren-group.com
"""

import os
from pathlib import Path

def setup_harren_email():
    """Setup Harren Group business email for AssetTrack"""
    
    print("🏢 Harren Group Email Setup for AssetTrack")
    print("=" * 50)
    print("📧 Using: sal-it-office@harren-group.com")
    
    print("\n📋 You'll need your email server details from IT department:")
    print("   • Email server hostname (e.g., mail.harren-group.com)")
    print("   • Email server port (usually 587 or 465)")
    print("   • Your email password")
    
    print("\n🔧 Let's configure your email settings:")
    
    # Get email server details
    email_host = input("\n📧 Enter your email server hostname (e.g., mail.harren-group.com): ").strip()
    if not email_host:
        email_host = "mail.harren-group.com"
        print(f"   Using default: {email_host}")
    
    email_port = input("🔌 Enter email server port (587 or 465): ").strip()
    if not email_port:
        email_port = "587"
        print(f"   Using default: {email_port}")
    
    email_password = input("🔑 Enter password for sal-it-office@harren-group.com: ").strip()
    
    if email_password:
        # Create/update .env file
        env_file = Path('.env')
        env_content = ""
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_content = f.read()
        
        # Update email settings
        email_settings = {
            'EMAIL_HOST': email_host,
            'EMAIL_PORT': email_port,
            'EMAIL_HOST_USER': 'sal-it-office@harren-group.com',
            'EMAIL_HOST_PASSWORD': email_password,
            'EMAIL_DOMAIN': 'harren-group.com'
        }
        
        for key, value in email_settings.items():
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
        
        print("\n✅ Email configuration saved!")
        print(f"📧 From: sal-it-office@harren-group.com")
        print(f"🌐 Server: {email_host}:{email_port}")
        
        # Test configuration
        test_email_config()
        
    else:
        print("❌ No password provided. Email will use console backend for development.")
        print("💡 You can run this script again later to configure email.")

def test_email_config():
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
        print(f"🌐 Email host: {settings.EMAIL_HOST}")
        print(f"🔌 Email port: {settings.EMAIL_PORT}")
        
        print("✅ Email configuration looks good!")
        print("\n💡 To test actual sending:")
        print("   1. Go to a handover in your AssetTrack app")
        print("   2. Click 'Employee Signature'")
        print("   3. Draw a signature and click 'Send'")
        print("   4. Check if email is sent to the employee")
        
    except Exception as e:
        print(f"❌ Error testing email configuration: {e}")

if __name__ == "__main__":
    setup_harren_email()
    
    print("\n🎉 Setup complete!")
    print("\n📚 Next steps:")
    print("1. Restart your Django server: python manage.py runserver")
    print("2. Test the 'Send' button in handover signature modal")
    print("3. Check that emails are sent from sal-it-office@harren-group.com")
    print("\n📞 If you need help with email server settings, contact your IT department.")
