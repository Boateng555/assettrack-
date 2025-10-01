from django import template
from django.urls import reverse
from assets.models import Employee
from datetime import date

register = template.Library()

@register.filter
def employee_avatar_url(employee):
    """
    Get the appropriate avatar URL for an employee.
    Always returns a working, professional avatar URL.
    """
    if not employee:
        return get_professional_avatar_url(employee)
    
    # Priority 1: Use stored professional avatar if available
    if employee.avatar_url and 'dicebear.com' in employee.avatar_url:
        return employee.avatar_url
    
    # Priority 2: Use stored non-generic avatar if available
    if employee.avatar_url and not is_generic_avatar(employee.avatar_url):
        return employee.avatar_url
    
    # Priority 3: Use Azure AD photo if employee has Azure AD ID and no stored avatar
    if employee.azure_ad_id and not employee.avatar_url:
        return reverse('assets:employee_photo', kwargs={'employee_id': employee.id})
    
    # Priority 4: Always fall back to professional placeholder
    return get_professional_avatar_url(employee)

def get_better_placeholder_url(employee):
    """
    Generate a better placeholder URL based on employee name.
    Uses DiceBear API for professional, clean avatars with initials.
    """
    if not employee or not employee.name:
        return "https://api.dicebear.com/7.x/initials/svg?seed=default&backgroundColor=6b7280&textColor=ffffff&fontSize=40"
    
    # Clean the name for use as seed
    seed = employee.name.lower().replace(' ', '').replace('.', '').replace('-', '')
    
    # Extract initials (first letter of first and last name)
    name_parts = employee.name.strip().split()
    if len(name_parts) >= 2:
        initials = (name_parts[0][0] + name_parts[-1][0]).upper()
    else:
        initials = employee.name[:2].upper()
    
    # Use DiceBear initials style for clean, professional look
    # Similar to the generic user icon with checkmark style
    return f"https://api.dicebear.com/7.x/initials/svg?seed={seed}&backgroundColor=6b7280&textColor=ffffff&fontSize=40&text={initials}"

def get_professional_avatar_url(employee):
    """
    Generate a professional avatar URL that looks like the dark blue circular avatar with white initials.
    Matches the exact style shown in the reference image.
    """
    if not employee or not employee.name:
        return "https://api.dicebear.com/7.x/initials/svg?seed=default&backgroundColor=1e40af&textColor=ffffff&fontSize=40&fontWeight=500&radius=50"
    
    # Clean the name for use as seed
    seed = employee.name.lower().replace(' ', '').replace('.', '').replace('-', '')
    
    # Extract initials (first letter of first and last name)
    name_parts = employee.name.strip().split()
    if len(name_parts) >= 2:
        initials = (name_parts[0][0] + name_parts[-1][0]).upper()
    else:
        initials = employee.name[:2].upper()
    
    # Dark blue background with white text - matches the reference image exactly
    # Using blue-700 color (#1e40af) for the dark blue background
    return f"https://api.dicebear.com/7.x/initials/svg?seed={seed}&backgroundColor=1e40af&textColor=ffffff&fontSize=40&fontWeight=500&radius=50&text={initials}"

def is_generic_avatar(avatar_url):
    """
    Check if the avatar URL is a generic/placeholder that should be replaced.
    """
    if not avatar_url:
        return True
    
    # Check for various generic avatar patterns
    generic_patterns = [
        'randomuser.me',
        'ui-avatars.com',
        'gravatar.com/avatar/',
        'placeholder.com',
        'dummyimage.com',
        'unsplash.com/photo-1472099645785-5658abf4ff4e'  # Add the hardcoded admin avatar
    ]
    
    return any(pattern in avatar_url.lower() for pattern in generic_patterns)

@register.filter
def user_avatar_url(user):
    """
    Get the appropriate avatar URL for a Django User.
    Always returns a working, professional avatar URL.
    """
    if not user:
        return get_professional_avatar_url_for_user(user)
    
    # Check if user has an associated employee record
    try:
        employee = user.employee
        if employee:
            return employee_avatar_url(employee)
    except Employee.DoesNotExist:
        pass
    
    # For admin users without employee records, use their username/name
    return get_professional_avatar_url_for_user(user)

def get_professional_avatar_url_for_user(user):
    """
    Generate a professional avatar URL for Django User objects.
    """
    if not user:
        return "https://api.dicebear.com/7.x/initials/svg?seed=default&backgroundColor=1e40af&textColor=ffffff&fontSize=40&fontWeight=500&radius=50"
    
    # Use full name if available, otherwise username
    display_name = user.get_full_name() if user.get_full_name() else user.username
    
    # Clean the name for use as seed
    seed = display_name.lower().replace(' ', '').replace('.', '').replace('-', '')
    
    # Extract initials (first letter of first and last name)
    name_parts = display_name.strip().split()
    if len(name_parts) >= 2:
        initials = (name_parts[0][0] + name_parts[-1][0]).upper()
    else:
        initials = display_name[:2].upper()
    
    # Dark blue background with white text - matches the reference image exactly
    return f"https://api.dicebear.com/7.x/initials/svg?seed={seed}&backgroundColor=1e40af&textColor=ffffff&fontSize=40&fontWeight=500&radius=50&text={initials}"

@register.filter
def health_reference_date(asset):
    """
    Get the reference date used for health calculations.
    For Azure AD assets, uses last_azure_sync date (when discovered).
    For manual assets, uses purchase_date.
    """
    if not asset:
        return None
    
    # For Azure AD assets, prioritize Azure sync date over purchase date
    if asset.azure_ad_id and asset.last_azure_sync:
        # Asset came from Azure AD - use sync date as reference (when it was discovered)
        return asset.last_azure_sync.date()
    elif asset.azure_ad_id and asset.azure_last_signin:
        # Use Azure last sign-in date if available
        return asset.azure_last_signin.date()
    elif asset.purchase_date:
        # Manually added asset - use purchase date
        return asset.purchase_date
    elif asset.last_azure_sync:
        # Fallback to Azure sync date if no other date available
        return asset.last_azure_sync.date()
    else:
        return None
