@echo off
setlocal

cd /d "%~dp0..\lina"

call npm run build
if errorlevel 1 (
    pause
    exit /b 1
)

docker build -f Dockerfile-simple -t jumpserver/web:v4.10.16-ce-fa .

if errorlevel 1 (
    pause
    exit /b 1
)

cd /d "%~dp0.."

docker compose -f docker-compose-fa.yml up -d --no-deps --force-recreate web

echo.
echo Done.
pause