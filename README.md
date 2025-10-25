# RBXMX to Rojo Converter

A desktop application to convert RBXMX (Roblox Model XML) files to Rojo projects.

## Features

- 🎯 Convert RBXMX files to Rojo project structure
- 📁 Automatically generates `.lua` files from scripts
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

1. Click "Select RBXMX File" and choose your `.rbxmx` file
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

## How to Get RBXMX Files

In Roblox Studio:
1. Open your game/place
2. Select the model you want to export
3. Go to **File → Save to File As...**
4. Choose **"Model Files (*.rbxmx)"**
5. Save the file

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

- `.rbxmx` - Roblox Model XML (recommended)
- `.rbxlx` - Roblox Place XML (also works)

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
1. Check that your RBXMX file contains scripts
2. Ensure Python 3.8+ is installed
3. Try the example file in `examples/example.rbxmx`
4. Open an issue on GitHub with details

## Star History

If this project helped you, consider giving it a ⭐ on GitHub!
