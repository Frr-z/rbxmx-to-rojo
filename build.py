"""
Build script to create executable using PyInstaller
"""
import os
import sys
import subprocess
from pathlib import Path


def build_executable():
    """Build the executable using PyInstaller"""
    print("Building RBXMX to Rojo Converter executable...")
    
    # Get paths
    current_dir = Path(__file__).parent
    src_dir = current_dir / "src"
    main_file = src_dir / "main.py"
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # GUI application (no console window)
        "--name=rbxmx-to-rojo",  # Name of the executable
        "--clean",  # Clean cache before building
        str(main_file)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, cwd=current_dir)
        print("\n✓ Build completed successfully!")
        print(f"Executable can be found in: {current_dir / 'dist' / 'rbxmx-to-rojo.exe'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}")
        return False
    except FileNotFoundError:
        print("\n✗ PyInstaller not found. Please install it first:")
        print("  pip install pyinstaller")
        return False


if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
