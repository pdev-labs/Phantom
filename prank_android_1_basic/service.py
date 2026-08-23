import os
import time
import glob
import random
from jnius import autoclass

MediaPlayer = autoclass('android.media.MediaPlayer')

def start_audio():
    audio_path = os.path.join(os.path.dirname(__file__), 'assets', 'prank_audio.mp3')
    if not os.path.exists(audio_path):
        return None
    
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
