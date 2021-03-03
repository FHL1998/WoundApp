import json
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, ListProperty
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.utils import asynckivy

from custom_gestures.gesture_box import GestureBox

APPID = '7d69d611da6df43f8d7fb5bdff3b617e'
Window.size = (500, 850)


class ToolPage(FloatLayout):
    location = ListProperty(['Singapore', 'SG'])
    conditions = StringProperty()
    current_weather = ObjectProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()
    conditions_image = StringProperty()
    temp_type = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.update_weather()

    def update_weather(self):
        config = ToolApp.get_running_app().config
        self.temp_type = config.getdefault('General', 'temp_type', 'metric').lower()
        weather_template = "http://api.openweathermap.org/data/2.5/" + "weather?q={},{}&units={}&APPID={}"
        weather_url = weather_template.format(*self.location, self.temp_type, APPID)
        request = UrlRequest(weather_url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions = data['weather'][0]['description']
        self.conditions_image = "http://openweathermap.org/img/w/{}.png".format(data['weather'][0]['icon'])
        self.temp_now = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']
        self.ids.temp_min.text = "Lowest : {} °C".format(self.temp_min)
        self.ids.temp_now.text = "Current : {} °C".format(self.temp_now)
        self.ids.temp_max.text = "Highest : {} °C".format(self.temp_max)

    def show_current_weather(self, location=None):
        self.clear_widgets()

        if self.current_weather is None:
            self.current_weather = ToolPage()

        if location is not None:
            self.current_weather.location = location

        self.current_weather.update_weather()
        self.add_widget(self.current_weather)

    @staticmethod
    def tool_to_info():
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = "Info"


class ToolApp(MDApp):
    def build(self):
        return ToolPage()

    def build_config(self, config):
        config.setdefaults('General', {'temp_type': "Metric"})


if __name__ == '__main__':
    ToolApp().run()
