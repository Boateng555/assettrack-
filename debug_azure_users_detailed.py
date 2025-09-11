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

def debug_azure_users():
    print("🔍 Detailed Azure AD User Debug")
    print("=" * 50)
    
    # Initialize Azure AD integration
    azure = AzureADIntegration()
    
    # Get access token
    print("🔑 Getting access token...")
    token = azure.get_access_token()
    if not token:
        print("❌ Failed to get access token")
        return
    
    print("✅ Access token obtained")
    
    # Get users
    print("\n👥 Getting users from Azure AD...")
    users = azure.get_users()
    
    if not users:
        print("❌ No users found in Azure AD")
        return
    
    print(f"✅ Found {len(users)} users in Azure AD")
    
    # Analyze each user
    print("\n📊 User Analysis:")
    print("-" * 80)
    
    for i, user in enumerate(users, 1):
        print(f"\n👤 User {i}:")
        print(f"   ID: {user.get('id', 'N/A')}")
        print(f"   Display Name: {user.get('displayName', 'N/A')}")
        print(f"   Email: {user.get('mail', 'N/A')}")
        print(f"   UPN: {user.get('userPrincipalName', 'N/A')}")
        print(f"   Department: {user.get('department', 'N/A')}")
        print(f"   Job Title: {user.get('jobTitle', 'N/A')}")
        print(f"   Employee ID: {user.get('employeeId', 'N/A')}")
        print(f"   Account Enabled: {user.get('accountEnabled', 'N/A')}")
        
        # Check if this user would be synced
        email = user.get('mail', '')
        azure_id = user.get('id', '')
        
        if not email:
            print("   ❌ No email - will not be synced")
        elif not azure_id:
            print("   ❌ No Azure ID - will not be synced")
        else:
            print("   ✅ Has required fields - will be synced")
            
            # Check if already exists
            existing = Employee.objects.filter(azure_ad_id=azure_id).first()
            if existing:
                print(f"   📝 Already exists in database: {existing.name} ({existing.email})")
            else:
                print("   ➕ Will be created as new employee")
    
    # Check current employees
    print(f"\n📋 Current Employees in Database:")
    print("-" * 40)
    employees = Employee.objects.all()
    print(f"Total employees: {employees.count()}")
    
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='')
    print(f"Azure AD employees: {azure_employees.count()}")
    
    if azure_employees.exists():
        print("Azure AD employees:")
        for emp in azure_employees:
            print(f"  - {emp.name} ({emp.email}) - Azure ID: {emp.azure_ad_id}")

if __name__ == "__main__":
    debug_azure_users()
