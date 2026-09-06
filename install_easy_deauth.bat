@echo off
setlocal

echo ==========================================
echo        Easy WiFi Lab Installer
echo ==========================================
echo.

where wsl.exe >nul 2>&1
if errorlevel 1 (
    echo WSL is not installed.
    echo Install it from an elevated PowerShell with:
    echo.
    echo     wsl --install
    echo.
    pause
    exit /b 1
)

echo Launching the Linux installer inside WSL...
echo NOTE: Wi-Fi monitor mode requires a compatible Wi-Fi adapter
echo       exposed to the Linux environment.
echo.

wsl.exe bash -lc "mkdir -p /tmp/easy_deauth_install && echo 'Copy the project ZIP contents into WSL, then run install_easy_deauth.sh.'"

echo.
echo The BAT bootstrap is ready.
echo For native Linux, run:
echo     bash install_easy_deauth.sh
echo.
pause
