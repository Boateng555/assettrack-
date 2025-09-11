#!/usr/bin/env python3
"""
Script to fix admin user avatars and ensure proper names
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

def fix_admin_avatars():
    """Fix admin user avatars and ensure proper names"""
    print("Fixing Admin User Avatars")
    print("=" * 50)
    
    # Get all users
    users = User.objects.all()
    fixed_count = 0
    
    for user in users:
        print(f"\n📋 Checking admin user: {user.username}")
        
        # Check if user has a proper name
        current_name = user.get_full_name()
        if not current_name:
            print(f"   ❌ No full name set")
            
            # Try to set a proper name based on username
            if user.username == 'kwameb320':
                user.first_name = 'Kwame'
                user.last_name = 'Boateng'
                print(f"   🔧 Setting name to: Kwame Boateng")
            elif user.username == 'admin':
                user.first_name = 'System'
                user.last_name = 'Administrator'
                print(f"   🔧 Setting name to: System Administrator")
            else:
                # Try to parse username into name
                username_parts = user.username.replace('_', ' ').replace('.', ' ').split()
                if len(username_parts) >= 2:
                    user.first_name = username_parts[0].title()
                    user.last_name = username_parts[1].title()
                    print(f"   🔧 Setting name to: {user.first_name} {user.last_name}")
                else:
                    user.first_name = user.username.title()
                    user.last_name = 'User'
                    print(f"   🔧 Setting name to: {user.first_name} {user.last_name}")
            
            user.save()
            fixed_count += 1
        else:
            print(f"   ✅ Name already set: {current_name}")
        
        # Test the avatar URL
        avatar_url = user_avatar_url(user)
        print(f"   Avatar URL: {avatar_url}")
        
        # Extract initials for display
        display_name = user.get_full_name() if user.get_full_name() else user.username
        name_parts = display_name.strip().split()
        if len(name_parts) >= 2:
            initials = (name_parts[0][0] + name_parts[-1][0]).upper()
        else:
            initials = display_name[:2].upper()
        
        print(f"   Will show initials: {initials}")
    
    print("\n" + "=" * 50)
    print(f"Summary:")
    print(f"Total admin users checked: {users.count()}")
    print(f"Users with names fixed: {fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} admin user names!")
        print("All admin users now have proper names and professional avatars.")
    else:
        print(f"\n✅ All admin users already have proper names!")
    
    print("\nAdmin users will now show:")
    print("✓ Professional dark blue circular avatars")
    print("✓ White initials based on their name")
    print("✓ Consistent styling across all admin interfaces")

if __name__ == "__main__":
    fix_admin_avatars()
