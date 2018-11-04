# INITIALIZE ALL THE SYSTEM GLOBALS HERE
import cv2
from imutils.video import FPS

fps = FPS().start()
THRESH_MAX = 0.09
THRESH_MIN = -0.02
font = cv2.FONT_HERSHEY_SIMPLEX
position_fps = (460, 70)
position_elapsed = (325, 30)
fontScale = 1
fontColor = (0, 255,0)
lineType = 2
