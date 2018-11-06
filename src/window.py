import cv2 
import Config
def localise_match(found, max_loc, templates, height, width, ratio):
    """ Calculates the bounding box for the region of interest """

    startx_coord = []
    starty_coord = []
    endx_coord = []
    endy_coord = []

    for i in range(len(templates)):
        (_, max_loc[i], ratio) = found[i]
        (startx, starty) = (
            int(max_loc[i][0] * ratio), int(max_loc[i][1] * ratio))
        (endx, endy) = (
            int((max_loc[i][0] + width[i]) * ratio), int((max_loc[i][1] + height[i]) * ratio))

        startx_coord.append(startx)
        starty_coord.append(starty)
        endx_coord.append(endx)
        endy_coord.append(endy)

    return startx_coord, starty_coord, endx_coord, endy_coord


def draw_match(frame, max_val, thresh_max,
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

    if max_of_all > thresh_max:
        is_drawn = True 
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        # if number == 1:
        #     cv2.rectangle(frame, (startx_coord[index_of_max], starty_coord[index_of_max]), (endx_coord[
        #         index_of_max], endy_coord[index_of_max]), (0, 0, 255), 2)
        #     cv2.putText(frame, articlename, (startx_coord[index_of_max], starty_coord[index_of_max] - 3),
        #                 font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        # else:
        #     cv2.rectangle(frame, (startx_coord[index_of_max], starty_coord[index_of_max]), (endx_coord[
        #         index_of_max], endy_coord[index_of_max]), (0, 255, 0), 2)
        #     cv2.putText(frame, articlename, (startx_coord[index_of_max], starty_coord[index_of_max] - 3),
        #                 font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    Config.fps.stop()
    # cv2.putText(frame, "Elapsed time: {:.2f}".format(Config.fps.elapsed()), Config.position_elapsed,
    #             Config.font, Config.fontScale, Config.fontColor, Config.lineType)
    # cv2.putText(frame, "FPS: {:.2f}".format(Config.fps.fps()),
    #             Config.position_fps, Config.font, Config.fontScale,
    #             Config.fontColor, Config.lineType)

    # cv2.imshow("Result", frame)
    print("\rFPS: {:.2f}".format(Config.fps.fps()), end='\r')
    return is_drawn, index_of_max, frame