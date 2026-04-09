@echo off
echo ========================================
echo   ZOMATO AI RECOMMENDER - QUICK START
echo ========================================
echo.

REM Check if backend is running
echo [1/3] Checking backend status...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is running on http://localhost:8000
) else (
    echo ❌ Backend is NOT running!
    echo.
    echo Starting backend server...
    start cmd /c "cd /d "%~dp0" && start_server.bat"
    echo Waiting for backend to start...
    timeout /t 5 /nobreak >nul
)

echo.
echo [2/3] Checking Next.js status...
netstat -an | findstr ":3000" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Next.js is already running
    echo.
    echo Restarting to pick up latest changes...
    taskkill /F /IM node.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
)

echo.
echo [3/3] Starting Next.js frontend...
cd /d "%~dp0frontend"
start cmd /k "npm run dev"

echo.
echo ========================================
echo   🎉 STARTUP COMPLETE!
echo ========================================
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo Wait 10-15 seconds for Next.js to compile...
echo Then open http://localhost:3000 in your browser
echo.
echo Press any key to open browser automatically...
pause >nul

start http://localhost:3000

echo.
echo ✅ Browser opened! Enjoy your AI recommender!
echo.
pause
