import smtplib
import ssl
from datetime import *
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.app import MDApp
from kivymd.uix import SpecificBackgroundColorBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

from analysis import area
from db.sqlite3_connect import select_data
from utils.config import globalvar as gl

Window.size = (400, 750)

doc = SimpleDocTemplate("Wound_Analysis_Report.pdf", pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=60, bottomMargin=15)

subject = "An email with attachment from Wound Analysis"
body = "This is an email with attachment sent from Wound Analysis.This application will strictly implement " \
       "confidentiality procedures, so your information will not be at risk of leakage. The report in the attachment " \
       "represents the analysis result, please follow the doctor’s advice for the true situation. "
sender_email = "fhlielts8@163.com"
receiver_email = "fhlielts8@163.com"

# sender_email = "164931787@qq.com"
password = 'ZOLMZPMAVKMQPAFO'

pdfmetrics.registerFont(TTFont('times_b2', 'site_packages/TIMES-B2.ttf'))
pdfmetrics.registerFont(TTFont('dour', 'site_packages/dour.ttf'))


# gl._init()
class CustomToolbar(RectangularElevationBehavior, SpecificBackgroundColorBehavior, BoxLayout):
    pass


class SelectableButton(RecycleDataViewBehavior, Button):
    """Add selection support to the Button"""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)


class EmailSendDialogsContent(BoxLayout):

    def email_dialog(self):
        # receiver_email = self.ids.receiver_email.text
        dialog = AKAlertDialog(
            header_icon="email-receive",
            header_bg=[1, 0.75, 0, 1],
            # progress_interval=3,
        )
        dialog.bind(on_progress_finish=dialog.dismiss)
        content = Factory.EmailDialog()
        content.ids.send.bind(on_release=dialog.dismiss)
        content.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()


class FeaturePage(FloatLayout):
    Patient_items = ListProperty([])
    Age_items = ListProperty([])
    Gender_items = ListProperty([])
    Swelling_items = ListProperty([])
    Redness_items = ListProperty([])
    Pus_items = ListProperty([])
    Area_items = ListProperty([])
    Infection_items = ListProperty([])
    now = datetime.now()

    def create_time(self, **kwargs):
        self.now = datetime.now()
        self.timelabel.text = self.now.strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def view_detailed_information(self):
        self.Name()
        self.Age()
        self.Gender()
        self.detect_Swelling()
        self.detect_Redness()
        self.detect_Pus()
        self.detect_Area()
        self.detect_Infection()

    def Name(self):
        """为name赋值"""
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "SELECT PatientName FROM Patient WHERE PatientName='{}'".format(PatientName)
        # sql = "SELECT PatientName FROM Patient WHERE PatientName='FanHaolin'"
        res = select_data(sql)
        self.ids.name.text = str(res[0][0])

    def Age(self):
        """为name赋值"""
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "SELECT Age FROM Patient WHERE PatientName='{}'".format(PatientName)
        # sql = "SELECT Age FROM Patient WHERE PatientName='FanHaolin'"
        res = select_data(sql)
        self.ids.age.text = str(res[0][0])

    # def Patient(self):
    # global row_patient
    # rows = select_data("SELECT PatientName FROM Patient WHERE PatientName='FanHaolin'")
    # for row_patient in rows:
    # for col in row_patient:
    # self.Patient_items.append(col)
    # print(row_patient)

    # def Age(self):
    # global row_Age
    # rows = select_data("SELECT Age FROM Patient WHERE PatientName='FanHaolin'")
    # for row_Age in rows:
    # for col in row_Age:
    # self.Age_items.append(col)
    # print(row_Age)

    def Gender(self):
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "SELECT Gender FROM Patient WHERE PatientName='{}'".format(PatientName)
        # sql = "SELECT Gender FROM Patient WHERE PatientName='FanHaolin'"
        res = select_data(sql)
        self.ids.gender.text = str(res[0][0])

    def detect_Swelling(self):
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "SELECT Swelling FROM Patient WHERE PatientName='{}'".format(PatientName)
        # sql = "SELECT Swelling FROM Patient WHERE PatientName='FanHaolin'"
        res = select_data(sql)
        self.ids.swelling.text = str(res[0][0])

    def detect_Redness(self):
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "SELECT Redness FROM Patient WHERE PatientName='{}'".format(PatientName)
        # sql = "SELECT Redness FROM Patient WHERE PatientName='FanHaolin'"
        res = select_data(sql)
        self.ids.redness.text = str(res[0][0])

    def detect_Pus(self):
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "SELECT Pus FROM Patient WHERE PatientName='{}'".format(PatientName)
        # sql = "SELECT Pus FROM Patient WHERE PatientName='FanHaolin'"
        res = select_data(sql)
        self.ids.pus.text = str(res[0][0])

    def detect_Area(self):
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "SELECT Area FROM Patient WHERE PatientName='{}'".format(PatientName)
        # sql = "SELECT Area FROM Patient WHERE PatientName='FanHaolin'"
        res = select_data(sql)
        self.ids.area.text = str(res[0][0])

    def detect_Infection(self):
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "SELECT Infection FROM Patient WHERE PatientName='{}'".format(PatientName)
        # sql = "SELECT Infection FROM Patient WHERE PatientName='FanHaolin'"
        res = select_data(sql)
        self.ids.infection.text = str(res[0][0])

    def show_email_send_dialog(self):
        dialog = AKAlertDialog(
            header_icon="shield-refresh",
            header_bg=[1, 0.75, 0, 1]
        )
        dialog.bind(on_progress_finish=dialog.dismiss)
        content = Factory.EmailSendDialogsContent()
        content.ids.send.bind(on_release=dialog.dismiss)
        content.ids.cancel.bind(on_release=dialog.dismiss)
        content.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    @staticmethod
    def feature_to_contour():
        App.get_running_app().screen_manager.current = "Contour"

    @staticmethod
    def feature_to_info():
        App.get_running_app().screen_manager.current = "Info"
        generate_pdf()

    @staticmethod
    def email_report():
        email()


