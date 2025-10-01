#!/usr/bin/env python
"""
Show Azure AD Users with Their Devices

This script demonstrates how Azure AD users sync with their complete information
including names, emails, phone numbers, and their devices.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.models import Employee, Asset

def show_azure_users_with_devices():
    """Show Azure AD users with their complete information and devices"""
    
    print("🔗 Azure AD Users with Their Devices")
    print("=" * 50)
    
    # Get Azure AD employees
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False)
    
    print(f"Found {azure_employees.count()} Azure AD employees:")
    print()
    
    for emp in azure_employees:
        print(f"👤 {emp.name}")
        print(f"   📧 Email: {emp.email}")
        print(f"   🏢 Department: {emp.department}")
        print(f"   💼 Job Title: {emp.job_title or 'Not specified'}")
        print(f"   📱 Phone: {emp.phone or 'Not specified'}")
        print(f"   🔗 Azure ID: {emp.azure_ad_id}")
        print(f"   📅 Last Sync: {emp.last_azure_sync}")
        
        # Get their devices
        devices = Asset.objects.filter(assigned_to=emp, azure_ad_id__isnull=False)
        print(f"   🖥️  Devices ({devices.count()}):")
        
        if devices.exists():
            for device in devices:
                print(f"      - {device.name} ({device.asset_type}) - {device.operating_system}")
        else:
            print("      - No Azure AD devices assigned")
        
        print()

def show_user_information_fields():
    """Show what information comes from Azure AD"""
    
    print("📋 Information That Syncs from Azure AD")
    print("=" * 40)
    
    print("✅ User Information:")
    print("   - Full Name (displayName)")
    print("   - Email Address (mail)")
    print("   - Department (department)")
    print("   - Job Title (jobTitle)")
    print("   - Employee ID (employeeId)")
    print("   - Phone Number (mobilePhone)")
    print("   - Profile Photo (photo)")
    print("   - Azure AD User ID")
    print("   - Azure AD Username")
    
    print("\n✅ Device Information:")
    print("   - Device Name")
    print("   - Device Type (laptop/phone/tablet)")
    print("   - Operating System")
    print("   - OS Version")
    print("   - Manufacturer")
    print("   - Model")
    print("   - Serial Number")
    print("   - Device Assignment")
    
    print("\n✅ Automatic Features:")
    print("   - Devices automatically assigned to users")
    print("   - Asset types automatically determined")
    print("   - Status automatically set to 'assigned'")
    print("   - Sync timestamps tracked")
    print("   - Photo URLs from Azure AD")

def show_device_assignment_example():
    """Show example of how devices get assigned"""
    
    print("\n🔄 How Device Assignment Works")
    print("=" * 35)
    
    print("1. User syncs from Azure AD with their information")
    print("2. System fetches all devices registered to that user")
    print("3. Each device becomes an asset in AssetTrack")
    print("4. Device is automatically assigned to the user")
    print("5. Asset status is set to 'assigned'")
    print("6. All device information is preserved")
    
    print("\nExample Flow:")
    print("Azure AD User: John Doe")
    print("├── Email: john.doe@company.com")
    print("├── Department: IT")
    print("├── Job Title: Software Engineer")
    print("└── Devices:")
    print("    ├── John's Laptop (Windows) → AssetTrack Asset")
    print("    ├── John's iPhone (iOS) → AssetTrack Asset")
    print("    └── John's iPad (iOS) → AssetTrack Asset")

if __name__ == "__main__":
    show_azure_users_with_devices()
    show_user_information_fields()
    show_device_assignment_example()
