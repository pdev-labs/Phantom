import os
import time
from jnius import autoclass

# JNI classes
MediaPlayer = autoclass('android.media.MediaPlayer')

def start_audio():
    audio_path = os.path.join(os.path.dirname(__file__), 'assets', 'prank_audio.mp3')
    mp = MediaPlayer()
    mp.setDataSource(audio_path)
    mp.prepare()
    mp.setLooping(True)
    mp.start()
    return mp

if __name__ == '__main__':
    # Start audio playback using native Android MediaPlayer
    # This ensures it survives even when the main Kivy activity is paused or destroyed
    mp = start_audio()
    
    # Keep the service running
    try:
        while True:
            time.sleep(1)
    except Exception as e:
        pass
    finally:
        if mp:
            mp.stop()
            mp.release()
