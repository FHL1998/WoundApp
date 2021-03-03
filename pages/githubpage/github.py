from threading import Thread

import re
import requests
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
from db.accountdb import insert_into_github_account
from db.sqlite3_connect import select_data, insert_data

Window.size = (500, 850)


class GithubPage(FloatLayout):

    def __init__(self, **kwargs):
        # 初始化信息
        super().__init__(**kwargs)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36',
            'Referer': 'https://github.com/',
            'Host': 'github.com'
        }

        self.session = requests.Session()
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'

    def login_GitHub(self):
        # 登录入口
        github_login_email = self.ids.email.text.lstrip()
        github_login_password = self.ids.password.text.lstrip()
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.get_token(),
            'login': github_login_email,
            'password': github_login_password
        }
        # print(login_email)
        # print(login_password)
        resp = self.session.post(
            self.post_url, data=post_data, headers=self.headers)
        # toast("Server Responded Successfully !")
        # print('StatusCode:', resp.status_code)
        if resp.status_code == 200:
            # toast("Server Responded Successfully !")
            match = re.search(r'"user-login" content="(.*?)"', resp.text)
            user_name = match.group(1)
            print('UserName:', user_name)
            if user_name != "":
                toast("Github Login Successfully !")
                info = App.get_running_app().screen_manager.get_screen('Info')
                info.children[0].ids.slide_name_label.text = user_name
                github_login_flag = True
                remember_me_flag = False
                database_user_search_sql = " SELECT Username FROM account WHERE Username='{}'".format(user_name)
                database_user_search = select_data(database_user_search_sql)
                #print(database_user_search)
                if database_user_search == "":
                    insert_into_github_account(user_name, github_login_email, github_login_password,
                                               remember_me_flag,
                                               github_login_flag)
                else:
                    App.get_running_app().screen_manager.current = 'Create'
            else:
                toast("Github Login Failed ! Please Check Password !")
        else:
            pass
            # toast("Server Responded Failed !")

    # Get login token
    def get_token(self):

        response = self.session.get(self.login_url, headers=self.headers)
        # print(response)
        if response.status_code != 200:
            toast('Get token fail !')
            return None
        match = re.search(
            r'name="authenticity_token" value="(.*?)"', response.text)
        if not match:
            toast('Get Token Fail !')
            return None
        return match.group(1)

    @staticmethod
    def github_login_to_create():
        App.get_running_app().screen_manager.current = 'Create'

    @staticmethod
    def github_login_to_login():
        App.get_running_app().screen_manager.current = 'Login'


class GithubApp(MDApp):
    def build(self):
        return GithubPage()


if __name__ == "__main__":
    GithubApp().run()

    # email = input('Account:')
    # password = input('Password:')

    # login = GithubLogin(email, password)
    # login.login_GitHub()
