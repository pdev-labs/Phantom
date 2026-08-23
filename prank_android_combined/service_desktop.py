import os
import time
import random
import glob
import threading
import subprocess
import sys

# Try to import desktop libraries. They will be bundled by PyInstaller.
try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    from pynput import mouse, keyboard
except ImportError:
    pass

class DesktopPrankService:
    def __init__(self):
        self.audio_files = []
        self.last_trigger_time = 0
        self.is_playing = False
        
        self.load_audio_files()
        pygame.mixer.init()
        
    def load_audio_files(self):
        audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'audio')
        self.audio_files = glob.glob(os.path.join(audio_dir, '*.mp3'))
        
    def maximize_volume(self):
        try:
            if sys.platform == "win32":
                # Maximize volume on Windows
                subprocess.call(["powershell", "-Command", "for($i=0;$i-lt 50;$i++){(new-object -com wscript.shell).SendKeys([char]175)}"])
            elif sys.platform == "darwin":
                # macOS
                subprocess.call(["osascript", "-e", "set volume output volume 100"])
            elif sys.platform.startswith("linux"):
                # Linux (try amixer or pactl)
                subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "100%"])
        except Exception as e:
            pass

    def trigger_prank(self):
        if time.time() - self.last_trigger_time < 2.0:
            return
        if self.is_playing:
            return
            
        if not self.audio_files:
            return
            
        self.last_trigger_time = time.time()
        self.maximize_volume()
        
        audio_file = random.choice(self.audio_files)
        
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
            self.is_playing = True
            
            # Wait for audio to finish
            def wait_for_audio():
                while pygame.mixer.music.get_busy():
                    time.sleep(0.5)
                self.is_playing = False
            threading.Thread(target=wait_for_audio, daemon=True).start()
        except Exception as e:
            self.is_playing = False

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.trigger_prank()

    def on_press(self, key):
        if key == keyboard.Key.enter:
            self.trigger_prank()

    def run(self):
        # Start listeners
        mouse_listener = mouse.Listener(on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        # Keep the main thread alive silently
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

def start_desktop_service():
    service = DesktopPrankService()
    service.run()

if __name__ == '__main__':
    start_desktop_service()
