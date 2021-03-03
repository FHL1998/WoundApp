from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd_extensions.akivymd.uix.swipemenu import AKSwipeMenu, AKSwipeMenuBottomContent, AKSwipeMenuTopContent
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineListItem, OneLineIconListItem

from db.sqlite3_connect import select_data

Window.size = (500, 850)


class PatientOneLineIconListItem(OneLineIconListItem):

    def gain_patient_name(self):
        selected_patient = self.text
        print(selected_patient)
        sql_age = "SELECT Age FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_age_result = select_data(sql_age)
        selected_patient_age = sql_age_result[0][0]
        print(selected_patient_age)
        sql_gender = "SELECT Gender FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_gender_result = select_data(sql_gender)
        selected_patient_gender = sql_gender_result[0][0]
        print(selected_patient_gender)
        sql_creation_date = "SELECT CreationDate FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_creation_date_result = select_data(sql_creation_date)
        selected_patient_creation_date = sql_creation_date_result[0][0]
        print(selected_patient_creation_date)
        self.ids.selected_patient_age = selected_patient_age

    def view_selected_patient_information(self):
        history = App.get_running_app().screen_manager.get_screen('History')
        selected_patient = self.text
        history.children[0].ids.search_field.text = selected_patient

        sql_creation_date = "SELECT CreationDate FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_creation_date_result = select_data(sql_creation_date)
        selected_patient_creation_date = sql_creation_date_result[0][0]
        history.children[0].ids.selected_patient_creation_date.text = str(selected_patient_creation_date)

        sql_age = "SELECT Age FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_age_result = select_data(sql_age)
        selected_patient_age = sql_age_result[0][0]
        history.children[0].ids.selected_patient_age.text = str(selected_patient_age)

        sql_gender = "SELECT Gender FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_gender_result = select_data(sql_gender)
        selected_patient_gender = sql_gender_result[0][0]
        history.children[0].ids.selected_patient_gender.text = str(selected_patient_gender)

        sql_swelling = "SELECT Swelling FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_swelling_result = select_data(sql_swelling)
        selected_patient_swelling = sql_swelling_result[0][0]
        history.children[0].ids.selected_patient_swelling.text = str(selected_patient_swelling)

        sql_area = "SELECT Area FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_area_result = select_data(sql_area)
        selected_patient_area = sql_area_result[0][0]
        history.children[0].ids.selected_patient_area.text = str(selected_patient_area)

        sql_infection = "SELECT Infection FROM Patient WHERE PatientName='{}'".format(selected_patient)
        sql_infection_result = select_data(sql_infection)
        selected_patient_infection = sql_infection_result[0][0]
        history.children[0].ids.selected_patient_infection.text = str(selected_patient_infection)


class HistoryPage(Screen):
    patient_information_items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.view_patient_name()\
        # Fself.set_list_md_icons(self, search=False)

    # def on_start(self):
    # rows = select_data("SELECT PatientName FROM Patient ORDER BY CreationDate")
    # for row in rows:
    # for patient_name in row:
    # self.root.ids.container.add_widget(
    # OneLineListItem(text=f" {patient_name}")
    # )
    def make_search_textfield_null(self):
        self.ids.search_field.text = ''

    def set_list_patient_information(self, text="", search=False):
        """Builds a list of icons for the screen MDIcons."""

        def add_patient_item(patient_name):
            self.ids.rv.data.append(
                {
                    "viewclass": "PatientOneLineIconListItem",
                    "text": patient_name,
                }
            )

        self.ids.rv.data = []
        rows = select_data("SELECT PatientName FROM Patient ORDER BY CreationDate")
        # print(rows)
        for row in rows:
            # print(row)
            for patient_name in row:
                # print(patient_name)
                if search:
                    if text in patient_name:
                        add_patient_item(patient_name)
                        # self.ids.result_field.text = patient_name
                else:
                    add_patient_item(patient_name)

    # def view_patient_name(self):
    # """Builds a list of icons for the screen MDIcons."""
    # rows = select_data("SELECT PatientName FROM Patient WHERE PatientName='FanHaolin'")
    # rows = select_data("SELECT PatientName FROM Patient ORDER BY CreationDate")
    # for row in rows:
    # for col in row:
    # self.patient_information_items.append(col)
    @staticmethod
    def history_to_info():
        App.get_running_app().screen_manager.current = 'Info'


class HistoryApp(MDApp):
    def build(self):
        return HistoryPage()


if __name__ == '__main__':
    HistoryApp().run()
