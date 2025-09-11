#!/usr/bin/env python3
"""
Test script for the new better avatar system
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
from assets.templatetags.employee_filters import employee_avatar_url, get_professional_avatar_url, is_generic_avatar

def test_better_avatars():
    """Test the new better avatar system"""
    print("Testing Better Avatar System...")
    print("=" * 50)
    
    # Test the helper functions
    print("1. Testing helper functions...")
    
    # Test is_generic_avatar function
    test_urls = [
        "https://randomuser.me/api/portraits/men/1.jpg",
        "https://ui-avatars.com/api/?name=John+Doe",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=john",
        "https://example.com/real-photo.jpg",
        None
    ]
    
    for url in test_urls:
        is_generic = is_generic_avatar(url)
        print(f"   {url or 'None'}: {'Generic' if is_generic else 'Real'}")
    
    # Test professional placeholder generation
    print("\n2. Testing professional placeholder generation...")
    test_names = ["John Smith", "Sarah Johnson", "Mike Davis", "Lisa Wilson"]
    
    for name in test_names:
        placeholder_url = get_professional_avatar_url(type('MockEmployee', (), {'name': name})())
        print(f"   {name}: {placeholder_url}")
    
    # Test with real employees
    print("\n3. Testing with real employees...")
    employees = Employee.objects.all()[:5]  # Test first 5 employees
    
    for employee in employees:
        avatar_url = employee_avatar_url(employee)
        is_generic = is_generic_avatar(employee.avatar_url) if employee.avatar_url else True
        
        print(f"   {employee.name}:")
        print(f"     Current avatar: {employee.avatar_url or 'None'}")
        print(f"     Is generic: {is_generic}")
        print(f"     New avatar URL: {avatar_url}")
        print()
    
    print("=" * 50)
    print("Better Avatar System Test Complete!")

if __name__ == "__main__":
    test_better_avatars()
