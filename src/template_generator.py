import cv2
import os
import argparse
from pathlib import Path 
from PIL import Image

def get_template_path(path, count):
    tokenize = path.split('/')
    main_dir = tokenize[2]
    path_to_image = "../data/%s/templates/%s_%c_%d.jpg" % (main_dir, main_dir, path[-5], count)
    return path_to_image

def resize_image(path, basewidth):
    image = Image.open(path)
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    image.save(path)

def validate_path(path):
    if path.is_file():
        if not(str(path).endswith('avi') or str(path).endswith('mp4')):
            return -1
        else:
            return 1
    return 0

def generate_template(training_video, angle_of_rotation):
    training_video = str(training_video)
    video_capture = cv2.VideoCapture(training_video)
    success, image = video_capture.read()
    count = 0
    success = True
    while success:
        if count%angle_of_rotation == 0:
            template_path = get_template_path(training_video, count)
            cv2.imwrite(template_path,image)
            resize_image(template_path, 250)
        success, image = video_capture.read()
        count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-tv', '--training_video', required=True, action='append', dest='training_video_set',default=[],help='Add the training video path',)
    parser.add_argument('-a', '--angle', action='store', dest='angle',help='Give the angle of rotation')
    args = parser.parse_args()
    training_video_set = args.training_video_set
    angle = 45
    if args.angle:
        angle = args.angle

    for video in training_video_set:
        video = Path(video)
        err = validate_path(video)
        if err == 1:
            generate_template(video, angle)
        elif err == -1:
            print("Invalid format. Allowed formats .avi .mp4")
        elif err == 0:
            print(str(video), "File does not exist")
