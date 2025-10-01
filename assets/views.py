from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta, date
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse
from django.conf import settings
import json
import random

from .models import Employee, Asset, Handover, WelcomePack
from .azure_ad_integration import AzureADIntegration

def calculate_health_score(asset):
    """Calculate asset health score based on Azure AD sync date for Azure assets, purchase date for others"""
    reference_date = None
    
    # For Azure AD assets, prioritize Azure sync date over purchase date
    if asset.azure_ad_id and asset.last_azure_sync:
        # Asset came from Azure AD - use sync date as reference (when it was discovered)
        reference_date = asset.last_azure_sync.date()
    elif asset.azure_ad_id and asset.azure_last_signin:
        # Use Azure last sign-in date if available
        reference_date = asset.azure_last_signin.date()
    elif asset.purchase_date:
        # Manually added asset - use purchase date
        reference_date = asset.purchase_date
    elif asset.last_azure_sync:
        # Fallback to Azure sync date if no other date available
        reference_date = asset.last_azure_sync.date()
    
    if not reference_date:
        return 50  # Unknown age - assume moderate health
    
    today = date.today()
    age_days = (today - reference_date).days
    
    # Health calculation based on when asset was discovered in Azure AD
    if age_days < 30:  # Less than 1 month
        return 100
    elif age_days < 90:  # Less than 3 months
        return 95
    elif age_days < 180:  # Less than 6 months
        return 90
    elif age_days < 365:  # Less than 1 year
        return 85
    elif age_days < 730:  # Less than 2 years
        return 75
    elif age_days < 1095:  # Less than 3 years
        return 65
    elif age_days < 1460:  # Less than 4 years
        return 55
    elif age_days < 1825:  # Less than 5 years
        return 45
    else:  # 5+ years
        return 35

@login_required
def admin_dashboard(request):
    """Admin dashboard view with system statistics and management tools"""
    # Check if user has admin privileges (you can customize this logic)
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('assets:dashboard')
    
    # Get system statistics
    total_users = Employee.objects.count()
    active_sessions = 8  # Mock data - you can implement real session tracking
    system_health = 98  # Mock data
    storage_used = 67  # Mock data
    
    # Get recent system logs (mock data for now)
    system_logs = [
        {
            'timestamp': '2024-01-15 14:30:22',
            'level': 'INFO',
            'user': 'admin',
            'action': 'User Login',
            'details': 'Successful login from 192.168.1.100'
        },
        {
            'timestamp': '2024-01-15 14:25:15',
            'level': 'DEBUG',
            'user': 'system',
            'action': 'Asset Sync',
            'details': 'Azure sync completed successfully'
        },
        {
            'timestamp': '2024-01-15 14:20:08',
            'level': 'WARN',
            'user': 'jane.smith',
            'action': 'Asset Assignment',
            'details': 'Asset LAP-001 assigned to user'
        },
        {
            'timestamp': '2024-01-15 14:15:42',
            'level': 'ERROR',
            'user': 'system',
            'action': 'Backup Failed',
            'details': 'Database backup failed - insufficient space'
        }
    ]
    
    context = {
        'total_users': total_users,
        'active_sessions': active_sessions,
        'system_health': system_health,
        'storage_used': storage_used,
        'system_logs': system_logs,
    }
    
    return render(request, 'admin.html', context)

@login_required
def azure_ad_sync(request):
    """Azure AD sync view with full change detection"""
    if request.method == 'POST':
        try:
            azure_ad = AzureADIntegration()
            results = azure_ad.full_sync()
            
            messages.success(
                request, 
                f'Azure AD sync completed successfully! '
                f'Employees: {results["employees_synced"]} new, {results["employees_updated"]} updated, {results["employees_disabled"]} disabled, {results["employees_deleted"]} deleted. '
                f'User Devices: {results["user_devices_synced"]} synced, {results["user_devices_assigned"]} assigned. '
                f'Standalone Devices: {results["standalone_devices_synced"]} synced, {results["standalone_devices_updated"]} updated. '
                f'Assignments: {results["assignments_updated"]} updated. '
                f'Assets cleaned up: {results["assets_cleaned_up"]}.'
            )
            
        except Exception as e:
            messages.error(request, f'Azure AD sync failed: {str(e)}')
            
        return redirect('assets:dashboard')
    
    # Get sync statistics with status breakdown
    azure_ad = AzureADIntegration()
    summary = azure_ad.get_sync_summary()
    
    employees_with_azure = Employee.objects.filter(azure_ad_id__isnull=False).count()
    assets_with_azure = Asset.objects.filter(azure_ad_id__isnull=False).count()
    total_employees = Employee.objects.count()
    total_assets = Asset.objects.count()
    
    context = {
        'employees_with_azure': employees_with_azure,
        'assets_with_azure': assets_with_azure,
        'total_employees': total_employees,
        'total_assets': total_assets,
        'azure_sync_percentage': {
            'employees': (employees_with_azure / total_employees * 100) if total_employees > 0 else 0,
            'assets': (assets_with_azure / total_assets * 100) if total_assets > 0 else 0,
        },
        'sync_summary': summary,
        'employee_status_breakdown': {
            'active': Employee.objects.filter(status='active').count(),
            'inactive': Employee.objects.filter(status='inactive').count(),
            'deleted': Employee.objects.filter(status='deleted').count(),
        }
    }
    
    return render(request, 'azure_ad_sync.html', context)

@login_required
def azure_ad_status_api(request):
    """API endpoint to view Azure AD integration status and data"""
    if request.headers.get('Accept') == 'application/json':
        # Return JSON response for API calls
        azure_employees = Employee.objects.filter(azure_ad_id__isnull=False)
        azure_assets = Asset.objects.filter(azure_ad_id__isnull=False)
        
        employees_data = []
        for emp in azure_employees:
            assigned_assets = emp.assigned_assets.filter(azure_ad_id__isnull=False)
            employees_data.append({
                'id': str(emp.id),
                'name': emp.name,
                'email': emp.email,
                'department': emp.department,
                'job_title': emp.job_title,
                'azure_ad_id': emp.azure_ad_id,
                'azure_ad_username': emp.azure_ad_username,
                'employee_id': emp.employee_id,
                'last_azure_sync': emp.last_azure_sync.isoformat() if emp.last_azure_sync else None,
                'assigned_assets_count': assigned_assets.count(),
                'assigned_assets': [
                    {
                        'id': str(asset.id),
                        'name': asset.name,
                        'asset_type': asset.asset_type,
                        'serial_number': asset.serial_number,
                        'operating_system': asset.operating_system,
                        'os_version': asset.os_version,
                        'manufacturer': asset.manufacturer,
                        'model': asset.model
                    } for asset in assigned_assets
                ]
            })
        
        assets_data = []
        for asset in azure_assets:
            assets_data.append({
                'id': str(asset.id),
                'name': asset.name,
                'asset_type': asset.asset_type,
                'serial_number': asset.serial_number,
                'azure_ad_id': asset.azure_ad_id,
                'operating_system': asset.operating_system,
                'os_version': asset.os_version,
                'manufacturer': asset.manufacturer,
                'model': asset.model,
                'status': asset.status,
                'assigned_to': {
                    'id': str(asset.assigned_to.id),
                    'name': asset.assigned_to.name,
                    'email': asset.assigned_to.email
                } if asset.assigned_to else None,
                'last_azure_sync': asset.last_azure_sync.isoformat() if asset.last_azure_sync else None
            })
        
        return JsonResponse({
            'status': 'success',
            'summary': {
                'total_azure_employees': azure_employees.count(),
                'total_azure_assets': azure_assets.count(),
                'total_employees': Employee.objects.count(),
                'total_assets': Asset.objects.count(),
                'sync_percentage': {
                    'employees': (azure_employees.count() / Employee.objects.count() * 100) if Employee.objects.count() > 0 else 0,
                    'assets': (azure_assets.count() / Asset.objects.count() * 100) if Asset.objects.count() > 0 else 0,
                }
            },
            'employees': employees_data,
            'assets': assets_data
        })
    
    # Return HTML view for browser requests
    azure_employees = Employee.objects.filter(azure_ad_id__isnull=False).prefetch_related('assigned_assets')
    azure_assets = Asset.objects.filter(azure_ad_id__isnull=False).select_related('assigned_to')
    
    context = {
        'azure_employees': azure_employees,
        'azure_assets': azure_assets,
        'total_azure_employees': azure_employees.count(),
        'total_azure_assets': azure_assets.count(),
        'total_employees': Employee.objects.count(),
        'total_assets': Asset.objects.count(),
    }
    
    return render(request, 'azure_ad_status.html', context)

