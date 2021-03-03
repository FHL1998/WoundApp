from kivy.app import App
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivymd.app import MDApp

from custom_gestures.gesture_box import GestureBox
Window.size = (500, 850)


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class SegmentPage(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def segment_to_model():
        App.get_running_app().screen_manager.current = 'Model'

    @staticmethod
    def segment_to_detail():
        App.get_running_app().screen_manager.current = 'Detail'

    @staticmethod
    def refresh():
        App.get_running_app().screen_manager.current = 'Segment'


class SegmentApp(MDApp):
    def build(self):
        return SegmentPage()


if __name__ == "__main__":
    SegmentApp().run()
