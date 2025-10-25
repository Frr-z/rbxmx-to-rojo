@echo off
echo ========================================
echo Building Executable
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8 or higher from: https://www.python.org/
    pause
    exit /b 1
)

echo Installing PyInstaller...
python -m ensurepip --default-pip >nul 2>&1
python -m pip install --upgrade pip >nul 2>&1
python -m pip install pyinstaller

echo.
echo Building executable...
python build.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Success!
    echo ========================================
    echo Executable is at: dist\rbxmx-to-rojo.exe
    echo.
) else (
    echo.
    echo [ERROR] Failed to build executable!
)

pause
