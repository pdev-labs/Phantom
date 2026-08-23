import os
import time
import glob
import random
import json
from jnius import autoclass

MediaPlayer = autoclass('android.media.MediaPlayer')
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'mode': 'basic'}

def start_basic_audio():
    audio_dir = os.path.join(os.path.dirname(__file__), 'assets', 'audio')
    files = glob.glob(os.path.join(audio_dir, '*.mp3'))
    if not files: return None
    audio_path = random.choice(files)
    
    mp = MediaPlayer()
    mp.setDataSource(audio_path)
    mp.prepare()
    mp.setLooping(True)
    mp.start()
    return mp

if __name__ == '__main__':
    settings = load_settings()
    mp = None
    if settings.get('mode') == 'basic':
        mp = start_basic_audio()
        
    # If mode is sensors, we'd launch the sensor listener logic here
    # For brevity in this combined app, we just implement the basic mode fallback
    
    try:
        while True:
            time.sleep(1)
    except:
        pass
    finally:
        if mp:
            mp.stop()
            mp.release()
