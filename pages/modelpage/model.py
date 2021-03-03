import os
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen

from custom_gestures.gesture_box import GestureBox
from time import strftime
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.image import Image, AsyncImage
# from asyncio_task.asyncio import EventLoopWorker
from asyncio_task.asyncio_insert_data import EventLoopWorker, Segment
from kivy.clock import Clock

# Clock.max_iteration = 10000
Window.size = (400, 750)


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class MyBackdropFrontLayer(ScrollView):

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

        self.event_loop_worker = worker = Segment(path)
        worker.start()
        # segment = App.get_running_app().screen_manager.get_screen('Segment')
        # source = segment.children[0].ids.original_image.source.lstrip()
        App.get_running_app().screen_manager.current = "Segment"

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
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload Image", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_segmentation(self):
        # 绑定保存和取消的方法
        content = SaveDialog(save=self.segment, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload file", content=content, size_hint=(0.9, 0.9))
        # 打开窗口
        self._popup.open()

    def segment(self, path, filename):
        file_path = os.path.join(path, filename)
        self.ids.status.text = file_path
        self.event_loop_worker = worker = Segment(file_path)
        worker.start()
        App.get_running_app().screen_manager.current = "Segment"
        self.dismiss_popup()


class MyBackdropBackLayer(ScreenManager):

    # def capture(self, *args):
    # camera = self.ids.camera
    # timestamp = strftime("%Y%m%d%H%M%S")
    # camera.export_to_png("capture_{}.png".format(timestamp))

    @staticmethod
    def model_to_info():
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = 'Info'

    @staticmethod
    def model_to_segment():
        App.get_running_app().screen_manager.current = "Segment"


class ExampleBackdrop(Screen):
    pass


class ItemBackdropBackLayer(ThemableBehavior, BoxLayout):
    icon = StringProperty("android")
    text = StringProperty()
    selected_item = BooleanProperty(False)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            for item in self.parent.children:
                if item.selected_item:
                    item.selected_item = False
            self.selected_item = True
        return super().on_touch_down(touch)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


Factory.register('SaveDialog', cls=SaveDialog)


class ModelPage(GestureBox):
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

        self.event_loop_worker = worker = Segment(path)
        worker.start()
        App.get_running_app().screen_manager.current = "Segment"

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload Image", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_segmentation(self):
        # 绑定保存和取消的方法
        content = SaveDialog(save=self.segment, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload file", content=content, size_hint=(0.9, 0.9))
        # 打开窗口
        self._popup.open()

    def segment(self, path, filename):
        file_path = os.path.join(path, filename)
        self.ids.status.text = file_path
        self.event_loop_worker = worker = Segment(file_path)
        worker.start()
        App.get_running_app().screen_manager.current = "Segment"
        self.dismiss_popup()

    def save(self, path, filename):
        file_path = os.path.join(path, filename)
        self.ids.status.text = file_path
        self.event_loop_worker = worker = EventLoopWorker(file_path)
        self.ids.upload_tip.text = "Uploading......\nThe Upload Direction is:"
        worker.start()

        self.dismiss_popup()

    @staticmethod
    def model_to_info():
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = 'Info'

    @staticmethod
    def model_to_segment():
        App.get_running_app().screen_manager.current = "Segment"


class ModelApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.ids = None

    def build(self):
        # self.root = ExampleBackdrop()
        return ModelPage()

    # def capture(self, *args):
    # camera = self.ids.camera

    # timestamp = strftime("%Y%m%d%H%M%S")
    # camera.export_to_png("capture_{}.png".format(timestamp))


if __name__ == '__main__':
    ModelApp().run()
