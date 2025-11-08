# windfall
A cross-platform SD card manager for the Nintendo Wii, built with a Python GUI and a C/C++ core

---

## Overview
Windfall handles the annoying parts of Wii SD card setup so you don’t have to. Essentially, the "heavy lifting".
It detects your SD card, analyzes your homebrew files, and helps you organize everything safely—without messy manual sorting.

The project is a blend of C++/C and Python.

<p align="center">
  <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/piarsquared/windfall/:workflow">
  <img alt="Platforms" src="https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-blue?style=for-the-badge">
  <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/piarsquared/windfall?style=for-the-badge">
  <img alt="GitHub License" src="https://img.shields.io/github/license/piarsquared/windfall">
</p>

---

## Features
- **SD Card Auto-Detection**  
  Finds connected SD cards across Windows, Linux, and macOS.

- **Homebrew Folder Validation**  
  Checks for required folders (`apps`, `wads`, etc.) and warns about missing or misplaced files.

- **File Movement Preview**  
  Shows exactly what’s being moved where before anything is written.

- **Safe Mode**  
  Copies files without overwriting anything unless you approve it.

- **Cross-Platform Support**  
  Designed to run on Windows, Linux, and macOS.
  Primarily tested on Windows and Linux.

- **Modern GUI**  
  A clean, lightweight interface built with CustomTkinter.

---

## Getting Started

### Download
You can find compiled releases for each platform on the project’s releases page.

### Run Windfall
- Windows: run the packaged executable  
- Linux/macOS: run the Python entry script or download the compiled build

### Requirements

For libraries, please view `requirements.txt` in the primary directory.

- Python 3.11+ (for source installs)
- A FAT32-formatted SD or SDHC card
- Basic permissions to access removable storage

---

## Roadmap
Planned and experimental features:

- [ ] Wii NAND backup mover

- [ ] Homebrew app metadata viewer (reading meta.xml)

- [ ] Plugin system for advanced file rules

- [ ] Auto-download and install common homebrew packages

---

## Contributing

### Tech Stack
- **GUI:** Python (CustomTkinter)  
- **Core Logic:** C / C++  
- **Bindings:** ctypes or cffi (subject to change)

### Building the Native Backend
Instructions (will vary per platform):
- Clone repository
- Build C/C++ library with your compiler of choice
- Place the resulting shared library (`.dll`, `.so`, `.dylib`) in the `/core` directory
- Python will pick it up automatically on launch

Pull requests are welcome. Bug fixes, new features, and platform testing all help.

