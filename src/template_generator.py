'''Module to generate templates of a given Mesh Model'''
import argparse
from pathlib import Path
import cv2
from PIL import Image
from utilities import printProgressBar1

def get_template_path(path, count):
    ''' Get the path of the template that will be generated.'''
    tokenize = path.split('/')
    main_dir = tokenize[2]
    path_to_image = "../data/%s/templates/%s_%c_%d.jpg" % (
        main_dir, main_dir, path[-5], count)
    return path_to_image


def resize_image(path, basewidth):
    ''' Resize the generated image with a locked ratio to
    conform to the base width used for detection'''
    image = Image.open(path)
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    image.save(path)


def validate_path(path):
    ''' Validate the given video file path and format'''
    if path.is_file():
        if not(str(path).endswith('avi') or str(path).endswith('mp4')):
            return -1
        return 1
    return 0


def generate_template(training_video, angle_of_rotation, base_width):
    ''' Generate templates for the given video and save them'''
    training_video = str(training_video)
    video_capture = cv2.VideoCapture(training_video)
    number_of_frame = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(number_of_frame)
    print("Generating templates for {}".format(training_video))
    success, image = video_capture.read()
    count = 0
    success = True
    while success:
        if count % angle_of_rotation == 0:
            template_path = get_template_path(training_video, count)
            cv2.imwrite(template_path, image)
            resize_image(template_path, base_width)
        success, image = video_capture.read()
        count += 1
        printProgressBar1(count, number_of_frame,
                            prefix='Progress:', suffix='Complete', length=50)



if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-tv', '--training_video', required=True, action='append',
                        dest='training_video_set', default=[], help='Add the training video path',)
    PARSER.add_argument('-a', '--angle', action='store',
                        dest='angle', help='Give the angle of rotation')
    PARSER.add_argument('-bw', '--basewidth', action='store',
                        dest='basewidth', help='Give the base width of the template')
    ARGS = PARSER.parse_args()
    TRAINING_VIDEO_SET = ARGS.training_video_set
    ANGLE = 45
    BASE_WIDTH = 150

    if ARGS.basewidth:
        BASE_WIDTH = ARGS.basewidth

    if ARGS.angle:
        ANGLE = ARGS.angle

    for video in TRAINING_VIDEO_SET:
        video = Path(video)
        err = validate_path(video)
        if err == 1:
            generate_template(video, int(ANGLE), int(BASE_WIDTH))
        elif err == -1:
            print("Invalid format. Allowed formats .avi .mp4")
        elif err == 0:
            print(str(video), "File does not exist")
