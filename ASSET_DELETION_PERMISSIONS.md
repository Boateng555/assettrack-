# Asset Deletion Permissions System

## Overview
The AssetTrack system now includes a comprehensive role-based permission system for asset deletion. This ensures that only authorized users can delete assets, improving security and preventing accidental data loss.

## 🔒 **Permission Levels**

### **1. Admin Users (Superusers & Staff)**
- **Can delete ANY asset** regardless of permission settings
- **Full access** to all deletion operations
- **Override all restrictions**

### **2. Regular Users**
- **Cannot delete assets by default**
- **Can only delete assets** if explicitly granted permission
- **Permission is asset-specific**

### **3. Asset Owners (if assigned)**
- **Can delete assets** only if the asset is not deletion-restricted
- **Limited to assets assigned to them**

## 🎯 **Permission Fields**

### **`can_delete` (Boolean)**
- **`True`**: Non-admin users can delete this asset
- **`False`**: Only admin users can delete this asset (default)

### **`deletion_restricted` (Boolean)**
- **`True`**: Deletion is restricted to admin users only (default)
- **`False`**: Deletion is allowed for users with `can_delete=True`

## 🚀 **How It Works**

### **Permission Check Logic**
```python
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
```

### **UI Behavior**
- **Delete buttons are disabled** for users without permission
- **Visual feedback** shows when deletion is not allowed
- **Clear error messages** explain why deletion is denied

## 🛠️ **Management Commands**

### **Set Default Permissions**
```bash
# Set all assets to admin-only deletion (default)
python manage.py set_asset_permissions

# Restrict all assets to admin-only deletion
python manage.py set_asset_permissions --restrict-all

# Allow all assets to be deleted by any user
python manage.py set_asset_permissions --allow-deletion
```

### **Admin Interface**
- **Permission fields** are visible in the Django admin
- **Easy to manage** permissions for individual assets
- **Bulk operations** available for multiple assets

## 📱 **User Experience**

### **For Admin Users**
- **Full access** to all deletion operations
- **No restrictions** on any assets
- **Can manage permissions** for other users

### **For Regular Users**
- **Delete buttons are grayed out** for restricted assets
- **Clear tooltips** explain why deletion is not allowed
- **Access denied messages** when trying to delete restricted assets

### **Visual Indicators**
- **Red delete button**: User can delete this asset
- **Gray delete button**: User cannot delete this asset
- **Tooltip**: Shows "Delete not allowed - Admin only"

## 🔧 **Configuration Examples**

### **Example 1: Admin-Only Asset**
```python
asset.can_delete = False
asset.deletion_restricted = True
# Result: Only admin users can delete
```

### **Example 2: User-Deletable Asset**
```python
asset.can_delete = True
asset.deletion_restricted = False
# Result: Any user can delete
```

### **Example 3: Owner-Only Asset**
```python
asset.can_delete = False
asset.deletion_restricted = False
# Result: Only the assigned user can delete
```

## 🚨 **Security Features**

### **Server-Side Validation**
- **Permission checks** happen on the server
- **Cannot be bypassed** by client-side manipulation
- **Audit trail** of all deletion attempts

### **Role-Based Access**
- **User roles** determine base permissions
- **Asset-specific** permissions for fine-grained control
- **Hierarchical** permission system

### **Error Handling**
- **Graceful degradation** when permissions are denied
- **Clear error messages** for users
- **Logging** of permission violations

## 📊 **Use Cases**

### **High-Value Assets**
- **Servers, network equipment**
- **Software licenses**
- **Restrict to admin-only deletion**

### **Standard Assets**
- **Laptops, monitors, peripherals**
- **Allow deletion by assigned users**
- **Maintain audit trail**

### **Temporary Assets**
- **Test equipment, loaner devices**
- **Allow deletion by any user**
- **Quick cleanup of temporary items**

## 🔮 **Future Enhancements**

### **Advanced Permissions**
- **Time-based restrictions** (e.g., no deletion during business hours)
- **Approval workflows** for high-value asset deletion
- **Deletion quotas** per user/role

### **Audit & Compliance**
- **Deletion request logs**
- **Approval tracking**
- **Compliance reporting**

### **Integration Features**
- **LDAP/Active Directory** role mapping
- **SAML** permission integration
- **API-based** permission management

## 📝 **Best Practices**

### **1. Default to Restrictive**
- **Start with admin-only deletion**
- **Gradually grant permissions** as needed
- **Regular review** of permission settings

### **2. Document Permissions**
- **Clear policies** for asset deletion
- **User training** on permission system
- **Regular audits** of permission settings

### **3. Monitor Usage**
- **Track deletion patterns**
- **Identify permission issues**
- **Optimize permission settings**

## 🎉 **Conclusion**

The asset deletion permission system provides:
- **Enhanced security** for valuable assets
- **Flexible permission management** for different use cases
- **Clear user feedback** on deletion capabilities
- **Admin control** over asset lifecycle

This system ensures that your AssetTrack deployment maintains data integrity while providing the flexibility needed for efficient asset management.






