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
    try:
        Context = autoclass('android.content.Context')
        AudioManager = autoclass('android.media.AudioManager')
        PythonService = autoclass('org.phantom.basic.phantombasic.ServicePranksrv')
        audio_manager = PythonService.mService.getSystemService(Context.AUDIO_SERVICE)
        max_vol = audio_manager.getStreamMaxVolume(AudioManager.STREAM_MUSIC)
        audio_manager.setStreamVolume(AudioManager.STREAM_MUSIC, max_vol, 0)
    except Exception as e:
        pass
        
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
