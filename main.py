from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import time
from filesharer import FileSharer
from kivy.core.clipboard import Clipboard
import webbrowser
Builder.load_file('frontend.kv')


class CameraScreen(Screen):

    def start(self):
        """Starts the camera"""
        self.ids.camera.play = True
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops the camera"""
        self.ids.camera.play = False
        self.ids.camera.texture = None

    def capture(self):
        """Captures the image on the camera at current_time and outputs it to a
        .png file in the files directory."""
        current_time = time.strftime('%Y%m%d-%H%M')
        self.filepath = 'files/' + current_time + '.png'
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):

    link_message = 'Create a link first!' \
                   ''
    def create_link(self):
        """Accesses the filepath generated after clicking capture button
        and uploads it to the cloud while creating a shareable link
        and placing it in the label widget."""
        filepath = App.get_running_app().root.ids.camera_screen.filepath
        file_sharer = FileSharer(filepath)
        self.url = file_sharer.share()
        self.ids.link.text = self.url

    def open_link(self):
        """Open link in the web browser."""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = link_message

    def copy_link(self):
        """Copy link to the clipboard for pasting elsewhere."""
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = link_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
