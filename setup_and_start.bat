@echo off
echo ========================================
echo Zomato AI Recommender - Complete Setup
echo ========================================
echo.

echo Step 1: Running pre-flight checks...
python preflight_check.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Pre-flight checks failed!
    echo Please fix the issues above before continuing.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ All checks passed!
echo ========================================
echo.
echo Ready to start the server.
echo.
echo Press any key to start the API server...
pause > nul

echo.
echo Starting API server on http://localhost:8000
echo.
echo Keep this window open - it shows the server logs.
echo Open index.html in your browser to use the app.
echo Or open test_api.html to test the endpoints.
echo.
echo Press Ctrl+C to stop the server.
echo.

python -m uvicorn src.phase0.api.main:app --reload --port 8000
