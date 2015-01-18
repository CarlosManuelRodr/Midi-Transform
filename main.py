from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from kivy.logger import Logger
from kivy.config import Config
from kivy.clock import Clock
import os
import tempfile
import threading
import time
from miditransform import *

# PyGame support midi on Windows, OSX and Linux.
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2" or _platform == "win32" or _platform == "darwin":
    import pygame
    import pygame.mixer as mixer
    Config.set('graphics', 'width', '500')
    Config.set('graphics', 'height', '500')
else:
    import android.mixer as mixer

# Global.
open_filename = ""
file_loaded = False
status_label = 0

transformation_none_gui = 0
transformation_invert_gui = 0
transformation_revert_gui = 0
pitch_switch_gui = 0
pitch_slider_gui = 0

def show_popup(title, text):
    box = BoxLayout(orientation='vertical')
    box.add_widget(Label(text=text))
    button = Button(text='Close', size_hint=(1, 0.3))
    box.add_widget(button)
    popup = Popup(title=title, content=box, auto_dismiss=False, size_hint=(None, None), size=(300, 300))
    button.bind(on_press=popup.dismiss)
    popup.open()

def transform(out_file):
    # Get options.
    if transformation_none_gui.state == "down":
        transformation = "None"
    elif transformation_invert_gui.state == "down":
        transformation = "Invert"
    elif transformation_revert_gui.state == "down":
        transformation = "Revert"

    if pitch_switch_gui:
        change_pitch = True
        pitch_change = int(pitch_slider_gui.value)
    else:
        change_pitch = False

    # Apply transformation to midi file.
    a = MidiFile()
    a.open(open_filename)

    if transformation == "Invert":
        a.invert()
    elif transformation == "Revert":
        a.revert()

    if change_pitch:
        a.change_pitch(pitch_change)

    a.save(out_file)

def set_status(text):
    if status_label != 0:
        status_label.text = text

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MenuBar(FloatLayout):
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def quit(self):
    	App.get_running_app().stop()

    def load(self, path, filename):
        global open_filename
        global file_loaded
        open_filename = os.path.join(path, filename[0]).encode('utf-8')
        self.dismiss_popup()
        if open_filename.endswith('.mid'):
            file_loaded = True
            set_status("File loaded.")
        else:
            open_filename = ""
            show_popup("Warning", "You must select a midi file.")

    def save(self, path, filename):
        if open_filename:
            save_filename = os.path.join(path, filename)
            self.dismiss_popup()
            if not save_filename.endswith('.mid'):
                save_filename += ".mid"

            transform(save_filename)
            show_popup("Success", "File saved successfully.")
        else:
            show_popup("Warning", "No file loaded")

class Root(BoxLayout):
    def reset_pitch_slider(self):
        self.ids.pitch_slider.value = 0
        self.ids.sliderval_label.text = str(0)

    def is_playing(self):
        return mixer.music.get_busy()

    def thread_play(self):
        global open_filename
        temp_file = os.path.join(tempfile.gettempdir(), "temp.mid")
        transform(temp_file)
        try:
            mixer.music.load(temp_file)
            mixer.music.play()
            mixer.music.set_volume(1.0)
            self.ids.play_button.text = "Stop"
            self.ids.options_layout.disabled = True

            while self.is_playing():
                time.sleep(0.5)
                pass

            self.ids.play_button.text = "Play preview"
            self.ids.options_layout.disabled = False

        except:
            Logger.info('Music: Error on play.')

    def start_midi_mixer(self):
        # Start audio mixer.
        freq = 44100
        bitsize = -16
        channels = 2
        buffer = 1024
        mixer.init(freq, bitsize, channels, buffer)

    def start_play(self):
        t = threading.Thread(target=self.thread_play)
        t.start()

    def stop_play(self):
        self.ids.play_button.text = "Play preview"
        self.ids.options_layout.disabled = False
        mixer.music.stop()

    def play_music(self):
        global file_loaded
        #show_popup("Warning", "No file loaded")
        if not self.is_playing():
            if file_loaded:
                Logger.info('Music: Starting to play.')
                self.start_play()
            else:
                show_popup("Warning", "No file loaded")
        else:
            Logger.info('Music: Stopping.')
            self.stop_play()

class MainApp(App):
    def build(self):
        global status_label
        global transformation_none_gui
        global transformation_invert_gui
        global transformation_revert_gui
        global pitch_switch_gui
        global pitch_slider_gui
        self.root = Root()
        self.root.start_midi_mixer()
        status_label = self.root.ids.status_label
        transformation_none_gui = self.root.ids.transformation_none
        transformation_invert_gui = self.root.ids.transformation_invert
        transformation_revert_gui = self.root.ids.transformation_revert
        pitch_switch_gui = self.root.ids.pitch_switch
        pitch_slider_gui = self.root.ids.pitch_slider
        return self.root

    def on_stop(self):
        self.root.stop_play()

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if '__main__' == __name__:
    MainApp().run()