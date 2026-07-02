@echo off
setlocal

echo ==========================================
echo Building JumpServer Web (FA)
echo ==========================================
echo.

cd /d "%~dp0..\lina"

if errorlevel 1 (
    echo Failed to enter lina directory.
    pause
    exit /b 1
)

call npm run build

if errorlevel 1 (
    echo.
    echo npm build FAILED.
    pause
    exit /b 1
)

docker build -f Dockerfile-simple -t jumpserver/web:v4.10.16-ce-fa .

if errorlevel 1 (
    echo.
    echo Docker build FAILED.
    pause
    exit /b 1
)

echo.
echo Web image built successfully.
pause