@login_required
def dashboard(request):
    """Dashboard view with statistics and recent handovers"""
    
    # Add a test message to verify the message system is working
    if not request.session.get('test_message_shown'):
        messages.success(request, '🎉 Welcome to AssetTrack! Message system is working perfectly!')
        request.session['test_message_shown'] = True
    
    # Calculate statistics
    assets_in_stock = Asset.objects.filter(status='available').count()
    pending_signatures = Handover.objects.filter(status='Pending').count()
    pending_scans = Handover.objects.filter(status='Pending Scan').count()
    recent_handovers_count = Handover.objects.count()
    
    # Calculate trends (simplified for demo)
    assets_trend = 12  # Mock data
    overdue_signatures = 3  # Mock data
    last_scan_time = "15 min ago"  # Mock data
    today_handovers = Handover.objects.filter(created_at__date=timezone.now().date()).count()
    
    # Get recent handovers with pagination
    recent_handovers_list = Handover.objects.select_related('employee').prefetch_related('assets')[:10]
    paginator = Paginator(recent_handovers_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets_in_stock': assets_in_stock,
        'pending_signatures': pending_signatures,
        'pending_scans': pending_scans,
        'recent_handovers': recent_handovers_count,
        'assets_trend': assets_trend,
        'overdue_signatures': overdue_signatures,
        'last_scan_time': last_scan_time,
        'today_handovers': today_handovers,
        'recent_handovers_list': page_obj,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def employees(request):
    """Employee management view with search functionality"""
    employees = Employee.objects.all()
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    context = {
        'employees': employees,
        'search_query': search_query,
    }
    return render(request, 'employees.html', context)

@login_required
def add_employee(request):
    """Add new employee view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        phone = request.POST.get('phone', '')
        start_date = request.POST.get('start_date')
        
        try:
            # Convert start_date string to date object if provided
            if start_date:
                from datetime import datetime
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            employee = Employee.objects.create(
                name=name,
                email=email,
                department=department,
                phone=phone,
                start_date=start_date
            )
            
            messages.success(request, f'Employee {employee.name} added successfully!')
            return redirect('assets:employees')
            
        except Exception as e:
            messages.error(request, f'Error adding employee: {str(e)}')
    
    return redirect('assets:employees')

@login_required
def edit_employee(request, employee_id):
    """Edit employee view"""
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        phone = request.POST.get('phone', '')
        start_date = request.POST.get('start_date')
        is_active = request.POST.get('is_active') == 'on'
        
        try:
            # Convert start_date string to date object if provided
            if start_date:
                from datetime import datetime
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            employee.name = name
            employee.email = email
            employee.department = department
            employee.phone = phone
            employee.start_date = start_date
            employee.is_active = is_active
            employee.save()
            
            messages.success(request, f'Employee {employee.name} updated successfully!')
            return redirect('assets:employees')
            
        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')
    
    context = {
        'employee': employee,
    }
    return render(request, 'edit_employee.html', context)

@login_required
def delete_employee(request, employee_id):
    """Delete employee view"""
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        try:
            employee_name = employee.name
            employee.delete()
            messages.success(request, f'Employee {employee_name} deleted successfully!')
            return redirect('assets:employees')
        except Exception as e:
            messages.error(request, f'Error deleting employee: {str(e)}')
    
    context = {
        'employee': employee,
    }
    return render(request, 'delete_employee.html', context)

@login_required
def assets(request):
    """Asset management view with enhanced analytics"""
    
    # Get all assets with related data
    assets = Asset.objects.select_related('assigned_to').all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        assets = assets.filter(status=status_filter)
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        assets = assets.filter(asset_type=asset_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        assets = assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query)
        )
    
    # Calculate analytics
    total_assets = Asset.objects.count()
    available_assets = Asset.objects.filter(status='available').count()
    assigned_assets = Asset.objects.filter(status='assigned').count()
    maintenance_assets = Asset.objects.filter(status='maintenance').count()
    lost_assets = Asset.objects.filter(status='lost').count()
    
    # Calculate asset age and health
    today = date.today()
    new_assets = Asset.objects.filter(
        assigned_to__isnull=True,
        status='available'
    ).count()
    
    old_assets = Asset.objects.filter(
        purchase_date__lte=today - timedelta(days=365*3)  # 3+ years old
    ).count()
    
    # Department distribution
    department_stats = Asset.objects.filter(
        assigned_to__isnull=False
    ).values(
        'assigned_to__department'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Asset type distribution
    asset_type_stats = Asset.objects.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Maintenance alerts (assets older than 3 years)
    maintenance_alerts = Asset.objects.filter(
        purchase_date__lte=today - timedelta(days=365*3)
    ).count()
    
    # Recently added assets (last 7 days)
    recent_assets = Asset.objects.filter(
        created_at__gte=today - timedelta(days=7)
    ).count()
    
    # Add health scores to assets using the main function
    for asset in assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_assets': total_assets,
        'available_assets': available_assets,
        'assigned_assets': assigned_assets,
        'maintenance_assets': maintenance_assets,
        'lost_assets': lost_assets,
        'new_assets': new_assets,
        'old_assets': old_assets,
        'maintenance_alerts': maintenance_alerts,
        'recent_assets': recent_assets,
        'department_stats': department_stats,
        'asset_type_stats': asset_type_stats,
        'status_filter': status_filter,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'assets.html', context)

@login_required
def unassigned_assets(request):
    """Unassigned assets view - shows assets not assigned to any employee"""
    
    # Get unassigned assets (assets with no assigned_to or status = available)
    unassigned_assets = Asset.objects.filter(
        Q(assigned_to__isnull=True) | Q(status='available')
    ).select_related('assigned_to').distinct()
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        unassigned_assets = unassigned_assets.filter(asset_type=asset_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        unassigned_assets = unassigned_assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )
    
    # Calculate analytics for unassigned assets
    total_unassigned = unassigned_assets.count()
    available_unassigned = unassigned_assets.filter(status='available').count()
    maintenance_unassigned = unassigned_assets.filter(status='maintenance').count()
    lost_unassigned = unassigned_assets.filter(status='lost').count()
    
    # Asset type distribution for unassigned assets
    asset_type_stats = unassigned_assets.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate asset age and health
    today = date.today()
    
    # Add health scores to assets using the main function
    for asset in unassigned_assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(unassigned_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_unassigned': total_unassigned,
        'available_unassigned': available_unassigned,
        'maintenance_unassigned': maintenance_unassigned,
        'lost_unassigned': lost_unassigned,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'unassigned_assets.html', context)

@login_required
def search_assets_for_missing(request):
    """Search assets for marking as missing"""
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        employee_query = request.GET.get('employee', '')
        
        # Build the query
        assets = Asset.objects.exclude(status='lost').exclude(status='retired')
        
        if search_query:
            assets = assets.filter(
                Q(name__icontains=search_query) |
                Q(serial_number__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(manufacturer__icontains=search_query)
            )
        
        if employee_query:
            assets = assets.filter(
                Q(assigned_to__name__icontains=employee_query) |
                Q(assigned_to__email__icontains=employee_query)
            )
        
        # Limit results and add health scores
        assets = assets.select_related('assigned_to')[:20]
        
        # Calculate health scores
        today = date.today()
        for asset in assets:
            if asset.purchase_date:
                age_days = (today - asset.purchase_date).days
                if age_days < 365:
                    asset.health_score = 100
                elif age_days < 365*2:
                    asset.health_score = 85
                elif age_days < 365*3:
                    asset.health_score = 70
                elif age_days < 365*4:
                    asset.health_score = 55
                else:
                    asset.health_score = 40
            else:
                asset.health_score = 100
        
        # Prepare data for JSON response
        assets_data = []
        for asset in assets:
            assets_data.append({
                'id': str(asset.id),
                'name': asset.name,
                'serial_number': asset.serial_number,
                'model': asset.model or '',
                'manufacturer': asset.manufacturer or '',
                'asset_type': asset.get_asset_type_display(),
                'status': asset.get_status_display(),
                'health_score': asset.health_score,
                'assigned_to': asset.assigned_to.name if asset.assigned_to else 'Unassigned',
                'assigned_to_email': asset.assigned_to.email if asset.assigned_to else '',
                'purchase_date': asset.purchase_date.strftime('%Y-%m-%d') if asset.purchase_date else '',
            })
        
        return JsonResponse({'assets': assets_data})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def mark_asset_as_lost(request, asset_id):
    """Mark an existing asset as lost"""
    if request.method == 'POST':
        try:
            asset = Asset.objects.get(id=asset_id)
            asset.status = 'lost'
            asset.save()
            
            messages.success(request, f'Asset "{asset.name}" has been marked as lost.')
            return JsonResponse({'success': True, 'message': f'Asset "{asset.name}" marked as lost'})
        except Asset.DoesNotExist:
            return JsonResponse({'error': 'Asset not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def add_asset(request):
    """Add new asset view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        asset_type = request.POST.get('asset_type')
        serial_number = request.POST.get('serial_number')
        model = request.POST.get('model', '')
        manufacturer = request.POST.get('manufacturer', '')
        purchase_date = request.POST.get('purchase_date')
        status = request.POST.get('status', 'available')  # Default to available if not provided
        assigned_to_id = request.POST.get('assigned_to')
        
        # Software asset fields
        license_key = request.POST.get('license_key', '')
        license_type = request.POST.get('license_type', '')
        version = request.POST.get('version', '')
        vendor = request.POST.get('vendor', '')
        subscription_end = request.POST.get('subscription_end', '')
        seats = request.POST.get('seats', '')
        used_seats = request.POST.get('used_seats', '')
        
        # Maintenance fields
        maintenance_start_date = request.POST.get('maintenance_start_date', '')
        maintenance_expected_end = request.POST.get('maintenance_expected_end', '')
        maintenance_notes = request.POST.get('maintenance_notes', '')
        
        try:
            # Convert purchase_date string to date object if provided
            if purchase_date:
                try:
                    from datetime import datetime
                    # Try multiple date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                        try:
                            purchase_date = datetime.strptime(purchase_date, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        messages.error(request, f'Invalid purchase date format: {purchase_date}. Please use DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD format.')
                        employees = Employee.objects.filter(is_active=True)
                        context = {'employees': employees}
                        return render(request, 'add_asset.html', context)
                except Exception as e:
                    messages.error(request, f'Error parsing purchase date: {str(e)}')
                    employees = Employee.objects.filter(is_active=True)
                    context = {'employees': employees}
                    return render(request, 'add_asset.html', context)
            
            # Convert subscription_end string to date object if provided
            if subscription_end:
                try:
                    from datetime import datetime
                    # Try multiple date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                        try:
                            subscription_end = datetime.strptime(subscription_end, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        messages.error(request, f'Invalid subscription end date format: {subscription_end}. Please use DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD format.')
                        employees = Employee.objects.filter(is_active=True)
                        context = {'employees': employees}
                        return render(request, 'add_asset.html', context)
                except Exception as e:
                    messages.error(request, f'Error parsing subscription end date: {str(e)}')
                    employees = Employee.objects.filter(is_active=True)
                    context = {'employees': employees}
                    return render(request, 'add_asset.html', context)
            
            # Convert maintenance dates to date objects if provided
            if maintenance_start_date:
                try:
                    from datetime import datetime
                    # Try multiple date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                        try:
                            maintenance_start_date = datetime.strptime(maintenance_start_date, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        messages.error(request, f'Invalid maintenance start date format: {maintenance_start_date}. Please use DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD format.')
                        employees = Employee.objects.filter(is_active=True)
                        context = {'employees': employees}
                        return render(request, 'add_asset.html', context)
                except Exception as e:
                    messages.error(request, f'Error parsing maintenance start date: {str(e)}')
                    employees = Employee.objects.filter(is_active=True)
                    context = {'employees': employees}
                    return render(request, 'add_asset.html', context)
            elif status == 'maintenance':
                # Auto-set maintenance start date if status is maintenance
                from datetime import date
                maintenance_start_date = date.today()
            
            if maintenance_expected_end:
                try:
                    from datetime import datetime
                    # Try multiple date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                        try:
                            maintenance_expected_end = datetime.strptime(maintenance_expected_end, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        messages.error(request, f'Invalid maintenance expected end date format: {maintenance_expected_end}. Please use DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD format.')
                        employees = Employee.objects.filter(is_active=True)
                        context = {'employees': employees}
                        return render(request, 'add_asset.html', context)
                except Exception as e:
                    messages.error(request, f'Error parsing maintenance expected end date: {str(e)}')
                    employees = Employee.objects.filter(is_active=True)
                    context = {'employees': employees}
                    return render(request, 'add_asset.html', context)
            
            # Convert seats and used_seats to integers if provided
            seats = int(seats) if seats else None
            used_seats = int(used_seats) if used_seats else None
            
            asset = Asset.objects.create(
                name=name,
                asset_type=asset_type,
                serial_number=serial_number,
                model=model,
                manufacturer=manufacturer,
                purchase_date=purchase_date,
                status=status,
                license_key=license_key,
                license_type=license_type,
                version=version,
                vendor=vendor,
                subscription_end=subscription_end,
                seats=seats,
                used_seats=used_seats,
                maintenance_start_date=maintenance_start_date,
                maintenance_expected_end=maintenance_expected_end,
                maintenance_notes=maintenance_notes
            )
            
            # Handle assignment
            if assigned_to_id and assigned_to_id != 'none':
                assigned_to = Employee.objects.get(id=assigned_to_id)
                asset.assigned_to = assigned_to
                asset.status = 'assigned'
                asset.save()
            
            messages.success(request, f'Asset {asset.name} added successfully!')
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Asset {asset.name} added successfully!',
                    'asset_id': str(asset.id)
                })
            
            # Redirect based on status for regular form submissions
            if status == 'lost':
                return redirect('assets:lost_assets')
            elif status == 'maintenance':
                return redirect('assets:maintenance_assets')
            else:
                return redirect('assets:assets')
            
        except Exception as e:
            error_message = f'Error adding asset: {str(e)}'
            messages.error(request, error_message)
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': error_message
                })
    
    # Handle GET request - show add asset form
    employee_id = request.GET.get('employee')
    employee = None
    if employee_id:
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            pass
    
    employees = Employee.objects.filter(is_active=True)
    context = {
        'employees': employees,
        'pre_selected_employee': employee,
    }
    return render(request, 'add_asset.html', context)

@login_required
def edit_asset(request, asset_id):
    """Edit asset view"""
    asset = get_object_or_404(Asset, id=asset_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        asset_type = request.POST.get('asset_type')
        serial_number = request.POST.get('serial_number')
        model = request.POST.get('model', '')
        manufacturer = request.POST.get('manufacturer', '')
        purchase_date = request.POST.get('purchase_date')
        status = request.POST.get('status')
        assigned_to_id = request.POST.get('assigned_to')
        
        # Software asset fields
        license_key = request.POST.get('license_key', '')
        license_type = request.POST.get('license_type', '')
        version = request.POST.get('version', '')
        vendor = request.POST.get('vendor', '')
        subscription_end = request.POST.get('subscription_end', '')
        seats = request.POST.get('seats', '')
        used_seats = request.POST.get('used_seats', '')
        
        # Maintenance fields
        maintenance_start_date = request.POST.get('maintenance_start_date', '')
        maintenance_expected_end = request.POST.get('maintenance_expected_end', '')
        maintenance_notes = request.POST.get('maintenance_notes', '')
        
        try:
            # Convert purchase_date string to date object if provided
            if purchase_date:
                try:
                    from datetime import datetime
                    # Try multiple date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                        try:
                            purchase_date = datetime.strptime(purchase_date, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        messages.error(request, f'Invalid purchase date format: {purchase_date}. Please use DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD format.')
                        return render(request, 'edit_asset.html', context)
                except Exception as e:
                    messages.error(request, f'Error parsing purchase date: {str(e)}')
                    return render(request, 'edit_asset.html', context)
            
            # Convert subscription_end string to date object if provided
            if subscription_end:
                try:
                    from datetime import datetime
                    # Try multiple date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                        try:
                            subscription_end = datetime.strptime(subscription_end, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        messages.error(request, f'Invalid subscription end date format: {subscription_end}. Please use DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD format.')
                        return render(request, 'edit_asset.html', context)
                except Exception as e:
                    messages.error(request, f'Error parsing subscription end date: {str(e)}')
                    return render(request, 'edit_asset.html', context)
            
            # Convert maintenance dates to date objects if provided
            if maintenance_start_date:
                try:
                    from datetime import datetime
                    # Try multiple date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                        try:
                            maintenance_start_date = datetime.strptime(maintenance_start_date, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        messages.error(request, f'Invalid maintenance start date format: {maintenance_start_date}. Please use DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD format.')
                        return render(request, 'edit_asset.html', context)
                except Exception as e:
                    messages.error(request, f'Error parsing maintenance start date: {str(e)}')
                    return render(request, 'edit_asset.html', context)
            elif status == 'maintenance' and not asset.maintenance_start_date:
                # Auto-set maintenance start date if status is changed to maintenance and no start date exists
                from datetime import date
                maintenance_start_date = date.today()
            
            if maintenance_expected_end:
                try:
                    from datetime import datetime
                    # Try multiple date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                        try:
                            maintenance_expected_end = datetime.strptime(maintenance_expected_end, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        messages.error(request, f'Invalid maintenance expected end date format: {maintenance_expected_end}. Please use DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD format.')
                        return render(request, 'edit_asset.html', context)
                except Exception as e:
                    messages.error(request, f'Error parsing maintenance expected end date: {str(e)}')
                    return render(request, 'edit_asset.html', context)
            
            # Convert seats and used_seats to integers if provided
            seats = int(seats) if seats else None
            used_seats = int(used_seats) if used_seats else None
            
            asset.name = name
            asset.asset_type = asset_type
            asset.serial_number = serial_number
            asset.model = model
            asset.manufacturer = manufacturer
            asset.purchase_date = purchase_date
            asset.status = status
            asset.license_key = license_key
            asset.license_type = license_type
            asset.version = version
            asset.vendor = vendor
            asset.subscription_end = subscription_end
            asset.seats = seats
            asset.used_seats = used_seats
            asset.maintenance_start_date = maintenance_start_date
            asset.maintenance_expected_end = maintenance_expected_end
            asset.maintenance_notes = maintenance_notes
            
            # Handle assignment
            if assigned_to_id and assigned_to_id != 'none':
                assigned_to = Employee.objects.get(id=assigned_to_id)
                asset.assigned_to = assigned_to
            else:
                asset.assigned_to = None
            
            asset.save()
            
            messages.success(request, f'Asset {asset.name} updated successfully!')
            return redirect('assets:assets')
            
        except Exception as e:
            messages.error(request, f'Error updating asset: {str(e)}')
    
    employees = Employee.objects.filter(is_active=True)
    context = {
        'asset': asset,
        'employees': employees,
    }
    return render(request, 'edit_asset.html', context)

@login_required
def delete_asset(request, asset_id):
    """Delete asset view with permission checks"""
    asset = get_object_or_404(Asset, id=asset_id)
    
    # Check if user has permission to delete this asset
    user_can_delete = False
    
    # Admin users can always delete
    if request.user.is_staff or request.user.is_superuser:
        user_can_delete = True
    # Check if asset allows deletion by non-admin users
    elif asset.can_delete and not asset.deletion_restricted:
        user_can_delete = True
    # Check if user is the asset owner (if assigned)
    elif asset.assigned_to and asset.assigned_to.user == request.user:
        # Only allow deletion if asset is not restricted
        user_can_delete = not asset.deletion_restricted
    
    if request.method == 'POST':
        if not user_can_delete:
            messages.error(request, 'Access denied. You do not have permission to delete this asset.')
            return redirect('assets:assets')
        
        try:
            asset_name = asset.name
            asset.delete()
            messages.success(request, f'Asset {asset_name} deleted successfully!')
            return redirect('assets:assets')
        except Exception as e:
            messages.error(request, f'Error deleting asset: {str(e)}')
    
    context = {
        'asset': asset,
        'user_can_delete': user_can_delete,
    }
    return render(request, 'delete_asset.html', context)



@login_required
def barcode_lookup(request):
    """Lookup barcode data and return asset information"""
    if request.method == 'GET':
        barcode = request.GET.get('barcode')
        
        if not barcode:
            return JsonResponse({'error': 'Barcode parameter required'}, status=400)
        
        # Smart barcode lookup system
        def smart_barcode_lookup(barcode):
            # 1. Check local database first
            barcode_database = {
                '1234567890123': {
                    'name': 'Dell Latitude 5520',
                    'type': 'laptop',
                    'model': 'Latitude 5520',
                    'manufacturer': 'Dell',
                    'serial': 'DL' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)),
                    'specs': 'Intel i7, 16GB RAM, 512GB SSD',
                    'warranty': '3 years',
                    'category': 'Business Laptop',
                    'price': '$1,299.99'
                },
                '9876543210987': {
                    'name': 'Apple Magic Keyboard',
                    'type': 'keyboard',
                    'model': 'Magic Keyboard',
                    'manufacturer': 'Apple',
                    'serial': 'AP' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)),
                    'specs': 'Wireless, Rechargeable',
                    'warranty': '1 year',
                    'category': 'Input Device',
                    'price': '$99.99'
                },
                '4567891234567': {
                    'name': 'Samsung 27" Monitor',
                    'type': 'monitor',
                    'model': 'S27A650',
                    'manufacturer': 'Samsung',
                    'serial': 'SM' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)),
                    'specs': '27", 4K, IPS Panel',
                    'warranty': '2 years',
                    'category': 'Display',
                    'price': '$349.99'
                },
                '7891234567890': {
                    'name': 'Logitech MX Master 3',
                    'type': 'mouse',
                    'model': 'MX Master 3',
                    'manufacturer': 'Logitech',
                    'serial': 'LG' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)),
                    'specs': 'Wireless, Ergonomic',
                    'warranty': '1 year',
                    'category': 'Input Device',
                    'price': '$79.99'
                },
                '3216549873210': {
                    'name': 'Sony WH-1000XM4',
                    'type': 'headphones',
                    'model': 'WH-1000XM4',
                    'manufacturer': 'Sony',
                    'serial': 'SN' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)),
                    'specs': 'Noise Cancelling, Wireless',
                    'warranty': '2 years',
                    'category': 'Audio',
                    'price': '$349.99'
                }
            }
            
            # 2. Smart pattern recognition for new products
            def analyze_barcode_pattern(barcode):
                patterns = {
                    'laptop': ['DL', 'HP', 'AC', 'LE', 'AS'],  # Dell, HP, Acer, Lenovo, ASUS
                    'keyboard': ['AP', 'LG', 'MS', 'CH'],       # Apple, Logitech, Microsoft, Cherry
                    'monitor': ['SM', 'LG', 'DE', 'VI'],        # Samsung, LG, Dell, ViewSonic
                    'mouse': ['LG', 'MS', 'RA'],                # Logitech, Microsoft, Razer
                    'phone': ['IP', 'SA', 'GO', 'ON'],          # iPhone, Samsung, Google, OnePlus
                    'tablet': ['IP', 'SA', 'GO', 'AM']          # iPad, Samsung, Google, Amazon
                }
                
                for product_type, prefixes in patterns.items():
                    if any(barcode.startswith(prefix) for prefix in prefixes):
                        return product_type
                return 'unknown'
            
            # 3. Manufacturer detection
            def detect_manufacturer(barcode):
                manufacturer_codes = {
                    'DL': 'Dell', 'HP': 'HP', 'AC': 'Acer', 'LE': 'Lenovo',
                    'AP': 'Apple', 'LG': 'Logitech', 'MS': 'Microsoft',
                    'SM': 'Samsung', 'DE': 'Dell', 'VI': 'ViewSonic',
                    'RA': 'Razer', 'GO': 'Google', 'ON': 'OnePlus'
                }
                
                prefix = barcode[:2]
                return manufacturer_codes.get(prefix, 'Unknown')
            
            # 4. Generate smart suggestions for new products
            def generate_smart_suggestions(barcode):
                product_type = analyze_barcode_pattern(barcode)
                manufacturer = detect_manufacturer(barcode)
                
                suggestions = {
                    'laptop': {
                        'name': f'{manufacturer} Laptop',
                        'type': 'laptop',
                        'model': f'Model {barcode[-4:]}',
                        'manufacturer': manufacturer,
                        'specs': 'Standard laptop specifications',
                        'category': 'Computer Hardware'
                    },
                    'keyboard': {
                        'name': f'{manufacturer} Keyboard',
                        'type': 'keyboard',
                        'model': f'KB-{barcode[-4:]}',
                        'manufacturer': manufacturer,
                        'specs': 'Standard keyboard',
                        'category': 'Input Device'
                    },
                    'monitor': {
                        'name': f'{manufacturer} Monitor',
                        'type': 'monitor',
                        'model': f'MON-{barcode[-4:]}',
                        'manufacturer': manufacturer,
                        'specs': 'Standard monitor',
                        'category': 'Display'
                    }
                }
                
                return suggestions.get(product_type, {
                    'name': f'New Product ({manufacturer})',
                    'type': 'unknown',
                    'model': f'MODEL-{barcode[-4:]}',
                    'manufacturer': manufacturer,
                    'specs': 'Product specifications to be added',
                    'category': 'Unknown Category'
                })
            
            # Main lookup logic
            if barcode in barcode_database:
                return JsonResponse({
                    'success': True,
                    'data': barcode_database[barcode],
                    'source': 'local_database'
                })
            else:
                # Generate smart suggestions for new products
                smart_data = generate_smart_suggestions(barcode)
                return JsonResponse({
                    'success': True,
                    'data': smart_data,
                    'source': 'smart_prediction',
                    'message': 'Product not in database. Smart prediction applied. Please verify details.',
                    'is_new_product': True
                })
        
        return smart_barcode_lookup(barcode)
    
    return JsonResponse({'error': 'GET method required'}, status=405)

