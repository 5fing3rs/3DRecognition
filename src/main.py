import numpy as np
import argparse
import imutils
import glob
import cv2
import os
import time
from Item import Item
import Config

#setting video resolution
def make_1080p(cap):
    cap.set(3, 1920)
    cap.set(4, 1080)
    return cap

def make_720p(cap):
    cap.set(3, 1280)
    cap.set(4, 720)
    return cap

def make_480p(cap):
    cap.set(3, 640)
    cap.set(4, 480)
    return cap

def make_240p(cap):
    cap.set(3, 352)
    cap.set(4, 240)
    return cap

#extracting templates from template_directory to use it for match template
def template_processing(template_directory):
    """Extracts templates from template_directory &
       does some preprocessing on it"""

    templates = []
    tH = []
    tW = []

    for filename in os.listdir(template_directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            templates.append(cv2.imread(template_directory + '/' + filename))
            templates[-1] = cv2.cvtColor(templates[-1], cv2.COLOR_BGR2GRAY)
            templates[-1] = cv2.Canny(templates[-1], 50, 100)
            tempH, tempW = templates[-1].shape[:2]
            tH.append(tempH)
            tW.append(tempW)
            cv2.imshow("Template" + str(len(templates)), templates[-1])
        else:
            pass

    return templates, tH, tW


#gets the brightest and the dimmest pixel from the matched matrix
def match_templates(r, edged, templates, found, method=cv2.TM_CCOEFF_NORMED):

    maxLoc = []
    maxVal = []
    maxLoc = []
    minVal = []
    for i in range(len(templates)):

        result = cv2.matchTemplate(
            edged, templates[i], method)
        (minVal1, maxVal1, _, maxLoc1) = cv2.minMaxLoc(result)
        maxVal.append(maxVal1)
        minVal.append(minVal1)
        maxLoc.append(maxLoc1)
        if found[i] is None or maxVal[i] > found[i][0]:
            found[i] = (maxVal[i], maxLoc[i], r)

    return maxVal, maxLoc, minVal


#calculates the bounding box for the region of interest
def localise_match(found, maxLoc, templates, tH, tW, r):
    startX = []
    startY = []
    endX = []
    endY = []

    for i in range(len(templates)):
        (_, maxLoc[i], r) = found[i]
        (startX1, startY1) = (int(maxLoc[i][0] * r), int(maxLoc[i][1] * r))
        (endX1, endY1) = (int((maxLoc[i][0] + tW[i]) * r), int((maxLoc[i][1] + tH[i]) * r))

        startX.append(startX1)
        startY.append(startY1)
        endX.append(endX1)
        endY.append(endY1)

    return startX, startY, endX, endY

#picks the brightest detection out of the set of bright pixel
def draw_match(frame, maxVal, minVal, THRESH_MAX, THRESH_MIN, startX, startY, endX, endY):

    max_of_all = maxVal[0]
    index_of_max = 0
    iterator = 0
    is_drawn = False

    for i in maxVal:
        if max_of_all < i:
            max_of_all = i
            index_of_max = iterator
        iterator += 1


    if max_of_all > THRESH_MAX:
        is_drawn = True
        # print(max_of_all, minVal[index_of_max])
        # if minVal[index_of_max] > THRESH_MIN:
        cv2.rectangle(frame, (startX[index_of_max], startY[index_of_max]), (endX[index_of_max], endY[index_of_max]), (0, 0, 255), 2)
    cv2.imshow("Result", frame)
    return is_drawn,startX[index_of_max], startY[index_of_max], endX[index_of_max], endY[index_of_max]



def main():

    SUCCESS = True

    item = Item('syringe_body',1)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-td", "--templatedir", required=True, help="Path to template directory")
    arg_parser.add_argument("-v", "--videofile", required=False, help="Path to the video file")
    args = vars(arg_parser.parse_args())
    (templates, tH, tW) = template_processing(args["templatedir"])

    print(args['videofile'])

    if args['videofile'] is None:
        cap = cv2.VideoCapture(0)              #setting input to webcam/live video
        cap = make_240p(cap)
    else:
        try:
            cap = cv2.VideoCapture(args['videofile'])         #checking if input is through a video file
            cap = make_240p(cap)
        except:
            print("Error in checking the path to the video file.")
            print("Please check the path to the video file.")
            return

    while True and SUCCESS:
        ret, frame = cap.read()
        SUCCESS = ret
        if not SUCCESS:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     #converting the video to grayscale to proceed with extraction of edges
        found = []

        for i in range(len(templates)):
            found.append(None)

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:

            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            break_flag = 0

            for i in range(len(templates)):
                if resized.shape[0] < tH[i] or resized.shape[0] < tW[i]:
                    break_flag = 1

            if break_flag == 1:
                break


            edged = cv2.Canny(resized, 50,100)           #using Canny edge algorithm to extract edges from the video
            cv2.imshow('abv', edged)

            (maxVal, maxLoc, minVal) = match_templates(r, edged, templates, found, cv2.TM_CCOEFF_NORMED)


        (startX, startY, endX, endY) = localise_match(found, maxLoc, found, tH, tW, r)

        is_drawn, boxSX, boxSY, boxEX, boxEY = draw_match(frame, maxVal, minVal, Config.THRESH_MAX, Config.THRESH_MIN, startX, startY, endX, endY)
        if is_drawn:
            item.x_abscissa = (boxSX+boxEX)/2           #setting the x and y coordinates to be logged into the log file
            item.y_ordinate = (boxSY+boxEY)/2
        else :
            item.x_abscissa = None
            item.y_ordinate = None

        print("itemx",item.x_abscissa, "itemy",item.y_ordinate)
        item.log_position()                          #logging the coordinates into a file
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

main()
