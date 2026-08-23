import os
import time
import subprocess
import sys
import threading

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
except ImportError:
    pass

def maximize_volume():
    try:
        if sys.platform == "win32":
            subprocess.call(["powershell", "-Command", "for($i=0;$i-lt 50;$i++){(new-object -com wscript.shell).SendKeys([char]175)}"])
        elif sys.platform == "darwin":
            subprocess.call(["osascript", "-e", "set volume output volume 100"])
        elif sys.platform.startswith("linux"):
            subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "100%"])
    except:
        pass

def start_basic_prank():
    audio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'prank_audio.mp3')
    if not os.path.exists(audio_file):
        return
        
    pygame.mixer.init()
    maximize_volume()
    
    try:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1) # Loop indefinitely
        
        while True:
            time.sleep(1)
    except Exception as e:
        pass

if __name__ == '__main__':
    start_basic_prank()
