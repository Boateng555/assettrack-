# Azure AD Device Management Guide - Adding Devices and Assigning to Users

## Overview

This guide shows you how to add devices in Azure AD and assign them to users, which will then automatically sync to your AssetTrack system.

## Method 1: Azure AD Portal (Recommended)

### Step 1: Access Azure AD Portal

1. **Go to Azure Portal**: https://portal.azure.com
2. **Navigate to Azure Active Directory**
3. **Go to Devices** (under Manage section)

### Step 2: Add New Device

#### Option A: Register Device (For existing devices)

1. **Click "New registration"**
2. **Fill in device details**:
   - **Device name**: e.g., "John's Laptop"
   - **Device type**: Select appropriate type
   - **Operating system**: Windows, macOS, iOS, Android
   - **Manufacturer**: Dell, Apple, etc.
   - **Model**: Specific model number

3. **Click "Register"**

#### Option B: Add Device Manually

1. **Click "Add device"**
2. **Select "Add device"**
3. **Choose device type**:
   - **Windows**: For Windows computers
   - **macOS**: For Mac computers  
   - **iOS**: For iPhones/iPads
   - **Android**: For Android devices

4. **Fill in details**:
   - **Device name**: Descriptive name
   - **Serial number**: Device serial number
   - **Manufacturer**: Device manufacturer
   - **Model**: Device model
   - **Operating system**: OS version

### Step 3: Assign Device to User

1. **Find the device** in the devices list
2. **Click on the device name**
3. **Go to "Registered owners"**
4. **Click "Add owner"**
5. **Search for the user** by name or email
6. **Select the user**
7. **Click "Add"**

## Method 2: Using PowerShell (Advanced)

### Prerequisites

```powershell
# Install Azure AD module
Install-Module -Name AzureAD

# Connect to Azure AD
Connect-AzureAD
```

### Add Device Script

```powershell
# Create a new device
$device = New-AzureADDevice -DisplayName "John's Laptop" -DeviceId "ABC123XYZ" -DeviceOSType "Windows" -DeviceOSVersion "11.0"

# Assign device to user
$user = Get-AzureADUser -Filter "userPrincipalName eq 'john.doe@yourcompany.com'"
Add-AzureADDeviceRegisteredOwner -ObjectId $device.ObjectId -RefObjectId $user.ObjectId
```

## Method 3: Using Microsoft Graph API

### Add Device via API

```bash
# Get access token
curl -X POST "https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id={client-id}&client_secret={client-secret}&scope=https://graph.microsoft.com/.default"

# Create device
curl -X POST "https://graph.microsoft.com/v1.0/devices" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "John'\''s Laptop",
    "deviceId": "ABC123XYZ",
    "operatingSystem": "Windows",
    "operatingSystemVersion": "11.0",
    "manufacturer": "Dell",
    "model": "Latitude 5520"
  }'
```

## Device Types and Asset Mapping

### Asset Type Classification

| Azure AD Device Type | Asset Type | Description |
|---------------------|------------|-------------|
| Windows | laptop | Desktop and laptop computers |
| macOS | laptop | Mac computers and laptops |
| iOS | phone | iPhones and iPads |
| Android | phone | Android phones and tablets |
| Other | other | Other device types |

### Device Information Mapping

```json
{
  "azure_ad_device": {
    "id": "device-123",
    "displayName": "John's Laptop",
    "deviceId": "ABC123XYZ",
    "operatingSystem": "Windows",
    "operatingSystemVersion": "11.0",
    "manufacturer": "Dell",
    "model": "Latitude 5520"
  },
  "asset_track_asset": {
    "name": "John's Laptop",
    "asset_type": "laptop",
    "serial_number": "ABC123XYZ",
    "operating_system": "Windows",
    "os_version": "11.0",
    "manufacturer": "Dell",
    "model": "Latitude 5520",
    "status": "assigned",
    "assigned_to": "John Doe"
  }
}
```

## Step-by-Step: Complete Device Setup

### 1. Add Device in Azure AD

1. **Login to Azure Portal**
2. **Go to Azure Active Directory > Devices**
3. **Click "New registration"**
4. **Fill device information**:
   ```
   Device name: John's Work Laptop
   Device type: Windows
   Operating system: Windows 11
   Manufacturer: Dell
   Model: Latitude 5520
   Serial number: ABC123XYZ
   ```
5. **Click "Register"**

### 2. Assign Device to User

1. **Click on the device** you just created
2. **Go to "Registered owners" tab**
3. **Click "Add owner"**
4. **Search for user**: "John Doe"
5. **Select the user**
6. **Click "Add"**

### 3. Sync to AssetTrack

1. **Go to your AssetTrack admin panel**
2. **Navigate to Azure AD Sync**
3. **Click "Sync Now"**
4. **Verify the device appears** in your assets

## Bulk Device Import

### Using CSV Import (Azure AD)

