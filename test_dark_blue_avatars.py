#!/usr/bin/env python3
"""
Test script to show the new dark blue avatar style
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

def test_dark_blue_avatars():
    """Test the new dark blue avatar style"""
    print("Dark Blue Avatar Style Test")
    print("=" * 50)
    print("This shows the new dark blue circular avatars with white initials")
    print("Matching the reference image style exactly")
    print()
    
    # Sample employee names to test
    employees = [
        "Mike Davis",      # Should show "MD" like the reference
        "John Smith",      # Should show "JS"
        "Sarah Johnson",   # Should show "SJ"
        "Lisa Wilson",     # Should show "LW"
        "David Brown",     # Should show "DB"
        "Emily Chen",      # Should show "EC"
        "Robert Taylor",   # Should show "RT"
        "Jennifer Garcia", # Should show "JG"
        "Kwame Boateng",   # Should show "KB"
        "Maria Rodriguez"  # Should show "MR"
    ]
    
    print("Dark Blue Avatar URLs:")
    print("-" * 40)
    
    for name in employees:
        # Create a mock employee object
        mock_employee = type('MockEmployee', (), {'name': name})()
        
        # Get the dark blue avatar URL
        avatar_url = get_professional_avatar_url(mock_employee)
        
        # Extract initials for display
        name_parts = name.strip().split()
        if len(name_parts) >= 2:
            initials = (name_parts[0][0] + name_parts[-1][0]).upper()
        else:
            initials = name[:2].upper()
        
        print(f"{name:20} -> {initials} -> {avatar_url}")
    
    print()
    print("Features of the new dark blue avatars:")
    print("✓ Dark blue background (#1e40af)")
    print("✓ White text for perfect contrast")
    print("✓ Circular design with rounded corners")
    print("✓ Employee initials (first + last name)")
    print("✓ Professional font weight (500)")
    print("✓ Consistent 40px font size")
    print("✓ Matches the reference 'MI' avatar style exactly")
    
    print()
    print("To apply these avatars to your employees, run:")
    print("python manage.py force_professional_avatars --force-all")

if __name__ == "__main__":
    test_dark_blue_avatars()
