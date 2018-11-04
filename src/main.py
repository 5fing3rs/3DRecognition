import argparse
import imutils
import glob
import cv2
import os
import time
import numpy as np
from Item import Item
from utilities import printProgressBar
# from video_writer import OutputVideoWriter
import Config

# setting video resolution


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


# gets the brightest and the dimmest pixel from the matched matrix
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


# calculates the bounding box for the region of interest
def localise_match(found, maxLoc, templates, tH, tW, r):
    startX = []
    startY = []
    endX = []
    endY = []

    for i in range(len(templates)):
        (_, maxLoc[i], r) = found[i]
        (startX1, startY1) = (int(maxLoc[i][0] * r), int(maxLoc[i][1] * r))
        (endX1, endY1) = (
            int((maxLoc[i][0] + tW[i]) * r), int((maxLoc[i][1] + tH[i]) * r))

        startX.append(startX1)
        startY.append(startY1)
        endX.append(endX1)
        endY.append(endY1)

    return startX, startY, endX, endY

# picks the brightest detection out of the set of bright pixel


def draw_match(frame, maxVal, minVal, THRESH_MAX, THRESH_MIN, startX, startY, endX, endY, number, articlename):

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
        font = cv2.FONT_HERSHEY_SIMPLEX
        if number == 1:
            cv2.rectangle(frame, (startX[index_of_max], startY[index_of_max]), (endX[
                index_of_max], endY[index_of_max]), (0, 0, 255), 2)
            cv2.putText(frame,articlename,(startX[index_of_max], startY[index_of_max]-3), font, 0.5,(0,0,255),1,cv2.LINE_AA)
        else:
            cv2.rectangle(frame, (startX[index_of_max], startY[index_of_max]), (endX[
                index_of_max], endY[index_of_max]), (0, 255, 0), 2)
            cv2.putText(frame,articlename,(startX[index_of_max], startY[index_of_max]-3), font, 0.5,(0,0,255),1,cv2.LINE_AA)


        Config.fps.stop()
        cv2.putText(frame, "Elapsed time: {:.2f}".format(Config.fps.elapsed()),Config.position_elapsed, Config.font, Config.fontScale, Config.fontColor, Config.lineType)
        cv2.putText(frame,"FPS: {:.2f}".format(Config.fps.fps()), Config.position_fps, Config.font, Config.fontScale, Config.fontColor, Config.lineType)

    cv2.imshow("Result", frame)
    return is_drawn, startX[index_of_max], startY[index_of_max], endX[index_of_max], endY[index_of_max], frame


def write_video(video, frame):
    video.write(frame)

# terrible implementation


def main():
    # output_video = OutputVideoWriter('./output.avi',1,240,352,True)

    output_filename = "../output/output.avi"


    SUCCESS = True

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-td', action='append', dest='tempdirs',
                            default=[], required=True, help="Paths to template directories")
    arg_parser.add_argument("-v", action='store', dest="videofile",
                            required=False, help="Path to the video file")
    args = arg_parser.parse_args()
    item = []
    size = len(args.tempdirs)
    for i in range(0, size):
        item.append(Item('heart', 1))
        item[i].template_processing(args.tempdirs[i])

    print(args.videofile)


    number_of_frame = 0
    frame_count = 0 

    if args.videofile is None:
        cap = cv2.VideoCapture(0)  # setting input to webcam/live video
        # cap = make_240p(cap)
    else:
        try:
            # checking if input is through a video file
            cap = cv2.VideoCapture(args.videofile)
            cap = make_240p(cap)
            number_of_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(number_of_frame)
        except:
            print("Error in checking the path to the video file.")
            print("Please check the path to the video file.")
            return

    ret, frame = cap.read()
    hheight, wwidth, llayers = frame.shape
    writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'PIM1'),
                             25, (wwidth, hheight), True)


    printProgressBar(0, number_of_frame, prefix = 'Progress:', suffix = 'Complete', length = 50)


    while True and SUCCESS:
        ret, frame = cap.read()
        SUCCESS = ret
        if not SUCCESS:
            break
        # converting the video to grayscale to proceed with extraction of edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for i in range(0, size):
            item[i].found = []
            for j in range(len(item[i].templates)):
                item[i].found.append(None)

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:

            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            break_flag = 0

            for i in range(0, size):
                for j in range(len(item[i].templates)):
                    if resized.shape[0] < item[i].tH[j] or resized.shape[0] < item[i].tW[j]:
                        break_flag = 1

            if break_flag == 1:
                break

            # using Canny edge algorithm to extract edges from the video
            edged = cv2.Canny(resized, 50, 100)
            cv2.imshow('abv', edged)
            maxVal = []
            maxLoc = []
            minVal = []

            for i in range(0, size):
                (a, b, c) = match_templates(
                    r, edged, item[i].templates, item[i].found, cv2.TM_CCOEFF_NORMED)
                maxVal.append(a)
                maxLoc.append(b)
                minVal.append(c)

        startX = []
        startY = []
        endX = []
        endY = []

        for i in range(0, size):
            (a, b, c, d) = localise_match(
                item[i].found, maxLoc[i], item[i].found, item[i].tH, item[i].tW, r)
            startX.append(a)
            startY.append(b)
            endX.append(c)
            endY.append(d)

        is_drawn = []
        boxSX = []
        boxSY = []
        boxEX = []
        boxEY = []
        modframe = []

        for i in range(0, size):
            if i == 0:
                a, b, c, d, e, f = draw_match(
                    frame, maxVal[i], minVal[i], Config.THRESH_MAX, Config.THRESH_MIN, startX[i], startY[i], endX[i], endY[i], 1, item[i].article)
            else:
                a, b, c, d, e, f = draw_match(
                    modframe[i - 1], maxVal[i], minVal[i], Config.THRESH_MAX, Config.THRESH_MIN, startX[i], startY[i], endX[i], endY[i], 1, item[i].article)

            is_drawn.append(a)
            boxSX.append(b)
            boxSY.append(c)
            boxEX.append(d)
            boxEY.append(e)
            modframe.append(f)
        writer.write(modframe[size - 1])

        for i in range(0, size):
            if is_drawn[i]:
                # setting the x and y coordinates to be logged into the log
                # file
                item[i].x_abscissa = (boxSX[i] + boxEX[i]) / 2
                item[i].y_ordinate = (boxSY[i] + boxEY[i]) / 2
            else:
                item[i].x_abscissa = None
                item[i].y_ordinate = None

        for i in range(0, size):
            item[i].log_position()  # logging the coordinates into a file

        frame_count += 1
        printProgressBar(frame_count + 1, number_of_frame, prefix = 'Progress:', suffix = 'Complete', length = 50)
        Config.fps.update()

        if cv2.waitKey(1) == 27:
            break

    Config.fps.stop()
    cap.release()
    # output_video.release_video()
    writer.release()
    cv2.destroyAllWindows()

main()
