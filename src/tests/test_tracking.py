'''test to check if the object is being correctly detected. 
I manually calculated the coordinates of the object in the video
(the video is very short and the object doesnt move much)
I then checked the log file corresponding to that video and took an 
average of the coordinates of the position of the object'''

import os
import main2
import detector
from PIL import Image
import pytest
import csv
import time 
import sys
import glob

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def test_tracking():
    valx = 0	
    valy = 0
    count = 0
    time_curr = time.time()

    os.system("python3 main2.py -td ../data/heart/templates -v ../data/test_logging.mp4")

    #finding the latest folder in the directory
    folder = "../output/heart/"
    files_path = os.path.join(folder, '*')
    files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 
    # print(len(files))

	# for i in (0,main2.main.item_types):
	# 	valx += res.DetectorD.item_list[i].x_abscissa
	# 	valy += res.DetectorD.item_list[i].y_ordinate
	# 	count = i
    # time_curr = time.time()


    #calculating the average value of the coordinates
    with open(files[0]) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # for col in row[0]:
            # if(col != ''):
            try:
                valy += float(row[1])
                valx += float(row[0])
                count+=1
            except ValueError:
                pass

        # for row in reader:
        #     # if(col != ''):
        #     try:
        #         valy += float(row[1])
        #     except ValueError:
        #         pass
                    

    valx = valx/count
    valy = valy/count

    #asserting the calculated average to the manually calculated average
    assert(valx > 250 and valx < 280) #enter coordinates after manual checking in test video
    assert(valy > 140 and valy < 170) #enter coordinates after manual checking in test video

