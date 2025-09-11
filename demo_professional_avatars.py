#!/usr/bin/env python3
"""
Demo script to show the new professional avatar style
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.templatetags.employee_filters import get_professional_avatar_url

def demo_professional_avatars():
    """Demo the new professional avatar style"""
    print("Professional Avatar Demo")
    print("=" * 50)
    print("This shows the new professional avatar style that looks like verified user icons")
    print()
    
    # Sample employee names
    employees = [
        "John Smith",
        "Sarah Johnson", 
        "Mike Davis",
        "Lisa Wilson",
        "David Brown",
        "Emily Chen",
        "Robert Taylor",
        "Jennifer Garcia",
        "Kwame Boateng",
        "Maria Rodriguez"
    ]
    
    print("Professional Avatar URLs:")
    print("-" * 30)
    
    for name in employees:
        # Create a mock employee object
        mock_employee = type('MockEmployee', (), {'name': name})()
        
        # Get the professional avatar URL
        avatar_url = get_professional_avatar_url(mock_employee)
        
        print(f"{name:20} -> {avatar_url}")
    
    print()
    print("Features of the new professional avatars:")
    print("✓ Clean, circular design")
    print("✓ Dark blue background (#1e40af)")
    print("✓ White text for contrast")
    print("✓ Employee initials (first + last name)")
    print("✓ Professional font weight and size")
    print("✓ Consistent styling across all employees")
    print("✓ Matches the reference dark blue avatar style")
    
    print()
    print("To apply these avatars to your employees, run:")
    print("python manage.py cleanup_employee_avatars --force-all")

if __name__ == "__main__":
    demo_professional_avatars()
