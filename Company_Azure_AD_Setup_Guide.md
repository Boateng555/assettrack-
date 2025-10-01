# Company Azure AD Setup Guide

## 🎯 **Step-by-Step: Create New Azure AD App for Your Company**

### **Step 1: Access Azure Portal**
1. Go to **Azure Portal**: https://portal.azure.com
2. Sign in with your **company account**
3. Navigate to **Azure Active Directory**

### **Step 2: Create App Registration**
1. Go to **App registrations** (left menu)
2. Click **"New registration"**
3. Fill in the details:
   - **Name**: `AssetTrack Company Integration`
   - **Supported account types**: `Accounts in this organizational directory only`
   - **Redirect URI**: `Web` → `https://yourdomain.com/accounts/microsoft/login/callback/`
4. Click **"Register"**

### **Step 3: Get Application (Client) ID**
1. After registration, you'll see the **Overview** page
2. Copy the **Application (client) ID** - you'll need this
3. Copy the **Directory (tenant) ID** - you'll need this too

### **Step 4: Create Client Secret**
1. Go to **Certificates & secrets** (left menu)
2. Click **"New client secret"**
3. Add description: `AssetTrack Integration Secret`
4. Choose expiration: `24 months` (recommended)
5. Click **"Add"**
6. **IMPORTANT**: Copy the **Value** immediately - you won't see it again!

### **Step 5: Add API Permissions**
1. Go to **API permissions** (left menu)
2. Click **"Add a permission"**
3. Select **Microsoft Graph**
4. Choose **Application permissions**
5. Add these permissions:
   - `User.Read.All` - Read all users
   - `Device.Read.All` - Read all devices
   - `Directory.Read.All` - Read directory data
6. Click **"Add permissions"**
7. **IMPORTANT**: Click **"Grant admin consent"** - this is required!

### **Step 6: Update Environment Variables**
Create or update your `.env` file with the new credentials:

```env
# Company Azure AD Configuration
AZURE_TENANT_ID=your-company-tenant-id
AZURE_CLIENT_ID=your-new-app-client-id
AZURE_CLIENT_SECRET=your-new-app-client-secret
```

**Example:**
```env
AZURE_TENANT_ID=12345678-1234-1234-1234-123456789abc
AZURE_CLIENT_ID=87654321-4321-4321-4321-cba987654321
AZURE_CLIENT_SECRET=your-new-secret-value-here
```

### **Step 7: Test the Connection**
```bash
python setup_real_azure_ad.py --test
```

### **Step 8: Sync with Company Azure AD**
```bash
# Check sync status
python manage.py sync_azure_ad --summary

# Full sync
python manage.py sync_azure_ad
```

## 🔐 **Security Requirements**

### **Required Permissions:**
- ✅ `User.Read.All` - Read all users in your organization
- ✅ `Device.Read.All` - Read all devices in your organization
- ✅ `Directory.Read.All` - Read directory data

### **Admin Consent Required:**
- ✅ **Must be granted by Azure AD administrator**
- ✅ **Required for application permissions**
- ✅ **One-time setup**

## 📋 **Information You'll Need**

### **From Azure Portal:**
1. **Tenant ID** (Directory ID)
2. **Client ID** (Application ID)
3. **Client Secret** (Value from step 4)

### **From Your Company:**
1. **Admin access** to Azure AD
2. **Permission** to create app registrations
3. **Approval** for API permissions

## ⚠️ **Important Notes**

### **Security:**
- 🔒 **Keep credentials secure**
- 🔒 **Never commit .env file to version control**
- 🔒 **Use strong client secrets**
- 🔒 **Set appropriate expiration dates**

### **Permissions:**
- 🔐 **Admin consent required**
- 🔐 **Application permissions needed**
- 🔐 **Read-only access only**
- 🔐 **No write permissions**

### **Testing:**
- 🧪 **Test in development first**
- 🧪 **Verify permissions work**
- 🧪 **Check sync results**
- 🧪 **Monitor for errors**

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **Issue 1: "Insufficient privileges"**
**Solution**: Ensure admin consent is granted

#### **Issue 2: "Invalid client"**
**Solution**: Check Client ID and Tenant ID

#### **Issue 3: "Invalid secret"**
**Solution**: Check Client Secret value

#### **Issue 4: "Access denied"**
**Solution**: Verify API permissions are granted

### **Debug Commands:**
```bash
# Test connection
python setup_real_azure_ad.py --test

# Check sync status
python manage.py sync_azure_ad --summary

# View detailed logs
python manage.py sync_azure_ad --verbose
```

## 🎯 **Success Checklist**

- [ ] Azure AD app registered
- [ ] Client ID obtained
- [ ] Client secret created
- [ ] API permissions added
- [ ] Admin consent granted
- [ ] Environment variables updated
- [ ] Connection tested
- [ ] Sync completed
- [ ] Data verified

## 📞 **Support**

If you encounter issues:
1. **Check Azure AD permissions**
2. **Verify admin consent**
3. **Test connection**
4. **Review error logs**
5. **Contact Azure AD administrator**

## 🎉 **Next Steps**

Once configured:
1. **Add devices** to Azure AD
2. **Assign devices** to users
3. **Run sync** in AssetTrack
4. **Monitor** sync results
5. **Set up** regular sync schedule

**Your company Azure AD integration will be ready!** 🚀
