@echo off
setlocal
title Easy WiFi Lab - Installer
for /f "tokens=2 delims==" %%A in ('"wmic os get LocalDateTime /value" 2^>nul') do set "DT=%%A"
set "C=[36m"
set "G=[32m"
set "R=[31m"
set "D=[90m"
set "X=[0m"
set "B=[1m"
cls
echo.
echo %C%%B%   ███████╗ █████╗ ███████╗██╗   ██╗
echo   ██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝
echo   █████╗  ███████║███████╗ ╚████╔╝
echo   ██╔══╝  ██╔══██║╚════██║  ╚██╔╝
echo   ██║     ██║  ██║███████║   ██║
echo   ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝%X%
echo.
echo   %B%Easy WiFi Lab%X% %D%• WSL installer%X%
echo   %D%────────────────────────────────────────────────────────────%X%
echo.
where wsl.exe >nul 2>&1
if errorlevel 1 (
  echo   %R%[ERROR]%X% WSL is not installed.
  echo.
  pause
  exit /b 1
)
echo   %C%[INFO]%X% WSL detected.
echo   %G%[OK]%X% Windows launcher is ready.
echo.
echo   %D%Run install_easy_deauth.sh inside your WSL project directory.%X%
echo.
pause