1. **Prepare CSV file** with device information:
   ```csv
   Device Name,Device Type,Serial Number,Manufacturer,Model,OS,OS Version,Owner Email
   John's Laptop,Windows,ABC123XYZ,Dell,Latitude 5520,Windows,11.0,john.doe@company.com
   Jane's iPhone,iOS,DEF456GHI,Apple,iPhone 13,iOS,15.0,jane.smith@company.com
   ```

2. **Use PowerShell script**:
   ```powershell
   Import-Csv "devices.csv" | ForEach-Object {
     $device = New-AzureADDevice -DisplayName $_.'Device Name' -DeviceId $_.'Serial Number'
     $user = Get-AzureADUser -Filter "mail eq '$($_.'Owner Email')'"
     Add-AzureADDeviceRegisteredOwner -ObjectId $device.ObjectId -RefObjectId $user.ObjectId
   }
   ```

## Device Management Best Practices

### 1. Naming Conventions

**Recommended device names**:
- `{User Name}'s {Device Type}` - e.g., "John's Laptop"
- `{Department}-{User}-{Device}` - e.g., "IT-John-Laptop"
- `{Asset Tag}-{Device Type}` - e.g., "AT001-Laptop"

### 2. Device Information

**Always include**:
- ✅ Device name
- ✅ Serial number
- ✅ Manufacturer
- ✅ Model
- ✅ Operating system
- ✅ Owner assignment

### 3. Regular Maintenance

**Monthly tasks**:
- Review unassigned devices
- Update device information
- Remove obsolete devices
- Verify owner assignments

## Troubleshooting

### Common Issues

#### Issue 1: Device Not Syncing
**Symptoms**: Device exists in Azure AD but not in AssetTrack

**Solutions**:
1. Check device has an owner assigned
2. Verify device is enabled in Azure AD
3. Run manual sync in AssetTrack
4. Check sync logs for errors

#### Issue 2: Wrong Asset Type
**Symptoms**: Device synced but wrong asset type

**Solutions**:
1. Check operating system in Azure AD
2. Verify asset type mapping rules
3. Update device OS information
4. Re-sync the device

#### Issue 3: Device Not Assigned
**Symptoms**: Device synced but not assigned to user

**Solutions**:
1. Check device ownership in Azure AD
2. Verify user exists in AssetTrack
3. Check assignment sync logic
4. Run assignment sync

### Debug Commands

```bash
# Test device sync
python test_device_sync.py

# Check sync status
python manage.py sync_azure_ad --summary

# Sync devices only
python manage.py sync_azure_ad --devices-only

# Check device assignments
python manage.py shell -c "from assets.models import Asset; print(Asset.objects.filter(azure_ad_id__isnull=False).count())"
```

## Advanced Scenarios

### Scenario 1: Device Reassignment

1. **In Azure AD**: Remove old owner, add new owner
2. **In AssetTrack**: Run sync
3. **Result**: Device automatically reassigned

### Scenario 2: Device Retirement

1. **In Azure AD**: Delete or disable device
2. **In AssetTrack**: Run sync
3. **Result**: Device marked as retired/unassigned

### Scenario 3: Bulk Device Updates

1. **Prepare updated CSV** with device changes
2. **Use PowerShell script** to update Azure AD
3. **Run sync** in AssetTrack
4. **Verify changes** in asset inventory

## Monitoring and Reporting

### Device Sync Status

```bash
# Check sync summary
python manage.py sync_azure_ad --summary

# View device statistics
python manage.py shell -c "
from assets.models import Asset
print(f'Total assets: {Asset.objects.count()}')
print(f'Azure AD assets: {Asset.objects.filter(azure_ad_id__isnull=False).count()}')
print(f'Assigned assets: {Asset.objects.filter(assigned_to__isnull=False).count()}')
"
```

### Asset Reports

- **Devices by employee**: See all devices assigned to each user
- **Unassigned devices**: Find devices without owners
- **Device types**: Breakdown by laptop, phone, etc.
- **Sync status**: Track which devices are synced from Azure AD

## Security Considerations

### Device Security

1. **Device Compliance**: Ensure devices meet security requirements
2. **Access Control**: Limit who can assign devices
3. **Audit Trail**: Track all device changes
4. **Regular Reviews**: Periodically review device assignments

### Data Protection

1. **Sensitive Information**: Don't store sensitive data in device names
2. **Access Logs**: Monitor who accesses device information
3. **Backup**: Regular backup of device data
4. **Encryption**: Ensure device data is encrypted

## Conclusion

This guide provides comprehensive instructions for adding devices in Azure AD and assigning them to users. The devices will automatically sync to your AssetTrack system with proper asset types and assignments.

**Key Benefits**:
- ✅ **Centralized Management**: All devices managed in Azure AD
- ✅ **Automatic Sync**: Devices automatically appear in AssetTrack
- ✅ **Smart Assignment**: Devices automatically assigned to owners
- ✅ **Type Classification**: Devices correctly categorized
- ✅ **Real-time Updates**: Changes sync immediately

**Your device management is now fully integrated with Azure AD!** 🎉
