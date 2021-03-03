import time

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
import datetime
import logging
import re
import os

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd_extensions.akivymd.uix.datepicker import AKDatePicker
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

from db.sqlite3_connect import insert_data

Config.set('graphics', 'resizable', False)
Window.size = (500, 850)


class CreatePage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.CreationDate = AKDatePicker(callback=self.callback)

    def success(self):
        dialog = AKAlertDialog(
            header_icon="check-circle-outline", header_bg=[0, 0.7, 0, 1]
        )
        content = Factory.SuccessDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()
        time.sleep(1)
        # App.get_running_app().screen_manager.current = 'Upload'

    def callback(self, CreationDate):
        if not CreationDate:
            return
        self.ids.CreationDate.text = "%d / %d / %d" % (CreationDate.year, CreationDate.month, CreationDate.day)

    def open(self):
        self.CreationDate.open()

    @staticmethod
    def create_to_index():
        App.get_running_app().screen_manager.current = "Upload"

    def makeInputTextNull(self):
        #self.ids.PatientName.text = ''
        self.ids.Age.text = ''
        self.ids.Gender.text = ''
        self.ids.CreationDate.text = ''

    def createNewUser(self):

        PatientName = self.ids.PatientName.text.lstrip()
        Age = self.ids.Age.text.lstrip()
        Gender = self.ids.Gender.text.lstrip()
        CreationDate = self.ids.CreationDate.text.lstrip()

        if PatientName != "" and Age != "" and Gender != "" and CreationDate != "":
            sql = 'INSERT INTO PATIENT (PatientName,Age,Gender,CreationDate) ' \
                  'VALUES (\"' + PatientName + '\",\"' + Age + '\",\"' + Gender + '\",\"' + CreationDate + '\")'
            insert_data(sql)
            self.success()
            self.makeInputTextNull()
        elif PatientName == "":
            toast("Please input Patient Name in correct form first!")
        elif PatientName != "" and Age == "":
            toast("Please input Age in correct form!")
        elif PatientName != "" and Age != "" and Gender == "":
            toast("Please input Gender in correct form!")
        elif PatientName != "" and Age != "" and Gender != "" and CreationDate == "":
            if Gender != "Male" and Gender != "Female" and Gender != "male" and Gender != "female":
                toast("Gender must be Male or Female!")
            else:
                toast("Please input or select Creation Date in correct form!")

    @staticmethod
    def create_to_upload():
        # time.sleep(1)
        App.get_running_app().screen_manager.current = 'Upload'

    @staticmethod
    def skip_create():
        App.get_running_app().screen_manager.current = 'Upload'

    @staticmethod
    def back_home():
        App.get_running_app().screen_manager.current = 'Info'


class CreateApp(MDApp):
    def build(self):
        return CreatePage()


if __name__ == '__main__':
    CreateApp().run()
