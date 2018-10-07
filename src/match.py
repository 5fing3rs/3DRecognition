import numpy as np
import argparse
import imutils
import glob
import cv2
import os

ap = argparse.ArgumentParser()
# ap.add_argument("-t1", "--template1", required=True, help="Path to template image")
# ap.add_argument("-t2", "--template2", required=True, help="Path to template image")
ap.add_argument("-td", "--templatedir", required=True, help="Path to template directory")


ap.add_argument("-v", "--visualize",help="Flag indicating whether or not to visualize each iteration")
args = vars(ap.parse_args())


templates = []
tH = []
tW = []


for filename in os.listdir(args["templatedir"]):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        templates.append(cv2.imread(args["templatedir"] + '/' + filename))
        templates[-1] = cv2.cvtColor(templates[-1], cv2.COLOR_BGR2GRAY)
        templates[-1] = cv2.Canny(templates[-1], 50 , 200)
        tempH, tempW = templates[-1].shape[:2]
        tH.append(tempH)
        tW.append(tempW)
        cv2.imshow("Template"+str(len(templates)), templates[-1])
    else:
        pass


# for i in range(2):
#     templates.append(cv2.imread(args["template%d" %(i+1)]))
#     templates[i] = cv2.cvtColor(templates[i], cv2.COLOR_BGR2GRAY)
#     templates[i] = cv2.Canny(templates[i], 50 , 200)
#     tempH, tempW = templates[i].shape[:2]
#     tH.append(tempH)
#     tW.append(tempW)
#     cv2.imshow("Template"+str(i), templates[i])


cap=cv2.VideoCapture(0)


while True:
    ret, frame=cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found = []
    THRESH_MAX = 0.075
    THRESH_MIN = -0.02

    for i in range(len(templates)):
        found.append(None)

    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])

        break_flag = 0

        for i in range(len(templates)):
            if resized.shape[0] < tH[i] or resized.shape[0] < tW[i]:
                break_flag = 1

        if break_flag == 1:
            break

        edged = cv2.Canny(resized, 50, 200)
        cv2.imshow('abv',edged)
        maxVal = []
        maxLoc = []
        minVal = []


        for i in range(len(templates)):

            result = cv2.matchTemplate(edged, templates[i], cv2.TM_CCOEFF_NORMED)
            (minVal1, maxVal1, _, maxLoc1) = cv2.minMaxLoc(result)
            maxVal.append(maxVal1)
            minVal.append(minVal1)
            maxLoc.append(maxLoc1)
            if found[i] is None or maxVal[i] > found[i][0]:
                found[i] = (maxVal[i], maxLoc[i], r)

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
        # print(maxVal[i])

    # print(len(endX),len(endY),len(startX),len(startY))

    max_of_all = maxVal[0]
    index_of_max = 0
    iterator = 0

    for i in maxVal:
        if max_of_all < i:
            max_of_all = i
            index_of_max = iterator
        iterator += 1


    if max_of_all > THRESH_MAX:
        if minVal[index_of_max] > THRESH_MIN:
            cv2.rectangle(frame, (startX[index_of_max], startY[index_of_max]), (endX[index_of_max], endY[index_of_max]), (0, 0, 255), 2)
    cv2.imshow("Result", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
