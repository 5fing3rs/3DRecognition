# INITIALIZE ALL THE SYSTEM GLOBALS HERE
import cv2
from imutils.video import FPS
import time
import datetime

fps = FPS().start()
thresh_max = 0.152
thresh_min = -0.033 #-0.033
font = cv2.FONT_HERSHEY_SIMPLEX
position_fps = (460, 70)
position_elapsed = (325, 30)
fontScale = 0.5
fontColor = (0, 255,0)
lineType = 1
number_of_frame = 0
frame_count = 0
OUTPUT_FILE = '../output/output_video/{}.avi'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
