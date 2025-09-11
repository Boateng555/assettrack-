#!/usr/bin/env python3
"""
Test script to verify admin avatar functionality
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from django.contrib.auth.models import User
from assets.templatetags.employee_filters import user_avatar_url, get_professional_avatar_url_for_user

def test_admin_avatar():
    """Test the admin avatar functionality"""
    print("Admin Avatar Test")
    print("=" * 50)
    print("Testing the new admin avatar system for kwameb320")
    print()
    
    # Try to find the admin user
    try:
        admin_user = User.objects.get(username='kwameb320')
        print(f"✅ Found admin user: {admin_user.username}")
        print(f"   Full name: {admin_user.get_full_name() or 'Not set'}")
        print(f"   Email: {admin_user.email}")
        
        # Test the avatar URL generation
        avatar_url = user_avatar_url(admin_user)
        print(f"   Avatar URL: {avatar_url}")
        
        # Test the professional avatar function directly
        professional_url = get_professional_avatar_url_for_user(admin_user)
        print(f"   Professional URL: {professional_url}")
        
        # Check if user has an employee record
        try:
            employee = admin_user.employee
            print(f"   Has employee record: Yes")
            print(f"   Employee name: {employee.name}")
        except:
            print(f"   Has employee record: No (will use username)")
        
        print()
        print("Expected result:")
        print("✓ Admin user 'kwameb320' should show 'KW' initials")
        print("✓ Dark blue circular background")
        print("✓ White text")
        print("✓ Professional appearance")
        
    except User.DoesNotExist:
        print("❌ Admin user 'kwameb320' not found")
        print("Creating a test user to demonstrate the functionality...")
        
        # Create a test user to demonstrate
        test_user = User.objects.create_user(
            username='kwameb320',
            email='kwameb320@example.com',
            first_name='Kwame',
            last_name='Boateng'
        )
        
        avatar_url = user_avatar_url(test_user)
        print(f"✅ Test user created")
        print(f"   Username: {test_user.username}")
        print(f"   Full name: {test_user.get_full_name()}")
        print(f"   Avatar URL: {avatar_url}")
        
        # Clean up test user
        test_user.delete()
        print("   Test user cleaned up")
    
    print()
    print("Template Usage:")
    print("In templates, use: {{ user|user_avatar_url }}")
    print("This will automatically generate professional avatars for admin users")

if __name__ == "__main__":
    test_admin_avatar()
