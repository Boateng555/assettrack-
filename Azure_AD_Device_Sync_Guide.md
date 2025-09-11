# Azure AD Device Sync Guide - Automatic Device Import and Assignment

## Overview

The enhanced Azure AD integration now provides **automatic device synchronization** that imports all user devices from Azure AD as assets and automatically assigns them to their owners. This ensures that when users are synced, their laptops, phones, and other devices are ready for asset management.

## Key Features

### 🔄 **Automatic Device Import**
- **User Devices**: All devices registered to users in Azure AD are automatically imported
- **Asset Creation**: Each device becomes an asset in your system
- **Automatic Assignment**: Devices are automatically assigned to their owners
- **Asset Type Mapping**: Devices are categorized based on their operating system

### 📱 **Device Type Classification**
| Azure AD OS | Asset Type | Description |
|-------------|------------|-------------|
| Windows | laptop | Desktop and laptop computers |
| macOS | laptop | Mac computers and laptops |
| iOS | phone | iPhones and iPads |
| Android | phone | Android phones and tablets |
| Other | other | Other device types |

### 🎯 **Automatic Assignment**
- Devices are automatically assigned to their Azure AD owners
- Asset status is set to `assigned`
- Serial numbers are generated from Azure AD device IDs
- OS information is preserved

## How It Works

### 1. **User Sync Process**
When syncing employees from Azure AD:

1. **Employee Creation/Update**: User is created or updated in your system
2. **Device Discovery**: System fetches all devices registered to the user
3. **Asset Creation**: Each device becomes an asset with appropriate type
4. **Assignment**: Asset is automatically assigned to the employee
5. **Status Update**: Asset status is set to `assigned`

### 2. **Device Data Mapping**
```python
# Example device data from Azure AD
{
    'id': 'device-123',
    'displayName': 'John\'s Laptop',
    'deviceId': 'ABC123XYZ',
    'operatingSystem': 'Windows',
    'operatingSystemVersion': '11.0',
    'manufacturer': 'Dell',
    'model': 'Latitude 5520'
}

# Becomes this asset in your system
{
    'name': 'John\'s Laptop',
    'asset_type': 'laptop',
    'serial_number': 'ABC123XYZ',
    'operating_system': 'Windows',
    'os_version': '11.0',
    'manufacturer': 'Dell',
    'model': 'Latitude 5520',
    'status': 'assigned',
    'assigned_to': employee_object
}
```

## Usage Examples

### 1. **Sync Employees with Their Devices**
```bash
python manage.py sync_azure_ad --employees-only
```

**Output:**
```
Employee sync completed:
  - New: 2
  - Updated: 5
  - Disabled: 0
  - Deleted: 0
  - Devices synced: 8
  - Devices assigned: 8
```

### 2. **Full Sync with Devices**
```bash
python manage.py sync_azure_ad
```

**Output:**
```
Full Azure AD sync completed:
  - Employees: 2 new, 5 updated, 0 disabled, 0 deleted
  - User Devices: 8 synced, 8 assigned
  - Standalone Devices: 3 synced, 0 updated
  - Assignments: 8 updated
  - Assets cleaned up: 0
```

### 3. **Web Interface Results**
After running sync in the web interface:
```
Azure AD sync completed successfully!
Employees: 2 new, 5 updated, 0 disabled, 0 deleted.
User Devices: 8 synced, 8 assigned.
Standalone Devices: 3 synced, 0 updated.
Assignments: 8 updated.
Assets cleaned up: 0.
```

## Testing Scenarios

### Scenario 1: New User with Devices
1. **Create a user** in Azure AD
2. **Register devices** to the user in Azure AD
3. **Run sync**
4. **Result**: User and all their devices are imported and assigned

### Scenario 2: User Gets New Device
1. **User already exists** in your system
2. **Register new device** to user in Azure AD
3. **Run sync**
4. **Result**: New device is imported and assigned to the user

### Scenario 3: Device Reassignment
1. **Device is reassigned** to different user in Azure AD
2. **Run sync**
3. **Result**: Device assignment is updated in your system

### Scenario 4: User Termination
1. **User is deleted** from Azure AD
2. **Run sync**
3. **Result**: User is marked as deleted, devices are unassigned

## Device Management Features

### **Automatic Asset Creation**
- Each Azure AD device becomes an asset
- Asset name uses device display name or generates one
- Serial number uses Azure AD device ID
- OS information is preserved

