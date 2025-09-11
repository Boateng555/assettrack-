# Azure AD Integration Setup Guide

This guide will help you set up Microsoft Azure Active Directory integration with your AssetTrack system to automatically sync employee names and laptop assignments.

## Prerequisites

- Microsoft Azure Active Directory tenant
- Admin access to Azure AD
- Python requests library installed

## Step 1: Register an Application in Azure AD

1. Go to the [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Fill in the details:
   - **Name**: AssetTrack Integration
   - **Supported account types**: Accounts in this organizational directory only
   - **Redirect URI**: Leave blank (we're using client credentials flow)
5. Click **Register**

## Step 2: Get Application Credentials

1. From your registered app, note down:
   - **Application (client) ID** - This is your `AZURE_CLIENT_ID`
   - **Directory (tenant) ID** - This is your `AZURE_TENANT_ID`

2. Create a client secret:
   - Go to **Certificates & secrets**
   - Click **New client secret**
   - Add a description and choose expiration
   - Copy the **Value** (not the ID) - This is your `AZURE_CLIENT_SECRET`

## Step 3: Grant API Permissions

1. Go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Application permissions**
5. Add the following permissions:
   - `User.Read.All` - Read all users' full profiles
   - `Device.Read.All` - Read all devices
6. Click **Grant admin consent** for your organization

## Step 4: Configure Django Settings

Add the following to your `assettrack_django/settings.py`:

```python
# Azure AD Integration Settings
AZURE_TENANT_ID = 'your-tenant-id-here'
AZURE_CLIENT_ID = 'your-client-id-here'
AZURE_CLIENT_SECRET = 'your-client-secret-here'
```

## Step 5: Install Dependencies

```bash
pip install requests
```

## Step 6: Run Migrations

```bash
python manage.py migrate
```

## Step 7: Test the Integration

### Option 1: Web Interface
1. Start your Django server: `python manage.py runserver`
2. Navigate to **Azure Sync** in the navigation menu
3. Click **Sync Now** to perform a manual sync

### Option 2: Command Line
```bash
# Full sync (employees, devices, and assignments)
python manage.py sync_azure_ad

# Sync only employees
python manage.py sync_azure_ad --employees-only

# Sync only devices
python manage.py sync_azure_ad --devices-only

# Sync only device assignments
python manage.py sync_azure_ad --assignments-only
```

## What Gets Synced

### Employees
- Full name (displayName)
- Email address (mail)
- Department
- Job title
- Employee ID
- Azure AD username (userPrincipalName)

### Devices
- Device name (displayName)
- Serial number (deviceId)
- Model and manufacturer
- Operating system and version
- Device type (laptop/desktop)

### Device Assignments
- Links devices to employees based on Azure AD device ownership
- Updates asset status to "assigned" when linked

## Troubleshooting

### Common Issues

1. **"Azure AD credentials not configured"**
   - Check that all three environment variables are set correctly
   - Verify the values in your Django settings

2. **"Insufficient privileges"**
   - Ensure you've granted admin consent for the API permissions
   - Verify the application has the correct permissions

3. **"No users found"**
   - Check that users exist in your Azure AD tenant
   - Verify the application has User.Read.All permission

4. **"No devices found"**
   - Ensure devices are registered in Azure AD
   - Check that the application has Device.Read.All permission

### Debug Mode

To see detailed logs, add this to your Django settings:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'assets.azure_ad_integration': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Security Considerations

- Store Azure AD credentials securely (use environment variables in production)
- Regularly rotate client secrets
- Use the principle of least privilege for API permissions
- Monitor sync logs for any unusual activity

## Automation

For production use, consider setting up automated syncs using:

1. **Django Management Command with Cron**:
   ```bash
   # Add to crontab to run every hour
   0 * * * * /path/to/python /path/to/manage.py sync_azure_ad
   ```

2. **Celery Tasks** for background processing
3. **Azure Logic Apps** for event-driven syncs

## Support

If you encounter issues:
1. Check the Django logs for error messages
2. Verify your Azure AD configuration
3. Test with a small subset of users first
4. Ensure your Azure AD tenant has the necessary licenses







