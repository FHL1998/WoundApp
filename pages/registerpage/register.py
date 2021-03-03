from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog
from db.accountdb import insert_into_account

Window.size = (500, 850)


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


class RegisterPage(FloatLayout):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def create_new_user(self):
        global user
        username = self.ids.username.text.lstrip()
        email = self.ids.email.text.lstrip()
        password = self.ids.password.text.lstrip()
        confirm_password = self.ids.confirm_password.text.lstrip()
        github_login_flag = False
        # print(username)
        # print(email)
        # print(password)
        # print(confirm_password)
        if self.ids.username.text != "" and self.ids.email.text != "" and self.ids.email.text.count(
                "@") == 1 and self.ids.email.text.count(".") > 0:
            if username and password:
                if password == confirm_password:
                    user, LabelText = insert_into_account(username, email, password,github_login_flag)
                    if user:
                        self.success()
                else:
                    toast("Please make sure to enter the same password !")
                    # self.on_call_popup(LabelText)
            else:
                toast("Please ensure that all information is completed !")
        else:
            self.error()

    def success(self):
        dialog = AKAlertDialog(
            header_icon="check-circle-outline", header_bg=[0, 0.7, 0, 1]
        )
        content = Factory.SuccessRegisterDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()
        self.reset()
        # App.get_running_app().screen_manager.current = "login"

    def error(self):
        dialog = AKAlertDialog(
            header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
        )
        content = Factory.ErrorRegisterDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    # def login(self):
    # self.reset()
    # App.get_running_app().screen_manager.current = "login"

    def reset(self):
        self.ids.email.text = ""
        self.ids.password.text = ""
        self.ids.confirm_password.text = ""
        self.ids.username.text = ""
        # App.get_running_app().screen_manager.current = 'Login'

    @staticmethod
    def register_to_login():
        App.get_running_app().screen_manager.current = 'Login'


class RegisterApp(MDApp):
    def build(self):
        # self.screen = Builder.load_file('login.kv')
        return RegisterPage()


if __name__ == "__main__":
    RegisterApp().run()
