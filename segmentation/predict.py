import logging
import os
import cv2
from keras.models import load_model
from utils.io.data import save_results, load_test_images, DataGen
from utils.learning.metrics import dice_coef, precision, recall


def import_file(file):
    # plt.imshow(file)
    # plt.savefig("uploadimage/input.jpg")
    logging.info('start import file')
    postfix = os.path.splitext(file)[-1][1:]
    logging.info('postfix is:' + postfix)
    if postfix == 'jpg':
        logging.info('It\'s ready to analyze uploadimage.jpg')
        # sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='FanHaolin'"
        # insert_data(sql)
    elif postfix == 'png':
        logging.info('It\'s ready to analyze uploadimage.png')
        # sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='FanHaolin'"
        # insert_data(sql)
    elif postfix == 'jpeg':
        logging.info('It\'s ready to analyze uploadimage.jpeg')
        # sql = "UPDATE Patient SET Image ='" + file + "' WHERE PatientName='FanHaolin'"
        # insert_data(sql)
    else:
        logging.info('Unable to import %s file' % postfix)


def segment_file(file):
    # plt.imshow(file)
    # plt.savefig("uploadimage/input.jpg")
    logging.info('start import file')
    postfix = os.path.splitext(file)[-1][1:]
    logging.info('postfix is:' + postfix)
    if postfix == 'jpg':
        logging.info('It\'s ready to analyze uploadimage.jpg')
        img = cv2.imread(file)
        cv2.imwrite("segmentation/test/images/1.png", img)
        image_segment(file)
    elif postfix == 'png':
        logging.info('It\'s ready to analyze uploadimage.png')
        img = cv2.imread(file)
        cv2.imwrite("segmentation/test/images/1.png", img)
        image_segment(file)
    elif postfix == 'jpeg':
        logging.info('It\'s ready to analyze uploadimage.jpeg')
        img = cv2.imread(file)
        cv2.imwrite("segmentation/test/images/1.png", img)
        image_segment(file)
    else:
        logging.info('Unable to import %s file' % postfix)


def image_segment(file):
    input_dim_x = 224
    input_dim_y = 224
    color_space = 'rgb'
    path = 'segmentation/'
    weight_file_name = 'my_model.hdf5'
    logging.info('Model is ready to be loaded')

    data_gen = DataGen(path, split_ratio=0.0, x=input_dim_x, y=input_dim_y, color_space=color_space)
    x_test, test_label_filenames_list = load_test_images(path)

    model = load_model('./model/' + weight_file_name
                       , custom_objects={'dice_coef': dice_coef, 'precision': precision, 'recall': recall, })

    for image_batch, label_batch in data_gen.generate_data(batch_size=len(x_test), test=True):
        prediction = model.predict(image_batch, verbose=1)
        save_results(prediction, 'rgb', path + 'test/predictions/', test_label_filenames_list)
        break