### **Smart Asset Type Detection**
- Windows/macOS → laptop
- iOS/Android → phone
- Other → other

### **Automatic Assignment**
- Devices are assigned to their Azure AD owners
- Asset status set to `assigned`
- Assignment relationship is maintained

### **Update Handling**
- Device information updates are synced
- Assignment changes are reflected
- OS updates are tracked

## Database Schema

### Asset Model Enhancements
```python
class Asset(models.Model):
    # ... existing fields ...
    
    # Azure AD Integration Fields
    azure_ad_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    operating_system = models.CharField(max_length=50, blank=True, null=True)
    os_version = models.CharField(max_length=50, blank=True, null=True)
    last_azure_sync = models.DateTimeField(null=True, blank=True)
    
    # Assignment
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
```

## API Endpoints

### Device Sync Status
```json
GET /api/azure-status/

Response:
{
    "status": "success",
    "summary": {
        "azure_users": 7,
        "local_employees": 19,
        "azure_synced_employees": 13,
        "active_employees": 13,
        "inactive_employees": 5,
        "deleted_employees": 1,
        "total_assets": 23,
        "azure_synced_assets": 8,
        "assigned_assets": 12
    }
}
```

## Monitoring and Reporting

### **Sync Statistics**
- Number of devices synced per user
- Device type breakdown
- Assignment status
- Sync timestamps

### **Asset Reports**
- Devices by employee
- Devices by type
- Unassigned devices
- Sync status

### **Audit Trail**
- Device creation history
- Assignment changes
- Sync timestamps
- Error logs

## Best Practices

### 1. **Regular Sync Schedule**
- **Development**: Sync manually as needed
- **Production**: Sync every 4-6 hours
- **Critical**: Sync immediately after device changes

### 2. **Device Management**
- Monitor device assignments
- Review unassigned devices
- Track device updates
- Audit sync results

### 3. **Data Integrity**
- Never manually delete Azure AD synced assets
- Use sync for assignment changes
- Keep device history
- Regular backup of asset data

### 4. **Performance**
- Sync during off-peak hours
- Monitor sync duration
- Optimize for large device counts
- Use incremental sync when possible

## Troubleshooting

### Common Issues

#### Issue 1: No Devices Found
**Symptoms**: Users sync but no devices are imported

**Solutions:**
1. Check Azure AD device registration
2. Verify user has registered devices
3. Check Azure AD permissions
4. Review sync logs

#### Issue 2: Devices Not Assigned
**Symptoms**: Devices imported but not assigned to users

**Solutions:**
1. Check device ownership in Azure AD
2. Verify user-device relationship
3. Check sync logic
4. Review assignment rules

#### Issue 3: Wrong Asset Types
**Symptoms**: Devices categorized incorrectly

**Solutions:**
1. Check OS information in Azure AD
2. Verify asset type mapping
3. Review device details
4. Update mapping rules

### Debug Commands

```bash
# Test device sync functionality
python test_device_sync.py

# Check sync summary
python manage.py sync_azure_ad --summary

# Sync employees with devices
python manage.py sync_azure_ad --employees-only

# Check asset assignments
python manage.py shell -c "from assets.models import Asset; print(Asset.objects.filter(azure_ad_id__isnull=False).count())"
```

## Migration Guide

### From Basic Sync to Device Sync

1. **Backup your database**
2. **Run the migration**:
   ```bash
   python manage.py migrate
   ```
3. **Test the device sync**:
   ```bash
   python test_device_sync.py
   ```
4. **Run initial sync**:
   ```bash
   python manage.py sync_azure_ad --employees-only
   ```
5. **Verify results**:
   ```bash
   python manage.py sync_azure_ad --summary
   ```

### Data Migration Notes
- Existing assets are preserved
- New device sync is additive
- No data loss during migration
- Enhanced features added seamlessly

## Conclusion

The enhanced Azure AD device sync provides **complete device lifecycle management** that automatically keeps your asset inventory synchronized with Azure AD. This ensures:

- ✅ **Automatic Device Import**: All user devices are imported as assets
- ✅ **Smart Assignment**: Devices are automatically assigned to their owners
- ✅ **Type Classification**: Devices are correctly categorized
- ✅ **Data Preservation**: OS and device information is maintained
- ✅ **Update Handling**: Device changes are automatically synced
- ✅ **Comprehensive Reporting**: Full audit trail of device management

**Your Azure AD integration now provides complete device management automatically!** 🎉
