# Azure AD (Entra ID) Integration Guide for Django AssetTrack Application

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Azure AD App Registration](#step-1-azure-ad-app-registration)
4. [Step 2: Configure Azure AD Permissions](#step-2-configure-azure-ad-permissions)
5. [Step 3: Create Client Secret](#step-3-create-client-secret)
6. [Step 4: Django Application Setup](#step-4-django-application-setup)
7. [Step 5: Environment Configuration](#step-5-environment-configuration)
8. [Step 6: Testing the Integration](#step-6-testing-the-integration)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)

---

## Overview

This guide provides step-by-step instructions for integrating Microsoft Azure Active Directory (Azure AD) with your Django AssetTrack application. The integration enables:

- **Single Sign-On (SSO)** using Azure AD credentials
- **Automatic user synchronization** from Azure AD to your application
- **Real-time user management** with Azure AD as the source of truth

### What You'll Achieve

✅ **Azure AD Login**: Users can log in using their Azure AD credentials  
✅ **User Sync**: Automatically import users from Azure AD  
✅ **Real-time Updates**: Keep user data synchronized  
✅ **Secure Authentication**: Enterprise-grade security  

---

## Prerequisites

Before starting, ensure you have:

- **Azure AD Tenant** (Microsoft 365 Developer Account or existing tenant)
- **Django Application** (AssetTrack) running locally
- **Python 3.8+** installed
- **pip** package manager
- **Git** (optional, for version control)

### Required Azure AD Permissions

You'll need **Global Administrator** or **Application Administrator** permissions in your Azure AD tenant.

---

## Step 1: Azure AD App Registration

### 1.1 Access Azure Portal

1. **Open your browser** and go to: https://portal.azure.com
2. **Sign in** with your Azure AD administrator account
3. **Navigate to** "Azure Active Directory" → "App registrations"

### 1.2 Create New App Registration

1. **Click** "+ New registration"
2. **Fill in the details:**
   - **Name**: `AssetTrack Django App`
   - **Supported account types**: "Accounts in this organizational directory only"
   - **Redirect URI**: `http://localhost:8000/accounts/microsoft/login/callback/`
   - **Platform configuration**: Web
3. **Click** "Register"

### 1.3 Record Important Information

After registration, note down these values:

- **Application (client) ID**: `dc7dc18b-b42b-469c-9a9b-a6387e2644b3`
- **Directory (tenant) ID**: `6553940f-2bee-484c-b66c-efb9cb83e8bd`

> **Important**: Keep these IDs secure. You'll need them for configuration.

---

## Step 2: Configure Azure AD Permissions

### 2.1 Add API Permissions

1. **In your app registration**, go to "API permissions"
2. **Click** "+ Add a permission"
3. **Select** "Microsoft Graph"
4. **Choose** "Application permissions"
5. **Add these permissions:**
   - `User.Read.All` - Read all users' full profiles
   - `Device.Read.All` - Read all devices
6. **Click** "Add permissions"

### 2.2 Grant Admin Consent

1. **Click** "Grant admin consent for [Your Organization]"
2. **Confirm** the action
3. **Verify** all permissions show "Granted for [Your Organization]"

### 2.3 Configure Authentication

1. **Go to** "Authentication" in the left menu
2. **Add platform** → "Web"
3. **Add redirect URI**: `http://localhost:8000/accounts/microsoft/login/callback/`
4. **Save** the configuration

---

## Step 3: Create Client Secret

### 3.1 Generate Client Secret

1. **Go to** "Certificates & secrets"
2. **Click** "+ New client secret"
3. **Fill in:**
   - **Description**: `AssetTrack Django App v2`
   - **Expiration**: 12 months (recommended)
4. **Click** "Add"

### 3.2 Copy the Secret Value

1. **Copy the secret value** immediately (you won't see it again!)
2. **Store it securely** - you'll need it for the `.env` file

> **Security Note**: Never commit the client secret to version control.

---

## Step 4: Django Application Setup

### 4.1 Install Required Packages

Open your terminal in the Django project directory and run:

```bash
pip install django-allauth python-dotenv requests
```

### 4.2 Update Django Settings

Edit your `assettrack_django/settings.py` file:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.microsoft',
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    # ... existing middleware ...
    'allauth.account.middleware.AccountMiddleware',
]

# django-allauth settings
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False

# Azure AD Configuration
AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')

# Microsoft Azure AD settings
SOCIALACCOUNT_PROVIDERS = {
    'microsoft': {
        'TENANT': AZURE_TENANT_ID,
        'SCOPE': [
            'User.Read',
            'email',
            'profile',
        ],
        'AUTH_PARAMS': {
            'prompt': 'select_account',
        },
        'METHOD': 'oauth2',
    }
}

# Update ALLOWED_HOSTS
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

### 4.3 Update URL Configuration

Edit your `assettrack_django/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Add this line
    path('', include('assets.urls')),
]
```

### 4.4 Run Database Migrations

```bash
python manage.py migrate
```

---

## Step 5: Environment Configuration

### 5.1 Create Environment File

Create a `.env` file in your project root:

```env
AZURE_TENANT_ID=6553940f-2bee-484c-b66c-efb9cb83e8bd
AZURE_CLIENT_ID=dc7dc18b-b42b-469c-9a9b-a6387e2644b3
AZURE_CLIENT_SECRET=your_client_secret_here
```

### 5.2 Configure Django Site

1. **Start your Django server**: `python manage.py runserver localhost:8000`
2. **Go to**: http://localhost:8000/admin/
3. **Log in** with your admin credentials
4. **Navigate to**: Sites → Sites
5. **Edit the default site**:
   - **Domain name**: `localhost:8000`
   - **Display name**: `AssetTrack Local`

### 5.3 Configure Social Application

1. **In Django admin**, go to "Social Applications"
2. **Click** "Add social application"
3. **Fill in:**
   - **Provider**: Microsoft
   - **Name**: AssetTrack Azure AD
   - **Client ID**: Your Azure Client ID
   - **Secret key**: Your Azure Client Secret
   - **Sites**: Move `localhost:8000` to "Chosen sites"

---

## Step 6: Testing the Integration

### 6.1 Test Azure AD Login

1. **Go to**: http://localhost:8000/
2. **Click** "Login with Microsoft"
3. **Sign in** with your Azure AD credentials
4. **Verify** you're redirected back to your application

### 6.2 Test User Synchronization

1. **Go to**: http://localhost:8000/azure-sync/
2. **Click** "Sync with Azure AD"
3. **Check** the success message
4. **Verify** users appear in your employees list

### 6.3 Test New User Creation

1. **Create a new user** in Azure AD
2. **Run the sync** again
3. **Verify** the new user appears in your application

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: 401 Unauthorized Error

**Symptoms**: "Failed to get Azure AD access token: 401 Client Error"

**Solutions**:
1. **Verify client secret** is correct and not expired
2. **Check API permissions** are granted with admin consent
3. **Ensure environment variables** are loaded correctly

#### Issue 2: Redirect URI Error

**Symptoms**: "The redirect URI is not valid"

**Solutions**:
1. **Use `localhost`** instead of `127.0.0.1` in Azure Portal
2. **Verify redirect URI** matches exactly: `http://localhost:8000/accounts/microsoft/login/callback/`

#### Issue 3: No Users Syncing

**Symptoms**: Sync shows "0 new, 0 updated"

**Solutions**:
1. **Check Azure AD has users** with email addresses
2. **Verify API permissions** include `User.Read.All`
3. **Check user accounts** are enabled in Azure AD

#### Issue 4: Email Conflict Errors

**Symptoms**: "UNIQUE constraint failed: assets_employee.email"

**Solutions**:
1. **Check for duplicate emails** in your database
2. **Update sync logic** to handle email conflicts
3. **Use unique email addresses** in Azure AD

### Debug Commands

Use these commands to troubleshoot:

```bash
# Test Azure AD connection
python test_azure_sync.py

# Debug specific user sync
python debug_nana_user.py

# Check environment variables
python check_azure_config.py
```

---

## Maintenance

### Regular Tasks

#### 1. Client Secret Rotation

**Frequency**: Every 12 months

**Steps**:
1. **Create new client secret** in Azure Portal
2. **Update `.env` file** with new secret
3. **Test the integration**
4. **Delete old secret** after confirming it works

#### 2. Monitor Sync Status

**Frequency**: Weekly

**Check**:
- Sync success rates
- New user creation
- Error logs

#### 3. Update Permissions

**Frequency**: As needed

**When to update**:
- Adding new Azure AD features
- Changing user data requirements
- Security policy updates

### Security Best Practices

1. **Never commit secrets** to version control
2. **Use environment variables** for sensitive data
3. **Rotate client secrets** regularly
4. **Monitor access logs** in Azure Portal
5. **Use least privilege** for API permissions

### Backup and Recovery

1. **Backup your `.env` file** securely
2. **Document all configuration** settings
3. **Test recovery procedures** regularly
4. **Keep Azure AD app registration** details safe

---

## Support and Resources

### Documentation Links

- [Azure AD Documentation](https://docs.microsoft.com/en-us/azure/active-directory/)
- [Django Allauth Documentation](https://django-allauth.readthedocs.io/)
- [Microsoft Graph API Reference](https://docs.microsoft.com/en-us/graph/)

### Community Resources

- [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-active-directory)
- [Microsoft Q&A](https://docs.microsoft.com/en-us/answers/topics/azure-active-directory.html)
- [Django Community](https://www.djangoproject.com/community/)

### Contact Information

For technical support:
- **Azure AD Issues**: Microsoft Support
- **Django Issues**: Django Community
- **Application Issues**: Your development team

---

## Conclusion

Congratulations! You have successfully integrated Azure AD with your Django AssetTrack application. The integration provides:

- ✅ **Secure authentication** using Azure AD
- ✅ **Automatic user synchronization**
- ✅ **Enterprise-grade security**
- ✅ **Scalable user management**

### Next Steps

1. **Test thoroughly** with your user base
2. **Monitor performance** and error rates
3. **Plan for production** deployment
4. **Train users** on the new login process

### Production Considerations

When moving to production:

1. **Update redirect URIs** to your production domain
2. **Configure proper SSL certificates**
3. **Set up monitoring** and alerting
4. **Plan for high availability**
5. **Document user procedures**

---

*This documentation was created for the AssetTrack Django application Azure AD integration project. Last updated: August 26, 2025.*
