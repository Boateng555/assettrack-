# 🔗 Real Azure AD Integration Setup Guide

## Prerequisites
- Microsoft Azure account with Azure AD tenant
- Admin access to your Azure AD tenant
- Your AssetTrack application ready to run

## Step 1: Create Azure AD App Registration

### 1.1 Go to Azure Portal
1. Visit [Azure Portal](https://portal.azure.com)
2. Sign in with your Microsoft account
3. Navigate to **Azure Active Directory** → **App registrations**

### 1.2 Register New Application
1. Click **"New registration"**
2. Fill in the details:
   - **Name**: `AssetTrack Integration`
   - **Supported account types**: `Accounts in this organizational directory only`
   - **Redirect URI**: `http://localhost:8000/` (for testing)
3. Click **"Register"**

### 1.3 Get Application Credentials
After registration, you'll get:
- **Application (client) ID** - This is your `AZURE_CLIENT_ID`
- **Directory (tenant) ID** - This is your `AZURE_TENANT_ID`

### 1.4 Create Client Secret
1. Go to **Certificates & secrets**
2. Click **"New client secret"**
3. Add description: `AssetTrack Integration Secret`
4. Choose expiration (recommend 12 months)
5. Click **"Add"**
6. **Copy the secret value immediately** - This is your `AZURE_CLIENT_SECRET`

## Step 2: Configure API Permissions

### 2.1 Add Microsoft Graph Permissions
1. Go to **API permissions**
2. Click **"Add a permission"**
3. Select **"Microsoft Graph"**
4. Choose **"Application permissions"**
5. Add these permissions:
   - `User.Read.All` - Read all users
   - `Device.Read.All` - Read all devices
   - `Directory.Read.All` - Read directory data
6. Click **"Add permissions"**

### 2.2 Grant Admin Consent
1. Click **"Grant admin consent for [Your Organization]"**
2. Confirm the permissions

## Step 3: Configure Your Django Settings

Add these settings to your `assettrack_django/settings.py`:

```python
# Azure AD Configuration
AZURE_TENANT_ID = 'your-tenant-id-here'
AZURE_CLIENT_ID = 'your-client-id-here'
AZURE_CLIENT_SECRET = 'your-client-secret-here'

# Optional: Configure sync settings
AZURE_SYNC_ENABLED = True
AZURE_SYNC_INTERVAL = 3600  # Sync every hour (in seconds)
```

## Step 4: Test with Real Data

### 4.1 Run Real Azure AD Sync
```bash
python manage.py sync_azure_ad
```

### 4.2 View Results
- Visit: http://localhost:8000/azure-status/
- Check the dashboard for synced employees and devices

## Step 5: Monitor Real-time Data

### 5.1 Check Synced Employees
- All employees from your Azure AD will be imported
- Their job titles, departments, and contact info will be synced
- Azure AD IDs will be stored for future syncs

### 5.2 Check Synced Devices
- All company devices registered in Azure AD will be imported
- Operating system and version information will be captured
- Device assignments will be tracked

## Troubleshooting

### Common Issues:

1. **"Azure AD credentials not configured"**
   - Check that all three settings are in your `settings.py`
   - Restart your Django server after adding settings

2. **"Insufficient privileges"**
   - Make sure you granted admin consent for the permissions
   - Verify you have admin access to the Azure AD tenant

3. **"No users found"**
   - Check that your Azure AD tenant has users
   - Verify the app has the correct permissions

4. **"Authentication failed"**
   - Double-check your tenant ID, client ID, and client secret
   - Make sure the client secret hasn't expired

## Security Best Practices

1. **Environment Variables**: Store credentials in environment variables:
   ```python
   import os
   
   AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID')
   AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
   AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
   ```

2. **Secret Management**: Use Azure Key Vault or similar for production

3. **Least Privilege**: Only grant the minimum permissions needed

4. **Regular Rotation**: Rotate client secrets regularly

## Next Steps

1. **Set up automated sync** using Django management commands
2. **Configure email notifications** for sync status
3. **Set up monitoring** for sync failures
4. **Train your team** on the new functionality

---

**🎯 Ready to test with real Azure AD data!** Follow these steps and you'll have real employees and devices syncing from your Azure AD tenant into your AssetTrack application.

