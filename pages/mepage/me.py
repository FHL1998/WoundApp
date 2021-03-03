import os
from functools import partial
from os import walk, path, remove

from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.material_resources import DEVICE_TYPE
from kivymd.toast import toast
from kivymd.uix import dialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDTextButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, ImageLeftWidget, OneLineAvatarListItem
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog
from kivymd.uix.list import OneLineAvatarIconListItem

from db.accountdb import reset
from db.sqlite3_connect import insert_data, select_data, create_table
from custom_gestures.gesture_box import GestureBox

Window.size = (500, 850)


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class SaveImageDialog(BoxLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ResetDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class IconRightSampleWidget(IRightBodyTouch, MDSwitch):
    pass


# class AvatarDialog(ScrollView):
# cancel = ObjectProperty(None)
# pass


# Factory.register('AvatarDialog', cls=AvatarDialog)


class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class OneLineLeftAvatarItem(OneLineAvatarListItem):
    divider = None
    source = StringProperty()


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class ResetPasswordDialogsContent(BoxLayout):

    def reset_password(self):
        me = App.get_running_app().screen_manager.get_screen('Me')
        global user, password_reset
        current_user = me.children[0].ids.name_input.text.lstrip()
        old_password = self.ids.old_password.text.lstrip()
        new_password = self.ids.new_password.text.lstrip()
        if old_password and new_password:
            if new_password != old_password:
                user, password_reset = reset(current_user, new_password)
                # set_password(user_forget_password, confirm_new_set_password)
                if user:
                    toast("Successfully Changed Password !")
                    # self.success_retrieve()
                else:
                    toast("Something Wrong !")
            else:
                toast("Please enter a password different from the original password !")
        else:
            toast("Please ensure that all information is completed !")


class MePage(FloatLayout):
    account_dialog = None
    language_setting_dialog = None
    reset_password_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # sql = 'SELECT * FROM user WHERE id=1'
        # self.ids.name_input.text = res[0][1]
        # self.me_name_callback()
        # info = App.get_running_app().screen_manager.get_screen('Info')
        # sql = "'SELECT * FROM account WHERE Email='{}'".format(info.children[0].ids.slide_name_label.text.lstrip())
        # res = select_data(sql)
        # self.ids.name_input.text = res[1][2]

    def save_head_image(self, path, filename):
        """保存头像路径"""
        self.head_path = os.path.join(path, filename)
        self.ids.test_image_box.canvas.after.children[2].source = self.head_path
        self.dismiss_popup()

    def show_head_image(self):
        """点击头像回调方法"""
        content = SaveImageDialog(save=self.save_head_image, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload image", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save_all_changes(self):
        """保存修改"""
        # name = self.ids.name_input.text
        # sql = "UPDATE user SET name='" + name + "' WHERE id = 1"
        # print(sql)
        # insert_data(sql)
        self.set_change_value()
        # 改变头像
        self.clear_widgets()
        self.__init__()
        self.return_info_button()
        toast("Successfully Saved All Changes!")

    def reset_all(self):
        """执行重置"""
        # 清除表内所有数据
        create_table()
        if os.name == 'posix':
            path = os.getcwd() + '/image'
        else:
            path = os.getcwd() + '\\image'
        # 更改名字
        sql = "UPDATE user SET name='FHL'"
        insert_data(sql)

        # 关闭弹窗
        # self.dismiss_popup()
        self.clear_widgets()
        self.__init__()
        self.set_change_value()

    def return_info_button(self):
        """返回主页"""
        self.clear_widgets()
        self.__init__()
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = 'Info'

    def set_change_value(self):
        """设置改变的值"""
        # info页面
        info = App.get_running_app().screen_manager.get_screen('Info')
        login = App.get_running_app().screen_manager.get_screen('Login')
        # name
        new_user_name = self.ids.name_input.text.lstrip()
        email = login.children[0].ids.email.text.lstrip()
        # head
        sql = "UPDATE account SET Username = '{}' WHERE Email='{}' ".format(new_user_name, email)
        insert_data(sql)
        info.children[0].ids.slide_name_label.text = self.ids.name_input.text

    def avatar_list(self):
        for root_dir, folders, files in walk("avatars"):
            for av in files:
                self.ids['avatar_grid'].add_widget(
                    ImageButton(
                        source="avatars/" + av,
                        on_release=partial(self.change_avatar, av)
                    )
                )

    def change_avatar(self, avatarImage, btn_id):
        self.avatar = ",avatars/" + avatarImage
        # me = App.get_running_app().screen_manager.get_screen('Me')
        # me.children[0].ids['me_avatar'].source = "avatars/" + avatarImage
        # self.root.ids['chng_avatar'].ids['av_btn'].source = "avatars/" + avatarImage
        self.ids['me_avatar'].source = "avatars/" + avatarImage
        info = App.get_running_app().screen_manager.get_screen('Info')
        info.children[0].ids['avatar_button'].source = "avatars/" + avatarImage
        # self.ids['nav'].ids['av_btn'].source = "avatars/" + avatarImage

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def password_visibility(self):
        login = App.get_running_app().screen_manager.get_screen('Login')
        login.children[0].ids.password.password = False if login.children[0].ids.password.password is True else True
        # self.ids['nav'].ids['av_btn'].source = "avatars/" + avatarImage

    def show_account_dialog(self):
        if not self.account_dialog:
            self.account_dialog = MDDialog(
                title="Set Backup Account",
                type="simple",
                # DEVICE_TYPE="mobile",
                items=[
                    OneLineLeftAvatarItem(
                        text="user01@gmail.com",
                        source="avatars/boy.png/",
                    ),
                    OneLineLeftAvatarItem(
                        text="user02@gmail.com",
                        source="image/boy.png/",
                        # source=f"{os.environ['WOUND_AVATARS']}boy.png"
                    ),
                    OneLineLeftAvatarItem(
                        text="Add Account",
                        source="https://wound-1301658428.cos.ap-nanjing.myqcloud.com/image/add.png",
                    ),
                ],
            )
        self.account_dialog.open()

    def show_language_setting_dialog(self):
        if not self.language_setting_dialog:
            self.language_setting_dialog = MDDialog(
                title="Language Setting",
                type="confirmation",
                items=[
                    ItemConfirm(text=i)
                    for i in [
                        "English",
                        "Simplified Chinese",
                        "Traditional Chinese",
                        "Russian",
                        "French",
                        "Japanese",
                        "Korean",
                        "German",
                        "Thai",
                    ]
                ],
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        # text_color=self.app.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="OK",
                        # text_color=self.app.theme_cls.primary_color
                    ),
                ],
            )
        # self.language_setting_dialog.md_bg_color = self.theme_cls.bg_dark
        self.language_setting_dialog.open()

    def show_alert_dialog(self):
        self.alert_dialog = MDDialog(
            title="Reset Settings?",
            text="This will reset your device to its default factory settings.",
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=(.21176470588235294, .09803921568627451, 1, 1),
                    # on_press=self.dialog.dismiss(),
                ),
                MDFlatButton(
                    text="CONFIRM", text_color=(.21176470588235294, .09803921568627451, 1, 1),
                    # on_press=self.reset_all(),
                ),
            ],
        )
        # self.alert_dialog.md_bg_color = self.theme_cls.bg_dark
        self.alert_dialog.open()

    def reset_warning(self):
        dialog = AKAlertDialog(
            header_icon="exclamation",
            header_bg=[1, 0.75, 0, 1]
        )
        dialog.bind(on_progress_finish=dialog.dismiss)
        content = Factory.ResetWarningDialog()
        content.ids.confirm.bind(on_release=dialog.dismiss)
        content.ids.cancel.bind(on_release=dialog.dismiss)
        content.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    def show_reset_password_dialog(self):
        dialog = AKAlertDialog(
            header_icon="shield-refresh",
            header_bg=[1, 0.75, 0, 1]
        )
        dialog.bind(on_progress_finish=dialog.dismiss)
        content = Factory.ResetPasswordDialogsContent()
        content.ids.submit.bind(on_release=dialog.dismiss)
        content.ids.dismiss.bind(on_release=dialog.dismiss)
        content.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        current_user = self.ids.name_input.text.lstrip()
        github_login_flag_sql = " SELECT Github FROM account WHERE Username='{}'".format(current_user)
        github_login_flag = select_data(github_login_flag_sql)
        # print(github_login_flag[0][0])
        # flag_type = type(github_login_flag[0][0])
        # print(flag_type)
        if github_login_flag[0][0] == 'False':
            # if github_login_flag[0][0]:
            dialog.open()
        else:
            toast("The Password Cannot Be Changed If Login via Github !")

    def reset_login_email_null(self):
        login = App.get_running_app().screen_manager.get_screen('Login')
        login.children[0].ids['email'].text = ""

    @staticmethod
    def return_upload_button():
        App.get_running_app().screen_manager.current = 'Upload'

    @staticmethod
    def me_to_login():
        App.get_running_app().screen_manager.current = 'Login'


class MeApp(MDApp):
    dialog = None

    def build(self):
        # self.theme_cls.theme_style = "Light"
        return MePage()
        # self.root.ids.backdrop.ids._front_layer.md_bg_color = [0, 0, 0, 0]


if __name__ == "__main__":
    MeApp().run()
