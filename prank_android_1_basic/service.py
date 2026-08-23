import os
import time
import glob
import random
from jnius import autoclass

MediaPlayer = autoclass('android.media.MediaPlayer')

def start_audio():
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
    mp = start_audio()
    try:
        while True:
            time.sleep(1)
    except:
        pass
    finally:
        if mp:
            mp.stop()
            mp.release()
