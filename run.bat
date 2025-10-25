@echo off
echo ========================================
echo RBXMX to Rojo Converter - Quick Start
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

echo [1/3] Installing dependencies...
python -m ensurepip --default-pip >nul 2>&1
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    echo Try running: python -m ensurepip --default-pip
    pause
    exit /b 1
)

echo [2/3] Creating example file...
python create_example.py

echo [3/3] Starting application...
echo.
python src\main.py

pause
