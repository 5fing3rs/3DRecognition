""" Main module for template extraction and matching """

import argparse
import imutils
import cv2
import threading
import sys
import time
import Config
import numpy as np
from imutils.video import FileVideoStream
from queue import Queue
from Item import Item
from utilities import printProgressBar
from video_utils import make_240p
from detector import Detector
from window import localise_match, draw_match

DetectorD = Detector(0.09, -0.02)

def write_video(video, frame):
    """ Write to video """
    video.write(frame)

# terrible implementation
def item_threading(ratio, edged, templates, found, i):

    ret_maxval, ret_maxloc = DetectorD.match_templates(ratio,
                                             edged,
                                             templates,
                                             found,
                                             i,
                                             cv2.TM_CCOEFF_NORMED)

    DetectorD.max_val[i] = ret_maxval
    DetectorD.max_loc[i] = ret_maxloc

def main():
    """ Main function """
    # output_video = OutputVideoWriter('./output.avi',1,240,352,True)

    output_filename = "../output/output.avi"

    success = True

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-td',
        action='append',
        dest='tempdirs',
        default=[],
        required=True,
        help="Paths to template directories")
    arg_parser.add_argument("-v", action='store', dest="videofile",
                            required=False, help="Path to the video file")
    args = arg_parser.parse_args()

    item_types = len(args.tempdirs)

    for i in range(0, item_types):
        obj_name = args.tempdirs[i].split('/')
        DetectorD.item_list.append(Item(obj_name[2], 1))
        DetectorD.item_list[i].template_processing(args.tempdirs[i])

    print(args.videofile)

    number_of_frame = 0
    frame_count = 0
    fvs = None

    if args.videofile is None:
        cap = cv2.VideoCapture(0)  # setting input to webcam/live video
        # cap = make_240p(cap)
    else:
        fvs = FileVideoStream(args.videofile).start()
        time.sleep(1.0)
        cap = cv2.VideoCapture(args.videofile)
        number_of_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        try:
            # checking if input is through a video file
            # cap = cv2.VideoCapture(args.videofile)
            # cap = make_240p(cap)
            fvs = FileVideoStream(args.videofile).start()
            time.sleep(1.0)

            number_of_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(number_of_frame)
        except BaseException:
            print("Error in checking the path to the video file.")
            print("Please check the path to the video file.")
            return

    # ret, frame = cap.read()
    frame = fvs.read()
    hheight, wwidth, _ = frame.shape    # '_' had llayers
    writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'PIM1'),
                             25, (wwidth, hheight), True)

    printProgressBar(0, 0, number_of_frame, prefix='Progress:',
                     suffix='Complete', length=50)

    while fvs.more():

        #### LIST DECLARATION ####
        DetectorD.max_val = []
        DetectorD.max_loc = []

        startx_coord = []
        starty_coord = []
        endx_coord = []
        endy_coord = []

        is_drawn = []
        modframe = []
        pixel_pos = []
        ##########################

        # ret, frame = cap.read()
        # success = ret
        # if not success:
        #     break

        frame = fvs.read()

        # converting the video to grayscale to proceed with extraction of edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for i in range(0, item_types):
            DetectorD.item_list[i].found = []
            for j in range(len(DetectorD.item_list[i].templates)):
                DetectorD.item_list[i].found.append(None)

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:

            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            ratio = gray.shape[1] / float(resized.shape[1])

            break_flag = 0

            for i in range(0, item_types):
                for j in range(len(DetectorD.item_list[i].templates)):
                    if (resized.shape[0] < DetectorD.item_list[i].height[j] or
                            resized.shape[0] < DetectorD.item_list[i].width[j]):
                        break_flag = 1

            if break_flag == 1:
                break

            # using Canny edge algorithm to extract edges from the video
            edged = cv2.Canny(resized, 50, 100)
            # cv2.imshow('abv', edged)

            item_threads = []
            for i in range(0, item_types):
                DetectorD.max_val.append(1)
                DetectorD.max_loc.append(1)
                item_threads.append(threading.Thread(target=item_threading, args=(ratio, edged, DetectorD.item_list[i].templates, DetectorD.item_list[i].found, i,)))

            for i in item_threads:
                i.start()
            for i in item_threads:
                i.join()


        for i in range(0, item_types):
            (ret_startx,
             ret_starty,
             ret_endx,
             ret_endy) = localise_match(DetectorD.item_list[i].found,
                                        DetectorD.max_loc[i],
                                        DetectorD.item_list[i].found,
                                        DetectorD.item_list[i].height,
                                        DetectorD.item_list[i].width,
                                        ratio)
            startx_coord.append(ret_startx)
            starty_coord.append(ret_starty)
            endx_coord.append(ret_endx)
            endy_coord.append(ret_endy)



        for i in range(0, item_types):
            if i == 0:
                ret_isdrawn, index_of_max, ret_frame = draw_match(
                    frame, DetectorD.max_val[i], Config.thresh_max, startx_coord[i], starty_coord[i], endx_coord[i], endy_coord[i], 1, DetectorD.item_list[i].article)
            else:
                ret_isdrawn, index_of_max, ret_frame = draw_match(
                    modframe[i - 1], DetectorD.max_val[i], Config.thresh_max, startx_coord[i], starty_coord[i], endx_coord[i], endy_coord[i], 1, DetectorD.item_list[i].article)

            is_drawn.append(ret_isdrawn)

            modframe.append(ret_frame)
            pixel_pos.append(index_of_max)

        writer.write(modframe[item_types - 1])

        for i in range(0, item_types):
            if is_drawn[i]:
                # setting the x and y coordinates to be logged into the log file
                DetectorD.item_list[i].x_abscissa = (
                    startx_coord[i][pixel_pos[i]] + endx_coord[i][pixel_pos[i]]) / 2
                DetectorD.item_list[i].y_ordinate = (
                    starty_coord[i][pixel_pos[i]] + endy_coord[i][pixel_pos[i]]) / 2
            else:
                DetectorD.item_list[i].x_abscissa = None
                DetectorD.item_list[i].y_ordinate = None

        for i in range(0, item_types):
            # logging the coordinates into a file
            DetectorD.item_list[i].log_position()

        frame_count += 1
        fps = Config.fps.fps()
        printProgressBar(fps, frame_count + 1, number_of_frame,
                         prefix='Progress:', suffix='Complete', length=50)

        Config.fps.update()

        if cv2.waitKey(1) == 27:
            break

    Config.fps.stop()
    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    if fvs:
        fvs.stop()

if __name__ == '__main__':
    main()
