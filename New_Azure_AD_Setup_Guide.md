# Complete Azure AD App Setup Guide

## 🎯 **Step 1: Access Azure Portal**

1. **Go to**: https://portal.azure.com
2. **Sign in** with your Azure account
3. **Navigate to**: Azure Active Directory (left menu)

## 🔑 **Step 2: Create App Registration**

1. **Click**: "App registrations" (left menu)
2. **Click**: "New registration" (top)
3. **Fill in the details**:
   - **Name**: `AssetTrack Integration`
   - **Supported account types**: `Accounts in this organizational directory only`
   - **Redirect URI**: `Web` → `https://localhost:8000/accounts/microsoft/login/callback/`
4. **Click**: "Register"

## 📋 **Step 3: Get Your Credentials**

After registration, you'll see the **Overview** page:

### **Copy These Values:**
1. **Application (client) ID** - Copy this value
2. **Directory (tenant) ID** - Copy this value

**Example:**
- Application ID: `12345678-1234-1234-1234-123456789abc`
- Directory ID: `87654321-4321-4321-4321-cba987654321`

## 🔐 **Step 4: Add API Permissions**

1. **Click**: "API permissions" (left menu)
2. **Click**: "Add a permission"
3. **Select**: "Microsoft Graph"
4. **Choose**: "Application permissions"
5. **Add these permissions**:
   - ✅ `User.Read.All` - Read all users
   - ✅ `Device.Read.All` - Read all devices  
   - ✅ `Directory.Read.All` - Read directory data
6. **Click**: "Add permissions"
7. **IMPORTANT**: Click "Grant admin consent" (required!)

## 🔒 **Step 5: Create Client Secret**

1. **Click**: "Certificates & secrets" (left menu)
2. **Click**: "New client secret"
3. **Add description**: `AssetTrack Integration Secret`
4. **Expires**: `24 months` (recommended)
5. **Click**: "Add"
6. **IMPORTANT**: Copy the **Value** immediately - you won't see it again!

## 📝 **Step 6: Update Environment Variables**

Create or update your `.env` file with the new credentials:

```env
# New Azure AD Configuration
AZURE_TENANT_ID=your-directory-tenant-id
AZURE_CLIENT_ID=your-application-client-id
AZURE_CLIENT_SECRET=your-client-secret-value
```

**Example:**
```env
AZURE_TENANT_ID=87654321-4321-4321-4321-cba987654321
AZURE_CLIENT_ID=12345678-1234-1234-1234-123456789abc
AZURE_CLIENT_SECRET=your-secret-value-here
```

## 🧪 **Step 7: Test Connection**

Run this command to test your new connection:

```bash
python setup_real_azure_ad.py --test
```

**Expected output:**
```
✅ Connection successful!
📊 Found X users in Azure AD
```

## 🔄 **Step 8: Sync with Azure AD**

Once connection is working, sync your data:

```bash
# Check sync status
python manage.py sync_azure_ad --summary

# Full sync
python manage.py sync_azure_ad
```

## ⚠️ **Important Notes**

### **Security:**
- 🔒 Keep credentials secure
- 🔒 Never commit .env file to version control
- 🔒 Use strong client secrets
- 🔒 Set appropriate expiration dates

### **Permissions:**
- 🔐 Admin consent required
- 🔐 Application permissions needed
- 🔐 Read-only access only
- 🔐 No write permissions

### **Testing:**
- 🧪 Test in development first
- 🧪 Verify permissions work
- 🧪 Check sync results
- 🧪 Monitor for errors

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **"Insufficient privileges"**
- **Solution**: Ensure admin consent is granted

#### **"Invalid client"**
- **Solution**: Check Client ID and Tenant ID

#### **"Invalid secret"**
- **Solution**: Check Client Secret value

#### **"Access denied"**
- **Solution**: Verify API permissions are granted

## 📞 **Need Help?**

If you encounter issues:
1. **Check Azure AD permissions**
2. **Verify admin consent**
3. **Test connection**
4. **Review error logs**
5. **Contact Azure AD administrator**

## 🎉 **Success Checklist**

- [ ] Azure AD app registered
- [ ] Client ID obtained
- [ ] Client secret created
- [ ] API permissions added
- [ ] Admin consent granted
- [ ] Environment variables updated
- [ ] Connection tested
- [ ] Sync completed
- [ ] Data verified

**You're ready to go!** 🚀
