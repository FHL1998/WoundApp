from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog
from db.accountdb import insert_into_account, retrieve, reset

Window.size = (500, 850)


class ForgetPage(Screen):

    def reset(self):
        self.ids.user_forget_password.text = ""
        self.ids.new_set_password.text = ""
        self.ids.confirm_new_set_password.text = ""

    def retrieve_password(self):
        global user, password_changed
        user_forget_password = self.ids.user_forget_password.text.lstrip()
        new_set_password = self.ids.new_set_password.text.lstrip()
        confirm_new_set_password = self.ids.confirm_new_set_password.text.lstrip()
        if new_set_password and confirm_new_set_password:
            if new_set_password == confirm_new_set_password:
                user, password_changed = retrieve(user_forget_password, confirm_new_set_password)
                # set_password(user_forget_password, confirm_new_set_password)
                if user:
                    # toast("Successfully Changed Password !")
                    self.success_retrieve()
                else:
                    self.error_retrieve()
            else:
                toast("Please make sure to enter the same password !")
        else:
            toast("Please ensure that all information is completed !")
        # if user:
        # toast("Successfully Changed Password !")
        # self.success_retrieve()
        # self.reset()

    def success_retrieve(self):
        dialog = AKAlertDialog(
            header_icon="check-circle-outline", header_bg=[0, 0.7, 0, 1]
        )
        content = Factory.SuccessRetrieveDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()
        self.reset()
        # App.get_running_app().screen_manager.current = "login"

    def error_retrieve(self):
        dialog = AKAlertDialog(
            header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
        )
        content = Factory.ErrorRetrieveDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    # def login(self):
    # self.reset()
    # App.get_running_app().screen_manager.current = "login"

    @staticmethod
    def forget_to_login():
        App.get_running_app().screen_manager.current = 'Login'


class ForgetApp(MDApp):
    def build(self):
        # self.screen = Builder.load_file('login.kv')
        return ForgetPage()


if __name__ == "__main__":
    ForgetApp().run()
