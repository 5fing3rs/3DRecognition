""" Main module for template extraction and matching """

import argparse
import imutils
import cv2
import numpy as np
from Item import Item
from utilities import printProgressBar
# from video_writer import OutputVideoWriter
import Config

# setting video resolution


def make_1080p(cap):
    """ Convert to 1080p """
    cap.set(3, 1920)
    cap.set(4, 1080)
    return cap


def make_720p(cap):
    """ Convert to 720p """
    cap.set(3, 1280)
    cap.set(4, 720)
    return cap


def make_480p(cap):
    """ Convert to 480p """
    cap.set(3, 640)
    cap.set(4, 480)
    return cap


def make_240p(cap):
    """ Convert to 240p """
    cap.set(3, 352)
    cap.set(4, 240)
    return cap


def match_templates(ratio, edged, templates, found, method=cv2.TM_CCOEFF_NORMED):
    """ Gets the brightest and the dimmest pixel from the matched matrix """

    max_loc = []
    max_val = []
    min_val = []
    for i in range(len(templates)):

        result = cv2.matchTemplate(
            edged, templates[i], method)
        (ret_minval, ret_maxval, _, ret_maxloc) = cv2.minMaxLoc(result)
        max_val.append(ret_maxval)
        min_val.append(ret_minval)
        max_loc.append(ret_maxloc)
        if found[i] is None or max_val[i] > found[i][0]:
            found[i] = (max_val[i], max_loc[i], ratio)

    return max_val, max_loc, min_val


def localise_match(found, max_loc, templates, tH, tW, ratio):
    """ Calculates the bounding box for the region of interest """

    startx_coord = []
    starty_coord = []
    endx_coord = []
    endy_coord = []

    for i in range(len(templates)):
        (_, max_loc[i], ratio) = found[i]
        (startX1, startY1) = (
            int(max_loc[i][0] * ratio), int(max_loc[i][1] * ratio))
        (endX1, endY1) = (
            int((max_loc[i][0] + tW[i]) * ratio), int((max_loc[i][1] + tH[i]) * ratio))

        startx_coord.append(startX1)
        starty_coord.append(startY1)
        endx_coord.append(endX1)
        endy_coord.append(endY1)

    return startx_coord, starty_coord, endx_coord, endy_coord


