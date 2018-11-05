""" Main module for template extraction and matching """

import argparse
import imutils
import cv2
import numpy as np
from Item import Item
from utilities import printProgressBar
from video_utils import make_240p
import Config

import threading
import sys
from queue import Queue
import time

from detector import Detector
from window import localise_match, draw_match

DetectorD = Detector(0.09, -0.02)

from imutils.video import FileVideoStream


# class FileVideoStream:
# 	def __init__(self, path, queueSize=128):
# 		# initialize the file video stream along with the boolean
# 		# used to indicate if the thread should be stopped or not
# 		self.stream = cv2.VideoCapture(path)
# 		self.stopped = False
 
# 		# initialize the queue used to store frames read from
# 		# the video file
# 		self.Q = Queue(maxsize=queueSize)

# 	def start(self):
# 		# start a thread to read frames from the file video stream
# 		t = Thread(target=self.update, args=())
# 		t.daemon = True
# 		t.start()
# 		return self

# 	def update(self):
# 		# keep looping infinitely
# 		while True:
# 			# if the thread indicator variable is set, stop the
# 			# thread
# 			if self.stopped:
# 				return
 
# 			# otherwise, ensure the queue has room in it
# 			if not self.Q.full():
# 				# read the next frame from the file
# 				(grabbed, frame) = self.stream.read()
 
# 				# if the `grabbed` boolean is `False`, then we have
# 				# reached the end of the video file
# 				if not grabbed:
# 					self.stop()
# 					return
 
# 				# add the frame to the queue
# 				self.Q.put(frame)

# 	def read(self):
# 		# return next frame in the queue
# 		return self.Q.get()

# 	def more(self):
# 		# return True if there are still frames in the queue
# 		return self.Q.qsize() > 0

# 	def stop(self):
# 		# indicate that the thread should be stopped
# 		self.stopped = True


def write_video(video, frame):
    """ Write to video """
    video.write(frame)

# terrible implementation


def main():
    """ Main function """
    # output_video = OutputVideoWriter('./output.avi',1,240,352,True)

    output_filename = "../output/output.avi"

    success = True


    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-td', action='append', dest='tempdirs',
                            default=[], required=True, help="Paths to template directories")
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
        # try:
        #     # checking if input is through a video file
        #     # cap = cv2.VideoCapture(args.videofile)
        #     # cap = make_240p(cap)
        #     fvs = FileVideoStream(args.videofile).start()
        #     time.sleep(1.0)
            
        #     number_of_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        #     print(number_of_frame)
        # except:
        #     print("Error in checking the path to the video file.")
        #     print("Please check the path to the video file.")
        #     return

    # ret, frame = cap.read()
    frame = fvs.read()
    hheight, wwidth, _ = frame.shape    # '_' had llayers
    writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'PIM1'),
                             25, (wwidth, hheight), True)

    printProgressBar(0, 0, number_of_frame, prefix='Progress:',
                     suffix='Complete', length=50)

    # while True and success:
    while fvs.more():
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
            max_val = []
            max_loc = []
            min_val = []

            for i in range(0, item_types):
                (ret_maxval, ret_maxloc, ret_minval) = DetectorD.match_templates(ratio, edged, DetectorD.item_list[i].templates,
                                                                       DetectorD.item_list[i].found, i, cv2.TM_CCOEFF_NORMED)
                max_val.append(ret_maxval)
                max_loc.append(ret_maxloc)
                min_val.append(ret_minval)

        startx_coord = []
        starty_coord = []
        endx_coord = []
        endy_coord = []

        for i in range(0, item_types):
            (ret_startx, ret_starty, ret_endx, ret_endy) = localise_match(DetectorD.item_list[i].found, max_loc[i], DetectorD.item_list[i].found,
                                                                          DetectorD.item_list[i].height, DetectorD.item_list[i].width, ratio)
            startx_coord.append(ret_startx)
            starty_coord.append(ret_starty)
            endx_coord.append(ret_endx)
            endy_coord.append(ret_endy)

        is_drawn = []
 
        modframe = []
        pixel_pos = []

        for i in range(0, item_types):
            if i == 0:
                ret_isdrawn, index_of_max, ret_frame = draw_match(
                    frame, max_val[i], Config.thresh_max, startx_coord[i], starty_coord[i], endx_coord[i], endy_coord[i], 1, DetectorD.item_list[i].article)
            else:
                ret_isdrawn, index_of_max, ret_frame = draw_match(
                    modframe[i - 1], max_val[i], min_val[i], Config.thresh_max, Config.thresh_min, startx_coord[i], starty_coord[i], endx_coord[i], endy_coord[i], 1, DetectorD.item_list[i].article)

            is_drawn.append(ret_isdrawn)

            modframe.append(ret_frame)
            pixel_pos.append(index_of_max)

        writer.write(modframe[item_types - 1])

        for i in range(0, item_types):
            if is_drawn[i]:
                # setting the x and y coordinates to be logged into the log
                # file
                DetectorD.item_list[i].x_abscissa = (
                    startx_coord[i][pixel_pos[i]] + endx_coord[i][pixel_pos[i]]) / 2
                DetectorD.item_list[i].y_ordinate = (
                    starty_coord[i][pixel_pos[i]] + endy_coord[i][pixel_pos[i]]) / 2
            else:
                DetectorD.item_list[i].x_abscissa = None
                DetectorD.item_list[i].y_ordinate = None

        for i in range(0, item_types):
            DetectorD.item_list[i].log_position()  # logging the coordinates into a file

        frame_count += 1
        # fps = "FPS: {:.2f}".format(Config.fps.fps())
        fps = Config.fps.fps()
        printProgressBar(fps, frame_count + 1, number_of_frame,
                         prefix='Progress:', suffix='Complete', length=50)
        # print("\rFPS: {:.2f}".format(Config.fps.fps()), end='\r')

        Config.fps.update()


        if cv2.waitKey(1) == 27:
            break

    Config.fps.stop()
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    if fvs:
        fvs.stop()


main()
