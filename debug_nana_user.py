#!/usr/bin/env python
import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration
from assets.models import Employee

def debug_nana_user():
    print("🔍 Debugging Nana User Sync")
    print("=" * 40)
    
    # Get the nana user from Azure AD
    azure = AzureADIntegration()
    users = azure.get_users()
    
    nana_user = None
    for user in users:
        if user.get('displayName', '').lower() == 'nana':
            nana_user = user
            break
    
    if not nana_user:
        print("❌ Nana user not found in Azure AD")
        return
    
    print(f"✅ Found nana user in Azure AD:")
    print(f"   ID: {nana_user.get('id')}")
    print(f"   Display Name: {nana_user.get('displayName')}")
    print(f"   Email: {nana_user.get('mail', 'None')}")
    print(f"   UPN: {nana_user.get('userPrincipalName')}")
    
    # Check if this user already exists in our database
    azure_id = nana_user.get('id')
    upn = nana_user.get('userPrincipalName', '')
    
    existing_by_azure_id = Employee.objects.filter(azure_ad_id=azure_id).first()
    existing_by_email = Employee.objects.filter(email=upn).first()
    
    print(f"\n📋 Database Check:")
    print(f"   Existing by Azure ID: {existing_by_azure_id}")
    print(f"   Existing by email: {existing_by_email}")
    
    if existing_by_azure_id:
        print(f"   ✅ User already exists with Azure ID")
    elif existing_by_email:
        print(f"   ⚠️  User exists with same email: {existing_by_email.name}")
    else:
        print(f"   ➕ User will be created as new")
        
        # Try to create the user manually to see the exact error
        try:
            email = nana_user.get('mail', '')
            if not email:
                email = nana_user.get('userPrincipalName', '')
            
            department = nana_user.get('department', '')
            if not department:
                department = 'IT'
            
            employee_data = {
                'name': nana_user.get('displayName', ''),
                'email': email,
                'department': department,
                'azure_ad_id': nana_user.get('id'),
                'azure_ad_username': nana_user.get('userPrincipalName', ''),
                'job_title': nana_user.get('jobTitle', ''),
                'employee_id': nana_user.get('employeeId', ''),
            }
            
            print(f"\n🔄 Attempting to create employee:")
            print(f"   Name: {employee_data['name']}")
            print(f"   Email: {employee_data['email']}")
            print(f"   Department: {employee_data['department']}")
            print(f"   Azure ID: {employee_data['azure_ad_id']}")
            
            new_employee = Employee.objects.create(**employee_data)
            print(f"   ✅ Successfully created: {new_employee}")
            
        except Exception as e:
            print(f"   ❌ Error creating employee: {e}")
            print(f"   Error type: {type(e).__name__}")

if __name__ == "__main__":
    debug_nana_user()
