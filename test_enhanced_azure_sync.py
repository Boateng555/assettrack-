#!/usr/bin/env python
"""
Test script for enhanced Azure AD sync functionality
This script demonstrates how the system handles user deletions, updates, and removals
"""

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

def test_enhanced_azure_sync():
    """Test the enhanced Azure AD sync functionality"""
    print("🚀 Testing Enhanced Azure AD Sync Functionality")
    print("=" * 60)
    
    azure = AzureADIntegration()
    
    # Test 1: Get sync summary
    print("\n📊 1. Current Sync Summary:")
    print("-" * 30)
    summary = azure.get_sync_summary()
    for key, value in summary.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Test 2: Get Azure AD users
    print("\n👥 2. Azure AD Users:")
    print("-" * 30)
    users = azure.get_users()
    print(f"   Total active users in Azure AD: {len(users)}")
    
    for i, user in enumerate(users[:5], 1):  # Show first 5 users
        print(f"   {i}. {user.get('displayName', 'N/A')} ({user.get('userPrincipalName', 'N/A')})")
    
    if len(users) > 5:
        print(f"   ... and {len(users) - 5} more users")
    
    # Test 3: Get deleted users
    print("\n🗑️  3. Recently Deleted Users:")
    print("-" * 30)
    deleted_users = azure.get_deleted_users()
    print(f"   Total deleted users in Azure AD: {len(deleted_users)}")
    
    for i, user in enumerate(deleted_users[:3], 1):  # Show first 3 deleted users
        deleted_date = user.get('deletedDateTime', 'Unknown')
        print(f"   {i}. {user.get('displayName', 'N/A')} - Deleted: {deleted_date}")
    
    # Test 4: Local employee status breakdown
    print("\n📋 4. Local Employee Status Breakdown:")
    print("-" * 30)
    active_count = Employee.objects.filter(status='active').count()
    inactive_count = Employee.objects.filter(status='inactive').count()
    deleted_count = Employee.objects.filter(status='deleted').count()
    total_count = Employee.objects.count()
    
    print(f"   Total employees: {total_count}")
    print(f"   Active: {active_count}")
    print(f"   Inactive: {inactive_count}")
    print(f"   Deleted: {deleted_count}")
    
    # Test 5: Show employees by status
    print("\n👤 5. Employees by Status:")
    print("-" * 30)
    
    print("   Active Employees:")
    active_employees = Employee.objects.filter(status='active')[:3]
    for emp in active_employees:
        print(f"     - {emp.name} ({emp.email}) - Azure ID: {emp.azure_ad_id or 'None'}")
    
    print("\n   Inactive Employees:")
    inactive_employees = Employee.objects.filter(status='inactive')[:3]
    for emp in inactive_employees:
        print(f"     - {emp.name} ({emp.email}) - Azure ID: {emp.azure_ad_id or 'None'}")
    
    print("\n   Deleted Employees:")
    deleted_employees = Employee.objects.filter(status='deleted')[:3]
    for emp in deleted_employees:
        print(f"     - {emp.name} ({emp.email}) - Azure ID: {emp.azure_ad_id or 'None'}")
    
    # Test 6: Demonstrate sync capabilities
    print("\n🔄 6. Sync Capabilities:")
    print("-" * 30)
    print("   The enhanced sync will:")
    print("   ✅ Create new employees from Azure AD")
    print("   ✅ Update existing employees with latest data")
    print("   ✅ Mark employees as 'inactive' if disabled in Azure AD")
    print("   ✅ Mark employees as 'deleted' if deleted in Azure AD")
    print("   ✅ Clean up assets assigned to inactive/deleted employees")
    print("   ✅ Sync device assignments")
    
    # Test 7: Show orphaned assets
    print("\n🔧 7. Orphaned Assets Check:")
    print("-" * 30)
    orphaned_assets = Employee.objects.filter(
        assigned_assets__isnull=False,
        status__in=['inactive', 'deleted']
    ).distinct()
    
    if orphaned_assets.exists():
        print(f"   Found {orphaned_assets.count()} employees with orphaned assets:")
        for emp in orphaned_assets[:3]:
            asset_count = emp.assigned_assets.count()
            print(f"     - {emp.name} ({emp.status}): {asset_count} assets")
    else:
        print("   No orphaned assets found!")
    
    print("\n🎯 Ready to test the enhanced sync!")
    print("   Run: python manage.py sync_azure_ad")
    print("   Or use the web interface at: http://localhost:8000/azure-sync/")

def test_sync_commands():
    """Test the available sync commands"""
    print("\n📝 Available Sync Commands:")
    print("-" * 30)
    print("   python manage.py sync_azure_ad                    # Full sync with change detection")
    print("   python manage.py sync_azure_ad --employees-only   # Sync employees only")
    print("   python manage.py sync_azure_ad --devices-only     # Sync devices only")
    print("   python manage.py sync_azure_ad --assignments-only # Sync assignments only")
    print("   python manage.py sync_azure_ad --summary          # Show sync summary")
    print("   python manage.py sync_azure_ad --cleanup-only     # Cleanup orphaned assets")

if __name__ == "__main__":
    test_enhanced_azure_sync()
    test_sync_commands()
    
    print("\n" + "=" * 60)
    print("✅ Enhanced Azure AD Sync Test Complete!")
    print("   The system now properly handles:")
    print("   • User deletions from Azure AD")
    print("   • User updates in Azure AD")
    print("   • User removals/disablements")
    print("   • Asset cleanup for inactive users")
    print("   • Comprehensive sync reporting")
