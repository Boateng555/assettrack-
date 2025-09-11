#!/usr/bin/env python
"""
Test script to demonstrate the Azure AD API functionality
This shows how to access the Azure AD integration data via API
"""

import requests
import json
from datetime import datetime

def test_azure_ad_api():
    """Test the Azure AD status API endpoint"""
    
    print("🚀 Testing Azure AD Integration API")
    print("=" * 50)
    
    # Base URL for the Django development server
    base_url = "http://localhost:8000"
    
    # Test the Azure AD status API
    api_url = f"{base_url}/azure-status/"
    
    print(f"📡 Making API request to: {api_url}")
    print()
    
    try:
        # Make the API request
        response = requests.get(api_url, headers={'Accept': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ API Response Received Successfully!")
            print()
            
            # Display summary
            summary = data['summary']
            print("📊 Summary:")
            print(f"  • Total Azure AD Employees: {summary['total_azure_employees']}")
            print(f"  • Total Azure AD Assets: {summary['total_azure_assets']}")
            print(f"  • Total Employees: {summary['total_employees']}")
            print(f"  • Total Assets: {summary['total_assets']}")
            print(f"  • Employee Sync Percentage: {summary['sync_percentage']['employees']:.1f}%")
            print(f"  • Asset Sync Percentage: {summary['sync_percentage']['assets']:.1f}%")
            print()
            
            # Display Azure AD employees
            print("👥 Azure AD Employees:")
            print("-" * 40)
            for emp in data['employees']:
                print(f"  • {emp['name']} ({emp['department']})")
                print(f"    Email: {emp['email']}")
                print(f"    Job Title: {emp['job_title']}")
                print(f"    Azure AD ID: {emp['azure_ad_id']}")
                print(f"    Assigned Assets: {emp['assigned_assets_count']}")
                print(f"    Last Sync: {emp['last_azure_sync']}")
                print()
            
            # Display Azure AD assets
            print("💻 Azure AD Assets:")
            print("-" * 40)
            for asset in data['assets']:
                assigned_to = asset['assigned_to']['name'] if asset['assigned_to'] else "Unassigned"
                print(f"  • {asset['name']} ({asset['asset_type']})")
                print(f"    OS: {asset['operating_system']} {asset['os_version']}")
                print(f"    Manufacturer: {asset['manufacturer']} {asset['model']}")
                print(f"    Status: {asset['status']}")
                print(f"    Assigned To: {assigned_to}")
                print(f"    Azure AD ID: {asset['azure_ad_id']}")
                print()
            
            print("🎯 API Test Completed Successfully!")
            print()
            print("🔗 This demonstrates how your app will integrate with Microsoft Azure AD:")
            print("  • Employees from Azure AD will be automatically synced")
            print("  • Their laptops and devices will be imported")
            print("  • Device assignments will be tracked")
            print("  • Real-time data will be available via API")
            
        else:
            print(f"❌ API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Django server.")
        print("Make sure the server is running with: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

def test_web_interface():
    """Test the web interface"""
    
    print("\n🌐 Testing Web Interface")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    print(f"📱 You can also view the data in your web browser:")
    print(f"   • Azure AD Status: {base_url}/azure-status/")
    print(f"   • Azure AD Sync: {base_url}/azure-sync/")
    print(f"   • Dashboard: {base_url}/")
    print()
    print("🔐 Note: You may need to log in first if authentication is required.")

def main():
    """Main test function"""
    
    print("🔗 AssetTrack Azure AD Integration API Test")
    print("=" * 60)
    print()
    
    # Test the API
    test_azure_ad_api()
    
    # Test web interface
    test_web_interface()
    
    print("\n✅ Testing completed!")
    print("\n📋 Next steps for real Azure AD integration:")
    print("  1. Configure Azure AD credentials in settings.py")
    print("  2. Set up your Azure AD tenant and app registration")
    print("  3. Run: python manage.py sync_azure_ad")
    print("  4. Monitor the integration via the web interface")
    print("  5. Set up automated sync schedules")

if __name__ == "__main__":
    main()

