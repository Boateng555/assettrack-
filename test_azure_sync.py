#!/usr/bin/env python
"""
Test script to check Azure AD sync functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration
from assets.models import Employee
from django.contrib.auth.models import User

def test_azure_ad_sync():
    """Test Azure AD sync functionality"""
    print("🔍 Testing Azure AD Sync...")
    print("=" * 50)
    
    # Check environment variables
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    
    print(f"✅ Environment variables:")
    print(f"   AZURE_TENANT_ID: {tenant_id}")
    print(f"   AZURE_CLIENT_ID: {client_id}")
    print(f"   AZURE_CLIENT_SECRET: {'Set' if client_secret else 'Not set'}")
    
    # Test Azure AD connection
    try:
        azure = AzureADIntegration()
        print(f"\n🔗 Azure AD Integration:")
        print(f"   Tenant ID: {azure.tenant_id}")
        print(f"   Client ID: {azure.client_id}")
        print(f"   Client Secret: {'Set' if azure.client_secret else 'Not set'}")
        
        # Test getting access token
        print(f"\n🔑 Testing access token...")
        token = azure.get_access_token()
        if token:
            print(f"   ✅ Access token obtained successfully")
        else:
            print(f"   ❌ Failed to get access token")
            return False
        
        # Test getting users
        print(f"\n👥 Testing user retrieval...")
        users = azure.get_users()
        print(f"   Found {len(users)} users in Azure AD")
        
        if users:
            print(f"   Sample users:")
            for i, user in enumerate(users[:3]):  # Show first 3 users
                print(f"     {i+1}. {user.get('displayName', 'N/A')} ({user.get('mail', 'N/A')})")
        
        # Check existing employees
        print(f"\n📊 Current employees in database:")
        employees = Employee.objects.all()
        print(f"   Total employees: {employees.count()}")
        
        azure_employees = Employee.objects.filter(azure_ad_id__isnull=False)
        print(f"   Azure AD employees: {azure_employees.count()}")
        
        if azure_employees.exists():
            print(f"   Sample Azure employees:")
            for emp in azure_employees[:3]:
                print(f"     - {emp.name} ({emp.email}) - Azure ID: {emp.azure_ad_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Azure AD sync: {e}")
        return False

if __name__ == '__main__':
    test_azure_ad_sync()
