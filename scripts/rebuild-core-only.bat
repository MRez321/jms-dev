@echo off
setlocal

cd /d "%~dp0..\core"

docker build -t jumpserver/core:v4.10.16-ce-fa .

if errorlevel 1 (
    pause
    exit /b 1
)

cd /d "%~dp0.."

docker compose -f docker-compose-fa.yml up -d --no-deps --force-recreate core celery

echo.
echo Done.
pause