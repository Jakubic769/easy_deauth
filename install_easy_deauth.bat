@echo off
setlocal
title Easy WiFi Lab - Installer
set "C=[36m"
set "G=[32m"
set "R=[31m"
set "D=[90m"
set "X=[0m"
set "B=[1m"
cls
echo.
echo %C%%B%   EASY WIFI LAB%X%
echo   %D%Professional WSL installer%X%
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
