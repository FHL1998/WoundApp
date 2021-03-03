from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from time import strftime
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation

Window.size = (500, 850)
from kivymd.app import MDApp


class CameraPage(BoxLayout):

    def __init__(self, **kwargs):
        super(CameraPage, self).__init__(**kwargs)

    def capture(self, *args):
        camera = self.ids.camera

        timestamp = strftime("%Y%m%d%H%M%S")
        camera.export_to_png("capture_{}.png".format(timestamp))

        with camera.canvas.after:
            Color(1, 1, 1, .3)
            Rectangle(pos=camera.pos, size=camera.size)

        anim = Animation(opacity=0, duration=.2)
        anim.start(camera)
        anim.bind(on_complete=self.flash)

    def flash(self, *args):
        camera = args[1]
        camera.canvas.after.clear()
        camera.opacity = 1

    @staticmethod
    def camera_to_upload():
        # time.sleep(1)
        App.get_running_app().screen_manager.current = 'Upload'

class CameraApp(MDApp):

    def build(self):
        return CameraPage()


if __name__ == "__main__":
    CameraApp().run()
