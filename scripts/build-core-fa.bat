@echo off
setlocal

echo ==========================================
echo Building JumpServer Core (FA)
echo ==========================================
echo.

cd /d "%~dp0..\core"

if errorlevel 1 (
    echo Failed to enter core directory.
    pause
    exit /b 1
)

docker build -t jumpserver/core:v4.10.16-ce-fa .

if errorlevel 1 (
    echo.
    echo Core build FAILED.
    pause
    exit /b 1
)

echo.
echo Core image built successfully.
pause