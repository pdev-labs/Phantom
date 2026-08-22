import os
import sys
import glob
import random
import platform
import subprocess
import threading

# Global state to prevent overlapping audio
is_playing = False
lock = threading.Lock()

def get_audio_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return glob.glob(os.path.join(script_dir, "*.mp3"))

def play_audio(file_path):
    global is_playing
    with lock:
        if is_playing:
            return
        is_playing = True
    
    def run_player():
        global is_playing
        try:
            sys_os = platform.system()
            if sys_os == "Linux":
                players = ["paplay", "mpg123", "ffplay", "cvlc", "mplayer"]
                for p in players:
                    if subprocess.run(["which", p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                        cmd = []
                        if os.environ.get("SUDO_USER"):
                            sudo_user = os.environ.get("SUDO_USER")
                            uid = subprocess.check_output(["id", "-u", sudo_user]).decode().strip()
                            cmd.extend(["sudo", "-u", sudo_user, "env", f"XDG_RUNTIME_DIR=/run/user/{uid}"])
                        
                        cmd.append(p)
                        if p == "ffplay":
                            cmd.extend(["-nodisp", "-autoexit"])
                        elif p == "cvlc":
                            cmd.extend(["--play-and-exit"])
                        cmd.append(file_path)
                        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
            elif sys_os == "Darwin":
                subprocess.run(["afplay", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif sys_os == "Windows":
                ps_script = f'(New-Object -ComObject wmplayer.ocx).cdromcollection.item(0); $player = New-Object -ComObject wmplayer.ocx; $player.URL = "{file_path}"; $player.controls.play(); while($player.playState -ne 1) {{ Start-Sleep -Milliseconds 100 }}'
                subprocess.run(["powershell", "-WindowStyle", "Hidden", "-Command", ps_script], creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        finally:
            with lock:
                is_playing = False

    t = threading.Thread(target=run_player)
    t.daemon = True
    t.start()

def trigger_prank():
    files = get_audio_files()
    if not files:
        return
    chosen = random.choice(files)
    play_audio(chosen)

if platform.system() == "Linux":
    # On Linux, pynput fails on Wayland. Use evdev directly.
    import evdev
    import asyncio

    def on_linux_input(keycode):
        if isinstance(keycode, (list, tuple)):
            keycode = keycode[0]
        keycode_str = str(keycode)
        if keycode_str == 'KEY_ENTER' or keycode_str.startswith('BTN_'):
            trigger_prank()

    async def monitor_device(device):
        try:
            async for event in device.async_read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    if key_event.keystate == key_event.key_down:
                        on_linux_input(key_event.keycode)
        except Exception:
            pass

    async def main_loop():
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if evdev.ecodes.EV_KEY in device.capabilities():
                asyncio.create_task(monitor_device(device))
        while True:
            await asyncio.sleep(3600)

    def start_listeners():
        try:
            asyncio.run(main_loop())
        except KeyboardInterrupt:
            pass

else:
    # On Windows/macOS, pynput works perfectly
    from pynput import mouse, keyboard

    def on_press(key):
        if key == keyboard.Key.enter:
            trigger_prank()

    def on_click(x, y, button, pressed):
        if pressed:
            trigger_prank()

    def start_listeners():
        keyboard_listener = keyboard.Listener(on_press=on_press)
        mouse_listener = mouse.Listener(on_click=on_click)
        
        keyboard_listener.start()
        mouse_listener.start()
        
        keyboard_listener.join()
        mouse_listener.join()

def daemonize():
    import signal
    try:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    except Exception:
        pass
    
    if platform.system() == "Windows":
        if len(sys.argv) == 1:
            subprocess.Popen([sys.executable, os.path.abspath(__file__), "run"], creationflags=0x08000000)
            sys.exit(0)
    else:
        # Standard double-fork to detach from terminal on Linux/macOS
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError:
            pass
        os.setsid()
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError:
            pass
        
        sys.stdout.flush()
        sys.stderr.flush()
        try:
            with open(os.devnull, 'r') as f:
                os.dup2(f.fileno(), sys.stdin.fileno())
            with open(os.devnull, 'a+') as f:
                os.dup2(f.fileno(), sys.stdout.fileno())
                os.dup2(f.fileno(), sys.stderr.fileno())
        except Exception:
            pass

if __name__ == "__main__":
    daemonize()
    start_listeners()
