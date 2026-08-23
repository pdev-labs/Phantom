import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from jnius import autoclass

class AudioPlayerApp(App):
    def build(self):
        self.is_playing = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        title = Label(text='[b]Phantom Basic[/b]', markup=True, font_size='32sp', size_hint=(1, 0.2))
        self.status_label = Label(text='Status: Stopped', font_size='24sp', size_hint=(1, 0.2))
        
        self.start_btn = Button(text='START GAME', font_size='24sp', size_hint=(1, 0.2), background_color=(0.2, 0.8, 0.2, 1))
        self.start_btn.bind(on_press=self.start_prank)
        
        self.stop_btn = Button(text='STOP GAME', font_size='24sp', size_hint=(1, 0.2), background_color=(0.8, 0.2, 0.2, 1))
        self.stop_btn.bind(on_press=self.stop_prank)
        
        self.toast_label = Label(text='', font_size='18sp', size_hint=(1, 0.2), color=(1, 0.3, 0.3, 1))
        
        layout.add_widget(title)
        layout.add_widget(self.status_label)
        layout.add_widget(self.start_btn)
        layout.add_widget(self.stop_btn)
        layout.add_widget(self.toast_label)
        
        return layout

    def start_prank(self, instance):
        if not self.is_playing:
            self.is_playing = True
            self.status_label.text = 'Status: Playing'
            if platform == 'android':
                try:
                    mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                    service = autoclass('org.phantom.basic.phantombasic.ServicePranksrv')
                    service.start(mActivity, '')
                except Exception as e:
                    self.status_label.text = f'Status: Error {e}'
            
    def stop_prank(self, instance):
        if self.is_playing:
            self.stop_btn.opacity = 0
            self.stop_btn.disabled = True
            self.toast_label.text = "Go to app settings to force stop"
            Clock.schedule_once(self.hide_toast, 3)
            
    def hide_toast(self, dt):
        self.toast_label.text = ""

if __name__ == '__main__':
    AudioPlayerApp().run()
