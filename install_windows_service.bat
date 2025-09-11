@echo off
echo ========================================
echo Installing Django AssetTrack as Windows Service
echo ========================================

echo.
echo Step 1: Installing NSSM (Non-Sucking Service Manager)...
echo Downloading NSSM...
powershell -Command "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'"
powershell -Command "Expand-Archive -Path 'nssm.zip' -DestinationPath '.' -Force"

echo.
echo Step 2: Installing the service...
nssm-2.24\win64\nssm.exe install DjangoAssetTrack
nssm-2.24\win64\nssm.exe set DjangoAssetTrack Application "python"
nssm-2.24\win64\nssm.exe set DjangoAssetTrack AppDirectory "%cd%"
nssm-2.24\win64\nssm.exe set DjangoAssetTrack AppParameters "manage.py runserver 0.0.0.0:8000 --settings=assettrack_django.settings_production"
nssm-2.24\win64\nssm.exe set DjangoAssetTrack DisplayName "Django AssetTrack"
nssm-2.24\win64\nssm.exe set DjangoAssetTrack Description "Django AssetTrack Application"
nssm-2.24\win64\nssm.exe set DjangoAssetTrack Start SERVICE_AUTO_START

echo.
echo Step 3: Starting the service...
nssm-2.24\win64\nssm.exe start DjangoAssetTrack

echo.
echo Service installed successfully!
echo The application will now start automatically when Windows starts.
echo.
echo To manage the service:
echo - Start: nssm-2.24\win64\nssm.exe start DjangoAssetTrack
echo - Stop: nssm-2.24\win64\nssm.exe stop DjangoAssetTrack
echo - Remove: nssm-2.24\win64\nssm.exe remove DjangoAssetTrack confirm

pause
