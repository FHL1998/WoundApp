import os
from abc import ABC

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivymd.app import MDApp
# from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.utils.fitimage import FitImage
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

from analysis import area
from asyncio_task.asyncio_insert_data import Analysis

Window.size = (400, 750)


# create = App.get_running_app().screen_manager.get_screen('Create')
# PatientName = create.children[0].ids.PatientName.text.lstrip()
# patient_name = area.PatienName


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class ContourPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def press_button():
        App.get_running_app().screen_manager.current = 'Upload'

    @staticmethod
    def contour_to_feature():
        App.get_running_app().screen_manager.current = 'Feature'

    def gain_patient_name_and_image(self):
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        self.ids.patient_name.text = PatientName
        self.ids[
            "input_image"].source = "https://wound-1301658428.cos.ap-nanjing.myqcloud.com/uploadimage/{}_input.jpg" \
            .format(PatientName)
        self.ids[
            "output_image"].source = "https://wound-1301658428.cos.ap-nanjing.myqcloud.com/outputimage/{}_output.jpg" \
            .format(PatientName)
        return PatientName


class ContourApp(MDApp):
    def build(self):
        return ContourPage()


if __name__ == "__main__":
    ContourApp().run()
