# Phantom 👻

> [!WARNING]
> **DISCLAIMER: For Educational Purposes Only**
> This project was created strictly for educational purposes and harmless pranking. **Do NOT run these scripts on someone else's computer maliciously or without their explicit consent.**

**Phantom** is a collection of stealthy, unkillable audio prank scripts designed to run completely detached from the terminal and aggressively ignore standard termination signals like `Ctrl+C`. 

This repository contains three primary pranks:

## 1. Prank 1: Infinite Loop (`prank_1_infinite_loop`)
A cross-platform, zero-dependency script that embeds an audio payload natively within the script itself using Base64 encoding.
- **Stealthy**: Extracts the audio into a temporary system directory `/tmp/.sys_audio_cache.mp3` or `%TEMP%`.
- **Zero-Dependency**: Runs using purely native OS commands (`paplay`, `afplay`, `certutil`, `powershell`).
- **Unkillable**: Spawns a background daemon that intentionally ignores `SIGTERM`, `SIGHUP`, and `SIGINT`.
- **Supported OS**: Windows (`.bat`), macOS (`.sh`), Linux (`.sh`).

## 2. Prank 2: Input Trigger (`prank_2_input_trigger`)
A Python-based daemon that silently monitors for global inputs (specifically the `Enter` key or any mouse click) and plays a random audio file from its directory every time the user interacts with their system.
- **Cross-Platform**: Uses `pynput` for Windows/macOS.
- **Wayland Support**: Uses direct `/dev/input/` hardware event monitoring via `evdev` to bypass Linux Wayland's strict global hook security.
- **Double-Fork Daemon**: Implements a standard double-fork to completely detach from the terminal and run as an invisible background process.
- **Cooldown Safety**: Prevents audio overlap so rapid typing doesn't create a deafening wall of noise.

## 3. Prank 3: Android App (`prank_3_android`)
A standalone, harmless Android audio player built using Kivy and Python.
- **Cross-Platform Building**: Compiled in the cloud using GitHub Actions and Buildozer to avoid local Android Studio dependencies.
- **Consent-Based**: Explicit "Start" and "Stop" buttons.
- **Harmless**: Requests zero special permissions and runs completely offline.

## Installation & Usage

Please see the individual directories for specific usage instructions. 
For Prank 2, a Python virtual environment is highly recommended.

```bash
# Example for Prank 2
cd prank_2_input_trigger
python -m venv venv
./venv/bin/pip install -r requirements.txt
sudo ./venv/bin/python prank_input.py
```

## Stopping the Prank

Because these scripts are engineered to be resilient against standard user attempts to close them (`Ctrl+C` or closing the terminal), you **must** use forceful termination signals.

See the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide for exact commands to kill the phantom processes on your specific operating system.

---

*Disclaimer: This repository is for educational and comedic purposes only. Do not deploy these scripts on systems where you do not have permission or where unexpected audio playback could cause disruption to critical environments.*
