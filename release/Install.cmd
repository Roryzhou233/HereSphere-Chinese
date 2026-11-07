@echo off
setlocal
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-Chinese.ps1" %*
set "patchExitCode=%errorlevel%"
pause
exit /b %patchExitCode%
