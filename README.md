# GpioCalculator

A lightweight, cross-platform GUI tool designed for embedded systems developers to calculate GPIO pin numbers across mainstream ARM-based SoC platforms (i.MX, Rockchip, Allwinner). It supports bidirectional GPIO calculation and auto-generates Linux GPIO sysfs commands for rapid hardware integration.

## Key Features

- **Multi-SoC Compatibility**: Full support for i.MX, Rockchip, and Allwinner SoC GPIO numbering schemes  
- **Bidirectional Calculation**:
  - **Forward**: Convert GPIO group/port/index to a numerical GPIO pin number  
  - **Reverse**: Resolve a numerical GPIO pin number back to a human-readable GPIO name  
- **Linux GPIO Command Generator**:
  - Export GPIO
  - Set GPIO direction (input/output)
  - Set output level (high/low)
  - Read GPIO input value
- **User-Friendly Interface**: Clean and intuitive GUI with dropdown selections and one-click operations  
- **Portable Executable**: Can be built as a single standalone Windows EXE without requiring a Python runtime  
- **Custom Icon Support**: Includes a calculator-style application icon for desktop integration  

## Prerequisites

### Run from Source

- **Python 3.8+**
  - Download from: https://www.python.org/downloads/
  - Ensure *Add Python to PATH* is enabled during installation
- **Tkinter**
  - Included with standard Python distributions (no extra installation required)

### Build Executable (Windows)

- **PyInstaller**
  ```bash
  pip install pyinstaller
  ```

## Installation & Quick Start

### Clone the Repository

```bash
git clone https://github.com/mgkiller7/GpioCalculator.git
cd GpioCalculator
```

### Run from Source

```bash
python GpioCalculator.py
```

## Build Standalone Executable (Windows)

### Manual Build Command

```bash
pyinstaller --onefile --windowed --icon=icon/icon.ico --add-data="icon/icon.ico;." --name GpioCalculator GpioCalculator.py
```

### One-Click Build Script

A pre-written batch script is included:

```bash
Build_GpioCalculator.bat
```

The script will:
- Check Python and PyInstaller availability
- Install PyInstaller if missing
- Build the executable automatically

### Build Output

```text
GpioCalculator/dist/GpioCalculator.exe
```

## Usage Guide

1. **Launch**
   - Run `GpioCalculator.py` (Python) or `GpioCalculator.exe` (Windows)

2. **Select SoC Platform**
   - i.MX
   - Rockchip
   - Allwinner

3. **Choose Calculation Mode**
   - **Forward**: Select GPIO group/port/index to calculate GPIO number
   - **Backward**: Enter GPIO number to resolve GPIO name

4. **Generate GPIO Commands**
   - Select command type (export, output high/low, input)
   - Click **Copy** to copy the generated sysfs command

5. **Exit**
   - Close the application window

## Project Structure

```text
GpioCalculator/
├── GpioCalculator.py          # Main application source code
├── icon/                      # Icon resources
│   ├── GpioCalculator.png     # Source PNG icon
│   ├── icon.ico               # Windows ICO icon
│   └── Generate_Icon.bat      # PNG-to-ICO conversion script
├── Build_GpioCalculator.bat   # One-click EXE build script
└── README.md                  # Project documentation
```

## Icon Customization

1. Replace `icon/GpioCalculator.png` with your custom PNG icon  
   - Recommended: 256x256, transparent background
2. Run the icon generation script:

```bash
cd icon
Generate_Icon.bat
```

## License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

## Acknowledgements

- **Tkinter** — Lightweight Python GUI framework  
- **PyInstaller** — Packaging Python applications into standalone executables  
- **ImageMagick** — PNG to ICO conversion (used in `Generate_Icon.bat`)  
- **ARM SoC Documentation** — GPIO numbering references from NXP, Rockchip, and Allwinner  

## Notes

- The Windows EXE build is Windows-only; Linux/macOS users should run from source
- Always verify GPIO numbering against the official SoC datasheet before hardware use
- Bug reports and feature requests are welcome via GitHub Issues
