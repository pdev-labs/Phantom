import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

class AudioPlayerApp(App):
    def build(self):
        self.sound = None
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
        
        start_btn = Button(
            text='Start Prank', 
            font_size='24sp', 
            size_hint=(1, 0.2), 
            background_color=(0.2, 0.8, 0.2, 1)
        )
        start_btn.bind(on_press=self.start_prank)
        
        stop_btn = Button(
            text='Stop Prank', 
            font_size='24sp', 
            size_hint=(1, 0.2),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        stop_btn.bind(on_press=self.stop_prank)
        
        exit_btn = Button(
            text='Exit', 
            font_size='20sp', 
            size_hint=(1, 0.2)
        )
        exit_btn.bind(on_press=self.exit_app)
        
        layout.add_widget(title)
        layout.add_widget(self.status_label)
        layout.add_widget(start_btn)
        layout.add_widget(stop_btn)
        layout.add_widget(exit_btn)
        
        # Safely locate and load the audio asset
        audio_path = os.path.join(os.path.dirname(__file__), 'assets', 'prank_audio.mp3')
        if os.path.exists(audio_path):
            self.sound = SoundLoader.load(audio_path)
            if self.sound:
                # Configure the sound to loop continuously
                self.sound.loop = True
            else:
                self.status_label.text = 'Status: Error loading audio format'
        else:
            self.status_label.text = 'Status: Audio file not found'
            
        return layout

    def start_prank(self, instance):
        if self.sound:
            if not self.is_playing:
                self.sound.play()
                self.is_playing = True
                self.status_label.text = 'Status: Playing'
        else:
            self.status_label.text = 'Status: Cannot play (No audio)'
            
    def stop_prank(self, instance):
        if self.sound and self.is_playing:
            self.sound.stop()
            self.is_playing = False
            self.status_label.text = 'Status: Stopped'
            
    def exit_app(self, instance):
        # Ensure audio stops cleanly before exit
        self.stop_prank(None)
        App.get_running_app().stop()
        
    def on_stop(self):
        # Catch Android lifecycle stop events
        self.stop_prank(None)

if __name__ == '__main__':
    AudioPlayerApp().run()
