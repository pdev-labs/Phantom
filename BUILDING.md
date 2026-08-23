# Building Phantom from Source

This guide explains how to manually build the Phantom standalone desktop binaries (Prank 2) and the Android APKs from source on your own machine.

---

## 1. Prerequisites

Regardless of your operating system, you will need:
- **Python 3.10 or higher** installed and added to your system PATH.
- **Git** (to clone the repository).

First, clone the repository:
```bash
git clone https://github.com/pdev-labs/Phantom.git
cd Phantom
```

---

## 2. Building Desktop Binaries (Windows, macOS, Linux)

We use `PyInstaller` to package the Python script into a standalone executable that doesn't require Python to be installed on the victim's machine.

### Windows (.exe)
1. Open PowerShell or Command Prompt.
2. Navigate to the `prank_2_input_trigger` directory:
   ```cmd
   cd prank_2_input_trigger
   ```
3. Install dependencies:
   ```cmd
   pip install pynput pyinstaller
   ```
4. Build the executable:
   ```cmd
   pyinstaller --onefile --noconsole --add-data "*.mp3;." prank_input.py
   ```
5. Your standalone `.exe` will be located in the `dist\` folder.

### macOS (.app / UNIX Executable)
1. Open Terminal.
2. Navigate to the `prank_2_input_trigger` directory:
   ```bash
   cd prank_2_input_trigger
   ```
3. Install dependencies:
   ```bash
   pip3 install pynput pyinstaller
   ```
4. Build the executable:
   ```bash
   pyinstaller --onefile --noconsole --add-data "*.mp3:." prank_input.py
   ```
5. Your executable will be located in the `dist/` folder.

### Linux (AppImage / DEB / RPM)
*Note: Linux requires X11/evdev for input monitoring.*
1. Open Terminal.
2. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-dev build-essential
   ```
3. Navigate to the directory and install Python packages:
   ```bash
   cd prank_2_input_trigger
   pip3 install evdev pynput pyinstaller
   ```
4. Build the executable:
   ```bash
   pyinstaller --onefile --noconsole --add-data "*.mp3:." prank_input.py
   ```
5. Your executable will be in the `dist/` folder. (To package it further into a `.deb` or `.rpm`, refer to the commands in `.github/workflows/build.yml`).

---

## 3. Building Android APKs (Linux or macOS)

*Note: Android APK compilation using Buildozer is strictly supported on Linux and macOS. If you are on Windows, you must use WSL (Windows Subsystem for Linux).*

### Prerequisites (Ubuntu/Debian or WSL2)
Install the system dependencies required by Buildozer:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

### Install Buildozer
```bash
pip3 install --user --upgrade buildozer cython virtualenv
```
Make sure `~/.local/bin` is in your PATH.

### Compiling the APK
We have three separate Android projects. Choose one to build:
1. `prank_android_1_basic` (Simple audio looper)
2. `prank_android_2_sensors` (Hardware sensor triggers)
3. `prank_android_combined` (Mode selector app)

Navigate to the project you want to build and run Buildozer:
```bash
cd prank_android_combined
buildozer android debug
```

The first time you run this, Buildozer will automatically download the Android SDK, NDK, and configure the toolchain. This can take anywhere from 10 to 30 minutes depending on your internet connection.

Once finished, the compiled APK will be located in the `bin/` directory!
