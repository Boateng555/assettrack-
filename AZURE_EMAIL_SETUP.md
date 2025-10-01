# Azure Email Integration Setup Guide

## Option 1: Azure Communication Services (Recommended)

### Step 1: Create Azure Communication Services Resource

1. **Go to Azure Portal**: https://portal.azure.com
2. **Search for "Communication Services"**
3. **Click "Create"**
4. **Fill in the details**:
   - Resource Group: Use existing or create new
   - Name: `assettrack-email-service`
   - Location: Choose closest to your users
5. **Click "Review + Create"** then **"Create"**

### Step 2: Get Connection String

1. **Go to your Communication Services resource**
2. **Click "Keys" in the left menu**
3. **Copy the "Connection String"** (starts with `endpoint=https://...`)

### Step 3: Configure Email Domain

1. **In your Communication Services resource**
2. **Go to "Email Communication"**
3. **Add your domain** (e.g., `assettrack.com`) or use Azure's domain
4. **Verify domain ownership** (follow Azure's instructions)

## Option 2: Azure SendGrid (Alternative)

### Step 1: Create SendGrid Account

1. **Go to Azure Portal**
2. **Search for "SendGrid"**
3. **Click "Create"**
4. **Choose pricing tier** (Free tier: 100 emails/day)
5. **Create the resource**

### Step 2: Get API Key

1. **Go to your SendGrid resource**
2. **Click "Manage"**
3. **Go to Settings > API Keys**
4. **Create new API key** with "Full Access"
5. **Copy the API key**

## Django Configuration

### Install Required Packages

```bash
# For Azure Communication Services
pip install azure-communication-email

# For SendGrid (alternative)
pip install sendgrid django-sendgrid-v5
```

### Update settings.py

```python
# For Azure Communication Services
EMAIL_BACKEND = 'azure_communication_email.EmailBackend'
AZURE_COMMUNICATION_CONNECTION_STRING = 'your_connection_string_here'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'

# For SendGrid (alternative)
# EMAIL_BACKEND = 'sendgrid.django.mail.SendgridBackend'
# SENDGRID_API_KEY = 'your_sendgrid_api_key'
# DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

## Testing Email

After setup, test with:

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email from AssetTrack',
    'noreply@yourdomain.com',
    ['test@example.com'],
    fail_silently=False,
)
```

## Professional Email Features

✅ **High deliverability** - Emails reach inbox, not spam
✅ **Professional sender** - Uses your domain
✅ **Scalable** - Handle thousands of emails
✅ **Reliable** - Azure infrastructure
✅ **Analytics** - Track email delivery and opens
