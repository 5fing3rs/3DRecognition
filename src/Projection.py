''' Module to get all the required templates for a given object '''

import cv2
import os
from PIL import Image

# CHANGE THIS INTO THE CONFIG FILE
BASE_DIR = os.getcwd()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def check_directory(template_storage_directory):
    if not os.path.isdir(template_storage_directory):
        mkdir_p(BASE_DIR + template_storage_directory)

def resize_image(path_to_image, basewidth):
    image = Image.open(path_to_image)
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    image.save(path_to_image)

def generate_template(video_stream):
    video_capture = cv2.VideoCapture(video_stream)
    success, image = video_capture.read()
    count = 0 
    success = True
    while success:
        if count%2 == 0:
            # cv2.imwrite("../data/syringe_body/templates/%c_syringe_body%d.jpg" % (video_stream[-5],count), image)
            # resize_image("../data/syringe_body/templates/%c_syringe_body%d.jpg" % (video_stream[-5],count), 250)
            tokenize = video_stream.split('/')
            print(tokenize)
            main_dir = tokenize[2]
            path_to_image = "../data/%s/templates/%s_%c_%d.jpg" % (main_dir, main_dir, video_stream[-5], count)
            cv2.imwrite(path_to_image, image)
            resize_image(path_to_image, 250)
            
        success, image = video_capture.read()
        count += 1

if __name__ == "__main__":
    video_stream = input("Enter Path To The Training Video : ")
    # template_storage_directory =  input("Enter The Directory To Store The Templates : ")
    # print(video_stream, template_storage_directory)
    # check_directory(template_storage_directory)
    generate_template(video_stream)
