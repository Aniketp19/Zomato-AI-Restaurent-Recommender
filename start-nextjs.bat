@echo off
echo ============================================================
echo Zomato AI Recommender - Next.js Frontend Quick Start
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if frontend exists
if exist "frontend" (
    echo Frontend directory already exists!
    echo.
    choice /C YN /M "Do you want to start the existing frontend"
    if errorlevel 2 goto :EOF
    if errorlevel 1 goto START
)

echo Step 1: Creating Next.js application...
echo This may take a few minutes...
echo.

npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*" --yes

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to create Next.js app
    pause
    exit /b 1
)

cd frontend

echo.
echo Step 2: Installing additional dependencies...
npm install axios

echo.
echo Step 3: Creating project structure...
mkdir components 2>nul
mkdir lib 2>nul
mkdir types 2>nul
mkdir public\images 2>nul

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo IMPORTANT: Now copy all the component files from:
echo   - NEXTJS_COMPLETE_SETUP.md (Part 1)
echo   - NEXTJS_COMPONENTS_PART2.md (Part 2)
echo.
echo Into their respective folders:
echo   - app/layout.tsx
echo   - app/page.tsx
echo   - app/globals.css
echo   - components/*.tsx
echo   - lib/api.ts
echo   - types/index.ts
echo   - next.config.js
echo   - tailwind.config.ts
echo   - .env.local
echo.
echo Then run: npm run dev
echo.
pause
exit /b 0

:START
cd frontend
echo.
echo Starting Next.js development server...
echo.
echo Open your browser to: http://localhost:3000
echo Backend should be running on: http://localhost:8000
echo.
start http://localhost:3000
npm run dev
