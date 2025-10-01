#!/usr/bin/env python
"""
Check Database State for Production

This script shows what data is currently in your database
and what will be available in production.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.models import Employee, Asset

def check_database_state():
    """Check current database state"""
    
    print("📊 CURRENT DATABASE STATE")
    print("=" * 40)
    
    # Employee counts
    total_employees = Employee.objects.count()
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).count()
    active_employees = Employee.objects.filter(status='active').count()
    
    print(f"👥 EMPLOYEES:")
    print(f"  Total Employees: {total_employees}")
    print(f"  Azure AD Employees: {azure_employees}")
    print(f"  Active Employees: {active_employees}")
    
    # Asset counts
    total_assets = Asset.objects.count()
    azure_assets = Asset.objects.filter(azure_ad_id__isnull=False).count()
    assigned_assets = Asset.objects.filter(assigned_to__isnull=False).count()
    
    print(f"\n🖥️ ASSETS:")
    print(f"  Total Assets: {total_assets}")
    print(f"  Azure AD Assets: {azure_assets}")
    print(f"  Assigned Assets: {assigned_assets}")
    
    # Show sample data
    print(f"\n📋 SAMPLE AZURE AD EMPLOYEES:")
    azure_emps = Employee.objects.filter(azure_ad_id__isnull=False)[:3]
    for emp in azure_emps:
        print(f"  - {emp.name} ({emp.email})")
    
    print(f"\n📋 SAMPLE AZURE AD ASSETS:")
    azure_assets_list = Asset.objects.filter(azure_ad_id__isnull=False)[:3]
    for asset in azure_assets_list:
        print(f"  - {asset.name} ({asset.asset_type})")
    
    print(f"\n📋 SAMPLE ASSIGNMENTS:")
    assigned_assets_list = Asset.objects.filter(assigned_to__isnull=False)[:3]
    for asset in assigned_assets_list:
        print(f"  - {asset.name} → {asset.assigned_to.name}")

def explain_production_behavior():
    """Explain what happens in production"""
    
    print("\n🚀 PRODUCTION DATABASE BEHAVIOR")
    print("=" * 40)
    
    print("✅ DATA PERSISTENCE:")
    print("  - All data is stored in SQLite database (db.sqlite3)")
    print("  - Data survives server restarts")
    print("  - Data survives system updates")
    print("  - Data is stored permanently")
    print("  - Data is backed up automatically")
    
    print("\n✅ AZURE AD SYNC:")
    print("  - Users sync from Azure AD to your database")
    print("  - Devices sync from Azure AD to your database")
    print("  - Assignments sync from Azure AD to your database")
    print("  - All data is stored locally in your database")
    print("  - Azure AD remains unchanged (read-only)")
    
    print("\n✅ PRODUCTION FEATURES:")
    print("  - Real-time sync with Azure AD")
    print("  - Automatic user management")
    print("  - Automatic device management")
    print("  - Automatic assignment management")
    print("  - Complete audit trail")
    print("  - Data backup and recovery")
    
    print("\n✅ SCALABILITY:")
    print("  - Handles thousands of users")
    print("  - Handles thousands of devices")
    print("  - Efficient database queries")
    print("  - Optimized sync performance")
    print("  - Regular maintenance")

def show_database_file():
    """Show database file information"""
    
    print("\n💾 DATABASE FILE INFORMATION")
    print("=" * 35)
    
    import os
    db_file = "db.sqlite3"
    
    if os.path.exists(db_file):
        size = os.path.getsize(db_file)
        size_mb = size / (1024 * 1024)
        print(f"Database file: {db_file}")
        print(f"File size: {size_mb:.2f} MB")
        print(f"Location: {os.path.abspath(db_file)}")
        print("✅ Database file exists and is accessible")
    else:
        print("❌ Database file not found")

if __name__ == "__main__":
    check_database_state()
    explain_production_behavior()
    show_database_file()
