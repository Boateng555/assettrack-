#!/usr/bin/env python3
"""
Script to find and fix broken avatar images
"""

import os
import sys
import django
import requests

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.models import Employee
from assets.templatetags.employee_filters import employee_avatar_url, get_professional_avatar_url, is_generic_avatar

def check_avatar_url(url):
    """Check if an avatar URL is working"""
    if not url:
        return False, "No URL"
    
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return True, "Working"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def fix_broken_avatars():
    """Find and fix broken avatar images"""
    print("Checking for broken avatar images...")
    print("=" * 50)
    
    employees = Employee.objects.all()
    broken_count = 0
    fixed_count = 0
    
    for employee in employees:
        print(f"\n📋 Checking {employee.name}:")
        
        # Check current avatar URL
        current_avatar = employee.avatar_url
        if current_avatar:
            print(f"   Current avatar: {current_avatar}")
            is_working, status = check_avatar_url(current_avatar)
            print(f"   Status: {status}")
            
            if not is_working or is_generic_avatar(current_avatar):
                print(f"   ❌ Broken or generic avatar detected")
                broken_count += 1
                
                # Get the correct professional avatar URL
                correct_avatar = get_professional_avatar_url(employee)
                print(f"   🔧 Will fix to: {correct_avatar}")
                
                # Update the employee
                employee.avatar_url = correct_avatar
                employee.save()
                fixed_count += 1
                print(f"   ✅ Fixed!")
            else:
                print(f"   ✅ Avatar is working")
        else:
            print(f"   ❌ No avatar URL set")
            broken_count += 1
            
            # Set the correct professional avatar URL
            correct_avatar = get_professional_avatar_url(employee)
            print(f"   🔧 Setting to: {correct_avatar}")
            
            # Update the employee
            employee.avatar_url = correct_avatar
            employee.save()
            fixed_count += 1
            print(f"   ✅ Fixed!")
    
    print("\n" + "=" * 50)
    print(f"Summary:")
    print(f"Total employees checked: {employees.count()}")
    print(f"Broken/generic avatars found: {broken_count}")
    print(f"Avatars fixed: {fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} broken avatars!")
        print("All employees now have working professional avatars.")
    else:
        print(f"\n✅ No broken avatars found. All avatars are working!")

def show_avatar_status():
    """Show the current status of all avatars"""
    print("Current Avatar Status")
    print("=" * 50)
    
    employees = Employee.objects.all()
    
    for employee in employees:
        avatar_url = employee_avatar_url(employee)
        is_generic = is_generic_avatar(employee.avatar_url) if employee.avatar_url else True
        
        status = "✅ Professional" if not is_generic else "❌ Generic/Broken"
        
        print(f"{employee.name:20} -> {status}")
        print(f"   URL: {avatar_url}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_avatar_status()
    else:
        fix_broken_avatars()
