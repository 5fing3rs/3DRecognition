""" INITIALIZE ALL THE SYSTEM GLOBALS HERE """
import cv2
from imutils.video import FPS
import time
import datetime

fps = FPS().start()
thresh_max = 0.11
thresh_min = -0.03
font = cv2.FONT_HERSHEY_SIMPLEX
position_fps = (10, 20)
position_elapsed = (10, 50)
fontScale = 0.8
fontColor = (0, 255,0)
lineType = 2
number_of_frame = 0
frame_count = 0
degradation_percent = 50
restoration_percent = (10000/degradation_percent)
OUTPUT_FILE = '../output/output_video/{}.avi'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H|%M|%S'))
