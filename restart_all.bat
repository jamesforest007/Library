@echo off
echo Restarting all services...

REM Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Administrator privileges required
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d """%~dp0""" && %~nx0' -Verb RunAs"
    exit /b
)

REM 1. Stop all services
echo Stopping services...
net stop w3svc 2>nul
taskkill /F /IM nginx.exe /T >nul 2>&1
taskkill /F /IM waitress-serve.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM 2. Copy static files
echo Copying static files...
mkdir C:\nginx\html\static 2>nul
xcopy /E /Y "app\static\*" "C:\nginx\html\static\"

REM 3. Start Waitress
echo Starting Waitress...
call venv\Scripts\activate.bat
set FLASK_ENV=development
set SECRET_KEY=your-secret-key-here
start /B waitress-serve --listen=127.0.0.1:8000 --call "app:create_app"

REM 4. Wait for Waitress to start
echo Waiting for Waitress...
timeout /t 2 /nobreak >nul

REM 5. Start Nginx
echo Starting Nginx...
cd /d C:\nginx
nginx.exe

echo.
echo All services restarted!
echo Visit http://localhost 