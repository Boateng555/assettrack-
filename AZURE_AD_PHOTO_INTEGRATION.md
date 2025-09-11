# Azure AD Photo Integration

This document explains how to use the Azure AD photo integration feature in AssetTrack.

## Overview

The Azure AD photo integration allows AssetTrack to display actual employee profile pictures from Azure Active Directory instead of placeholder images. When an employee has a profile picture uploaded to Azure AD, it will automatically be displayed in the AssetTrack interface.

## Features

- **Automatic Photo Sync**: Employee photos are automatically synced during Azure AD synchronization
- **Fallback Support**: If no Azure AD photo is available, falls back to stored avatar URL or default placeholder
- **Caching**: Photos are cached for 1 hour to improve performance
- **Secure Access**: Photos are served through a secure proxy that requires authentication

## How It Works

1. **Photo Detection**: During Azure AD sync, the system checks if each user has a profile photo
2. **URL Storage**: If a photo exists, the Azure AD photo URL is stored in the employee's `avatar_url` field
3. **Template Filter**: A custom template filter (`employee_avatar_url`) determines which photo to display
4. **Photo Proxy**: A Django view serves the photos securely, handling authentication with Azure AD

## Setup

### 1. Azure AD Configuration

Ensure your Azure AD integration is properly configured in your Django settings:

```python
# settings.py
AZURE_TENANT_ID = 'your-tenant-id'
AZURE_CLIENT_ID = 'your-client-id'
AZURE_CLIENT_SECRET = 'your-client-secret'
```

### 2. Required Permissions

Your Azure AD application needs the following Microsoft Graph permissions:
- `User.Read.All` - To read user profiles and photos
- `User.ReadWrite.All` - To read and write user data (if needed)

## Usage

### Automatic Sync

Photos are automatically synced when you run the Azure AD sync:

```bash
python manage.py azure_ad_sync
```

### Manual Photo Sync

To manually sync photos for existing employees:

```bash
# Sync all employees with Azure AD IDs
python manage.py sync_azure_photos

# Force sync all employees (even those with existing photos)
python manage.py sync_azure_photos --force

# Sync a specific employee
python manage.py sync_azure_photos --employee-id <employee-uuid>
```

### Testing

Run the test script to verify the integration:

```bash
python test_azure_photos.py
```

## Template Usage

The photo integration is automatically used in all templates. The custom filter `employee_avatar_url` handles the logic:

```html
{% load employee_filters %}

<!-- This will show Azure AD photo if available, otherwise fallback -->
<img src="{{ employee|employee_avatar_url }}" alt="{{ employee.name }}">
```

## API Endpoints

### Employee Photo Endpoint

- **URL**: `/employees/{employee_id}/photo/`
- **Method**: GET
- **Authentication**: Required
- **Description**: Serves the employee's photo from Azure AD

## Troubleshooting

### Common Issues

1. **No Photos Displaying**
   - Check if Azure AD integration is properly configured
   - Verify that users have profile pictures uploaded to Azure AD
   - Check the application permissions in Azure AD

2. **Permission Errors**
   - Ensure your Azure AD app has the required Microsoft Graph permissions
   - Check that the client secret is valid and not expired

3. **Performance Issues**
   - Photos are cached for 1 hour by default
   - Consider implementing additional caching if needed

### Debugging

Enable debug logging to see detailed information:

```python
# settings.py
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

- Photos are served through an authenticated proxy view
- Access tokens are cached and refreshed automatically
- No sensitive data is logged
- Photos are served with appropriate cache headers

## Future Enhancements

Potential improvements for the photo integration:

1. **Local Storage**: Store photos locally instead of proxying from Azure AD
2. **Image Optimization**: Resize and compress photos for better performance
3. **Batch Processing**: Process multiple photos in parallel
4. **Photo Upload**: Allow users to upload photos directly to AssetTrack
5. **Photo Management**: Add interface for managing employee photos

## Support

For issues with the Azure AD photo integration:

1. Check the troubleshooting section above
2. Review the Azure AD integration logs
3. Test with the provided test script
4. Contact the development team with specific error messages
