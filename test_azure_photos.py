#!/usr/bin/env python3
"""
Test script for Azure AD photo integration
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
from assets.azure_ad_integration import AzureADIntegration

def test_azure_photo_integration():
    """Test the Azure AD photo integration"""
    print("Testing Azure AD Photo Integration...")
    print("=" * 50)
    
    # Initialize Azure AD integration
    azure_ad = AzureADIntegration()
    
    # Test getting access token
    print("1. Testing access token...")
    token = azure_ad.get_access_token()
    if token:
        print("   ✓ Access token obtained successfully")
    else:
        print("   ✗ Failed to get access token")
        return
    
    # Test getting users
    print("\n2. Testing user retrieval...")
    users = azure_ad.get_users()
    print(f"   Found {len(users)} users in Azure AD")
    
    if not users:
        print("   ✗ No users found in Azure AD")
        return
    
    # Test getting photo URL for first user
    print("\n3. Testing photo URL retrieval...")
    first_user = users[0]
    user_id = first_user.get('id')
    user_name = first_user.get('displayName', 'Unknown')
    
    print(f"   Testing for user: {user_name} (ID: {user_id})")
    
    photo_url = azure_ad.get_user_photo_url(user_id)
    if photo_url:
        print(f"   ✓ Photo URL found: {photo_url}")
    else:
        print("   ✗ No photo found for this user")
    
    # Test getting photo data
    print("\n4. Testing photo data retrieval...")
    photo_data = azure_ad.get_user_photo_data(user_id)
    if photo_data:
        print(f"   ✓ Photo data retrieved successfully ({len(photo_data)} bytes)")
    else:
        print("   ✗ Failed to retrieve photo data")
    
    # Test local employees with Azure AD integration
    print("\n5. Testing local employee sync...")
    employees_with_azure = Employee.objects.filter(azure_ad_id__isnull=False)
    print(f"   Found {employees_with_azure.count()} local employees with Azure AD IDs")
    
    for employee in employees_with_azure[:3]:  # Test first 3
        print(f"   - {employee.name}: Azure ID = {employee.azure_ad_id}")
        if employee.avatar_url:
            print(f"     Avatar URL: {employee.avatar_url}")
        else:
            print(f"     No avatar URL set")
    
    print("\n" + "=" * 50)
    print("Azure AD Photo Integration Test Complete!")

if __name__ == "__main__":
    test_azure_photo_integration()
