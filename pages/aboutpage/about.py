import json
import threading
import time
import urllib.request

from kivy.factory import Factory
from kivy.metrics import dp
from kivy.app import App
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
import webbrowser

from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog
from kivymd_extensions.akivymd.uix.loaders import AKImageLoader, AKLabelLoader
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivymd_extensions.akivymd.uix.piechart import AKPieChart
from kivymd_extensions.sweetalert import SweetAlert

from custom_gestures.gesture_box import GestureBox

Window.size = (500, 850)
url = "http://oliverfan.top/posts/2adb/"


class AboutPage(MDScreen):
    items = [{"Python": 60, "Kivy": 20, "DL": 10, "Json": 10}]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def about_to_home():
        App.get_running_app().screen_manager.current = "Info"

    def open_website(self, value):
        webbrowser.open(value)

    def get_date(self):
        t = threading.Thread(target=self.send_request)
        t.start()

    def makeDataloaderNull(self):
        self.ids.user1.avatar = ''
        self.ids.user1.name = ''
        self.ids.user1.email = ''
        self.ids.user1.website = ''

    def set_user1(self, *kwargs):
        web = urllib.request.urlopen("https://my-json-server.typicode.com/TOESL100/dataloader/users/1")
        data = json.loads(web.read())
        json_str = json.dumps(data)
        data1 = json.loads(json_str)
        self.ids.user1.avatar = "http://oliverfan.top/medias/avatar.jpg"
        self.ids.user1.name = data1['name']
        self.ids.user1.email = data1['email']
        self.ids.user1.website = data1['website']

    def send_request(self):
        #self.makeDataloaderNull()
        self.set_user1()

    def got_error(self, *args):
        error_msg = "Timeout.Check connection"
        return toast(error_msg)

    def show_piechart(self):
        self.piechart = AKPieChart(
            items=self.items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(250), dp(250)),
        )
        self.ids.chart_box.add_widget(self.piechart)

    def top_center(self):
        dialog = AKAlertDialog(
            header_icon="bell",
            progress_interval=8,
            fixed_orientation="landscape",
            pos_hint={"center_x": 0.5, "top": 0.95},
            dialog_radius=0,
            size_landscape=["300dp", "70dp"],
            header_font_size="40dp",
            header_width_landscape="50dp",
            progress_color=[0.4, 0.1, 1, 1],
        )
        dialog.bind(on_progress_finish=dialog.dismiss)
        content = Factory.Notification()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()


class Loadercard(MDCard):
    pass


class AboutApp(MDApp):
    def build(self):
        return AboutPage()

    def open_website(self, value):
        webbrowser.open(value)


if __name__ == "__main__":
    AboutApp().run()
