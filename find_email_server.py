#!/usr/bin/env python3
"""
Find Harren Group Email Server Settings
This script helps you discover your email server configuration.
"""

import smtplib
import socket
from email.mime.text import MIMEText

def test_email_servers():
    """Test common email server configurations for Harren Group"""
    
    print("🔍 Finding Harren Group Email Server Settings")
    print("=" * 50)
    
    # Common email server configurations to test
    servers_to_test = [
        {
            'name': 'Microsoft 365 / Office 365',
            'host': 'smtp.office365.com',
            'port': 587,
            'description': 'Most common for business emails'
        },
        {
            'name': 'Google Workspace',
            'host': 'smtp.gmail.com',
            'port': 587,
            'description': 'If using Google Workspace'
        },
        {
            'name': 'Harren Group Custom Server',
            'host': 'mail.harren-group.com',
            'port': 587,
            'description': 'Custom company server'
        },
        {
            'name': 'Harren Group Custom Server (SSL)',
            'host': 'mail.harren-group.com',
            'port': 465,
            'description': 'Custom company server with SSL'
        },
        {
            'name': 'Exchange Server',
            'host': 'mail.harren-group.com',
            'port': 25,
            'description': 'Internal Exchange server'
        }
    ]
    
    print("🧪 Testing common email server configurations...")
    print("📧 Your email: sal-it-office@harren-group.com")
    print()
    
    working_servers = []
    
    for server in servers_to_test:
        print(f"🔍 Testing {server['name']}...")
        print(f"   Host: {server['host']}:{server['port']}")
        print(f"   Description: {server['description']}")
        
        try:
            # Test if we can connect to the server
            if server['port'] == 465:
                # SSL connection
                smtp = smtplib.SMTP_SSL(server['host'], server['port'], timeout=10)
            else:
                # TLS connection
                smtp = smtplib.SMTP(server['host'], server['port'], timeout=10)
                smtp.starttls()
            
            smtp.quit()
            print(f"   ✅ Connection successful!")
            working_servers.append(server)
            
        except Exception as e:
            print(f"   ❌ Connection failed: {str(e)[:50]}...")
        
        print()
    
    if working_servers:
        print("🎉 Found working email servers:")
        for i, server in enumerate(working_servers, 1):
            print(f"   {i}. {server['name']}")
            print(f"      Host: {server['host']}")
            print(f"      Port: {server['port']}")
            print()
        
        print("💡 Next steps:")
        print("1. Try the first working server")
        print("2. You'll need your email password")
        print("3. Run: python setup_harren_email.py")
        
    else:
        print("❌ No working servers found automatically.")
        print("\n💡 Manual steps to find your email server:")
        print("1. Check your email client settings (Outlook, etc.)")
        print("2. Contact your IT department")
        print("3. Check your phone's email settings")
        print("\n📞 Ask your IT department for:")
        print("   • SMTP server hostname")
        print("   • SMTP port (usually 587 or 465)")
        print("   • Authentication method")

def create_simple_config():
    """Create a simple configuration for testing"""
    
    print("\n🔧 Creating simple email configuration...")
    
    # Create a basic .env file for testing
    env_content = """# Harren Group Email Configuration
EMAIL_HOST=mail.harren-group.com
EMAIL_PORT=587
EMAIL_HOST_USER=sal-it-office@harren-group.com
EMAIL_HOST_PASSWORD=your_password_here
EMAIL_DOMAIN=harren-group.com
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with basic configuration")
    print("📝 Edit .env file and add your email password")
    print("🔄 Then restart your Django server")

if __name__ == "__main__":
    test_email_servers()
    create_simple_config()
    
    print("\n📚 What to do next:")
    print("1. Get your email password")
    print("2. Edit the .env file with your password")
    print("3. Test the 'Send' button in AssetTrack")
    print("4. If it doesn't work, contact your IT department")
