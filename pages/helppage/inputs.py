import kivy
# kivy.require('2.0.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window


class Inputs(BoxLayout):
    text_input = ObjectProperty(None)
    button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Inputs, self).__init__(**kwargs)

        # self.textInput = TextInput(size_hint=(.8, 1))
        # self.button = Button(text='Send', size_hint=(.2, 1))

        # # 0. Al presionar el botón de Send, llamar una función
        # self.button.bind(on_press=self.on_send)
        Clock.schedule_once(self.setup_bindings, 1)

        # self.add_widget(self.textInput)
        # self.add_widget(self.button)

    def setup_bindings(self, dt):
        self.button.bind(on_press=self.on_send)
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # 40 -> Enter
        if self.text_input.focus and keycode == 40:
            self.on_send(self.button)

    def set_messages_handler(self, handler):
        self.messages_handler = handler

    def set_ai(self, ai):
        self.ai = ai

    def on_send(self, instance):
        print('Send!')
        # 1. Leer mensaje desde el input
        # 2. Guardar mensaje en variable
        message = self.text_input.text

        if not message:
            return

        # 2.5. Agregar mensaje a pantalla
        self.messages_handler.add_message(message)

        # 3. Limpiar el input
        self.text_input.text = ''

        # 4. Pasarle el mensaje a la AI
        response = self.ai.message(message)

        if response:
            # 5. Agregar respuesta de AI a la pantalla
            self.messages_handler.add_message(response)