def draw_match(frame, max_val, min_val, THRESH_MAX, THRESH_MIN,
               startx_coord, starty_coord, endx_coord, endy_coord, number, articlename):
    """ Picks the brightest pixel out of the set of bright pixels and draws bounding box """

    max_of_all = max_val[0]
    index_of_max = 0
    iterator = 0
    is_drawn = False

    for i in max_val:
        if max_of_all < i:
            max_of_all = i
            index_of_max = iterator
        iterator += 1

    if max_of_all > THRESH_MAX:
        is_drawn = True
        # print(max_of_all, min_val[index_of_max])
        # if min_val[index_of_max] > THRESH_MIN:
        font = cv2.FONT_HERSHEY_SIMPLEX
        if number == 1:
            cv2.rectangle(frame, (startx_coord[index_of_max], starty_coord[index_of_max]), (endx_coord[
                index_of_max], endy_coord[index_of_max]), (0, 0, 255), 2)
            cv2.putText(frame, articlename, (startx_coord[index_of_max], starty_coord[index_of_max] - 3),
                        font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            cv2.rectangle(frame, (startx_coord[index_of_max], starty_coord[index_of_max]), (endx_coord[
                index_of_max], endy_coord[index_of_max]), (0, 255, 0), 2)
            cv2.putText(frame, articlename, (startx_coord[index_of_max], starty_coord[index_of_max] - 3),
                        font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    Config.fps.stop()
    cv2.putText(frame, "Elapsed time: {:.2f}".format(Config.fps.elapsed()), Config.position_elapsed,
                Config.font, Config.fontScale, Config.fontColor, Config.lineType)
    cv2.putText(frame, "FPS: {:.2f}".format(Config.fps.fps()),
                Config.position_fps, Config.font, Config.fontScale,
                Config.fontColor, Config.lineType)

    cv2.imshow("Result", frame)
    return is_drawn, index_of_max, frame


def write_video(video, frame):
    """ Write to video """

    video.write(frame)

# terrible implementation


def main():
    """ Main function """
    # output_video = OutputVideoWriter('./output.avi',1,240,352,True)

    output_filename = "../output/output.avi"

    success = True
    item_list = []

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-td', action='append', dest='tempdirs',
                            default=[], required=True, help="Paths to template directories")
    arg_parser.add_argument("-v", action='store', dest="videofile",
                            required=False, help="Path to the video file")
    args = arg_parser.parse_args()

    item_types = len(args.tempdirs)

    for i in range(0, item_types):
        obj_name = args.tempdirs[i].split('/')
        item_list.append(Item(obj_name[2], 1))
        item_list[i].template_processing(args.tempdirs[i])

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
    hheight, wwidth, _ = frame.shape    # '_' had llayers
    writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'PIM1'),
                             25, (wwidth, hheight), True)

    printProgressBar(0, number_of_frame, prefix='Progress:',
                     suffix='Complete', length=50)

    while True and success:
        ret, frame = cap.read()
        success = ret
        if not success:
            break
        # converting the video to grayscale to proceed with extraction of edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for i in range(0, item_types):
            item_list[i].found = []
            for j in range(len(item_list[i].templates)):
                item_list[i].found.append(None)

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:

            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            ratio = gray.shape[1] / float(resized.shape[1])

            break_flag = 0

            for i in range(0, item_types):
                for j in range(len(item_list[i].templates)):
                    if (resized.shape[0] < item_list[i].tH[j] or
                            resized.shape[0] < item_list[i].tW[j]):
                        break_flag = 1

            if break_flag == 1:
                break

            # using Canny edge algorithm to extract edges from the video
            edged = cv2.Canny(resized, 50, 100)
            cv2.imshow('abv', edged)
            max_val = []
            max_loc = []
            min_val = []

            for i in range(0, item_types):
                (ret_maxval, ret_maxloc, ret_minval) = match_templates(ratio, edged, item_list[i].templates,
                                                                       item_list[i].found, cv2.TM_CCOEFF_NORMED)
                max_val.append(ret_maxval)
                max_loc.append(ret_maxloc)
                min_val.append(ret_minval)

        startx_coord = []
        starty_coord = []
        endx_coord = []
        endy_coord = []

        for i in range(0, item_types):
            (ret_startx, ret_starty, ret_endx, ret_endy) = localise_match(item_list[i].found, max_loc[i], item_list[i].found,
                                                                          item_list[i].tH, item_list[i].tW, ratio)
            startx_coord.append(ret_startx)
            starty_coord.append(ret_starty)
            endx_coord.append(ret_endx)
            endy_coord.append(ret_endy)

        is_drawn = []
        # boxSX = []
        # boxSY = []
        # boxEX = []
        # boxEY = []
        modframe = []
        pixel_pos = []

        for i in range(0, item_types):
            if i == 0:
                ret_isdrawn, index_of_max, ret_frame = draw_match(
                    frame, max_val[i], min_val[i], Config.THRESH_MAX, Config.THRESH_MIN, startx_coord[i], starty_coord[i], endx_coord[i], endy_coord[i], 1, item_list[i].article)
            else:
                ret_isdrawn, index_of_max, ret_frame = draw_match(
                    modframe[i - 1], max_val[i], min_val[i], Config.THRESH_MAX, Config.THRESH_MIN, startx_coord[i], starty_coord[i], endx_coord[i], endy_coord[i], 1, item_list[i].article)

            is_drawn.append(ret_isdrawn)

            # boxSX.append(ret_startx)
            # boxSY.append(ret_starty)
            # boxEX.append(ret_endx)
            # boxEY.append(ret_endy)
            modframe.append(ret_frame)
            pixel_pos.append(index_of_max)

        writer.write(modframe[item_types - 1])

        for i in range(0, item_types):
            if is_drawn[i]:
                # setting the x and y coordinates to be logged into the log
                # file
                item_list[i].x_abscissa = (
                    startx_coord[i][pixel_pos[i]] + endx_coord[i][pixel_pos[i]]) / 2
                item_list[i].y_ordinate = (
                    starty_coord[i][pixel_pos[i]] + endy_coord[i][pixel_pos[i]]) / 2
            else:
                item_list[i].x_abscissa = None
                item_list[i].y_ordinate = None

        for i in range(0, item_types):
            item_list[i].log_position()  # logging the coordinates into a file

        frame_count += 1
        printProgressBar(frame_count + 1, number_of_frame,
                         prefix='Progress:', suffix='Complete', length=50)
        Config.fps.update()

        if cv2.waitKey(1) == 27:
            break

    Config.fps.stop()
    cap.release()
    # output_video.release_video()
    writer.release()
    cv2.destroyAllWindows()


main()
