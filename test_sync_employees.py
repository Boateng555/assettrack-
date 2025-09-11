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

def test_sync_employees():
    print("🔄 Testing Employee Sync")
    print("=" * 40)
    
    # Count employees before sync
    employees_before = Employee.objects.count()
    azure_employees_before = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='').count()
    
    print(f"📊 Before sync:")
    print(f"   Total employees: {employees_before}")
    print(f"   Azure AD employees: {azure_employees_before}")
    
    # Run the sync
    print("\n🔄 Running Azure AD sync...")
    azure = AzureADIntegration()
    new_count, updated_count = azure.sync_employees()
    
    print(f"\n✅ Sync completed:")
    print(f"   New employees: {new_count}")
    print(f"   Updated employees: {updated_count}")
    
    # Count employees after sync
    employees_after = Employee.objects.count()
    azure_employees_after = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='').count()
    
    print(f"\n📊 After sync:")
    print(f"   Total employees: {employees_after}")
    print(f"   Azure AD employees: {azure_employees_after}")
    
    # Show new Azure AD employees
    print(f"\n👥 New Azure AD employees:")
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).exclude(azure_ad_id='')
    
    for emp in azure_employees:
        if not emp.azure_ad_id.startswith('azure-user-'):  # Skip test data
            print(f"   - {emp.name} ({emp.email})")
            print(f"     Azure ID: {emp.azure_ad_id}")
            print(f"     UPN: {emp.azure_ad_username}")
            print(f"     Department: {emp.department or 'N/A'}")
            print(f"     Job Title: {emp.job_title or 'N/A'}")
            print()

if __name__ == "__main__":
    test_sync_employees()
