import os
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty, OptionProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.imagelist import SmartTile
from os import environ
from kivy.uix.screenmanager import Screen
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

from custom_gestures.gesture_box import GestureBox
from kivy.uix.image import Image
from asyncio_task.asyncio_insert_data import EventLoopWorker, Analysis

Window.size = (400, 750)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


Factory.register('SaveDialog', cls=SaveDialog)


# Factory.register('SaveDialog', cls=SaveDialog)


class UploadPage(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_loop_worker = None
        self.manager_open = False
        Window.bind(on_keyboard=self.events)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
            ext=['.png', '.jpg', '.jpeg']
        )

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.event_loop_worker = worker = Analysis(path)
        worker.start()
        App.get_running_app().screen_manager.current = "Contour"

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def dismiss_popup(self):
        #   关闭弹窗
        self._popup.dismiss()

    def show_save(self):
        # 绑定保存和取消的方法
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload file", content=content, size_hint=(0.9, 0.9))
        # 打开窗口
        self._popup.open()

    def show_contour(self):
        # 绑定保存和取消的方法
        content = SaveDialog(save=self.analyze, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload file", content=content, size_hint=(0.9, 0.9))
        # 打开窗口
        self._popup.open()

    def analyze(self, path, filename):
        file_path = os.path.join(path, filename)
        self.ids.status.text = file_path
        self.event_loop_worker = worker = Analysis(file_path)
        worker.start()
        App.get_running_app().screen_manager.current = "Contour"
        self.dismiss_popup()

    def save(self, path, filename):
        file_path = os.path.join(path, filename)
        self.ids.status.text = file_path
        self.event_loop_worker = worker = EventLoopWorker(file_path)
        self.ids.upload_tip.text = "Uploading......\nThe Upload Direction is:"
        worker.start()

        self.dismiss_popup()

    def callback(self, ins):
        if ins.icon == 'upload-network':
            self.show_save()
        elif ins.icon == 'calculator':
            self.file_manager_open()
        # elif ins.icon == 'camera':
        # App.get_running_app().screen_manager.current = "Camera"
        else:
            pass

    @staticmethod
    def upload_to_info():
        #   右滑返回上一界面（从 upload 到 info 界面)
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = 'Info'

    @staticmethod
    def upload_to_contour():
        App.get_running_app().screen_manager.current = "Contour"


class UploadApp(MDApp):
    data = {
        'upload-network': 'Upload Image',
        'calculator': 'Analyze Image',
        'camera': 'Take Photo',
    }

    def ThemeMode(self, *args):
        t = self.theme_cls.theme_style
        t = "Light" if t != "Light" else "Dark"
        self.theme_cls.theme_style = t

    def build(self):
        self.theme_cls.theme_style = "Light"
        # UploadPage = Builder.load_file("upload.kv")
        return UploadPage()


if __name__ == '__main__':
    UploadApp().run()
