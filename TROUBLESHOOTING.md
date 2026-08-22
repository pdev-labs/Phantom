# Troubleshooting & Kill Guide

Since the Phantom pranks are explicitly designed to detach from the terminal and ignore standard `Ctrl+C` termination signals, you will need to forcefully kill the background processes if you want to stop them.

## How to Kill the Pranks

### Linux
If you are running `prank_1_infinite_loop` or `prank_2_input_trigger`, open a terminal and run the following commands to send a forceful `SIGKILL` (Signal 9) which cannot be ignored by the script:

```bash
# Kill the launcher script and any python daemon
sudo pkill -9 -f "prank_linux.sh"
sudo pkill -9 -f "prank_input.py"

# Kill any active audio players
sudo pkill -9 -f "paplay|mpg123|ffplay|cvlc|mplayer"
```

### macOS
macOS uses `afplay` natively. Run the following in your terminal:

```bash
sudo pkill -9 -f "prank_mac.sh"
sudo pkill -9 -f "prank_input.py"
sudo pkill -9 -f "afplay"
```

### Windows
Open a Command Prompt (`cmd`) and forcefully terminate the hidden PowerShell or Python processes:

```cmd
:: Kill the Python daemon
taskkill /F /IM python.exe /T
taskkill /F /IM pythonw.exe /T

:: Kill the hidden PowerShell audio player
taskkill /F /IM powershell.exe /T
```

*(Note: Killing `powershell.exe` will close any other legitimate PowerShell windows you might have open).*

---

## Known Issues

### `Xlib.xauth: warning` on Linux (Prank 2)
If you see a warning about `Xlib.xauth` and `pynput` crashes, it means you are likely running a **Wayland** display server. Wayland intentionally blocks global input capturing.

**Solution**: Run the script using `sudo`. The script is programmed to detect Linux and drop back to the hardware-level `evdev` driver (which requires root to access `/dev/input/`), bypassing Wayland completely.

```bash
sudo ./venv/bin/python prank_input.py
```

### No Sound Playing on Linux
The scripts attempt to use a variety of common native audio players (`paplay`, `mpg123`, `ffplay`, `cvlc`, `mplayer`). If none of these are installed on the victim's system, the script will silently fail. 
Ensure the system has at least one basic audio player installed (e.g., `sudo pacman -S pulseaudio-utils` for `paplay`).
