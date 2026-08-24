import os
import time
from jnius import autoclass
try:
    from android.broadcast import BroadcastReceiver
except ImportError:
    BroadcastReceiver = None

MediaPlayer = autoclass('android.media.MediaPlayer')
Context = autoclass('android.content.Context')
PythonService = autoclass('org.phantom.basic.phantombasic.ServicePranksrv')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
String = autoclass('java.lang.String')

def start_foreground():
    mService = PythonService.mService
    channel_id = "phantom_channel"
    channel_name = "Phantom Playback"
    
    # Create notification channel for Android O+
    if autoclass('android.os.Build$VERSION').SDK_INT >= 26:
        channel = NotificationChannel(
            String(channel_id),
            String(channel_name),
            NotificationManager.IMPORTANCE_LOW
        )
        notification_manager = mService.getSystemService(Context.NOTIFICATION_SERVICE)
        notification_manager.createNotificationChannel(channel)
        builder = NotificationBuilder(mService, String(channel_id))
    else:
        builder = NotificationBuilder(mService)
        
    builder.setContentTitle(String("Phantom"))
    builder.setContentText(String("Playing background audio..."))
    # Use standard android icon since we might not have app icon mapped easily
    builder.setSmallIcon(17301540) # android.R.drawable.ic_media_play
    
    # Add Stop Action
    stop_intent = Intent("org.phantom.STOP_PHANTOM")
    # FLAG_IMMUTABLE is required on Android 12+ (flag 67108864)
    stop_pending_intent = PendingIntent.getBroadcast(mService, 0, stop_intent, 67108864)
    builder.addAction(17301539, String("Stop"), stop_pending_intent) # android.R.drawable.ic_media_pause
    
    notification = builder.build()
    mService.startForeground(1, notification)

def start_audio():
    audio_path = os.path.join(os.path.dirname(__file__), 'assets', 'prank_audio.mp3')
    if not os.path.exists(audio_path):
        return None
    try:
        AudioManager = autoclass('android.media.AudioManager')
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

should_stop = False

def on_broadcast(context, intent):
    global should_stop
    if intent.getAction() == "org.phantom.STOP_PHANTOM":
        should_stop = True

if __name__ == '__main__':
    try:
        start_foreground()
    except Exception as e:
        pass
        
    br = None
    if BroadcastReceiver:
        br = BroadcastReceiver(on_broadcast, actions=['org.phantom.STOP_PHANTOM'])
        br.start()
        
    mp = start_audio()
    try:
        while not should_stop:
            time.sleep(0.5)
    except Exception as e:
        pass
    finally:
        if mp:
            try:
                mp.stop()
                mp.release()
            except:
                pass
        if br:
            try:
                br.stop()
            except:
                pass
        try:
            PythonService.mService.stopForeground(True)
            PythonService.mService.stopSelf()
        except:
            pass
