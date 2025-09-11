# Windows Server Deployment Guide for Django AssetTrack

## Prerequisites

### 1. Install Python on Windows Server
- Download Python 3.8+ from https://python.org
- During installation, check "Add Python to PATH"
- Verify installation: `python --version`

### 2. Install Visual C++ Redistributable (if needed)
- Download from Microsoft: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install if you get DLL errors

## Step-by-Step Deployment

### Step 1: Get Server Information
1. Run the PowerShell script to get server details:
   ```powershell
   powershell -ExecutionPolicy Bypass -File get_server_info.ps1
   ```
2. Note down the server's IP address (e.g., 192.168.1.100)

### Step 2: Update Configuration
1. Edit `assettrack_django/settings_production.py`
2. Replace the placeholder IP addresses with your actual server IP:
   ```python
   ALLOWED_HOSTS = [
       'localhost',
       '127.0.0.1',
       '192.168.1.100',  # Your actual server IP
       'your-domain.com',  # If you have a domain
   ]
   ```

### Step 3: Deploy the Application
1. Run the deployment script:
   ```cmd
   deploy_windows_server.bat
   ```
2. Follow the prompts to create a superuser if needed

### Step 4: Configure Firewall
1. Run the firewall configuration script:
   ```cmd
   configure_firewall.bat
   ```

### Step 5: Test the Application
1. Open a web browser
2. Navigate to: `http://[YOUR_SERVER_IP]:8000`
   - Example: `http://192.168.1.100:8000`

## Optional: Install as Windows Service

### For Automatic Startup
1. Run the service installation script:
   ```cmd
   install_windows_service.bat
   ```
2. The application will now start automatically when Windows starts

### Service Management
- Start service: `nssm-2.24\win64\nssm.exe start DjangoAssetTrack`
- Stop service: `nssm-2.24\win64\nssm.exe stop DjangoAssetTrack`
- Remove service: `nssm-2.24\win64\nssm.exe remove DjangoAssetTrack confirm`

## Manual Deployment (Alternative)

If you prefer manual deployment:

### 1. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 2. Collect Static Files
```cmd
python manage.py collectstatic --noinput --settings=assettrack_django.settings_production
```

### 3. Run Migrations
```cmd
python manage.py migrate --settings=assettrack_django.settings_production
```

### 4. Create Superuser
```cmd
python manage.py createsuperuser --settings=assettrack_django.settings_production
```

### 5. Start Server
```cmd
python manage.py runserver 0.0.0.0:8000 --settings=assettrack_django.settings_production
```

## Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   - Check what's using the port: `netstat -ano | findstr :8000`
   - Kill the process or use a different port

2. **Firewall blocking access**
   - Run `configure_firewall.bat` as Administrator
   - Or manually add firewall rules

3. **Python not found**
   - Ensure Python is installed and added to PATH
   - Restart command prompt after installation

4. **Permission denied**
   - Run scripts as Administrator
   - Check file permissions

5. **Database errors**
   - Ensure the database file is writable
   - Check if SQLite is working properly

### Logs
- Application logs: `logs/django.log`
- Windows Event Viewer: Check Application logs for service issues

## Security Considerations

1. **Change Django Secret Key**
   - Generate a new secret key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Update in settings_production.py

2. **Use HTTPS in Production**
   - Install SSL certificate
   - Update CSRF_TRUSTED_ORIGINS with HTTPS URLs
   - Set SESSION_COOKIE_SECURE = True

3. **Database Security**
   - Consider using SQL Server or PostgreSQL for production
   - Use strong database passwords

4. **Network Security**
   - Configure firewall rules properly
   - Use VPN if accessing from external networks

## Performance Optimization

1. **Use a Production WSGI Server**
   - Install waitress: `pip install waitress`
   - Run with: `waitress-serve --host=0.0.0.0 --port=8000 assettrack_django.wsgi:application`

2. **Static Files**
   - Use a web server (IIS, nginx) to serve static files
   - Configure STATIC_ROOT properly

3. **Database Optimization**
   - Use connection pooling
   - Optimize database queries

## Backup and Maintenance

1. **Database Backup**
   ```cmd
   python manage.py dumpdata > backup.json --settings=assettrack_django.settings_production
   ```

2. **Restore Database**
   ```cmd
   python manage.py loaddata backup.json --settings=assettrack_django.settings_production
   ```

3. **Regular Updates**
   - Keep Django and dependencies updated
   - Monitor security patches

## Support

If you encounter issues:
1. Check the logs in `logs/django.log`
2. Verify all prerequisites are installed
3. Ensure firewall and network settings are correct
4. Test with a simple Django application first
