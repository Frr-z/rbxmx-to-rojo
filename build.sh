#!/bin/bash
echo "========================================"
echo "Building Executable"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python 3 not found!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Installing PyInstaller..."
python3 -m pip install --upgrade pip > /dev/null 2>&1
python3 -m pip install pyinstaller

echo ""
echo "Building executable..."
python3 build.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Success!"
    echo "========================================"
    echo "Executable is at: dist/rbxmx-to-rojo"
    echo ""
else
    echo ""
    echo "[ERROR] Failed to build executable!"
fi
