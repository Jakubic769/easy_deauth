@echo off
setlocal
title Easy WiFi Lab - Launcher
set "C=[36m"
set "G=[32m"
set "R=[31m"
set "D=[90m"
set "X=[0m"
set "B=[1m"
cls
echo.
echo %C%%B%   EASY WIFI LAB%X%
echo   %D%Passive Wi-Fi discovery ^| launcher%X%
echo   %D%────────────────────────────────────────────────────────────%X%
echo.
where wsl.exe >nul 2>&1
if errorlevel 1 (
  echo   %R%[ERROR]%X% WSL is not installed.
  pause
  exit /b 1
)
echo   %C%[INFO]%X% Starting Easy WiFi Lab...
echo.
wsl.exe bash -lc "command -v easy_deauth >/dev/null 2>&1 && easy_deauth || { echo '[ERROR] easy_deauth is not installed.'; echo 'Run install_easy_deauth.sh first.'; exit 1; }"
if errorlevel 1 (
  echo.
  echo   %R%[ERROR]%X% Easy WiFi Lab exited with an error.
) else (
  echo.
  echo   %G%[OK]%X% Easy WiFi Lab finished.
)
echo.
pause
