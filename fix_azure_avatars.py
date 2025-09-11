#!/usr/bin/env python3
"""
Script to fix Azure AD employees who have no photos
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
from assets.templatetags.employee_filters import get_professional_avatar_url
from assets.azure_ad_integration import AzureADIntegration

def check_azure_photo_exists(employee):
    """Check if an Azure AD employee has a photo"""
    if not employee.azure_ad_id:
        return False
    
    try:
        azure_ad = AzureADIntegration()
        photo_url = azure_ad.get_user_photo_url(employee.azure_ad_id)
        return photo_url is not None
    except Exception as e:
        print(f"   Error checking photo for {employee.name}: {e}")
        return False

def fix_azure_avatars():
    """Fix Azure AD employees who have no photos"""
    print("Fixing Azure AD Employees with No Photos")
    print("=" * 50)
    
    # Get all employees with Azure AD IDs
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='')
    fixed_count = 0
    
    print(f"Found {azure_employees.count()} employees with Azure AD IDs")
    print()
    
    for employee in azure_employees:
        print(f"📋 Checking {employee.name} (Azure AD ID: {employee.azure_ad_id})")
        
        # Check if they have a photo in Azure AD
        has_photo = check_azure_photo_exists(employee)
        
        if has_photo:
            print(f"   ✅ Has Azure AD photo - keeping as is")
        else:
            print(f"   ❌ No Azure AD photo found")
            
            # Check current avatar
            current_avatar = employee.avatar_url
            if current_avatar and 'dicebear.com' in current_avatar:
                print(f"   ✅ Already has professional avatar: {current_avatar}")
            else:
                print(f"   🔧 Setting professional avatar")
                
                # Set the professional avatar URL
                professional_avatar = get_professional_avatar_url(employee)
                employee.avatar_url = professional_avatar
                employee.save()
                fixed_count += 1
                print(f"   ✅ Set to: {professional_avatar}")
        
        print()
    
    print("=" * 50)
    print(f"Summary:")
    print(f"Total Azure AD employees checked: {azure_employees.count()}")
    print(f"Employees fixed with professional avatars: {fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} Azure AD employees!")
        print("They will now show professional avatars instead of broken images.")
    else:
        print(f"\n✅ All Azure AD employees already have proper avatars!")

def show_azure_avatar_status():
    """Show the current status of Azure AD employee avatars"""
    print("Azure AD Employee Avatar Status")
    print("=" * 50)
    
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='')
    
    for employee in azure_employees:
        has_photo = check_azure_photo_exists(employee)
        current_avatar = employee.avatar_url
        
        if has_photo:
            status = "✅ Has Azure AD photo"
        elif current_avatar and 'dicebear.com' in current_avatar:
            status = "✅ Has professional avatar"
        else:
            status = "❌ Needs professional avatar"
        
        print(f"{employee.name:20} -> {status}")
        if not has_photo and current_avatar and 'dicebear.com' in current_avatar:
            print(f"   Professional avatar: {current_avatar}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_azure_avatar_status()
    else:
        fix_azure_avatars()
