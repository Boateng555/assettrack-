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

def test_new_user_sync():
    print("🧪 Testing New User Sync")
    print("=" * 40)
    
    # Show current state
    print("📊 Current State:")
    total_employees = Employee.objects.count()
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='').count()
    
    print(f"   Total employees: {total_employees}")
    print(f"   Azure AD employees: {azure_employees}")
    
    # Show all Azure AD employees
    print(f"\n👥 Current Azure AD Employees:")
    azure_emps = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='')
    for emp in azure_emps:
        if not emp.azure_ad_id.startswith('azure-user-'):  # Skip test data
            print(f"   - {emp.name} ({emp.email})")
    
    # Get users from Azure AD
    print(f"\n🔍 Checking Azure AD for new users...")
    azure = AzureADIntegration()
    users = azure.get_users()
    
    print(f"   Found {len(users)} users in Azure AD")
    
    # Show Azure AD users that aren't in our database
    print(f"\n🆕 Users in Azure AD but not in database:")
    azure_ids_in_db = set(emp.azure_ad_id for emp in azure_emps if not emp.azure_ad_id.startswith('azure-user-'))
    
    new_users_found = 0
    for user in users:
        azure_id = user.get('id')
        if azure_id and azure_id not in azure_ids_in_db:
            new_users_found += 1
            print(f"   - {user.get('displayName', 'Unknown')} ({user.get('userPrincipalName', 'No UPN')})")
            print(f"     Azure ID: {azure_id}")
    
    if new_users_found == 0:
        print("   No new users found")
    
    # Run sync
    print(f"\n🔄 Running sync...")
    new_count, updated_count = azure.sync_employees()
    
    print(f"\n✅ Sync Results:")
    print(f"   New employees: {new_count}")
    print(f"   Updated employees: {updated_count}")
    
    # Show final state
    print(f"\n📊 Final State:")
    total_employees_after = Employee.objects.count()
    azure_employees_after = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='').count()
    
    print(f"   Total employees: {total_employees_after}")
    print(f"   Azure AD employees: {azure_employees_after}")
    
    if new_count > 0:
        print(f"\n🎉 New employees added:")
        new_emps = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='')
        for emp in new_emps:
            if not emp.azure_ad_id.startswith('azure-user-'):
                print(f"   - {emp.name} ({emp.email})")
                print(f"     Department: {emp.department}")
                print(f"     Azure ID: {emp.azure_ad_id}")

if __name__ == "__main__":
    test_new_user_sync()
