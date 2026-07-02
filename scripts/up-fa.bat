@echo off

cd /d "%~dp0.."

docker compose -f docker-compose-fa.yml up -d

pause