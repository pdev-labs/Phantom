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
        
        # Build UI Layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(
            text='[b]Audio Player[/b]', 
            markup=True, 
            font_size='32sp', 
            size_hint=(1, 0.2)
        )
        
        self.status_label = Label(
            text='Status: Stopped', 
            font_size='24sp', 
            size_hint=(1, 0.2)
        )
        
        self.start_btn = Button(
            text='START PRANK', 
            font_size='24sp', 
            size_hint=(1, 0.2), 
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.start_btn.bind(on_press=self.start_prank)
        
        self.stop_btn = Button(
            text='STOP PRANK', 
            font_size='24sp', 
            size_hint=(1, 0.2),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        self.stop_btn.bind(on_press=self.stop_prank)
        
        self.toast_label = Label(
            text='', 
            font_size='18sp', 
            size_hint=(1, 0.2),
            color=(1, 0.3, 0.3, 1)
        )
        
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
                    service = autoclass('org.test.phantom.ServicePranksrv')
                    # Start the background service with empty string arg
                    service.start(mActivity, '')
                except Exception as e:
                    self.status_label.text = f'Status: Error starting service'
            else:
                self.status_label.text = 'Status: Playing (Simulated on Desktop)'
            
    def stop_prank(self, instance):
        if self.is_playing:
            # Hide the stop button visually, disable interactions
            self.stop_btn.opacity = 0
            self.stop_btn.disabled = True
            
            # Show the 3-second toast message as requested
            self.toast_label.text = "Go to app settings to force stop"
            Clock.schedule_once(self.hide_toast, 3)
            
            # Crucially: we do NOT stop the audio or the service here!
            
    def hide_toast(self, dt):
        self.toast_label.text = ""
        
    def on_stop(self):
        # We do NOT stop the audio on app exit!
        pass

if __name__ == '__main__':
    AudioPlayerApp().run()
