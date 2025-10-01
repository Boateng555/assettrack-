#!/usr/bin/env python
"""
Fake Device Generator for AssetTrack Testing

This script creates fake devices and assigns them to users for testing purposes.
Perfect when you don't have real devices to work with.

Run this script to populate your system with sample devices.
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.models import Employee, Asset

def create_fake_devices():
    """Create fake devices for testing purposes"""
    
    print("🖥️  Creating Fake Devices for Testing")
    print("=" * 50)
    
    # Get existing employees
    employees = Employee.objects.filter(status='active')[:10]  # Limit to 10 employees
    
    if not employees:
        print("❌ No active employees found. Please create some employees first.")
        return False
    
    print(f"📋 Found {len(employees)} employees to assign devices to")
    
    # Device templates
    device_templates = {
        'laptop': [
            {'manufacturer': 'Dell', 'models': ['Latitude 5520', 'Latitude 7420', 'XPS 13', 'Inspiron 15']},
            {'manufacturer': 'HP', 'models': ['EliteBook 850', 'ProBook 450', 'Pavilion 15', 'ZBook Studio']},
            {'manufacturer': 'Lenovo', 'models': ['ThinkPad X1', 'ThinkPad T14', 'IdeaPad 5', 'Yoga 7i']},
            {'manufacturer': 'Apple', 'models': ['MacBook Pro 13"', 'MacBook Pro 16"', 'MacBook Air M2', 'MacBook Air M1']}
        ],
        'phone': [
            {'manufacturer': 'Apple', 'models': ['iPhone 14', 'iPhone 13', 'iPhone 12', 'iPhone SE']},
            {'manufacturer': 'Samsung', 'models': ['Galaxy S23', 'Galaxy S22', 'Galaxy A54', 'Galaxy Note 20']},
            {'manufacturer': 'Google', 'models': ['Pixel 7', 'Pixel 6', 'Pixel 5', 'Pixel 4a']},
            {'manufacturer': 'OnePlus', 'models': ['OnePlus 11', 'OnePlus 10', 'OnePlus 9', 'OnePlus 8T']}
        ],
        'tablet': [
            {'manufacturer': 'Apple', 'models': ['iPad Pro 12.9"', 'iPad Pro 11"', 'iPad Air', 'iPad Mini']},
            {'manufacturer': 'Samsung', 'models': ['Galaxy Tab S8', 'Galaxy Tab S7', 'Galaxy Tab A8', 'Galaxy Tab S6']},
            {'manufacturer': 'Microsoft', 'models': ['Surface Pro 9', 'Surface Pro 8', 'Surface Go 3', 'Surface Laptop Studio']}
        ],
        'desktop': [
            {'manufacturer': 'Dell', 'models': ['OptiPlex 7090', 'OptiPlex 5090', 'Precision 3660', 'Inspiron 3880']},
            {'manufacturer': 'HP', 'models': ['EliteDesk 800', 'ProDesk 400', 'Pavilion Desktop', 'Z2 Mini']},
            {'manufacturer': 'Apple', 'models': ['iMac 24"', 'iMac 27"', 'Mac Studio', 'Mac Pro']}
        ]
    }
    
    # OS versions
    os_versions = {
        'Windows': ['11.0', '10.0', '10.0.19044', '10.0.19043'],
        'macOS': ['13.0', '12.0', '11.0', '10.15'],
        'iOS': ['16.0', '15.0', '14.0', '13.0'],
        'Android': ['13.0', '12.0', '11.0', '10.0']
    }
    
    created_devices = []
    
    for employee in employees:
        # Randomly assign 1-3 devices per employee
        num_devices = random.randint(1, 3)
        
        for i in range(num_devices):
            # Choose random device type
            device_type = random.choice(list(device_templates.keys()))
            template = random.choice(device_templates[device_type])
            
            # Generate device details
            manufacturer = template['manufacturer']
            model = random.choice(template['models'])
            
            # Generate serial number
            serial_number = f"FAKE{random.randint(100000, 999999)}"
            
            # Generate device name
            device_name = f"{employee.name}'s {model}"
            
            # Determine OS based on device type
            if device_type == 'laptop':
                if manufacturer == 'Apple':
                    os_type = 'macOS'
                    os_version = random.choice(os_versions['macOS'])
                else:
                    os_type = 'Windows'
                    os_version = random.choice(os_versions['Windows'])
            elif device_type == 'phone':
                if manufacturer == 'Apple':
                    os_type = 'iOS'
                    os_version = random.choice(os_versions['iOS'])
                else:
                    os_type = 'Android'
                    os_version = random.choice(os_versions['Android'])
            elif device_type == 'tablet':
                if manufacturer == 'Apple':
                    os_type = 'iOS'
                    os_version = random.choice(os_versions['iOS'])
                else:
                    os_type = 'Android'
                    os_version = random.choice(os_versions['Android'])
            else:  # desktop
                if manufacturer == 'Apple':
                    os_type = 'macOS'
                    os_version = random.choice(os_versions['macOS'])
                else:
                    os_type = 'Windows'
                    os_version = random.choice(os_versions['Windows'])
            
            # Create asset
            try:
                asset = Asset.objects.create(
                    name=device_name,
                    asset_type=device_type,
                    serial_number=serial_number,
                    manufacturer=manufacturer,
                    model=model,
                    operating_system=os_type,
                    os_version=os_version,
                    status='assigned',
                    assigned_to=employee,
                    purchase_date=datetime.now() - timedelta(days=random.randint(30, 365)),
                    warranty_expiry=datetime.now() + timedelta(days=random.randint(365, 1095)),
                    notes=f"Fake device for testing - {device_type} assigned to {employee.name}"
                )
                
                created_devices.append(asset)
                print(f"✅ Created: {device_name} → {employee.name}")
                
            except Exception as e:
                print(f"❌ Failed to create {device_name}: {e}")
    
    print(f"\n🎉 Fake device creation completed!")
    print(f"📊 Created {len(created_devices)} fake devices")
    
    return created_devices

def show_device_summary():
    """Show summary of all devices in the system"""
    
    print("\n📊 Device Summary")
    print("=" * 30)
    
    # Total assets
    total_assets = Asset.objects.count()
    print(f"Total assets: {total_assets}")
    
    # Assets by type
    asset_types = Asset.objects.values('asset_type').distinct()
    for asset_type in asset_types:
        count = Asset.objects.filter(asset_type=asset_type['asset_type']).count()
        print(f"  {asset_type['asset_type'].title()}: {count}")
    
    # Assigned vs unassigned
    assigned_assets = Asset.objects.filter(assigned_to__isnull=False).count()
    unassigned_assets = Asset.objects.filter(assigned_to__isnull=True).count()
    print(f"Assigned assets: {assigned_assets}")
    print(f"Unassigned assets: {unassigned_assets}")
    
    # Assets by manufacturer
    manufacturers = Asset.objects.values('manufacturer').distinct()
    print(f"\nManufacturers:")
    for manufacturer in manufacturers:
        if manufacturer['manufacturer']:
            count = Asset.objects.filter(manufacturer=manufacturer['manufacturer']).count()
            print(f"  {manufacturer['manufacturer']}: {count}")

def create_sample_azure_devices():
    """Create sample devices that simulate Azure AD devices"""
    
    print("\n🔗 Creating Sample Azure AD Devices")
    print("=" * 40)
    
    # Get some employees
    employees = Employee.objects.filter(status='active')[:5]
    
    if not employees:
        print("❌ No active employees found.")
        return False
    
    # Sample Azure AD device data
    azure_devices = [
        {
            'name': 'John\'s Work Laptop',
            'asset_type': 'laptop',
            'serial_number': 'AZURE001',
            'manufacturer': 'Dell',
            'model': 'Latitude 5520',
            'operating_system': 'Windows',
            'os_version': '11.0',
            'azure_ad_id': 'azure-device-001',
            'assigned_to': employees[0] if len(employees) > 0 else None
        },
        {
            'name': 'Jane\'s iPhone',
            'asset_type': 'phone',
            'serial_number': 'AZURE002',
            'manufacturer': 'Apple',
            'model': 'iPhone 13',
            'operating_system': 'iOS',
            'os_version': '15.0',
            'azure_ad_id': 'azure-device-002',
            'assigned_to': employees[1] if len(employees) > 1 else None
        },
        {
            'name': 'Bob\'s MacBook',
            'asset_type': 'laptop',
            'serial_number': 'AZURE003',
            'manufacturer': 'Apple',
            'model': 'MacBook Pro',
            'operating_system': 'macOS',
            'os_version': '12.0',
            'azure_ad_id': 'azure-device-003',
            'assigned_to': employees[2] if len(employees) > 2 else None
        },
        {
            'name': 'Sarah\'s iPad',
            'asset_type': 'tablet',
            'serial_number': 'AZURE004',
            'manufacturer': 'Apple',
            'model': 'iPad Pro',
            'operating_system': 'iOS',
            'os_version': '16.0',
            'azure_ad_id': 'azure-device-004',
            'assigned_to': employees[3] if len(employees) > 3 else None
        },
        {
            'name': 'Mike\'s Android Phone',
            'asset_type': 'phone',
            'serial_number': 'AZURE005',
            'manufacturer': 'Samsung',
            'model': 'Galaxy S23',
            'operating_system': 'Android',
            'os_version': '13.0',
            'azure_ad_id': 'azure-device-005',
            'assigned_to': employees[4] if len(employees) > 4 else None
        }
    ]
    
    created_count = 0
    for device_data in azure_devices:
        try:
            # Check if device already exists
            existing = Asset.objects.filter(azure_ad_id=device_data['azure_ad_id']).first()
            if not existing:
                Asset.objects.create(**device_data)
                created_count += 1
                print(f"✅ Created: {device_data['name']} → {device_data['assigned_to'].name if device_data['assigned_to'] else 'Unassigned'}")
            else:
                print(f"⚠️  Already exists: {device_data['name']}")
        except Exception as e:
            print(f"❌ Failed to create {device_data['name']}: {e}")
    
    print(f"\n🎉 Sample Azure AD devices created: {created_count}")
    return created_count

def cleanup_fake_devices():
    """Remove all fake devices (for testing cleanup)"""
    
    print("\n🧹 Cleaning Up Fake Devices")
    print("=" * 30)
    
    # Remove devices with fake serial numbers
    fake_devices = Asset.objects.filter(serial_number__startswith='FAKE')
    fake_count = fake_devices.count()
    
    if fake_count > 0:
        fake_devices.delete()
        print(f"✅ Removed {fake_count} fake devices")
    else:
        print("ℹ️  No fake devices found to clean up")
    
    # Remove Azure AD test devices
    azure_devices = Asset.objects.filter(azure_ad_id__startswith='azure-device-')
    azure_count = azure_devices.count()
    
    if azure_count > 0:
        azure_devices.delete()
        print(f"✅ Removed {azure_count} Azure AD test devices")
    else:
        print("ℹ️  No Azure AD test devices found to clean up")

def show_help():
    """Show help information"""
    
    print("\n🆘 Fake Device Generator Help")
    print("=" * 40)
    
    print("\nAvailable commands:")
    print("  python create_fake_devices.py --create     # Create fake devices")
    print("  python create_fake_devices.py --azure      # Create Azure AD sample devices")
    print("  python create_fake_devices.py --summary   # Show device summary")
    print("  python create_fake_devices.py --cleanup    # Remove fake devices")
    print("  python create_fake_devices.py --help       # Show this help")
    
    print("\nExamples:")
    print("  # Create 20 fake devices for testing")
    print("  python create_fake_devices.py --create")
    
    print("\n  # Create sample Azure AD devices")
    print("  python create_fake_devices.py --azure")
    
    print("\n  # Show current device summary")
    print("  python create_fake_devices.py --summary")
    
    print("\n  # Clean up all fake devices")
    print("  python create_fake_devices.py --cleanup")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("🖥️  Fake Device Generator for AssetTrack")
        print("=" * 50)
        print("Use --help to see available commands")
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--create":
        print("🖥️  Creating Fake Devices for Testing")
        print("=" * 50)
        create_fake_devices()
        show_device_summary()
        
    elif command == "--azure":
        print("🔗 Creating Sample Azure AD Devices")
        print("=" * 50)
        create_sample_azure_devices()
        show_device_summary()
        
    elif command == "--summary":
        show_device_summary()
        
    elif command == "--cleanup":
        cleanup_fake_devices()
        show_device_summary()
        
    elif command == "--help":
        show_help()
        
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)