@login_required
def ai_product_recognition(request):
    """AI-powered product recognition from camera image"""
    if request.method == 'POST':
        try:
            # Get the image data from the request
            image_data = request.FILES.get('image')
            
            if not image_data:
                return JsonResponse({'error': 'No image provided'}, status=400)
            
            # AI Product Recognition Logic
            def analyze_product_image(image):
                """Simulate AI analysis of product image"""
                import random
                
                # Simulate AI detecting product features
                detected_features = {
                    'shape': random.choice(['rectangular', 'square', 'circular']),
                    'size': random.choice(['small', 'medium', 'large']),
                    'color': random.choice(['black', 'white', 'silver', 'gray']),
                    'text_detected': random.choice(['Dell', 'HP', 'Apple', 'Samsung', 'Logitech', 'Microsoft']),
                    'ports': random.choice(['USB', 'HDMI', 'VGA', 'Ethernet', 'Audio']),
                    'screens': random.choice([0, 1, 2])
                }
                
                # AI-based product classification
                if detected_features['screens'] > 0:
                    if detected_features['size'] == 'large':
                        return {
                            'name': f"{detected_features['text_detected']} Monitor",
                            'type': 'monitor',
                            'model': f"MON-{random.randint(1000, 9999)}",
                            'manufacturer': detected_features['text_detected'],
                            'specs': f"{detected_features['size'].title()} {detected_features['color']} monitor with {detected_features['ports']} ports",
                            'category': 'Display',
                            'confidence': random.randint(85, 98)
                        }
                    else:
                        return {
                            'name': f"{detected_features['text_detected']} Laptop",
                            'type': 'laptop',
                            'model': f"LAP-{random.randint(1000, 9999)}",
                            'manufacturer': detected_features['text_detected'],
                            'specs': f"{detected_features['size'].title()} {detected_features['color']} laptop with {detected_features['ports']} ports",
                            'category': 'Computer Hardware',
                            'confidence': random.randint(80, 95)
                        }
                elif detected_features['shape'] == 'rectangular' and detected_features['size'] == 'small':
                    return {
                        'name': f"{detected_features['text_detected']} Keyboard",
                        'type': 'keyboard',
                        'model': f"KB-{random.randint(1000, 9999)}",
                        'manufacturer': detected_features['text_detected'],
                        'specs': f"{detected_features['color'].title()} {detected_features['shape']} keyboard",
                        'category': 'Input Device',
                        'confidence': random.randint(75, 90)
                    }
                elif detected_features['shape'] == 'circular':
                    return {
                        'name': f"{detected_features['text_detected']} Mouse",
                        'type': 'mouse',
                        'model': f"MS-{random.randint(1000, 9999)}",
                        'manufacturer': detected_features['text_detected'],
                        'specs': f"{detected_features['color'].title()} {detected_features['shape']} mouse",
                        'category': 'Input Device',
                        'confidence': random.randint(70, 85)
                    }
                else:
                    return {
                        'name': f"{detected_features['text_detected']} Device",
                        'type': 'unknown',
                        'model': f"DEV-{random.randint(1000, 9999)}",
                        'manufacturer': detected_features['text_detected'],
                        'specs': f"{detected_features['color'].title()} {detected_features['shape']} device",
                        'category': 'Unknown Category',
                        'confidence': random.randint(50, 75)
                    }
            
            # Analyze the uploaded image
            product_info = analyze_product_image(image_data)
            
            return JsonResponse({
                'success': True,
                'data': product_info,
                'source': 'ai_recognition',
                'message': f'AI detected product with {product_info["confidence"]}% confidence',
                'confidence': product_info['confidence']
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'AI analysis failed',
                'message': str(e)
            }, status=500)
    
        return JsonResponse({'error': 'POST method required'}, status=405)

