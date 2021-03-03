# 导入 kivy 的 App 类，它是所有 kivy 应用的基类
from kivy.app import App
# Kivy 内置了丰富的控件(widget)，如
# 按钮 (button), 复选框 (checkbox),
# 标签 (label), 输入框 (textinput),
# 滚动容器 (scrollable container) 等
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd_extensions.akivymd.uix.onboarding import AKOnboarding

Window.size = (400, 750)


class IndexPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.i = 0

    @staticmethod
    def index_to_info():
        App.get_running_app().screen_manager.current = "Login"

    def clicked(self):
        # 每0.04s调用update_bar方法一次
        self.update_bar_trigger = Clock.schedule_interval(self.update_bar, 0.04)

    def update_bar(self, dt):
        if self.i <= 100:
            # 赋值
            self.ids.progress_bar.value += self.i
            self.i += 1
            self.update_bar_trigger()


# 从 App 类中继承了 kivy 应用最基本的方法，如创建窗口、设置窗口的大小和位置等
class IndexApp(MDApp):
    # 实现 TestApp 类的 build 方法（继承自 App 类）
    def build(self):
        # build 方法返回的控件，在 Kivy 中，称之为“根控件” (root widget)
        # Kivy 将自动缩放根控件，让它填满整个窗口。
        return IndexPage()


# 当.py文件被直接运行时，
# if __name__ == '__main__'之下的代码块 将被运行
# 当.py文件以模块形式被导入时，
# if __name__ == '__main__'之下的代码块 不被运行
if __name__ == "__main__":
    from kivy.core.window import Window
    Window.clearcolor = [.8, .8, .8, 1]
    IndexApp().run()
