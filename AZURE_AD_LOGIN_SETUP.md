# Microsoft Azure AD (Entra ID) Login Integration Setup Guide

## ✅ What's Already Done

Your Django project has been successfully configured with django-allauth and Microsoft Azure AD integration:

- ✅ django-allauth installed and configured
- ✅ Microsoft provider added to settings
- ✅ Environment variables configured
- ✅ Templates updated with login/logout buttons
- ✅ Database migrations applied
- ✅ Site configuration updated

## 🔧 Remaining Setup Steps

### Step 1: Create Client Secret in Azure Portal

1. **Go to Azure Portal:**
   - Navigate to [Azure Portal](https://portal.azure.com)
   - Go to "Azure Active Directory" → "App registrations"
   - Find your app: **AssetTrackTestApp**

2. **Create Client Secret:**
   - Click on your app → "Certificates & secrets" (left menu)
   - Click "New client secret"
   - Description: `AssetTrack Django App`
   - Expiration: 12 months (recommended)
   - Click "Add"
   - **IMPORTANT:** Copy the generated secret value immediately (you won't see it again!)

3. **Update your `.env` file:**
   ```bash
   AZURE_CLIENT_SECRET=your-actual-secret-here
   ```

### Step 2: Configure Redirect URI in Azure Portal

1. **In your Azure App Registration:**
   - Go to "Authentication" (left menu)
   - Click "Add a platform" → "Web"
   - Add this redirect URI:
   ```
   http://127.0.0.1:8000/accounts/microsoft/login/callback/
   ```
   - Click "Configure"
   - Save the configuration

### Step 3: Configure Social Application in Django Admin

1. **Start your server:**
   ```bash
   python manage.py runserver
   ```

2. **Access Django Admin:**
   - Go to: http://127.0.0.1:8000/admin/
   - Login with your superuser credentials

3. **Configure Social Application:**
   - Go to "Social Applications" → "Add social application"
   - Fill in the details:
     - **Provider:** Microsoft
     - **Name:** AssetTrack Microsoft
     - **Client ID:** `dc7dc18b-b42b-469c-9a9b-a6387e2644b3`
     - **Secret Key:** Your client secret from Step 1
     - **Sites:** Move `127.0.0.1:8000` to "Chosen sites"
   - Click "Save"

## 🧪 Testing the Integration

### Run the Test Script
```bash
python test_azure_login.py
```

This will verify your setup and show any missing configurations.

### Test the Login Flow
1. **Visit your app:** http://127.0.0.1:8000/
2. **Click:** "Login with Microsoft" button
3. **You should be redirected to Microsoft login**
4. **After successful login, you'll be redirected back to your app**

## 📁 Files Modified

- `assettrack_django/settings.py` - Added allauth configuration
- `assettrack_django/urls.py` - Added allauth URLs
- `templates/base.html` - Added login/logout buttons
- `.env` - Your Azure AD credentials
- `.env.example` - Template for environment variables

## 🔑 Your Azure AD Configuration

- **Tenant ID:** `6553940f-2bee-484c-b66c-efb9cb83e8bd`
- **Client ID:** `dc7dc18b-b42b-469c-9a9b-a6387e2644b3`
- **Client Secret:** (Set in Step 1)
- **Redirect URI:** `http://127.0.0.1:8000/accounts/microsoft/login/callback/`

## 🚨 Troubleshooting

### Common Issues:

1. **"NoReverseMatch: 'logout' not found"**
   - ✅ Fixed: Updated template to use `account_logout`

2. **"NoReverseMatch: 'socialaccount_signin' not found"**
   - ✅ Fixed: Updated template to use `provider_login_url`

3. **"Client secret not set"**
   - Create client secret in Azure Portal (Step 1)

4. **"Redirect URI mismatch"**
   - Configure redirect URI in Azure Portal (Step 2)

5. **"Social application not configured"**
   - Configure social application in Django Admin (Step 3)

### Test Your Setup:
```bash
python test_azure_login.py
```

## 🔒 Security Notes

- Keep your `.env` file secure and never commit it to version control
- The client secret should be kept confidential
- For production, use HTTPS and update the redirect URI accordingly
- Consider using Azure Key Vault for production secrets

## 🚀 Production Deployment

When deploying to production:

1. **Update redirect URI in Azure Portal:**
   ```
   https://yourdomain.com/accounts/microsoft/login/callback/
   ```

2. **Update site configuration in Django Admin:**
   - Domain: `yourdomain.com`
   - Name: `AssetTrack Production`

3. **Use environment variables for production secrets**

4. **Enable HTTPS**

## 📞 Support

If you encounter issues:
1. Run `python test_azure_login.py` to diagnose problems
2. Check the Django debug logs
3. Verify Azure Portal configuration
4. Ensure all environment variables are set correctly

---

**🎉 Once you complete Steps 1-3, your Azure AD login integration will be fully functional!**
