from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class Messages(GridLayout):
    def __init__(self, **kwargs):
        super(Messages, self).__init__(**kwargs)
        # self.orientation = 'tb-lr'

        # self.message1 = Label(text='Mensaje 1', size_hint=(1, .10))
        # self.message2 = Label(text='Mensaje 2', size_hint=(1, .10))
        # self.message3 = Label(text='Mensaje 3', size_hint=(1, .10))
        # self.add_widget(self.message1)
        # self.add_widget(self.message2)
        # self.add_widget(self.message3)

    def add_message(self, message):
        # Create Label whose text will be the message
        label = Label(text=message, size_hint=(1, .10))

        # Agregar label a layout
        self.add_widget(label)