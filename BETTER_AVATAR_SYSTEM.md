# Better Avatar System

This document explains the improved avatar system that handles missing pictures and provides better-looking placeholders.

## Problem Solved

The original system had issues with:
- **Generic placeholders**: Random user images that didn't look professional
- **Duplicate employees**: Multiple entries for the same person with different avatars
- **Missing pictures**: Employees with no photos showing generic initials or broken images

## New Features

### 1. **Better Placeholder Images**
- Uses **DiceBear API** for professional-looking avatar placeholders
- Consistent, colorful avatars based on employee names
- No more generic random user images

### 2. **Smart Fallback System**
- **Priority 1**: Azure AD profile photos (if available)
- **Priority 2**: Stored avatar URLs (if not generic)
- **Priority 3**: Better placeholder based on employee name

### 3. **Duplicate Employee Cleanup**
- Identifies and removes duplicate employee entries
- Preserves employees with related data (assets, handovers, etc.)
- Keeps the oldest employee record

### 4. **Generic Avatar Detection**
- Automatically detects generic/placeholder images
- Replaces them with better alternatives
- Supports multiple generic avatar services

## Usage

### **Automatic Improvement**
The system automatically improves avatars when:
- Running Azure AD sync
- Loading employee pages
- Displaying employee lists

### **Manual Cleanup**
```bash
# Force better avatars for all employees
python manage.py cleanup_employee_avatars

# Remove duplicate employees
python manage.py cleanup_employee_avatars --remove-duplicates

# See what would be changed (dry run)
python manage.py cleanup_employee_avatars --dry-run

# Force all updates
python manage.py cleanup_employee_avatars --force-all
```

### **Testing**
```bash
# Test the new avatar system
python test_better_avatars.py
```

## How It Works

### **Template Filter Logic**
```python
def employee_avatar_url(employee):
    # 1. Try Azure AD photo first
    if employee.azure_ad_id:
        return photo_proxy_url
    
    # 2. Use stored avatar if not generic
    if employee.avatar_url and not is_generic_avatar(employee.avatar_url):
        return employee.avatar_url
    
    # 3. Generate better placeholder
    return get_better_placeholder_url(employee)
```

### **Better Placeholder Generation**
```python
def get_professional_avatar_url(employee):
    # Clean name for consistent seed
    seed = employee.name.lower().replace(' ', '').replace('.', '').replace('-', '')
    
    # Extract initials (first letter of first and last name)
    name_parts = employee.name.strip().split()
    if len(name_parts) >= 2:
        initials = (name_parts[0][0] + name_parts[-1][0]).upper()
    else:
        initials = employee.name[:2].upper()
    
    # Use DiceBear API for professional dark blue avatars
    return f"https://api.dicebear.com/7.x/initials/svg?seed={seed}&backgroundColor=1e40af&textColor=ffffff&fontSize=40&fontWeight=500&radius=50&text={initials}"
```

### **Generic Avatar Detection**
```python
def is_generic_avatar(avatar_url):
    generic_patterns = [
        'randomuser.me',
        'ui-avatars.com',
        'gravatar.com/avatar/',
        'placeholder.com',
        'dummyimage.com'
    ]
    return any(pattern in avatar_url.lower() for pattern in generic_patterns)
```

## Examples

### **Before (Generic Avatars)**
- `https://randomuser.me/api/portraits/men/1.jpg`
- `https://ui-avatars.com/api/?name=John+Smith&background=random`
- Generic initials like "Jo", "Kw", "Lis"

### **After (Better Avatars)**
- `https://api.dicebear.com/7.x/initials/svg?seed=johnsmith&backgroundColor=1e40af&textColor=ffffff&fontSize=40&fontWeight=500&radius=50&text=JS`
- Consistent, dark blue circular avatars with white initials
- Unique for each employee based on their name

## Benefits

1. **Professional Appearance**: Better-looking placeholders that match your brand
2. **Consistency**: Same employee always gets the same avatar
3. **No Duplicates**: Clean employee database without duplicates
4. **Automatic**: Works without manual intervention
5. **Fallback Safe**: Always provides a good-looking avatar

## Configuration

### **Customizing Avatar Style**
You can change the DiceBear avatar style by modifying the `get_better_placeholder_url` function:

```python
# Different styles available:
# - avataaars (cartoon people)
# - bottts (robots)
# - identicon (geometric patterns)
# - initials (letter-based)
# - pixel-art (8-bit style)

return f"https://api.dicebear.com/7.x/bottts/svg?seed={seed}&backgroundColor=b6e3f4"
```

### **Customizing Colors**
```python
# Change background color
return f"https://api.dicebear.com/7.x/avataaars/svg?seed={seed}&backgroundColor=ff6b6b&mouth=smile"

# Add more customization
return f"https://api.dicebear.com/7.x/avataaars/svg?seed={seed}&backgroundColor=b6e3f4&mouth=smile&style=circle"
```

## Troubleshooting

### **Common Issues**

1. **Avatars Not Updating**
   - Run the cleanup command: `python manage.py cleanup_employee_avatars`
   - Check if employees have Azure AD IDs
   - Verify Azure AD integration is working

2. **Duplicate Employees**
   - Run: `python manage.py cleanup_employee_avatars --remove-duplicates --dry-run`
   - Review the output before running without `--dry-run`

3. **Generic Avatars Still Showing**
   - Check if the avatar URL is in the generic patterns list
   - Add new generic patterns to `is_generic_avatar` function
   - Force update: `python manage.py cleanup_employee_avatars --force-all`

### **Testing**
```bash
# Test the system
python test_better_avatars.py

# Check specific employee
python manage.py cleanup_employee_avatars --employee-id <uuid>
```

## Migration

### **From Old System**
1. Run the cleanup command to update existing employees
2. The system automatically handles new employees
3. No database migrations required

### **To New System**
1. Update templates (already done)
2. Run cleanup command
3. Test with the provided test script

## Support

For issues with the better avatar system:
1. Run the test script to verify functionality
2. Check the cleanup command output
3. Review the template filter logic
4. Contact development team with specific error messages
