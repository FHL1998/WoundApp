import logging
import os
import cv2
import numpy as np
from kivy.app import App
from matplotlib import pyplot as plt
from db.sqlite3_connect import insert_data
from utils.config import globalvar as gl

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

global pus_result
global infection_result
global wound_area
global redness_result
global swelling_result
global PatientName

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKID7C4LPIVnTvAHIaMKipiKglbBbkeInpPk '  # 替换为用户的 secretId
secret_key = 'Ng4DQjskNp1OVMtDOKVVTNCnFVW1KWWu'  # 替换为用户的 secretKey
region = 'ap-nanjing'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


def gain_patientname():
    create = App.get_running_app().screen_manager.get_screen('Create')
    PatientName = create.children[0].ids.PatientName.text.lstrip()
    print(PatientName)
    return PatientName


def import_file(file):
    # plt.imshow(file)
    # plt.savefig("uploadimage/input.jpg")
    logging.info('start import file')
    postfix = os.path.splitext(file)[-1][1:]
    logging.info('postfix:' + postfix)
    if postfix == 'jpg':
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='{}'".format(PatientName)
        logging.info('It\'s ready to analyze uploadimage.jpg')
        # sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)

    elif postfix == 'png':
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='{}'".format(PatientName)
        logging.info('It\'s ready to analyze uploadimage.png')
        # sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)

    elif postfix == 'jpeg':
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='{}'".format(PatientName)
        logging.info('It\'s ready to analyze uploadimage.jpeg')
        # sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)

    else:
        logging.info('Unable to import %s file' % postfix)


def image_feature(file):
    gl._init()
    logging.info('Analyzing file')
    postfix = os.path.splitext(file)[-1][1:]
    logging.info('postfix' + postfix)
    if postfix == 'jpg':
        logging.info('Analyzing uploadimage.jpg')
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='{}'".format(PatientName)
        insert_data(sql)
        image_analyze(file)
        detect_redness(file)
        detect_pus(file)
        detect_infection(file)
        find_area(file)
        swelling_analyze(file)

    elif postfix == 'png':
        logging.info('Analyzing uploadimage.jpg')
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='{}'".format(PatientName)
        insert_data(sql)
        image_analyze(file)
        detect_redness(file)
        detect_pus(file)
        detect_infection(file)
        find_area(file)
        swelling_analyze(file)

    elif postfix == 'jpeg':
        logging.info('Analyzing uploadimage.jpg')
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='{}'".format(PatientName)
        insert_data(sql)
        image_analyze(file)
        detect_redness(file)
        detect_pus(file)
        detect_infection(file)
        find_area(file)
        swelling_analyze(file)

    else:
        logging.info('Unable to import %s file' % postfix)


def image_analyze(file):
    img_bgr = cv2.imread(file)
    create = App.get_running_app().screen_manager.get_screen('Create')
    PatientName = create.children[0].ids.PatientName.text.lstrip()
    upload_image_file_path = "uploadimage/{}_input.jpg".format(PatientName)
    output_image_file_path = "outputimage/{}_output.jpg".format(PatientName)
    print(upload_image_file_path)
    cv2.imwrite(upload_image_file_path, img_bgr)
    # cv2.imwrite("uploadimage/{}_input.jpg".format(PatientName), img_bgr)
    client.upload_file(
        Bucket='wound-1301658428',
        LocalFilePath=upload_image_file_path,  # 本地文件的路径
        Key=upload_image_file_path,  # 上传到桶之后的文件名
    )
    img_bgr = img_bgr[330:470, 470:630]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)
    edged = cv2.Canny(img_bin, 180, 200)
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    good_cnts = [x for x in cnts if cv2.contourArea(x) > 2]
    img_rgb_c = cv2.drawContours(img_rgb, good_cnts, -1, (0, 255, 0), 3)
    img_rgb_c = cv2.cvtColor(img_rgb_c, cv2.COLOR_BGR2RGB)

    cv2.imwrite(output_image_file_path, img_rgb_c)
    client.upload_file(
        Bucket='wound-1301658428',
        LocalFilePath=output_image_file_path,  # 本地文件的路径
        Key=output_image_file_path,  # 上传到桶之后的文件名
    )
    # plt.imshow(img_rgb_c)
    # plt.savefig("outputimage/contour.jpg")


