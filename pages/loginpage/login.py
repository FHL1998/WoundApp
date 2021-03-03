from threading import Thread

from kivy.uix.popup import Popup
from kivymd.icon_definitions import md_icons
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDCustomBottomSheet, MDListBottomSheet
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.relativelayout import MDRelativeLayout

from db.accountdb import get_password
from db.database import DataBase
import time
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
import sys
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

from db.sqlite3_connect import select_data, insert_data

Window.size = (500, 850)


# db = DataBase("users.txt")


class LoginPage(FloatLayout):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    # text = StringProperty()
    hint_text = StringProperty()
    remember_me = BooleanProperty(False)

    def reset(self):
        # self.ids.email.text = ""
        self.ids.password.text = ""

    def auto_password_fill(self):
        email_input = self.ids.email.text.lstrip()
        remember_status_sql = "SELECT Remember FROM account WHERE Email='{}'".format(email_input)
        remember_status = select_data(remember_status_sql)[0][0]
        if remember_status:
            sql = "SELECT password FROM account WHERE Email='{}'".format(email_input)
            remembered_password = select_data(sql)
            self.ids.password.text = remembered_password[0][0]
        else:
            pass

    def detect_remember_option(self):
        email_input = self.ids.email.text.lstrip()
        remember_status_sql = "SELECT Remember FROM account WHERE Email='{}'".format(email_input)
        remember_status = select_data(remember_status_sql)[0][0]
        # print(remember_status)
        if remember_status:
            toast('This account has already been remembered !')
        else:
            toast("If login successfully, the current account will be remembered! ")
        # self.ids['remember_me'].active = self.remember_me
        # self.remember_me = True
        # email_input = self.ids.email.text.lstrip()
        # sql = " UPDATE account SET Remember ='{}' WHERE Email='{}'".format(self.remember_me, email_input)
        # insert_data(sql)
        # print(self.remember_me)

    def login_validate(self, *args):

        email_input = self.ids.email.text.lstrip()
        # self.ids['remember_me'].active = self.remember_me
        # sql = " UPDATE account SET Remember ='{}' WHERE Email='{}'".format(self.remember_me, email_input)
        # insert_data(sql)
        # print(self.remember_me)
        remember = "SELECT Remember FROM account WHERE Email='{}'".format(email_input)
        password_input = self.ids.password.text.lstrip()
        email, password = get_password(email_input)

        if email:
            if password == password_input:
                self.reset()
                info = App.get_running_app().screen_manager.get_screen('Info')
                sql = " SELECT * FROM account WHERE Email='{}'".format(email_input)
                login_username_result_callback = select_data(sql)
                #print(login_username_result_callback)
                info.children[0].ids.slide_name_label.text = login_username_result_callback[0][0]
                t = Thread(target=self.success_login)
                t.start()
                if self.ids.remember_me.active:
                    self.ids['remember_me'].active = self.remember_me
                    self.remember_me = True
                    email_input = self.ids.email.text.lstrip()
                    sql = " UPDATE account SET Remember ='{}' WHERE Email='{}'".format(self.remember_me, email_input)
                    insert_data(sql)
                    print(self.remember_me)
            else:
                t = Thread(target=self.start_failure)
                t.start()
                toast("Password valid or incorrect !")
        else:
            t = Thread(target=self.start_failure)
            t.start()
            toast("User Not Found ! Please input correct Email Address !")

    def failure(self, *args):
        t = Thread(target=self.start_failure)
        t.start()

    def start_success(self, *args):
        time.sleep(2)
        return self.ids.progressbutton_success.success()

    def start_failure(self, *args):
        time.sleep(2)
        return self.ids.progressbutton_success.failure()

    def success_login(self, *args):
        self.start_success()
        time.sleep(1)
        App.get_running_app().screen_manager.current = 'Create'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.messages

    def show_user_list_bottom_sheet(self):
        rows = select_data("SELECT Email FROM account WHERE Github='False' ORDER BY UserName")
        # print(rows)
        bottom_sheet_menu = MDListBottomSheet()
        for user_emails in rows:
            for user_email in user_emails:
                bottom_sheet_menu.add_item(
                    str(user_email),
                    lambda x, y=str(user_email): self.callback_for_user_list_items(
                        f"{y}"
                    ),
                    icon="account-clock",

                )
        bottom_sheet_menu.open()

    def callback_for_user_list_items(self, text):
        self.ids.email.text = text

    @staticmethod
    def login_to_github_login():
        App.get_running_app().screen_manager.current = 'Github'

    @staticmethod
    def login_to_add():
        App.get_running_app().screen_manager.current = 'Create'

    @staticmethod
    def login_to_register():
        App.get_running_app().screen_manager.current = 'Register'

    @staticmethod
    def login_to_forget():
        App.get_running_app().screen_manager.current = 'Forget'

    @staticmethod
    def login_to_info():
        App.get_running_app().screen_manager.current = 'Info'


class LoginApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        # self.screen = Builder.load_file('login.kv')
        return LoginPage()

    def ThemeMode(self, *args):
        t = self.theme_cls.theme_style
        t = "Light" if t != "Light" else "Dark"
        self.theme_cls.theme_style = t


if __name__ == "__main__":
    LoginApp().run()
