# PowerShell script to get server information for Django deployment
Write-Host "========================================" -ForegroundColor Green
Write-Host "Windows Server Information for Django Deployment" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`n1. Server Name:" -ForegroundColor Yellow
Write-Host $env:COMPUTERNAME

Write-Host "`n2. Operating System:" -ForegroundColor Yellow
Get-WmiObject -Class Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture

Write-Host "`n3. Network Adapters and IP Addresses:" -ForegroundColor Yellow
Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | ForEach-Object {
    Write-Host "Adapter: $($_.Name)" -ForegroundColor Cyan
    Write-Host "  Status: $($_.Status)"
    Write-Host "  Interface: $($_.InterfaceDescription)"
    
    $ipConfig = Get-NetIPAddress -InterfaceIndex $_.ifIndex -AddressFamily IPv4
    if ($ipConfig) {
        Write-Host "  IPv4 Address: $($ipConfig.IPAddress)" -ForegroundColor Green
        Write-Host "  Subnet Mask: $($ipConfig.PrefixLength)"
    }
    
    $gateway = Get-NetRoute -InterfaceIndex $_.ifIndex -AddressFamily IPv4 | Where-Object {$_.NextHop -ne "0.0.0.0"}
    if ($gateway) {
        Write-Host "  Gateway: $($gateway.NextHop)"
    }
    Write-Host ""
}

Write-Host "`n4. Firewall Status:" -ForegroundColor Yellow
$firewall = Get-NetFirewallProfile
foreach ($profile in $firewall) {
    Write-Host "$($profile.Name): $($profile.Enabled)"
}

Write-Host "`n5. Python Installation Check:" -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python: Not installed or not in PATH" -ForegroundColor Red
}

Write-Host "`n6. Port 8000 Status:" -ForegroundColor Yellow
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000) {
    Write-Host "Port 8000 is in use by:" -ForegroundColor Red
    $port8000 | ForEach-Object {
        Write-Host "  Process ID: $($_.OwningProcess)"
        $process = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "  Process Name: $($process.ProcessName)"
        }
    }
} else {
    Write-Host "Port 8000 is available" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Deployment Instructions:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "1. Copy your Django project to this server"
Write-Host "2. Update the IP address in settings_production.py"
Write-Host "3. Run deploy_windows_server.bat"
Write-Host "4. Or install as Windows Service using install_windows_service.bat"
Write-Host "5. Configure Windows Firewall to allow port 8000"
Write-Host "6. Access your application at http://[SERVER_IP]:8000"

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
