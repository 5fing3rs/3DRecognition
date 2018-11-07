''' Utility Functions
'''

from datetime import datetime , timedelta
import math
import argparse
from pathlib import Path
import cv2
from PIL import Image

def printProgressBar (fps,iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    estimated_time = None
    if fps != 0:
        estimated_time = math.ceil((total-iteration)/(fps))
    else:
        estimated_time = int(9999)
    fps = "FPS: {:.2f}".format(fps)

    estimated_time = "Estimated Time : {}".format(str(timedelta(seconds=estimated_time)))
    print('\r%s |%s| %s%% %s\t\t%s\t\t%s' % (prefix, bar, percent, suffix, fps, estimated_time), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def resize_image(image, basewidth):
    ''' Resize the generated image with a locked ratio to
    conform to the base width used for detection'''
    wpercent = (basewidth / float(image.shape[1]))
    hsize = int((float(image.shape[0]) * float(wpercent)))
    image = cv2.resize(image, (basewidth, hsize), interpolation=cv2.INTER_AREA)
    return image
