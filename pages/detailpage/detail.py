from kivy.app import App
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from datetime import *

from kivymd.app import MDApp

Window.size = (400, 750)


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class DetailPage(BoxLayout):
    now = datetime.now()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def back_to_segment():
        App.get_running_app().screen_manager.current = 'Segment'

    @staticmethod
    def detail_to_info():
        App.get_running_app().screen_manager.current = 'Info'

    def time(self, **kwargs):
        self.now = datetime.now()
        self.timelabel.text = self.now.strftime('%Y-%m-%d %H:%M:%S')


class DetailApp(MDApp):
    def build(self):
        return DetailPage()


if __name__ == "__main__":
    DetailApp().run()
