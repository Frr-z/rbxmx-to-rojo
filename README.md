# RBXMX to Rojo Converter

A desktop application to convert Roblox files (RBXMX, RBXLX, RBXM, RBXL) to Rojo projects.

## Features

- 🎯 Convert Roblox files to Rojo project structure
- 📁 Supports multiple formats: **RBXMX, RBXLX, RBXM, RBXL**
- 🏗️ Handles both **models** and **entire place files**
- 📝 Automatically generates `.lua` files from scripts
- 🔧 Creates necessary `meta.json` files
- 📦 Generates `default.project.json` for Rojo
- 🖥️ User-friendly GUI interface
- ⚡ Fast conversion process

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

#### Windows
```bash
# Run the quick start script
run.bat
```

#### Linux/macOS
```bash
# Make the script executable
chmod +x run.sh

# Run it
./run.sh
```

### Manual Installation

1. Clone or download this repository
2. Install dependencies:

```bash
# Windows
python -m pip install -r requirements.txt

# Linux/macOS
python3 -m pip install -r requirements.txt

# Optional: For binary file support (.rbxm/.rbxl)
python -m pip install rbx-binary

# If you don't have pip:
# Ubuntu/Debian: sudo apt install python3-pip
# Fedora: sudo dnf install python3-pip
# macOS: pip should come with Python
```

3. Run the application:

```bash
# Windows
python src/main.py

# Linux/macOS
python3 src/main.py
```

## Usage

### Run the Application

```bash
# Windows
python src/main.py

# Linux/macOS
python3 src/main.py
```

### Steps to Convert

1. Click "Select File" and choose your Roblox file (`.rbxmx`, `.rbxlx`, `.rbxm`, or `.rbxl`)
2. Click "Select Output Folder" to choose where the project will be created
3. Click "Convert" and wait for completion
4. Use the generated project with Rojo!

## Building Executable

To create a standalone executable:

**Windows:**
```bash
build.bat
```

**Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

**Manual Build:**
```bash
# Windows
python -m pip install pyinstaller
python build.py

# Linux/macOS
python3 -m pip install pyinstaller
python3 build.py
```

The executable will be created in the `dist/` folder.

## How to Get Roblox Files

### For Models:
In Roblox Studio:
1. Open your game/place
2. Select the model you want to export
3. Go to **File → Save to File As...**
4. Choose format:
   - **"Model Files (*.rbxmx)"** - XML format (recommended)
   - **"Model Files (*.rbxm)"** - Binary format

### For Entire Places:
In Roblox Studio:
1. Open your place/game
2. Go to **File → Save to File As...**
3. Choose format:
   - **"Place Files (*.rbxlx)"** - XML format (recommended)
   - **"Place Files (*.rbxl)"** - Binary format
4. Save the file

**Note:** XML formats (`.rbxmx`, `.rbxlx`) work out of the box. Binary formats (`.rbxm`, `.rbxl`) require the `rbx-binary` package.

## Project Structure Output

After conversion, you'll have:

```
project-name/
├── default.project.json    # Rojo configuration
└── src/                    # Source code
    ├── Script.server.lua
    ├── LocalScript.client.lua
    └── ModuleScript.lua
```

## Using with Rojo

After conversion:

1. Install Rojo: [rojo.space](https://rojo.space/)
2. Navigate to the project folder
3. Run:
   ```bash
   rojo serve
   ```
4. Install the Rojo plugin in Roblox Studio
5. Click "Connect" in the plugin
6. Your changes will sync automatically!

## Requirements

- Python 3.8+
- tkinter (usually included with Python)

## Supported Formats

| Format | Type | Description | Support |
|--------|------|-------------|---------|
| `.rbxmx` | Model (XML) | Roblox Model XML | ✅ Full Support |
| `.rbxlx` | Place (XML) | Roblox Place XML | ✅ Full Support |
| `.rbxm` | Model (Binary) | Roblox Model Binary | ⚠️ Requires rbx-binary |
| `.rbxl` | Place (Binary) | Roblox Place Binary | ⚠️ Requires rbx-binary |

**Recommended:** Use XML formats (`.rbxmx` or `.rbxlx`) for best compatibility.

## What Gets Converted

✅ **Converted:**
- Scripts (server-side)
- LocalScripts (client-side)
- ModuleScripts
- Folder hierarchy containing scripts
- Script source code

❌ **Not Converted:**
- Visual properties (Position, Color, Size, etc.)
- Parts without scripts
- Terrain
- Meshes and textures
- UI elements (unless they contain scripts)

The converter focuses on extracting **code and script structure** for Rojo-based development.

## References

- [RBXMX File Format](https://fileinfo.com/extension/rbxmx)
- [Rojo Documentation](https://rojo.space/docs/v7/)
- [rbxlx-to-rojo (Original Rust implementation)](https://github.com/rojo-rbx/rbxlx-to-rojo)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the original [rbxlx-to-rojo](https://github.com/rojo-rbx/rbxlx-to-rojo) Rust implementation
- Built for the Roblox developer community

## Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

## Support

If you encounter any issues:
1. Check that your file contains scripts
2. Ensure Python 3.8+ is installed
3. For binary files (`.rbxm`/`.rbxl`), install: `pip install rbx-binary`
4. Try the example file in `examples/example.rbxmx`
5. Open an issue on GitHub with details

## Star History

If this project helped you, consider giving it a ⭐ on GitHub!
