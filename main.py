import webbrowser
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from os import walk, path, remove
from functools import partial
from pages.loginpage.login import LoginPage
from pages.githubpage.github import GithubPage
from pages.registerpage.register import RegisterPage
from pages.forgetpage.forget import ForgetPage
from pages.createpage.create import CreatePage
from pages.contourpage.contour import ContourPage
# from pages.camerapage.camera import CameraPage
# from pages.detailpage.detail import DetailPage
from pages.featurepage.feature import FeaturePage, email
from pages.historypage.history import HistoryPage
from pages.helppage.help import HelpPage
from pages.indexpage.index import IndexPage
from pages.infopage.info import InfoPage

from pages.mepage.me import MePage
from pages.modelpage.model import ModelPage
# from pages.segmentpage.segment import SegmentPage
from pages.toolpage.tool import ToolPage
from pages.uploadpage.upload import UploadPage
from pages.aboutpage.about import AboutPage

Window.size = (500, 850)


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class MyApp(MDApp):

    def build(self):
        self.icon = 'image/hospital1.png'
        # 加载kv文件
        self.load_kv("pages/indexpage/index.kv")
        self.load_kv("pages/loginpage/login.kv")
        self.load_kv("pages/githubpage/github.kv")
        self.load_kv("pages/registerpage/register.kv")
        self.load_kv("pages/forgetpage/forget.kv")
        self.load_kv("pages/createpage/create.kv")
        self.load_kv("pages/uploadpage/upload.kv")
        # self.load_kv("pages/camerapage/camera.kv")
        self.load_kv("pages/contourpage/contour.kv")
        self.load_kv("pages/featurepage/feature.kv")
        self.load_kv("pages/historypage/history.kv")
        self.load_kv("pages/infopage/info.kv")
        self.load_kv("pages/mepage/me.kv")
        self.load_kv('pages/helppage/help.kv')
        self.load_kv('pages/modelpage/model.kv')
        # self.load_kv('pages/segmentpage/segment.kv')
        # self.load_kv('pages/detailpage/detail.kv')
        self.load_kv('pages/toolpage/tool.kv')
        self.load_kv('pages/aboutpage/about.kv')

        self.screen_manager = ScreenManager()
        pages = {'Index': IndexPage(),
                 'Info': InfoPage(),
                 'Login': LoginPage(),
                 'Github': GithubPage(),
                 'Register': RegisterPage(),
                 'Forget': ForgetPage(),
                 'Create': CreatePage(),
                 'Upload': UploadPage(),
                 'Model': ModelPage(),
                 # 'Segment': SegmentPage(),
                 'Me': MePage(),
                 'Help': HelpPage(),
                 'Contour': ContourPage(),
                 'Feature': FeaturePage(),
                 # 'Detail': DetailPage(),
                 'History':HistoryPage(),
                 'Tool': ToolPage(),
                 'About': AboutPage()
                 }
        # pages = {'Index': IndexPage(), 'Info': InfoPage(), 'Login': LoginPage(), 'Create': CreatePage(),
        # 'Upload': UploadPage(),'Camera':CameraPage(),
        # 'Me': MePage(), 'Help': HelpPage(), 'Contour': ContourPage(), 'Segment': SegmentPage(),
        # 'Feature': FeaturePage(), 'Model': ModelPage(), 'Detail': DetailPage(), 'Tool': ToolPage(),
        # 'Chat': ChatPage()}
        for item, page in pages.items():
            self.default_page = page
            screen = Screen(name=item)
            # 添加页面
            screen.add_widget(self.default_page)
            # 向屏幕管理器添加页面
            self.screen_manager.add_widget(screen)
        return self.screen_manager

    data = {
        'upload-network': 'Upload Image',
        'calculator': 'Analyze Image',
        'camera': 'Take Photo',
    }

    def change_avatar(self, avatarImage, btn_id):
        self.avatar = ",avatars/" + avatarImage
        # self.root.ids['chng_avatar'].ids['av_btn'].source = "avatars/" + avatarImage
        self.root.ids['me_avatar'].source = "avatars/" + avatarImage
        # self.root.ids['dashboard'].ids['av_btn'].source = "avatars/" + avatarImage

    def ThemeMode(self, *args):
        t = self.theme_cls.theme_style
        t = "Light" if t != "Light" else "Dark"
        self.theme_cls.theme_style = t

    def switch_theme_style(self):
        self.theme_cls.theme_style = (
            "Light" if self.theme_cls.theme_style != "Light" else "Dark"
        )

    def open_website(self, value):
        webbrowser.open(value)

    @staticmethod
    def email_report():
        email()

    @staticmethod
    def register_to_login():
        App.get_running_app().screen_manager.current = 'Login'

    @staticmethod
    def forget_to_login():
        App.get_running_app().screen_manager.current = 'Login'

    @staticmethod
    def create_to_info():
        App.get_running_app().screen_manager.current = 'Info'

    @staticmethod
    def feature_to_info():
        App.get_running_app().screen_manager.current = "Info"


if __name__ == "__main__":
    recite_app = MyApp()
    # 设置标题
    recite_app.title = 'Wound Analysis'
    recite_app.run()
