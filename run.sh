#!/bin/bash
echo "========================================"
echo "RBXMX to Rojo Converter - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python 3 not found!"
    echo "Please install Python 3.8 or higher"
    echo ""
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "Fedora: sudo dnf install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

echo "[1/3] Installing dependencies..."
python3 -m pip install --upgrade pip > /dev/null 2>&1
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    echo "Try running: sudo apt install python3-pip"
    exit 1
fi

echo "[2/3] Creating example file..."
python3 create_example.py

echo "[3/3] Starting application..."
echo ""
python3 src/main.py
