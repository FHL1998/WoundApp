import webbrowser

from kivy.app import App
from kivy.core.window import Window, Animation
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix import SpecificBackgroundColorBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

from db.sqlite3_connect import select_data

Window.size = (500, 850)


class DashboardPage(Screen):
    pass


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(object):
    pass


class CustomToolbar(RectangularElevationBehavior, SpecificBackgroundColorBehavior, BoxLayout):
    pass


class QrcodeDialog(BoxLayout):
    # cancel = ObjectProperty(None)
    pass


Factory.register('QrcodeDialog', cls=QrcodeDialog)


class InfoPage(MDNavigationLayout):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tap_target_view = MDTapTargetView(
            widget=self.ids.menu_btn,
            title_text="This is the MENU button",
            description_text="Press the button to activate\n navigation drawer",
            outer_radius=dp(150),
            outer_circle_alpha=0.8,
            widget_position="left_top",
        )
        # self.set_name()

    def on_enter(self):
        self.tap_target_view.start()

    def tap_target_start(self):
        if self.tap_target_view.state == "close":
            self.ids['nav'].set_state("close")
            self.tap_target_view.start()
        else:
            self.ids['nav'].set_state("open")
            self.tap_target_view.stop()

    def open_website(self, value):
        webbrowser.open(value)

    def set_name(self):
        """为name赋值"""
        sql = 'SELECT name FROM user WHERE id=1'
        res = select_data(sql)
        self.ids.slide_name_label.text = res[0][0]

    def me_name_callback(self):
        login = App.get_running_app().screen_manager.get_screen('Login')
        github = App.get_running_app().screen_manager.get_screen('Github')
        login_email = login.children[0].ids.email.text.lstrip()
        github_login_email = github.children[0].ids.email.text.lstrip()
        # print(github_login_email)
        if login_email == "":
            if github_login_email != "":
                github_login_flag_sql = " SELECT Github FROM account WHERE Email='{}'".format(github_login_email)
                github_login_flag = select_data(github_login_flag_sql)
                # print(github_login_flag)
                if github_login_flag:
                    me = App.get_running_app().screen_manager.get_screen('Me')
                    sql = " SELECT * FROM account WHERE Email='{}'".format(github_login_email)
                    res = select_data(sql)
                    me.children[0].ids.name_input.text = res[0][0]

        else:
            me = App.get_running_app().screen_manager.get_screen('Me')
            sql = " SELECT * FROM account WHERE Email='{}'".format(login_email)
            login_username_result = select_data(sql)
            me.children[0].ids.name_input.text = login_username_result[0][0]
            # self.ids.slide_name_label.text = login_username_result[0][0]

    def qrcode(self):
        dialog = AKAlertDialog(
            header_icon="qrcode-scan",
            progress_interval=4,
            pos_hint={"center_x": 0.5, "center_y": 0.72},
            fixed_orientation="landscape",
            header_font_size="40dp",
            header_width_landscape="50dp",
            header_bg=[0, 0.7, 0, 1],
            size_landscape=["240dp", "190dp"],
        )
        content = Factory.QrcodeDialog()
        dialog.bind(on_progress_finish=dialog.dismiss)
        # content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    def warning(self):
        dialog = AKAlertDialog(
            header_icon="exclamation",
            header_bg=[1, 0.75, 0, 1]
        )
        dialog.bind(on_progress_finish=dialog.dismiss)
        content = Factory.WarningDialog()
        content.ids.confirm.bind(on_release=dialog.dismiss)
        content.ids.cancel.bind(on_release=dialog.dismiss)
        content.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    @staticmethod
    def me_slide_button():
        App.get_running_app().screen_manager.current = 'Me'

    @staticmethod
    def add_patient_slide_button():
        App.get_running_app().screen_manager.current = 'Create'

    @staticmethod
    def upload_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Upload'

    @staticmethod
    def model_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Model'

    @staticmethod
    def tool_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Tool'

    @staticmethod
    def help_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Help'

    @staticmethod
    def about_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'About'

    def navBar(self, navState):
        self.ids['nav'].set_state(navState)

    @staticmethod
    def info_to_history():
        App.get_running_app().screen_manager.current = 'History'


class InfoApp(MDApp):
    def build(self):
        return InfoPage()

    def navBar(self, navState):
        self.root.ids['nav'].set_state(navState)


if __name__ == "__main__":
    InfoApp().run()
