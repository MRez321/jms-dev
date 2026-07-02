@echo off
setlocal

echo ==========================================
echo JumpServer FA Deploy
echo ==========================================
echo.

REM ==========================================================
REM Build Core
REM ==========================================================

echo [1/4] Building Core...
cd /d "%~dp0..\core"

docker build -t jumpserver/core:v4.10.16-ce-fa .

if errorlevel 1 (
    echo.
    echo *************************************
    echo Core build FAILED
    echo *************************************
    pause
    exit /b 1
)

REM ==========================================================
REM Build Web
REM ==========================================================

echo.
echo [2/4] Building Web...
cd /d "%~dp0..\lina"

call npm run build

if errorlevel 1 (
    echo.
    echo *************************************
    echo npm build FAILED
    echo *************************************
    pause
    exit /b 1
)

docker build -f Dockerfile-simple -t jumpserver/web:v4.10.16-ce-fa .

if errorlevel 1 (
    echo.
    echo *************************************
    echo Web Docker build FAILED
    echo *************************************
    pause
    exit /b 1
)

REM ==========================================================
REM Recreate only modified containers
REM ==========================================================

echo.
echo [3/4] Restarting modified containers...

cd /d "%~dp0.."

docker compose -f docker-compose-fa.yml up -d --no-deps --force-recreate core celery web

if errorlevel 1 (
    echo.
    echo *************************************
    echo Docker recreate FAILED
    echo *************************************
    pause
    exit /b 1
)

REM ==========================================================
REM Show status
REM ==========================================================

echo.
echo [4/4] Current container status...
docker compose -f docker-compose-fa.yml ps

echo.
echo ==========================================
echo Deployment completed successfully.
echo ==========================================
echo.
echo Web UI:
echo http://localhost:8180
echo.
pause