import random

from kivy.app import App
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp

from custom_gestures.gesture_box import GestureBox
from pages.helppage.ai import AI
from kivy.config import Config
from pages.helppage.messages import Messages
from pages.helppage.inputs import Inputs

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '750')


# Window.size = (500, 850)
# Window.size = (450, 650)


class HelpPage(FloatLayout):
    messages = ObjectProperty(None)
    inputs = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.messages
        self.messages.bind(minimum_height=self.messages.setter('height'))

        self.ai = AI()
        self.inputs.set_messages_handler(self.messages)
        self.inputs.set_ai(self.ai)

    def refresh_chat(self):
        self.clear_widgets()
        self.__init__()

    @staticmethod
    def chat_to_help():
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = "Info"


class HelpApp(MDApp):
    def build(self):
        return HelpPage()


if __name__ == "__main__":
    HelpApp().run()