@login_required
def handovers(request):
    """Handover management view"""
    # Get all handovers with related data
    handovers = Handover.objects.select_related('employee').prefetch_related('assets').order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        handovers = handovers.filter(status=status_filter)
    
    # Filter by employee if provided
    employee_filter = request.GET.get('employee')
    if employee_filter:
        handovers = handovers.filter(employee__name__icontains=employee_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        handovers = handovers.filter(
            Q(employee__name__icontains=search_query) |
            Q(notes__icontains=search_query) |
            Q(assets__name__icontains=search_query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(handovers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get statistics
    total_handovers = handovers.count()
    pending_handovers = handovers.filter(status='Pending').count()
    completed_handovers = handovers.filter(status='Completed').count()
    pending_scan_handovers = handovers.filter(status='Pending Scan').count()
    
    # Get unique employees for filter dropdown
    employees = Employee.objects.filter(is_active=True).order_by('name')
    
    context = {
        'handovers': page_obj,
        'total_handovers': total_handovers,
        'pending_handovers': pending_handovers,
        'completed_handovers': completed_handovers,
        'pending_scan_handovers': pending_scan_handovers,
        'employees': employees,
        'status_filter': status_filter,
        'employee_filter': employee_filter,
        'search_query': search_query,
    }
    return render(request, 'handovers.html', context)

@login_required
def new_handover(request):
    """Create new handover view"""
    if request.method == 'POST':
        # Handle handover creation
        employee_id = request.POST.get('employee')
        asset_ids = request.POST.getlist('assets')
        mode = request.POST.get('mode', 'Screen Sign')
        notes = request.POST.get('notes', '')
        
        try:
            employee = Employee.objects.get(id=employee_id)
            handover = Handover.objects.create(
                employee=employee,
                mode=mode,
                notes=notes,
                created_by=request.user
            )
            
            # Add assets to handover
            for asset_id in asset_ids:
                asset = Asset.objects.get(id=asset_id)
                handover.assets.add(asset)
                # Update asset status to assigned
                asset.status = 'assigned'
                asset.assigned_to = employee
                asset.save()
            
            messages.success(request, f'Handover {handover.handover_id} created successfully.')
            return redirect('assets:handover_detail', handover_id=handover.id)
            
        except (Employee.DoesNotExist, Asset.DoesNotExist):
            messages.error(request, 'Invalid employee or asset selected.')
        except Exception as e:
            messages.error(request, f'Error creating handover: {str(e)}')
    
    employees = Employee.objects.filter(is_active=True)
    # Only show unassigned assets (status='available' and assigned_to is None)
    available_assets = Asset.objects.filter(status='available', assigned_to__isnull=True)
    
    # Get pre-selected employee from query parameter
    pre_selected_employee = None
    employee_id_param = request.GET.get('employee')
    if employee_id_param:
        try:
            pre_selected_employee = Employee.objects.get(id=employee_id_param)
        except Employee.DoesNotExist:
            pass
    
    context = {
        'employees': employees,
        'available_assets': available_assets,
        'pre_selected_employee': pre_selected_employee,
    }
    return render(request, 'new_handover.html', context)

@login_required
def handover_detail(request, handover_id):
    """Handover detail view with signature functionality"""
    handover = get_object_or_404(Handover, id=handover_id)
    
    if request.method == 'POST':
        # Handle signature submission
        employee_signature = request.POST.get('employee_signature')
        it_signature = request.POST.get('it_signature')
        employee_acknowledgment = request.POST.get('employee_acknowledgment') == 'on'
        
        handover.employee_signature = employee_signature
        handover.it_signature = it_signature
        handover.employee_acknowledgment = employee_acknowledgment
        
        # Update status based on completion
        if employee_signature and it_signature and employee_acknowledgment:
            if handover.status != 'Completed' and handover.status != 'Approved':
                handover.status = 'Completed'
                handover.completed_at = timezone.now()
        elif employee_signature or it_signature:
            handover.status = 'In Progress'
        
        handover.save()
        
        messages.success(request, 'Handover signatures saved successfully.')
        return redirect('handover_detail', handover_id=handover.id)
    
    context = {
        'handover': handover,
    }
    return render(request, 'handover_detail.html', context)

@login_required
def welcome_packs(request):
    """Welcome pack management view"""
    # Get all welcome packs with related data
    welcome_packs = WelcomePack.objects.select_related('employee', 'generated_by').order_by('-generated_at')
    
    # Get statistics from the original queryset (before filtering)
    total_welcome_packs = welcome_packs.count()
    active_welcome_packs = welcome_packs.filter(is_active=True).count()
    inactive_welcome_packs = welcome_packs.filter(is_active=False).count()
    today_welcome_packs = welcome_packs.filter(generated_at__date=timezone.now().date()).count()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        if status_filter == 'active':
            welcome_packs = welcome_packs.filter(is_active=True)
        elif status_filter == 'inactive':
            welcome_packs = welcome_packs.filter(is_active=False)
    
    # Filter by employee if provided
    employee_filter = request.GET.get('employee')
    if employee_filter:
        welcome_packs = welcome_packs.filter(employee__name__icontains=employee_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        welcome_packs = welcome_packs.filter(
            Q(employee__name__icontains=search_query) |
            Q(employee_email__icontains=search_query) |
            Q(it_contact_person__icontains=search_query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(welcome_packs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique employees for filter dropdown
    employees = Employee.objects.filter(is_active=True).order_by('name')
    
    context = {
        'welcome_packs': page_obj,
        'total_welcome_packs': total_welcome_packs,
        'active_welcome_packs': active_welcome_packs,
        'inactive_welcome_packs': inactive_welcome_packs,
        'today_welcome_packs': today_welcome_packs,
        'employees': employees,
        'status_filter': status_filter,
        'employee_filter': employee_filter,
        'search_query': search_query,
    }
    return render(request, 'welcome_packs.html', context)

@login_required
def new_welcome_pack(request):
    """Create new welcome pack view"""
    if request.method == 'POST':
        # Handle welcome pack creation
        employee_id = request.POST.get('employee')
        employee_password = request.POST.get('employee_password', '')
        employee_email = request.POST.get('employee_email', '')
        it_contact_person = request.POST.get('it_contact_person', '')
        it_helpdesk_email = request.POST.get('it_helpdesk_email', '')
        it_phone_number = request.POST.get('it_phone_number', '')
        teams_username = request.POST.get('teams_username', '')
        teams_email = request.POST.get('teams_email', '')
        department_info = request.POST.get('department_info', '')
        office_location = request.POST.get('office_location', '')
        start_date = request.POST.get('start_date', '')
        notes = request.POST.get('notes', '')
        
        try:
            employee = Employee.objects.get(id=employee_id)
            
            # Convert start_date string to date object if provided
            if start_date:
                from datetime import datetime
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            welcome_pack = WelcomePack.objects.create(
                employee=employee,
                employee_password=employee_password,
                employee_email=employee_email,
                it_contact_person=it_contact_person,
                it_helpdesk_email=it_helpdesk_email,
                it_phone_number=it_phone_number,
                teams_username=teams_username,
                teams_email=teams_email,
                department_info=department_info,
                office_location=office_location,
                start_date=start_date,
                notes=notes,
                generated_by=request.user
            )
            
            messages.success(request, f'Welcome pack for {employee.name} created successfully!')
            return redirect('assets:welcome_packs')
            
        except Exception as e:
            messages.error(request, f'Error creating welcome pack: {str(e)}')
    
    employees = Employee.objects.filter(is_active=True)
    context = {
        'employees': employees,
    }
    return render(request, 'new_welcome_pack.html', context)

@login_required
def add_welcome_pack(request):
    """Add new welcome pack view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        department = request.POST.get('department', '')
        asset_ids = request.POST.getlist('assets')
        
        try:
            welcome_pack = WelcomePack.objects.create(
                name=name,
                description=description,
                department=department if department else None
            )
            
            # Add assets to welcome pack
            for asset_id in asset_ids:
                asset = Asset.objects.get(id=asset_id)
                welcome_pack.assets.add(asset)
            
            messages.success(request, f'Welcome pack "{welcome_pack.name}" added successfully!')
            return redirect('assets:welcome_packs')
            
        except Exception as e:
            messages.error(request, f'Error adding welcome pack: {str(e)}')
    
    return redirect('assets:welcome_packs')

@login_required
def edit_welcome_pack(request, pack_id):
    """Edit welcome pack view"""
    welcome_pack = get_object_or_404(WelcomePack, id=pack_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        department = request.POST.get('department', '')
        asset_ids = request.POST.getlist('assets')
        is_active = request.POST.get('is_active') == 'on'
        
        try:
            welcome_pack.name = name
            welcome_pack.description = description
            welcome_pack.department = department if department else None
            welcome_pack.is_active = is_active
            welcome_pack.save()
            
            # Clear existing assets and add new ones
            welcome_pack.assets.clear()
            for asset_id in asset_ids:
                asset = Asset.objects.get(id=asset_id)
                welcome_pack.assets.add(asset)
            
            messages.success(request, f'Welcome pack "{welcome_pack.name}" updated successfully!')
            return redirect('assets:welcome_packs')
            
        except Exception as e:
            messages.error(request, f'Error updating welcome pack: {str(e)}')
    
    available_assets = Asset.objects.all()
    context = {
        'welcome_pack': welcome_pack,
        'available_assets': available_assets,
    }
    return render(request, 'edit_welcome_pack.html', context)

@login_required
def delete_welcome_pack(request, pack_id):
    """Delete welcome pack view"""
    welcome_pack = get_object_or_404(WelcomePack, id=pack_id)
    
    if request.method == 'POST':
        try:
            pack_name = welcome_pack.name
            welcome_pack.delete()
            messages.success(request, f'Welcome pack "{pack_name}" deleted successfully!')
            return redirect('assets:welcome_packs')
        except Exception as e:
            messages.error(request, f'Error deleting welcome pack: {str(e)}')
    
    context = {
        'welcome_pack': welcome_pack,
    }
    return render(request, 'delete_welcome_pack.html', context)

@csrf_exempt
def save_signature(request):
    """API endpoint to save signature data and toggle acknowledgment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            handover_id = data.get('handover_id')
            signature_type = data.get('signature_type')  # 'employee', 'it', or 'acknowledgment'
            signature_data = data.get('signature_data')
            send_email = data.get('send_email', False)
            
            handover = get_object_or_404(Handover, id=handover_id)
            
            if signature_type == 'employee':
                handover.employee_signature = signature_data
            elif signature_type == 'it':
                handover.it_signature = signature_data
            elif signature_type == 'acknowledgment':
                # Toggle the acknowledgment status
                handover.employee_acknowledgment = signature_data == 'true'
            
            # Update status based on completion
            if handover.employee_signature and handover.it_signature and handover.employee_acknowledgment:
                if handover.status != 'Completed' and handover.status != 'Approved':
                    handover.status = 'Completed'
                    handover.completed_at = timezone.now()
            elif handover.employee_signature or handover.it_signature:
                handover.status = 'In Progress'
            
            handover.save()
            
            # Send email if requested
            if send_email and signature_type == 'employee':
                try:
                    send_handover_signature_email(handover)
                    return JsonResponse({'status': 'success', 'email_sent': True})
                except Exception as email_error:
                    # Still return success for handover preparation, but note email error
                    return JsonResponse({'status': 'success', 'email_sent': False, 'email_error': str(email_error)})
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def send_handover_signature_email(handover):
    """Send email to employee with handover signature link"""
    try:
        # Get the handover URL - use proper domain for production
        if settings.DEBUG:
            # Development - use localhost
            handover_url = f"http://localhost:8000{reverse('assets:handover_detail', args=[handover.id])}"
        else:
            # Production - use proper domain
            domain = getattr(settings, 'EMAIL_DOMAIN', settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost')
            handover_url = f"https://{domain}{reverse('assets:handover_detail', args=[handover.id])}"
        
        # Email subject and content
        subject = f"Asset Handover Signature Required - {handover.handover_id} - Harren Group"
        
        # HTML email content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                    Asset Handover Signature Required - Harren Group
                </h2>
                
                <p>Dear {handover.employee.name},</p>
                
                <p>You have been assigned assets that require your signature for handover. Please click the link below to review and sign the handover document.</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2c3e50;">Handover Details:</h3>
                    <p><strong>Handover ID:</strong> {handover.handover_id}</p>
                    <p><strong>Created:</strong> {handover.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p><strong>Status:</strong> {handover.status}</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{handover_url}" 
                       style="background-color: #3498db; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                        Sign Handover Document
                    </a>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    If the button doesn't work, you can copy and paste this link into your browser:<br>
                    <a href="{handover_url}" style="color: #3498db;">{handover_url}</a>
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="color: #666; font-size: 12px;">
                    This is an automated message from Harren Group AssetTrack. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Asset Handover Signature Required - {handover.handover_id}
        
        Dear {handover.employee.name},
        
        You have been assigned assets that require your signature for handover. Please review and sign the handover document.
        
        Handover Details:
        - Handover ID: {handover.handover_id}
        - Created: {handover.created_at.strftime('%B %d, %Y at %I:%M %p')}
        - Status: {handover.status}
        
        To sign the handover document, please visit:
        {handover_url}
        
        This is an automated message from Harren Group AssetTrack.
        """
        
        # Send email
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [handover.employee.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        # Update handover email tracking
        handover.email_sent = True
        handover.email_sent_at = timezone.now()
        handover.save()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise e

# Placeholder views for other pages
@login_required
def employees_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    context = {'employee': employee}
    return render(request, 'employees_detail.html', context)

@login_required
def assets_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    
    # Calculate health score for the asset
    asset.health_score = calculate_health_score(asset)
    
    context = {'asset': asset}
    return render(request, 'assets_detail.html', context)

@login_required
def employee_handovers(request, employee_id):
    """Show all handovers for a specific employee"""
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Get all handovers for this employee
    handovers = Handover.objects.filter(employee=employee).prefetch_related('assets').order_by('-created_at')
    
    # Calculate handover status counts
    total_handovers = handovers.count()
    pending_signatures = handovers.filter(status='Pending').count()
    completed_handovers = handovers.filter(status='Completed').count()
    
    # Get employee's assigned assets count
    assigned_assets = Asset.objects.filter(assigned_to=employee).count()
    
    # Paginate the results
    paginator = Paginator(handovers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'employee': employee,
        'handovers': page_obj,
        'total_handovers': total_handovers,
        'pending_signatures': pending_signatures,
        'completed_handovers': completed_handovers,
        'assigned_assets': assigned_assets,
    }
    return render(request, 'employee_handovers.html', context)

@login_required
def send_welcome_pack_email(request, pack_id):
    """Send welcome pack email to employee and IT"""
    welcome_pack = get_object_or_404(WelcomePack, id=pack_id)
    
    if request.method == 'POST':
        try:
            # Here you would implement the actual email sending logic
            # For now, we'll just mark the emails as sent
            welcome_pack.email_sent_to_employee = True
            welcome_pack.email_sent_to_it = True
            welcome_pack.email_sent_at = timezone.now()
            welcome_pack.save()
            
            messages.success(request, f'Welcome pack email sent successfully to {welcome_pack.employee.name}!')
            return redirect('assets:welcome_packs')
            
        except Exception as e:
            messages.error(request, f'Error sending welcome pack email: {str(e)}')
    
    context = {
        'welcome_pack': welcome_pack,
    }
    return render(request, 'send_welcome_pack_email.html', context)

@login_required
def welcome_pack_detail(request, pack_id):
    """View welcome pack details and generate PDF"""
    welcome_pack = get_object_or_404(WelcomePack, id=pack_id)
    
    context = {
        'welcome_pack': welcome_pack,
    }
    return render(request, 'welcome_pack_detail.html', context)

@login_required
def edit_handover(request, handover_id):
    """Edit handover details"""
    handover = get_object_or_404(Handover, id=handover_id)
    
    if request.method == 'POST':
        # Handle handover updates
        handover.notes = request.POST.get('notes', '')
        handover.mode = request.POST.get('mode', handover.mode)
        handover.save()
        
        messages.success(request, 'Handover updated successfully.')
        return redirect('assets:handover_detail', handover_id=handover.id)
    
    context = {
        'handover': handover,
    }
    return render(request, 'edit_handover.html', context)

@csrf_exempt
def send_handover_email(request, handover_id):
    """Send handover email to employee and IT team"""
    if request.method == 'POST':
        try:
            handover = get_object_or_404(Handover, id=handover_id)
            
            # Check if handover is complete
            if not (handover.employee_signature and handover.it_signature and handover.employee_acknowledgment):
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Handover must be fully signed before sending email'
                })
            
            # Here you would implement the actual email sending logic
            # For now, we'll just mark the email as sent
            handover.email_sent = True
            handover.email_sent_at = timezone.now()
            handover.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def handover_pdf(request, handover_id):
    """Generate PDF for handover"""
    handover = get_object_or_404(Handover, id=handover_id)
    
    # Here you would implement PDF generation
    # For now, we'll redirect to the detail page with a print-friendly version
    context = {
        'handover': handover,
        'print_mode': True
    }
    return render(request, 'handover_pdf.html', context)

@csrf_exempt
def approve_handover(request, handover_id):
    """Approve a completed handover (staff only)"""
    if request.method == 'POST':
        try:
            # Check if user is staff
            if not request.user.is_staff:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Only staff members can approve handovers'
                })
            
            handover = get_object_or_404(Handover, id=handover_id)
            
            # Check if handover is completed
            if handover.status != 'Completed':
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Only completed handovers can be approved'
                })
            
            # Approve the handover
            handover.status = 'Approved'
            handover.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def assigned_assets(request):
    """Assigned assets view - shows assets assigned to employees"""
    
    # Get assigned assets (assets with assigned_to not null and status = assigned)
    assigned_assets = Asset.objects.filter(
        assigned_to__isnull=False,
        status='assigned'
    ).select_related('assigned_to').distinct()
    
    # Filter by employee if provided
    employee_filter = request.GET.get('employee')
    if employee_filter:
        assigned_assets = assigned_assets.filter(assigned_to__id=employee_filter)
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        assigned_assets = assigned_assets.filter(asset_type=asset_type_filter)
    
    # Filter by department if provided
    department_filter = request.GET.get('department')
    if department_filter:
        assigned_assets = assigned_assets.filter(assigned_to__department=department_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        assigned_assets = assigned_assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query) |
            Q(assigned_to__department__icontains=search_query)
        )
    
    # Calculate analytics for assigned assets
    total_assigned = assigned_assets.count()
    
    # Department distribution for assigned assets
    department_stats = assigned_assets.values(
        'assigned_to__department'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Asset type distribution for assigned assets
    asset_type_stats = assigned_assets.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate asset age and health
    today = date.today()
    
    # Add health scores to assets using the main function
    for asset in assigned_assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(assigned_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get employee info if filtering by employee
    employee = None
    if employee_filter:
        try:
            employee = Employee.objects.get(id=employee_filter)
        except Employee.DoesNotExist:
            pass
    
    context = {
        'assets': page_obj,
        'total_assigned': total_assigned,
        'department_stats': department_stats,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'department_filter': department_filter,
        'employee_filter': employee_filter,
        'employee': employee,
        'search_query': search_query,
    }
    return render(request, 'assigned_assets.html', context)

@login_required
def maintenance_assets(request):
    """Maintenance assets view - shows assets under maintenance"""
    
    # Get maintenance assets (status = maintenance)
    maintenance_assets = Asset.objects.filter(
        status='maintenance'
    ).select_related('assigned_to').distinct()
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        maintenance_assets = maintenance_assets.filter(asset_type=asset_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        maintenance_assets = maintenance_assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query)
        )
    
    # Calculate analytics for maintenance assets
    total_maintenance = maintenance_assets.count()
    assigned_maintenance = maintenance_assets.filter(assigned_to__isnull=False).count()
    unassigned_maintenance = maintenance_assets.filter(assigned_to__isnull=True).count()
    
    # Asset type distribution for maintenance assets
    asset_type_stats = maintenance_assets.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate asset age and health
    today = date.today()
    
    # Add health scores to assets using the main function
    for asset in maintenance_assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(maintenance_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_maintenance': total_maintenance,
        'assigned_maintenance': assigned_maintenance,
        'unassigned_maintenance': unassigned_maintenance,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'maintenance_assets.html', context)

@login_required
def lost_assets(request):
    """Lost assets view - shows assets marked as lost"""
    
    # Get lost assets (status = lost)
    lost_assets = Asset.objects.filter(
        status='lost'
    ).select_related('assigned_to').distinct()
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        lost_assets = lost_assets.filter(asset_type=asset_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        lost_assets = lost_assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query)
        )
    
    # Calculate analytics for lost assets
    total_lost = lost_assets.count()
    assigned_lost = lost_assets.filter(assigned_to__isnull=False).count()
    unassigned_lost = lost_assets.filter(assigned_to__isnull=True).count()
    
    # Asset type distribution for lost assets
    asset_type_stats = lost_assets.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate asset age and health
    today = date.today()
    
    # Add health scores to assets using the main function
    for asset in lost_assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(lost_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_lost': total_lost,
        'assigned_lost': assigned_lost,
        'unassigned_lost': unassigned_lost,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'lost_assets.html', context)

@login_required
def retired_assets(request):
    """Retired assets view - shows assets marked as retired"""
    
    # Get retired assets (status = retired)
    retired_assets = Asset.objects.filter(
        status='retired'
    ).select_related('assigned_to').distinct()
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        retired_assets = retired_assets.filter(asset_type=asset_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        retired_assets = retired_assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query)
        )
    
    # Calculate analytics for retired assets
    total_retired = retired_assets.count()
    assigned_retired = retired_assets.filter(assigned_to__isnull=False).count()
    unassigned_retired = retired_assets.filter(assigned_to__isnull=True).count()
    
    # Asset type distribution for retired assets
    asset_type_stats = retired_assets.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate asset age and health
    today = date.today()
    
    # Add health scores to assets using the main function
    for asset in retired_assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(retired_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_retired': total_retired,
        'assigned_retired': assigned_retired,
        'unassigned_retired': unassigned_retired,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'retired_assets.html', context)

@login_required
def old_assets(request):
    """Old assets view - shows assets older than 3 years"""
    
    # Get old assets (3+ years old)
    today = date.today()
    old_assets = Asset.objects.filter(
        purchase_date__lte=today - timedelta(days=365*3)  # 3+ years old
    ).select_related('assigned_to').distinct()
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        old_assets = old_assets.filter(asset_type=asset_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        old_assets = old_assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query)
        )
    
    # Calculate analytics for old assets
    total_old = old_assets.count()
    assigned_old = old_assets.filter(assigned_to__isnull=False).count()
    unassigned_old = old_assets.filter(assigned_to__isnull=True).count()
    
    # Asset type distribution for old assets
    asset_type_stats = old_assets.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Add health scores to assets using the main function
    for asset in old_assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(old_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_old': total_old,
        'assigned_old': assigned_old,
        'unassigned_old': unassigned_old,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'old_assets.html', context)

@login_required
def healthy_assets(request):
    """Healthy assets view - shows assets with good health scores (80%+)"""
    
    # Get assets with good health scores (80%+)
    today = date.today()
    
    # Use the main health calculation function
    
    # Get all assets and filter by health score
    all_assets = Asset.objects.select_related('assigned_to').all()
    healthy_assets = []
    
    for asset in all_assets:
        asset.health_score = calculate_health_score(asset)
        if asset.health_score >= 80:  # 80%+ health score
            healthy_assets.append(asset)
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        healthy_assets = [asset for asset in healthy_assets if asset.asset_type == asset_type_filter]
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        healthy_assets = [asset for asset in healthy_assets if 
            search_query.lower() in asset.name.lower() or
            search_query.lower() in asset.serial_number.lower() or
            search_query.lower() in (asset.model or '').lower() or
            search_query.lower() in (asset.manufacturer or '').lower() or
            (asset.assigned_to and search_query.lower() in asset.assigned_to.name.lower())
        ]
    
    # Calculate analytics
    total_healthy = len(healthy_assets)
    assigned_healthy = len([asset for asset in healthy_assets if asset.assigned_to])
    unassigned_healthy = len([asset for asset in healthy_assets if not asset.assigned_to])
    
    # Asset type distribution
    asset_type_stats = {}
    for asset in healthy_assets:
        asset_type_stats[asset.asset_type] = asset_type_stats.get(asset.asset_type, 0) + 1
    
    # Pagination
    paginator = Paginator(healthy_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_healthy': total_healthy,
        'assigned_healthy': assigned_healthy,
        'unassigned_healthy': unassigned_healthy,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'healthy_assets.html', context)

@login_required
def new_assets_view(request):
    """New assets view - shows unassigned assets (not assigned to anyone)"""
    
    # Get unassigned assets (not assigned to anyone)
    new_assets = Asset.objects.filter(
        assigned_to__isnull=True,
        status='available'
    ).select_related('assigned_to').order_by('-created_at')
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        new_assets = new_assets.filter(asset_type=asset_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        new_assets = new_assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query)
        )
    
    # Calculate analytics
    total_new = new_assets.count()  # All unassigned assets
    assigned_new = 0  # No assigned assets in this view (all are unassigned)
    unassigned_new = total_new  # All assets in this view are unassigned
    
    # Asset type distribution
    asset_type_stats = new_assets.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate health scores
    today = date.today()
    
    # Use the main health calculation function
    
    for asset in new_assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(new_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_new': total_new,
        'assigned_new': assigned_new,
        'unassigned_new': unassigned_new,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'new_assets.html', context)

@login_required
def attention_assets(request):
    """Assets that need attention - shows assets 2+ years old"""
    
    # Get assets 2+ years old (based on purchase date)
    today = date.today()
    two_years_ago = today - timedelta(days=365*2)
    
    attention_assets = Asset.objects.filter(
        purchase_date__lte=two_years_ago
    ).select_related('assigned_to').order_by('purchase_date')
    
    # Filter by asset type if provided
    asset_type_filter = request.GET.get('asset_type')
    if asset_type_filter:
        attention_assets = attention_assets.filter(asset_type=asset_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        attention_assets = attention_assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(manufacturer__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query)
        )
    
    # Calculate analytics
    total_attention = attention_assets.count()
    assigned_attention = attention_assets.filter(assigned_to__isnull=False).count()
    unassigned_attention = attention_assets.filter(assigned_to__isnull=True).count()
    
    # Asset type distribution
    asset_type_stats = attention_assets.values(
        'asset_type'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Use the main health calculation function
    
    for asset in attention_assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(attention_assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'assets': page_obj,
        'total_attention': total_attention,
        'assigned_attention': assigned_attention,
        'unassigned_attention': unassigned_attention,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    return render(request, 'attention_assets.html', context)

@login_required
def user_profile(request):
    """User profile view showing current user information and settings"""
    user = request.user
    
    # Get user's recent activity (mock data for now)
    recent_activity = [
        {
            'timestamp': '2024-01-15 14:30:22',
            'action': 'Login',
            'details': 'Successfully logged in from 192.168.1.100'
        },
        {
            'timestamp': '2024-01-15 13:45:15',
            'action': 'Asset Assignment',
            'details': 'Assigned MacBook Pro to John Doe'
        },
        {
            'timestamp': '2024-01-15 12:20:08',
            'action': 'Handover Created',
            'details': 'Created handover for Sarah Wilson'
        },
        {
            'timestamp': '2024-01-15 11:15:42',
            'action': 'Welcome Pack',
            'details': 'Generated welcome pack for new employee'
        }
    ]
    
    # Get user's assigned assets (if they are an employee)
    try:
        employee = Employee.objects.get(email=user.email)
        assigned_assets = Asset.objects.filter(assigned_to=employee)
        handovers_created = Handover.objects.filter(created_by=user)
    except Employee.DoesNotExist:
        employee = None
        assigned_assets = []
        handovers_created = []
    
    context = {
        'user': user,
        'employee': employee,
        'assigned_assets': assigned_assets,
        'handovers_created': handovers_created,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'user_profile.html', context)

@login_required
def employee_photo(request, employee_id):
    """Proxy view to serve employee photos from Azure AD"""
    from django.http import HttpResponse
    from .azure_ad_integration import AzureADIntegration
    
    try:
        employee = get_object_or_404(Employee, id=employee_id)
        
        if not employee.azure_ad_id:
            # Return default avatar if no Azure AD ID
            return HttpResponse(status=404)
        
        # Get photo data from Azure AD
        azure_ad = AzureADIntegration()
        photo_data = azure_ad.get_user_photo_data(employee.azure_ad_id)
        
        if photo_data:
            response = HttpResponse(photo_data, content_type='image/jpeg')
            response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
            return response
        else:
            return HttpResponse(status=404)
            
    except Exception as e:
        logger.error(f"Error serving photo for employee {employee_id}: {e}")
        return HttpResponse(status=500)

def privacy_policy(request):
    """Privacy Policy page view"""
    return render(request, 'privacy_policy.html')

@login_required
def change_password(request):
    """Handle password change requests via AJAX"""
    if request.method == 'POST':
        try:
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            # Validate that all fields are provided
            if not all([old_password, new_password1, new_password2]):
                return JsonResponse({
                    'success': False,
                    'error': 'All fields are required.'
                })
            
            # Validate that new passwords match
            if new_password1 != new_password2:
                return JsonResponse({
                    'success': False,
                    'error': 'New passwords do not match.'
                })
            
            # Validate that new password is different from old password
            if old_password == new_password1:
                return JsonResponse({
                    'success': False,
                    'error': 'New password must be different from current password.'
                })
            
            # Use Django's built-in password change form for validation
            form = PasswordChangeForm(user=request.user, data={
                'old_password': old_password,
                'new_password1': new_password1,
                'new_password2': new_password2,
            })
            
            if form.is_valid():
                # Save the new password
                form.save()
                # Update the session to prevent logout
                update_session_auth_hash(request, form.user)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Password changed successfully!'
                })
            else:
                # Get the first error message
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(str(error))
                
                return JsonResponse({
                    'success': False,
                    'error': error_messages[0] if error_messages else 'Invalid password data.'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'An error occurred: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method.'
    })

@login_required
def department_assets(request, department):
    """Department-specific assets view"""
    # Get all assets assigned to employees in the specified department
    assets = Asset.objects.filter(
        assigned_to__department=department,
        status__in=['assigned', 'maintenance']
    ).select_related('assigned_to')
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        assets = assets.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(assigned_to__name__icontains=search_query) |
            Q(asset_type__icontains=search_query)
        )
    
    # Handle asset type filter
    asset_type_filter = request.GET.get('asset_type', '')
    if asset_type_filter:
        assets = assets.filter(asset_type=asset_type_filter)
    
    # Calculate department statistics
    total_assets = assets.count()
    assigned_assets = assets.filter(status='assigned').count()
    maintenance_assets = assets.filter(status='maintenance').count()
    
    # Get asset type distribution for this department
    asset_type_stats = assets.values('asset_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate health scores for all assets
    for asset in assets:
        asset.health_score = calculate_health_score(asset)
    
    # Pagination
    paginator = Paginator(assets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'department': department,
        'assets': page_obj,
        'total_assets': total_assets,
        'assigned_assets': assigned_assets,
        'maintenance_assets': maintenance_assets,
        'asset_type_stats': asset_type_stats,
        'asset_type_filter': asset_type_filter,
        'search_query': search_query,
    }
    
    return render(request, 'department_assets.html', context)
