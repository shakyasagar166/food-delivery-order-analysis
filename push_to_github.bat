@echo off
title Push Food Delivery Project to GitHub
color 0A
echo ======================================================================
echo       🍔 FOOD DELIVERY ORDER ANALYSIS - GITHUB PUSH WIZARD
echo ======================================================================
echo.

:: Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/ and try again.
    pause
    exit /b
)

cd /d "%~dp0"

echo [1/5] Initializing Git repository...
if not exist ".git" (
    git init
) else (
    echo Git repository already initialized.
)

echo.
echo [2/5] Staging all project files...
git add .

echo.
echo [3/5] Creating commit...
git commit -m "feat: complete food delivery analytics platform (MySQL, Excel, Power BI, Web App)"

echo.
echo [4/5] Setting main branch...
git branch -M main

echo.
echo ======================================================================
echo Step 1: Go to https://github.com/new
echo Step 2: Create a new repository named: food-delivery-order-analysis
echo Step 3: Copy the HTTPS repository URL
echo         (Example: https://github.com/your-username/food-delivery-order-analysis.git)
echo ======================================================================
echo.

set /p REPO_URL="Enter your GitHub Repository URL: "

if "%REPO_URL%"=="" (
    echo [ERROR] Repository URL cannot be empty.
    pause
    exit /b
)

echo.
echo [5/5] Adding remote and pushing to GitHub...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo Pushing code to %REPO_URL% ...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo  SUCCESS! Your project is now live on GitHub!
    echo ======================================================================
) else (
    echo.
    echo [NOTE] If push failed due to authentication, please log in to GitHub in your browser/terminal.
)

echo.
pause
