import os
import json
import time
import random
import glob
from jnius import autoclass, PythonJavaClass, java_method

MediaPlayer = autoclass('android.media.MediaPlayer')
Context = autoclass('android.content.Context')
PythonService = autoclass('org.phantom.sensors.phantomsensors.ServicePranksrv')

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')
STATE_FILE = os.path.join(os.path.dirname(__file__), 'state.json')

class HardwareListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self, callback):
        super(HardwareListener, self).__init__()
        self.callback = callback

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        self.callback(event)

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        pass

class BroadcastListener(PythonJavaClass):
    __javainterfaces__ = ['android/content/BroadcastReceiver']
    
    def __init__(self, callback):
        super(BroadcastListener, self).__init__()
        self.callback = callback

    # A python BroadcastReceiver class implemented in Java via Kivy
    # Wait, Kivy doesn't have BroadcastReceiver in __javainterfaces__ directly 
    # The standard way is using android.broadcast.BroadcastReceiver
    
# Better to use android.broadcast for receivers
try:
    from android.broadcast import BroadcastReceiver
except ImportError:
    BroadcastReceiver = None

class PrankService:
    def __init__(self):
        self.media_player = None
        self.settings = {}
        self.armed = False
        self.audio_files = []
        self.last_trigger_time = 0
        self.sensors_registered = False
        
        self.load_audio_files()
        
        # Sensor setup
        self.sensor_manager = PythonService.mService.getSystemService(Context.SENSOR_SERVICE)
        Sensor = autoclass('android.hardware.Sensor')
        self.accel = self.sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        self.gyro = self.sensor_manager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
        self.sensor_listener = HardwareListener(self.on_sensor)
        
        # Broadcasts
        self.br = None
        if BroadcastReceiver:
            self.br = BroadcastReceiver(self.on_broadcast, actions=[
                'android.intent.action.ACTION_POWER_CONNECTED',
                'android.intent.action.ACTION_POWER_DISCONNECTED',
                'android.bluetooth.device.action.ACL_CONNECTED',
                'android.bluetooth.device.action.ACL_DISCONNECTED'
            ])

    def load_audio_files(self):
        audio_dir = os.path.join(os.path.dirname(__file__), 'assets', 'audio')
        self.audio_files = glob.glob(os.path.join(audio_dir, '*.mp3'))

    def read_state(self):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'armed': False, 'audio': 'Stopped', 'stop_audio_cmd': False}

    def write_state(self, state):
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)

    def read_settings(self):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}

    def on_broadcast(self, context, intent):
        if not self.armed: return
        action = intent.getAction()
        if action == 'android.intent.action.ACTION_POWER_CONNECTED' and self.settings.get('charger_connected'):
            self.trigger_prank()
        elif action == 'android.intent.action.ACTION_POWER_DISCONNECTED' and self.settings.get('charger_disconnected'):
            self.trigger_prank()
        elif action == 'android.bluetooth.device.action.ACL_CONNECTED' and self.settings.get('bluetooth_connected'):
            self.trigger_prank()
        elif action == 'android.bluetooth.device.action.ACL_DISCONNECTED' and self.settings.get('bluetooth_disconnected'):
            self.trigger_prank()

    def on_sensor(self, event):
        if not self.armed: return
        # Debounce: 2 seconds
        if time.time() - self.last_trigger_time < 2.0:
            return
            
        sensor_type = event.sensor.getType()
        Sensor = autoclass('android.hardware.Sensor')
        values = event.values
        
        if sensor_type == Sensor.TYPE_ACCELEROMETER:
            x, y, z = values[0], values[1], values[2]
            accel_sq = (x*x + y*y + z*z)
            # Shake logic
            if self.settings.get('shake') and accel_sq > 250:  # arbitrary threshold
                self.trigger_prank()
                return
            # Tilt logic (Z axis close to 0 instead of 9.8)
            if self.settings.get('tilt') and abs(z) < 2.0 and abs(y) > 5.0:
                self.trigger_prank()
                return
            # Flip logic (Z axis negative ~ -9.8)
            if self.settings.get('flip') and z < -8.0:
                self.trigger_prank()
                return
                
        elif sensor_type == Sensor.TYPE_GYROSCOPE:
            # Spin logic
            x, y, z = values[0], values[1], values[2]
            spin_sq = (x*x + y*y + z*z)
            if self.settings.get('spin') and spin_sq > 20: # arbitrary fast spin
                self.trigger_prank()
                return

    def trigger_prank(self):
        self.last_trigger_time = time.time()
        if not self.audio_files:
            return
            
        if self.media_player:
            try:
                self.media_player.stop()
                self.media_player.release()
            except:
                pass
            
        audio_file = random.choice(self.audio_files)
        self.media_player = MediaPlayer()
        self.media_player.setDataSource(audio_file)
        self.media_player.prepare()
        self.media_player.start()
        
        st = self.read_state()
        st['audio'] = 'Playing'
        self.write_state(st)

    def stop_audio(self):
        if self.media_player:
            try:
                self.media_player.stop()
                self.media_player.release()
            except:
                pass
            self.media_player = None
            
        st = self.read_state()
        st['audio'] = 'Stopped'
        st['stop_audio_cmd'] = False
        self.write_state(st)

    def run(self):
        while True:
            st = self.read_state()
            self.armed = st.get('armed', False)
            self.settings = self.read_settings()
            
            # Check if UI requested an audio stop
            if st.get('stop_audio_cmd', False):
                self.stop_audio()
                
            # Manage sensors
            if self.armed and not self.sensors_registered:
                SensorManager = autoclass('android.hardware.SensorManager')
                if self.accel:
                    self.sensor_manager.registerListener(self.sensor_listener, self.accel, SensorManager.SENSOR_DELAY_NORMAL)
                if self.gyro:
                    self.sensor_manager.registerListener(self.sensor_listener, self.gyro, SensorManager.SENSOR_DELAY_NORMAL)
                if self.br:
                    self.br.start()
                self.sensors_registered = True
            elif not self.armed and self.sensors_registered:
                self.sensor_manager.unregisterListener(self.sensor_listener)
                if self.br:
                    self.br.stop()
                self.sensors_registered = False
                self.stop_audio()
                
            # Check if media finished playing
            if self.media_player and not self.media_player.isPlaying():
                st = self.read_state()
                if st.get('audio') == 'Playing':
                    st['audio'] = 'Stopped'
                    self.write_state(st)
                    
            time.sleep(1)

if __name__ == '__main__':
    service = PrankService()
    try:
        service.run()
    except Exception as e:
        pass
