@echo off
REM Ayodhya Ramnagri Tourism - Environment Verification Script

echo.
echo ================================================
echo   Deployment Verification Check
echo ================================================
echo.

echo [1] Checking .env file...
if exist ".env" (
    echo OK - .env file found
    for /f "tokens=*" %%a in ('type ".env" ^| findstr /i "DATABASE_URL"') do (
        echo OK - DATABASE_URL is configured
    )
) else (
    echo ERROR - .env file NOT found
    echo   Please run: copy .env.example .env
    echo   Then update with your credentials
)

echo.
echo [2] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo OK - Python is installed
    python --version
) else (
    echo ERROR - Python is NOT installed
    echo   Download from: https://www.python.org/downloads/
)

echo.
echo [3] Checking backend dependencies...
if exist "backend\requirements.txt" (
    echo OK - backend\requirements.txt found
) else (
    echo ERROR - backend\requirements.txt NOT found
)

echo.
echo [4] Checking backend files...
if exist "backend\database.py" (
    echo OK - backend\database.py found
) else (
    echo ERROR - backend\database.py NOT found
)

if exist "backend\main.py" (
    echo OK - backend\main.py found
) else (
    echo ERROR - backend\main.py NOT found
)

echo.
echo [5] Checking frontend files...
if exist "index.html" (
    echo OK - index.html found
) else (
    echo ERROR - index.html NOT found
)

if exist "pages\booking.html" (
    echo OK - pages\booking.html found
) else (
    echo ERROR - pages\booking.html NOT found
)

echo.
echo ================================================
echo   Next steps:
echo   1. Ensure MySQL is running
echo   2. Run: start-backend.bat
echo   3. Run: start-frontend.bat
echo   4. Open: http://localhost:5500
echo ================================================
echo.

pause
