#!/usr/bin/env python3
"""
Test Email System for AssetTrack
This script shows you how the email system works in development mode.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_system():
    """Test the email system"""
    
    print("🧪 Testing AssetTrack Email System")
    print("=" * 50)
    
    print(f"📧 Email backend: {settings.EMAIL_BACKEND}")
    print(f"📧 From email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"🌐 Email domain: {settings.EMAIL_DOMAIN}")
    
    print("\n📧 Sending test email...")
    print("(In development mode, this will be displayed below)")
    print("-" * 50)
    
    try:
        # Send a test email
        send_mail(
            subject='Asset Handover Signature Required - TEST-001 - Harren Group',
            message='''Asset Handover Signature Required - TEST-001

Dear John Doe,

You have been assigned assets that require your signature for handover. Please review and sign the handover document.

Handover Details:
- Handover ID: TEST-001
- Created: January 15, 2025 at 2:30 PM
- Status: Pending

To sign the handover document, please visit:
http://localhost:8000/handovers/test-handover-id/

This is an automated message from Harren Group AssetTrack.''',
            from_email='it-office-sal@harren-group.com',
            recipient_list=['employee@harren-group.com'],
            fail_silently=False,
        )
        
        print("-" * 50)
        print("✅ Test email sent successfully!")
        print("\n💡 In development mode:")
        print("   • Emails are displayed in the console above")
        print("   • No actual emails are sent")
        print("   • Perfect for testing the system")
        
        print("\n🚀 How to test in your AssetTrack app:")
        print("   1. Go to a handover in your app")
        print("   2. Click 'Employee Signature'")
        print("   3. Draw a signature")
        print("   4. Click 'Send' button")
        print("   5. Check the console/terminal for the email content")
        
    except Exception as e:
        print(f"❌ Error sending test email: {e}")

def show_production_setup():
    """Show how to set up production email"""
    
    print("\n🏢 For Production Email Setup:")
    print("=" * 30)
    print("📞 Contact your IT department and ask for:")
    print("   • SMTP server hostname (e.g., smtp.office365.com)")
    print("   • SMTP port (usually 587)")
    print("   • Email password or App Password")
    print("   • Authentication method")
    
    print("\n🔧 Then update your .env file with:")
    print("   EMAIL_HOST=your_smtp_server")
    print("   EMAIL_PORT=587")
    print("   EMAIL_HOST_USER=it-office-sal@harren-group.com")
    print("   EMAIL_HOST_PASSWORD=your_password")
    
    print("\n📝 And change in settings.py:")
    print("   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'")

if __name__ == "__main__":
    test_email_system()
    show_production_setup()
    
    print("\n🎉 Email system is ready for testing!")
    print("📧 All emails will be displayed in the console")
    print("💡 Perfect for development and testing!")
