@echo off
setlocal

call "%~dp0build-core-fa.bat"
if errorlevel 1 exit /b 1

call "%~dp0build-web-fa.bat"
if errorlevel 1 exit /b 1

echo.
echo ==========================================
echo Everything built successfully.
echo ==========================================
pause