class FeatureApp(MDApp):
    # title = "Wound Feature"

    def build(self):
        return FeaturePage()

    # def email_report(self):
    # receiver_email = self.ids.receiver_email.text
    # email()


def generate_pdf():
    swelling = gl.get_value('swelling')
    wound_area = area.wound_area
    redness = area.redness_result
    infection = area.infection_result
    pus = area.pus_result

    create = App.get_running_app().screen_manager.get_screen('Create')
    PatientName = create.children[0].ids.PatientName.text.lstrip()
    upload_image_file_path = "uploadimage/{}_input.jpg".format(PatientName)
    Story = []
    logo = "image/hospital1.png"
    input_image = upload_image_file_path
    # input_image = 'uploadimage/input.jpg'
    contour = "outputimage/{}_output.jpg".format(PatientName)
    #contour = 'outputimage/contour.jpg'
    formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    # create = App.get_running_app().screen_manager.get_screen('Create')
    full_name = PatientName
    # full_name = "Fan Haolin"

    im = Image(logo, 1 * inch, 1 * inch)
    input_image = Image(input_image, 3 * inch, 2 * inch)
    contour = Image(contour, 2.3 * inch, 2 * inch)
    component_data = [['Original Image', 'Contour Result'],
                      [input_image, contour],
                      ]
    component_table = Table(component_data, colWidths=[230, 230])
    component_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 8),  # (列,行)坐标
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # 在默认用户空间中，原点（0,0）点位于左下角
        ('FONTSIZE', (0, 0), (-1, -1), 14),  # 字体大小
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),  # 设置第一行背景颜色
        ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.grey),  # 设置表格左边线颜色为灰色，线宽为0.1
        ('TEXTCOLOR', (0, 1), (-2, -1), colors.royalblue),  # 设置表格内文字颜色
        # ('ALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # 对齐
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # 对齐
        ('GRID', (0, 0), (-1, -1), 0.6, colors.red),  # 设置表格框线为红色，线宽为0.5
    ]))

    Story.append(im)
    # Story.append(im2)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleStyle", alignment=TA_CENTER, ))
    ptext = '<font size="26">Wound Analysis Report</font>'
    Story.append(Paragraph(ptext, styles["TitleStyle"]))
    styles.add(ParagraphStyle(name='Letter', fontName="dour", alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Letter_title', fontName="times_b2", alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Corner', fontName="times_b2", alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    Story.append(Spacer(1, 32))
    ptext = '<font size="14">Generation Date:%s</font>' % formatted_time
    Story.append(Paragraph(ptext, styles["Letter"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size="14">Patient Name:%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    Story.append(component_table)
    Story.append(Spacer(1, 12))
    ptext = f'<font size="14">Swelling :{swelling}  </font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = f'<font size="14">Redness :{redness}  </font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = f'<font size="14">Pus :{pus}  </font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = f'<font size="14">Area :{wound_area}  </font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = f'<font size="14">Infection :{infection}  </font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 45))  # length=1,width=50

    ptext = '<font size="12">Dear %s:</font>' % full_name.split()[0].strip()
    Story.append(Paragraph(ptext, styles["Letter_title"]))

    Story.append(Spacer(1, 24))
    ptext = f'<font size="12">The above report is for reference only, please consult a professional doctor for ' \
            f'details.</font> '
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 24))
    ptext = f'<font size="12">The Result will strictly abide by the doctor-patient confidentiality agreement.</font> '
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 24))
    ptext = f'<font size="12">Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Letter_title"]))
    Story.append(Spacer(1, 12))
    ptext = f'<font size="12">Wound Analysis Application</font>'
    Story.append(Paragraph(ptext, styles["Letter_title"]))
    Story.append(Spacer(1, 28))
    # string = String(150,100,'Copyright xa2 2021 Wound Analysis All Rights Reserved.', fontSize=10, fillColor=colors.red)
    # Story.append(Paragraph(string, styles["Corner"]))
    ptext = f'<font size="10">Copyright @ 2021 Wound Analysis All Rights Reserved.</font>'
    Story.append(Paragraph(ptext, styles["Corner"]))
    doc.build(Story)


def email():
    generate_pdf()
    # Create a multipart message and set headers
    message = MIMEMultipart()
    # message["From"] = "fhlielts8@163.com"
    # message["To"] = "wlwqtgm<wlwqtgm@163.com>"

    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "Wound_Analysis_Report.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.163.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


if __name__ == "__main__":
    FeatureApp().run()
