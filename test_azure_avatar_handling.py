#!/usr/bin/env python3
"""
Test script to show how Azure AD employees get professional avatars when they don't have photos
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
from assets.templatetags.employee_filters import employee_avatar_url, get_professional_avatar_url, is_generic_avatar

def test_azure_avatar_handling():
    """Test how Azure AD employees get professional avatars"""
    print("Azure AD Avatar Handling Test")
    print("=" * 50)
    print("This shows how employees with Azure AD IDs get professional avatars when they don't have photos")
    print()
    
    azure_ad = AzureADIntegration()
    has_azure_config = azure_ad.get_access_token() is not None
    
    if not has_azure_config:
        print("⚠️  Azure AD not configured - will show placeholder behavior only")
        print()
    
    # Get employees with Azure AD IDs
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False)
    
    if not azure_employees.exists():
        print("No employees with Azure AD IDs found.")
        print("Creating sample scenarios...")
        
        # Create sample scenarios
        sample_employees = [
            {"name": "John Smith", "azure_ad_id": "12345", "has_photo": True},
            {"name": "Sarah Johnson", "azure_ad_id": "67890", "has_photo": False},
            {"name": "Mike Davis", "azure_ad_id": "11111", "has_photo": False},
            {"name": "Lisa Wilson", "azure_ad_id": "22222", "has_photo": True},
        ]
        
        for sample in sample_employees:
            print(f"\n📋 {sample['name']} (Azure ID: {sample['azure_ad_id']})")
            
            if sample['has_photo']:
                print(f"   ✅ Has Azure AD photo")
                print(f"   🖼️  Avatar: Azure AD photo URL")
            else:
                print(f"   ❌ No Azure AD photo")
                print(f"   🖼️  Avatar: Professional placeholder")
                
                # Show what the professional avatar would look like
                mock_employee = type('MockEmployee', (), {'name': sample['name']})()
                professional_url = get_professional_avatar_url(mock_employee)
                print(f"   🔗 URL: {professional_url}")
    else:
        print(f"Found {azure_employees.count()} employees with Azure AD IDs:")
        print()
        
        for employee in azure_employees[:5]:  # Show first 5
            print(f"📋 {employee.name} (Azure ID: {employee.azure_ad_id})")
            
            if has_azure_config:
                # Check if they have an Azure AD photo
                photo_url = azure_ad.get_user_photo_url(employee.azure_ad_id)
                
                if photo_url:
                    print(f"   ✅ Has Azure AD photo")
                    print(f"   🖼️  Avatar: Azure AD photo")
                else:
                    print(f"   ❌ No Azure AD photo")
                    print(f"   🖼️  Avatar: Professional placeholder")
                    
                    # Show what the professional avatar would look like
                    professional_url = get_professional_avatar_url(employee)
                    print(f"   🔗 URL: {professional_url}")
            else:
                print(f"   ⚠️  Azure AD not configured - can't check for photos")
                print(f"   🖼️  Current avatar: {employee.avatar_url or 'None'}")
                
                # Show what they would get
                avatar_url = employee_avatar_url(employee)
                print(f"   🖼️  Would get: {avatar_url}")
            
            print()
    
    print("=" * 50)
    print("Summary:")
    print("✓ Employees WITH Azure AD photos → Show real photos")
    print("✓ Employees WITHOUT Azure AD photos → Get professional placeholders")
    print("✓ Professional placeholders are consistent and look good")
    print()
    print("To apply this to all employees, run:")
    print("python manage.py force_professional_avatars --azure-only")

if __name__ == "__main__":
    test_azure_avatar_handling()