def detect_redness(file):
    global redness_result
    gl._init()
    img_bgr = cv2.imread(file)
    img_bgr = img_bgr[330:470, 470:630]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)
    edged = cv2.Canny(img_bin, 180, 200)
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    good_cnts = [x for x in cnts if cv2.contourArea(x) > 2]
    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)

    img_open = img_bin
    kernel_erode = np.ones((8, 8), np.uint8)
    erosion = cv2.erode(img_open, kernel_erode, iterations=3)
    kernel_dilate = np.ones((8, 8), np.uint8)

    _, thresh_bin = cv2.threshold(img_bin, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_cut = cv2.bitwise_and(img_rgb, img_rgb, mask=thresh_bin)
    hsv = cv2.cvtColor(img_cut, cv2.COLOR_RGB2HSV)
    reds = []
    for i in range(hsv.shape[0]):
        for j in range(hsv.shape[1]):
            if 0 < hsv[i, j, 0] < 60:
                reds.append(hsv[i, j])

    np.prod(hsv.shape)
    h = []
    for red in reds:
        h.append(red[0])
    red_number = 0
    for h_value in h:
        if h_value > 13:
            red_number = red_number + 1
    # print(red_number)
    if red_number > 0:
        redness_result = 'Positive'
        # redness_result = str(redness_result)
        gl.set_value('redness', redness_result)
        print(redness_result)
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Redness ='" + redness_result + "' WHERE PatientName='{}'".format(PatientName)
        insert_data(sql)
    else:
        redness_result = 'Negative'
        # redness_result = str(redness_result)
        gl.set_value('redness', redness_result)
        print(redness_result)
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Redness ='" + redness_result + "' WHERE PatientName='{}'".format(PatientName)
        # sql = "UPDATE Patient SET Redness ='" + redness_result + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)


def detect_pus(file):
    global pus_result
    gl._init()
    img_bgr = cv2.imread(file)
    img_bgr = img_bgr[330:470, 470:630]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)
    edged = cv2.Canny(img_bin, 180, 200)
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    good_cnts = [x for x in cnts if cv2.contourArea(x) > 2]
    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)

    img_open = img_bin
    kernel_erode = np.ones((8, 8), np.uint8)
    erosion = cv2.erode(img_open, kernel_erode, iterations=3)
    kernel_dilate = np.ones((8, 8), np.uint8)

    _, thresh_bin = cv2.threshold(img_bin, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_cut = cv2.bitwise_and(img_rgb, img_rgb, mask=thresh_bin)
    hsv = cv2.cvtColor(img_cut, cv2.COLOR_RGB2HSV)
    reds = []
    for i in range(hsv.shape[0]):
        for j in range(hsv.shape[1]):
            if 0 < hsv[i, j, 0] < 60:
                reds.append(hsv[i, j])

    np.prod(hsv.shape)
    h = []
    for red in reds:
        h.append(red[0])
    yellow_number = 0
    for h_value in h:
        if h_value > 4 & h_value < 5:
            yellow_number = yellow_number + 1
    # print(yellow_number)
    if yellow_number > 0:
        pus_result = 'Positive'
        # pus_result = str(pus_result)
        gl.set_value('pus', pus_result)
        print(pus_result)
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Pus ='" + pus_result + "' WHERE PatientName='{}'".format(PatientName)
        # sql = "UPDATE Patient SET Pus ='" + pus_result + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)
    else:
        pus_result = 'Negative'
        # pus_result = str(pus_result)
        gl.set_value('pus', pus_result)
        print(pus_result)
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Pus ='" + pus_result + "' WHERE PatientName='{}'".format(PatientName)
        # sql = "UPDATE Patient SET Pus ='" + pus_result + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)


def detect_infection(file):
    global infection_result
    gl._init()
    img_bgr = cv2.imread(file)
    img_bgr = img_bgr[330:470, 470:630]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)
    edged = cv2.Canny(img_bin, 180, 200)
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    good_cnts = [x for x in cnts if cv2.contourArea(x) > 2]
    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)

    img_open = img_bin
    kernel_erode = np.ones((8, 8), np.uint8)
    erosion = cv2.erode(img_open, kernel_erode, iterations=3)
    kernel_dilate = np.ones((8, 8), np.uint8)

    _, thresh_bin = cv2.threshold(img_bin, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_cut = cv2.bitwise_and(img_rgb, img_rgb, mask=thresh_bin)
    hsv = cv2.cvtColor(img_cut, cv2.COLOR_RGB2HSV)
    reds = []
    for i in range(hsv.shape[0]):
        for j in range(hsv.shape[1]):
            if 0 < hsv[i, j, 0] < 60:
                reds.append(hsv[i, j])

    np.prod(hsv.shape)
    h = []
    for red in reds:
        h.append(red[0])
    red_number = 0
    green_number = 0
    for h_value in h:
        if h_value > 13:
            red_number = red_number + 1
    for h_value in h:
        if h_value > 5 & h_value < 7:
            green_number = green_number + 1
    if green_number < red_number:
        infection_result = 'Positive'
        # infection_result = str(infection_result)
        gl.set_value('infection', infection_result)
        # q = gl.get_value('infection')
        print(infection_result)
        # print(q)
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Infection ='" + infection_result + "' WHERE PatientName='{}'".format(PatientName)
        # sql = "UPDATE Patient SET Infection ='" + infection_result + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)
    else:
        infection_result = 'Negative'
        # infection_result = str(infection_result)
        gl.set_value('infection', infection_result)
        # q = gl.get_value('infection')
        print(infection_result)
        # print(q)
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Infection ='" + infection_result + "' WHERE PatientName='{}'".format(PatientName)
        # sql = "UPDATE Patient SET Infection ='" + infection_result + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)


def find_area(file):
    global wound_area
    gl._init()
    img_bgr = cv2.imread(file)
    img_bgr = img_bgr[330:470, 470:630]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)
    edged = cv2.Canny(img_bin, 180, 200)
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    good_cnts = [x for x in cnts if cv2.contourArea(x) > 2]

    img_open = img_bin
    kernel_erode = np.ones((8, 8), np.uint8)
    erosion = cv2.erode(img_open, kernel_erode, iterations=3)
    kernel_dilate = np.ones((8, 8), np.uint8)
    dilation = cv2.dilate(erosion, kernel_dilate, iterations=3)

    _, thresh_bin = cv2.threshold(img_bin, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh_bin_col = cv2.cvtColor(thresh_bin, cv2.COLOR_GRAY2RGB)
    img_cut = cv2.bitwise_and(img_rgb, img_rgb, mask=thresh_bin)
    wound_area = str(cv2.contourArea(good_cnts[0]))
    gl.set_value('wound_area', wound_area)
    print(wound_area)
    # sql = 'INSERT INTO PATIENT (Area) ' \
    # 'VALUES (\"' + Area + '\")'
    # sql = "INSERT INTO PATIENT (Area) VALUES('%f') WHERE PatientName = 'FanHaolin' % Area"
    # sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='FanHaolin'"
    create = App.get_running_app().screen_manager.get_screen('Create')
    PatientName = create.children[0].ids.PatientName.text.lstrip()
    sql = "UPDATE Patient SET Area ='" + wound_area + "' WHERE PatientName='{}'".format(PatientName)
    # sql = "UPDATE Patient SET Area ='" + wound_area + "' WHERE PatientName='FanHaolin'"
    insert_data(sql)
    img_cut = cv2.cvtColor(img_cut, cv2.COLOR_BGR2RGB)
    cv2.imwrite("outputimage/output2.jpg", img_cut)


# plt.imshow(img_cut)
# plt.savefig("outputimage/output2.jpg")

def swelling_analyze(file):
    global swelling_result
    gl._init()
    img_bgr = cv2.imread(file)
    img_bgr = img_bgr[330:470, 470:630]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)
    edged = cv2.Canny(img_bin, 180, 200)
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    good_cnts = [x for x in cnts if cv2.contourArea(x) > 2]
    (thresh, img_bin) = cv2.threshold(img_gray, 100, 230, cv2.THRESH_BINARY)
    img_bin = cv2.bitwise_not(img_bin)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.erode(img_bin, kernel, iterations=1)
    img_bin = cv2.dilate(img_bin, kernel, iterations=4)

    img_open = img_bin
    kernel_erode = np.ones((8, 8), np.uint8)
    erosion = cv2.erode(img_open, kernel_erode, iterations=3)
    kernel_dilate = np.ones((8, 8), np.uint8)

    _, thresh_bin = cv2.threshold(img_bin, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_cut = cv2.bitwise_and(img_rgb, img_rgb, mask=thresh_bin)
    hsv = cv2.cvtColor(img_cut, cv2.COLOR_RGB2HSV)
    reds = []
    for i in range(hsv.shape[0]):
        for j in range(hsv.shape[1]):
            if 0 < hsv[i, j, 0] < 60:
                reds.append(hsv[i, j])

    np.prod(hsv.shape)
    h = []
    s = []
    v = []

    for red in reds:
        h.append(red[0])
        s.append(red[1])
        v.append(red[2])
    Varience_h = np.var(h)
    Varience_s = np.var(s)
    Varience_v = np.var(v)
    # print(Varience_s)
    # print(Varience_v)
    if (Varience_v > 100) and (Varience_s > 1000):
        swelling_result = 'Positive'
        swelling_result = str(swelling_result)
        gl.set_value('swelling', swelling_result)
        print(swelling_result)
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Swelling ='" + swelling_result + "' WHERE PatientName='{}'".format(PatientName)
        # sql = "UPDATE Patient SET Swelling ='" + swelling_result + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)
    else:
        swelling_result = 'Negative'
        swelling_result = str(swelling_result)
        gl.set_value('swelling', swelling_result)
        print(swelling_result)
        create = App.get_running_app().screen_manager.get_screen('Create')
        PatientName = create.children[0].ids.PatientName.text.lstrip()
        sql = "UPDATE Patient SET Swelling ='" + swelling_result + "' WHERE PatientName='{}'".format(PatientName)
        # sql = "UPDATE Patient SET Swelling ='" + swelling_result + "' WHERE PatientName='FanHaolin'"
        insert_data(sql)
