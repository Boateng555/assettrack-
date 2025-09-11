@echo off
echo ========================================
echo Configuring Windows Firewall for Django
echo ========================================

echo.
echo Step 1: Adding inbound rule for Django application...
netsh advfirewall firewall add rule name="Django AssetTrack HTTP" dir=in action=allow protocol=TCP localport=8000

echo.
echo Step 2: Adding outbound rule for Django application...
netsh advfirewall firewall add rule name="Django AssetTrack HTTP Out" dir=out action=allow protocol=TCP localport=8000

echo.
echo Step 3: Verifying rules were added...
netsh advfirewall firewall show rule name="Django AssetTrack HTTP"
netsh advfirewall firewall show rule name="Django AssetTrack HTTP Out"

echo.
echo Firewall configuration completed!
echo Your Django application should now be accessible from other computers.
echo.
echo To remove these rules later, use:
echo netsh advfirewall firewall delete rule name="Django AssetTrack HTTP"
echo netsh advfirewall firewall delete rule name="Django AssetTrack HTTP Out"

pause
