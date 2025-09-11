#!/usr/bin/env python
"""
Debug script to see what users are in Azure AD
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
import requests

def debug_azure_users():
    """Debug what users are in Azure AD"""
    print("🔍 Debugging Azure AD Users...")
    print("=" * 50)
    
    try:
        azure = AzureADIntegration()
        
        # Test access token
        token = azure.get_access_token()
        if not token:
            print("❌ Failed to get access token")
            return
        
        print("✅ Access token obtained successfully")
        
        # Get all users without filter first
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        url = "https://graph.microsoft.com/v1.0/users"
        params = {
            '$select': 'id,displayName,mail,userPrincipalName,department,jobTitle,employeeId,accountEnabled'
        }
        
        print(f"\n👥 Getting all users from Azure AD...")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            users = data.get('value', [])
            
            print(f"✅ Found {len(users)} total users in Azure AD")
            
            if users:
                print(f"\n📋 User Details:")
                for i, user in enumerate(users):
                    print(f"   {i+1}. {user.get('displayName', 'N/A')}")
                    print(f"      - Email: {user.get('mail', 'N/A')}")
                    print(f"      - UPN: {user.get('userPrincipalName', 'N/A')}")
                    print(f"      - Enabled: {user.get('accountEnabled', 'N/A')}")
                    print(f"      - Department: {user.get('department', 'N/A')}")
                    print(f"      - Job Title: {user.get('jobTitle', 'N/A')}")
                    print()
            else:
                print("❌ No users found in Azure AD tenant")
                
        else:
            print(f"❌ Failed to get users: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    debug_azure_users()
