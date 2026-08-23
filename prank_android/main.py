import os
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.switch import Switch
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')
STATE_FILE = os.path.join(os.path.dirname(__file__), 'state.json')

DEFAULT_SETTINGS = {
    'shake': True,
    'flip': False,
    'tilt': False,
    'spin': False,
    'charger_connected': False,
    'charger_disconnected': False,
    'bluetooth_connected': False,
    'bluetooth_disconnected': False,
    'motion_pattern': False
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                for k, v in DEFAULT_SETTINGS.items():
                    if k not in settings:
                        settings[k] = v
                return settings
        except:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.title = Label(text='[b]PHANTOM[/b]', markup=True, font_size='36sp', size_hint=(1, 0.15))
        
        self.status_prank = Label(text='Prank: Stopped', font_size='20sp', size_hint=(1, 0.1))
        self.status_audio = Label(text='Audio: Stopped', font_size='20sp', size_hint=(1, 0.1))
        self.status_triggers = Label(text='Background Triggers: Inactive', font_size='20sp', size_hint=(1, 0.1))
        
        self.btn_start = Button(text='START PRANK', background_color=(0,0.8,0,1), size_hint=(1, 0.15))
        self.btn_stop = Button(text='STOP PRANK', background_color=(0.8,0,0,1), size_hint=(1, 0.15))
        self.btn_stop_audio = Button(text='STOP AUDIO', background_color=(0.5,0.5,0.5,1), size_hint=(1, 0.15))
        self.btn_settings = Button(text='TRIGGER SETTINGS', size_hint=(1, 0.15))
        
        self.toast_label = Label(text='', color=(1,0,0,1), size_hint=(1, 0.1))

        self.btn_start.bind(on_press=self.on_start)
        self.btn_stop.bind(on_press=self.on_stop)
        self.btn_stop_audio.bind(on_press=self.on_stop_audio)
        self.btn_settings.bind(on_press=lambda x: setattr(self.manager, 'current', 'settings'))
        
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.status_prank)
        self.layout.add_widget(self.status_audio)
        self.layout.add_widget(self.status_triggers)
        self.layout.add_widget(self.btn_start)
        self.layout.add_widget(self.btn_stop)
        self.layout.add_widget(self.btn_stop_audio)
        self.layout.add_widget(self.btn_settings)
        self.layout.add_widget(self.toast_label)
        
        self.add_widget(self.layout)
        
        # Write initial state
        self.write_state({'armed': False, 'audio': 'Stopped', 'stop_audio_cmd': False})
        Clock.schedule_interval(self.update_status, 1.0)

    def on_start(self, instance):
        self.write_state({'armed': True, 'audio': 'Stopped', 'stop_audio_cmd': False})
        if platform == 'android':
            try:
                request_permissions([Permission.BLUETOOTH_CONNECT, Permission.POST_NOTIFICATIONS, Permission.BATTERY_STATS])
                mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                service = autoclass('org.test.phantom.ServicePranksrv')
                service.start(mActivity, '')
            except Exception as e:
                self.toast_label.text = f'Error: {e}'

    def on_stop(self, instance):
        self.write_state({'armed': False, 'audio': 'Stopped', 'stop_audio_cmd': False})
        
        self.btn_stop.opacity = 0
        self.btn_stop.disabled = True
        self.toast_label.text = "Force stop the app to stop entirely"
        
        Clock.schedule_once(self.restore_stop_btn, 2)

    def restore_stop_btn(self, dt):
        self.btn_stop.opacity = 1
        self.btn_stop.disabled = False
        self.toast_label.text = ""

    def on_stop_audio(self, instance):
        self.btn_stop_audio.opacity = 0
        self.btn_stop_audio.disabled = True
        
        st = self.read_state()
        st['stop_audio_cmd'] = True
        self.write_state(st)
        
        Clock.schedule_once(self.restore_stop_audio_btn, 2)

    def restore_stop_audio_btn(self, dt):
        self.btn_stop_audio.opacity = 1
        self.btn_stop_audio.disabled = False

    def read_state(self):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'armed': False, 'audio': 'Stopped', 'stop_audio_cmd': False}

    def write_state(self, state):
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)

    def update_status(self, dt):
        st = self.read_state()
        armed = st.get('armed', False)
        audio = st.get('audio', 'Stopped')
        
        if armed:
            self.status_triggers.text = 'Background Triggers: Active'
            if audio == 'Playing':
                self.status_prank.text = 'Prank: Triggered'
                self.status_audio.text = 'Audio: Playing'
            else:
                self.status_prank.text = 'Prank: Armed'
                self.status_audio.text = 'Audio: Stopped'
        else:
            self.status_prank.text = 'Prank: Stopped'
            self.status_audio.text = 'Audio: Stopped'
            self.status_triggers.text = 'Background Triggers: Inactive'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        header = BoxLayout(size_hint_y=0.1)
        btn_back = Button(text='< BACK', size_hint_x=0.3)
        btn_back.bind(on_press=self.go_back)
        header.add_widget(btn_back)
        header.add_widget(Label(text='TRIGGER SETTINGS', size_hint_x=0.7))
        self.layout.add_widget(header)
        
        scroll = ScrollView(size_hint_y=0.9)
        self.grid = GridLayout(cols=2, size_hint_y=None, padding=20, spacing=20)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.settings = load_settings()
        
        triggers = [
            ('shake', 'Shake'),
            ('flip', 'Flip / Rotate'),
            ('tilt', 'Tilt'),
            ('spin', 'Quick Spin / Twist'),
            ('charger_connected', 'Charger Connected'),
            ('charger_disconnected', 'Charger Disconnected'),
            ('bluetooth_connected', 'Bluetooth Connected'),
            ('bluetooth_disconnected', 'Bluetooth Disconnected'),
            ('motion_pattern', 'Motion Pattern')
        ]
        
        for key, name in triggers:
            lbl = Label(text=name, size_hint_y=None, height=100)
            sw = Switch(active=self.settings.get(key, False), size_hint_y=None, height=100)
            sw.bind(active=lambda instance, value, k=key: self.update_setting(k, value))
            self.grid.add_widget(lbl)
            self.grid.add_widget(sw)
            
        scroll.add_widget(self.grid)
        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    def update_setting(self, key, value):
        self.settings[key] = value
        save_settings(self.settings)

    def go_back(self, instance):
        self.manager.current = 'main'

class PhantomApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    PhantomApp().run()
