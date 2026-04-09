@echo off
echo ===================================
echo  Restarting Next.js Development Server
echo ===================================
echo.

cd /d "%~dp0frontend"

echo Killing existing Next.js processes...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting Next.js dev server...
echo Server will run at http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

start /B npm run dev

echo.
echo ===================================
echo  Next.js is starting up...
echo  Check http://localhost:3000
echo ===================================
echo.

pause
