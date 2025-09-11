@echo off
echo ========================================
echo Django AssetTrack Deployment Script
echo For Windows Server
echo ========================================

echo.
echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Step 2: Installing/upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 3: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 4: Collecting static files...
python manage.py collectstatic --noinput --settings=assettrack_django.settings_production

echo.
echo Step 5: Running database migrations...
python manage.py migrate --settings=assettrack_django.settings_production

echo.
echo Step 6: Creating superuser (if needed)...
echo Do you want to create a superuser? (y/n)
set /p create_super=
if /i "%create_super%"=="y" (
    python manage.py createsuperuser --settings=assettrack_django.settings_production
)

echo.
echo Step 7: Getting server IP address...
ipconfig | findstr "IPv4"
echo.
echo Please note the IP address above and update your settings_production.py file
echo with the correct IP address in ALLOWED_HOSTS.

echo.
echo Step 8: Starting the server...
echo The server will start on http://0.0.0.0:8000
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver 0.0.0.0:8000 --settings=assettrack_django.settings_production

pause
