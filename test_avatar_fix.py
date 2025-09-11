#!/usr/bin/env python3
"""
Test script to verify the avatar fix is working
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.models import Employee
from assets.templatetags.employee_filters import employee_avatar_url

def test_avatar_fix():
    """Test that the avatar fix is working correctly"""
    print("Testing Avatar Fix")
    print("=" * 50)
    
    # Get all employees
    employees = Employee.objects.all()
    
    print(f"Testing {employees.count()} employees:")
    print()
    
    for employee in employees:
        # Get the avatar URL that would be used in templates
        avatar_url = employee_avatar_url(employee)
        
        # Check if it's a professional avatar
        is_professional = 'dicebear.com' in avatar_url
        is_azure = 'employee_photo' in avatar_url
        
        print(f"📋 {employee.name}")
        print(f"   Azure AD ID: {employee.avatar_url or 'None'}")
        print(f"   Stored avatar: {employee.avatar_url or 'None'}")
        print(f"   Template URL: {avatar_url}")
        
        if is_professional:
            print(f"   ✅ Using professional avatar")
        elif is_azure:
            print(f"   🔵 Using Azure AD photo")
        else:
            print(f"   ❓ Using other avatar")
        
        print()

if __name__ == "__main__":
    test_avatar_fix()
