""" Main module for template extraction and matching """

import argparse
import imutils
import cv2
import threading
import sys
import time
import Config
import numpy as np
from imutils.video import FileVideoStream, WebcamVideoStream
from queue import Queue
from Item import Item
from utilities import printProgressBar
from video_utils import make_240p
from detector import Detector
from window import Window

DetectorD = Detector(0.09, -0.02)
WindowW = Window()

def write_video(video, frame):
    """ Write to video """
    video.write(frame)

# terrible implementation


def main():
    """ Main function """

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

    DetectorD.item_types = len(args.tempdirs)

    for i in range(0, DetectorD.item_types):
        obj_name = args.tempdirs[i].split('/')
        DetectorD.item_list.append(Item(obj_name[2], 1))
        DetectorD.item_list[i].template_processing(args.tempdirs[i])


    Config.number_of_frame = 0
    Config.frame_count = 0
    fvs = None

    if args.videofile is None:
        fvs = WebcamVideoStream(src=0).start()
    else:
        fvs = FileVideoStream(args.videofile).start()
        time.sleep(1.0)
        cap = cv2.VideoCapture(args.videofile)
        Config.number_of_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        try:
            # checking if input is through a video file
            fvs = FileVideoStream(args.videofile).start()
            time.sleep(1.0)

            Config.number_of_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        except BaseException:
            print("Error in checking the path to the video file.")
            print("Please check the path to the video file.")
            return

    frame = fvs.read()
    hheight, wwidth, _ = frame.shape    # '_' had llayers
    writer = cv2.VideoWriter(Config.OUTPUT_FILE, cv2.VideoWriter_fourcc(*'PIM1'),
                             25, (wwidth, hheight), True)

    if args.videofile is not None:
        printProgressBar(0, 0, Config.number_of_frame, prefix='Progress:',
                        suffix='Complete', length=50)

    total_frames = 0

    vidflag = False
    webflag = True
    if args.videofile is None:
        vidflag = True
        webflag = True
    else:
        vidflag = fvs.more()
        webflag = False



    while vidflag:
        total_frames+=1
        if total_frames % 2 == 0:
            #taking every other frame
            pass

        #### LIST DECLARATION ####
        DetectorD.reset_max_loc_val()

        WindowW.reset_cartesian_list()

        WindowW.reset_is_drawn()
        WindowW.reset_pixel_pos()

        frame = fvs.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (9,9), 0)

        for i in range(0, DetectorD.item_types):
            DetectorD.item_list[i].found = []
            for j in range(len(DetectorD.item_list[i].templates)):
                DetectorD.item_list[i].found.append(None)

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:

            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            ratio = gray.shape[1] / float(resized.shape[1])

            break_flag = 0

            for i in range(0, DetectorD.item_types):
                for j in range(len(DetectorD.item_list[i].templates)):
                    if (resized.shape[0] < DetectorD.item_list[i].height[j] or
                            resized.shape[0] < DetectorD.item_list[i].width[j]):
                        break_flag = 1

            if break_flag == 1:
                break

            edged = cv2.Canny(resized, 50, 100)
            edged = cv2.dilate(edged, None,iterations=1)
            edged = cv2.erode(edged, None,iterations=1)


            cv2.imshow('abv', edged)

            DetectorD.reset_item_threads()
            for i in range(0, DetectorD.item_types):
                DetectorD.max_val.append(1)
                DetectorD.max_loc.append(1)
                DetectorD.item_threads.append(threading.Thread(target=DetectorD.item_threading, args=(ratio, edged, DetectorD.item_list[i].templates, DetectorD.item_list[i].found, i,)))

            DetectorD.spawn_item_threads()

        for i in range(0, DetectorD.item_types):
            (ret_startx,
             ret_starty,
             ret_endx,
             ret_endy) = WindowW.localise_match(DetectorD.item_list[i].found,
                                        DetectorD.max_loc[i],
                                        DetectorD.item_list[i].found,
                                        DetectorD.item_list[i].height,
                                        DetectorD.item_list[i].width,
                                        ratio)
            WindowW.startx_coord.append(ret_startx)
            WindowW.starty_coord.append(ret_starty)
            WindowW.endx_coord.append(ret_endx)
            WindowW.endy_coord.append(ret_endy)


        ret_frame = None
        for i in range(0, DetectorD.item_types):
            ret_isdrawn, index_of_max, ret_frame = WindowW.draw_match(
                frame, DetectorD.max_val[i], Config.thresh_max, i, DetectorD.item_list[i].article)
            WindowW.is_drawn.append(ret_isdrawn)
            WindowW.pixel_pos.append(index_of_max)

        writer.write(ret_frame)

        for i in range(0, DetectorD.item_types):
            if WindowW.is_drawn[i]:
                DetectorD.item_list[i].x_abscissa = (
                    WindowW.startx_coord[i][WindowW.pixel_pos[i]] + WindowW.endx_coord[i][WindowW.pixel_pos[i]]) / 2
                DetectorD.item_list[i].y_ordinate = (
                    WindowW.starty_coord[i][WindowW.pixel_pos[i]] + WindowW.endy_coord[i][WindowW.pixel_pos[i]]) / 2
            else:
                DetectorD.item_list[i].x_abscissa = None
                DetectorD.item_list[i].y_ordinate = None

        for i in range(0, DetectorD.item_types):
            DetectorD.item_list[i].log_position()

        Config.frame_count += 1
        fps = Config.fps.fps()
        if args.videofile is not None:
            printProgressBar(fps, Config.frame_count + 1, Config.number_of_frame,
                            prefix='Progress:', suffix='Complete', length=50)

        Config.fps.update()

        if webflag is False:
            vidflag = fvs.more()

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
