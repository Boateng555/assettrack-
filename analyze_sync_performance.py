#!/usr/bin/env python
"""
Analyze Sync Performance

This script analyzes why Azure AD sync takes time and shows performance metrics.
"""

import os
import sys
import django
import time
import requests

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assettrack_django.settings')
django.setup()

from assets.azure_ad_integration import AzureADIntegration
from assets.models import Employee, Asset

def analyze_sync_performance():
    """Analyze why sync takes time"""
    
    print("⏱️ AZURE AD SYNC PERFORMANCE ANALYSIS")
    print("=" * 45)
    
    # Check current data size
    total_employees = Employee.objects.count()
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).count()
    total_assets = Asset.objects.count()
    
    print(f"📊 CURRENT DATA SIZE:")
    print(f"  Total Employees: {total_employees}")
    print(f"  Azure AD Employees: {azure_employees}")
    print(f"  Total Assets: {total_assets}")
    print()
    
    # Test API performance
    print("🧪 TESTING API PERFORMANCE:")
    
    try:
        azure_ad = AzureADIntegration()
        
        # Test user API call
        start_time = time.time()
        users = azure_ad.get_users()
        user_time = time.time() - start_time
        
        print(f"  👥 User API call: {user_time:.2f} seconds")
        print(f"  📊 Users retrieved: {len(users)}")
        print(f"  ⚡ Rate: {len(users)/user_time:.1f} users/second")
        print()
        
        # Test device API call (if working)
        try:
            start_time = time.time()
            devices = azure_ad.get_devices()
            device_time = time.time() - start_time
            print(f"  🖥️  Device API call: {device_time:.2f} seconds")
            print(f"  📊 Devices retrieved: {len(devices)}")
            if len(devices) > 0:
                print(f"  ⚡ Rate: {len(devices)/device_time:.1f} devices/second")
        except Exception as e:
            print(f"  🖥️  Device API call: Failed ({str(e)[:50]}...)")
        print()
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False
    
    return True

def explain_sync_timing():
    """Explain why sync takes time"""
    
    print("🕐 WHY SYNC TAKES TIME")
    print("=" * 25)
    print()
    print("1. 📡 API RATE LIMITS:")
    print("   - Microsoft Graph has rate limits")
    print("   - Max 10,000 requests per 10 minutes")
    print("   - Your org has 1,478 users = many API calls")
    print()
    print("2. 🔄 DATA PROCESSING:")
    print("   - Each user needs individual processing")
    print("   - Database operations for each user")
    print("   - Photo downloads (if available)")
    print("   - Device lookups for each user")
    print()
    print("3. 🌐 NETWORK LATENCY:")
    print("   - API calls to Microsoft servers")
    print("   - Data transfer over internet")
    print("   - Multiple round trips required")
    print()
    print("4. 📊 DATA SIZE:")
    print("   - 1,478 users = large dataset")
    print("   - Each user has multiple attributes")
    print("   - Device data adds more complexity")
    print()
    print("5. 🔐 SECURITY CHECKS:")
    print("   - Authentication for each request")
    print("   - Permission validation")
    print("   - Rate limiting protection")

def show_optimization_tips():
    """Show how to optimize sync performance"""
    
    print("\n⚡ SYNC OPTIMIZATION TIPS")
    print("=" * 30)
    print()
    print("1. 🕐 SYNC DURING OFF-PEAK HOURS:")
    print("   - Early morning (6-8 AM)")
    print("   - Late evening (8-10 PM)")
    print("   - Weekends")
    print()
    print("2. 🔄 INCREMENTAL SYNC:")
    print("   - Only sync changed users")
    print("   - Use timestamps to track changes")
    print("   - Reduce API calls")
    print()
    print("3. 📊 BATCH PROCESSING:")
    print("   - Process users in batches")
    print("   - Reduce database operations")
    print("   - Optimize memory usage")
    print()
    print("4. 🚀 PARALLEL PROCESSING:")
    print("   - Process multiple users simultaneously")
    print("   - Use threading for API calls")
    print("   - Reduce total sync time")
    print()
    print("5. 💾 CACHING:")
    print("   - Cache user data locally")
    print("   - Reduce repeated API calls")
    print("   - Faster subsequent syncs")

def show_expected_timing():
    """Show expected sync timing"""
    
    print("\n⏱️ EXPECTED SYNC TIMING")
    print("=" * 25)
    print()
    print("📊 FOR 1,478 USERS:")
    print("  - Initial sync: 5-15 minutes")
    print("  - Incremental sync: 1-3 minutes")
    print("  - Device sync: 2-5 minutes")
    print("  - Full sync: 10-20 minutes")
    print()
    print("📈 PERFORMANCE FACTORS:")
    print("  - Internet speed")
    print("  - Server performance")
    print("  - API rate limits")
    print("  - Data complexity")
    print()
    print("🎯 OPTIMIZATION RESULTS:")
    print("  - With optimization: 2-5 minutes")
    print("  - Without optimization: 10-20 minutes")
    print("  - Difference: 3-4x faster")

if __name__ == "__main__":
    success = analyze_sync_performance()
    
    if success:
        explain_sync_timing()
        show_optimization_tips()
        show_expected_timing()
    else:
        print("❌ Performance analysis failed")
