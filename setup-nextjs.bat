@echo off
echo ============================================================
echo Setting up Next.js Frontend for Zomato AI Recommender
echo ============================================================

cd /d "%~dp0"

echo.
echo Step 1: Creating Next.js project with TypeScript...
echo.

npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*" --no-git

if %ERRORLEVEL% NEQ 0 (
    echo Failed to create Next.js project
    pause
    exit /b 1
)

cd frontend

echo.
echo Step 2: Installing additional dependencies...
echo.

npm install axios

echo.
echo Step 3: Creating project structure...
echo.

mkdir components 2>nul
mkdir lib 2>nul
mkdir types 2>nul
mkdir public\images 2>nul

echo.
echo ============================================================
echo Next.js frontend setup complete!
echo ============================================================
echo.
echo Next steps:
echo 1. cd frontend
echo 2. Copy the component files (will be provided)
echo 3. npm run dev
echo.
pause
