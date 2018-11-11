"""Module to make the detector output screen""" 
import cv2
import Config

class Window(object):
    """Initializing the attributes of a window""" 
    def __init__(self):
        self.startx_coord = []
        self.starty_coord = []
        self.endx_coord = []
        self.endy_coord = []
        self.is_drawn = []
        self.pixel_pos = []

    def reset_cartesian_list(self):
        """Resetting the coordinates for the bounding boxes"""
        self.startx_coord = []
        self.starty_coord = []
        self.endx_coord = []
        self.endy_coord = []

    def reset_is_drawn(self):
        """Resetting the is_drawn flag for each bounding box"""
        self.is_drawn = []

    def reset_pixel_pos(self):
        """Resetting the pixel_pos"""
        self.pixel_pos = []

    def localise_match(self, found, max_loc, templates, height, width, ratio):
        """ Calculates the bounding box for the region of interest """

        _startx_coord = []
        _starty_coord = []
        _endx_coord = []
        _endy_coord = []

        for i in range(len(templates)):
            (_, max_loc[i], ratio) = found[i]
            (startx, starty) = (
                int(max_loc[i][0] * ratio), int(max_loc[i][1] * ratio))
            (endx, endy) = (
                int((max_loc[i][0] + width[i]) * ratio), int((max_loc[i][1] + height[i]) * ratio))

            _startx_coord.append(startx)
            _starty_coord.append(starty)
            _endx_coord.append(endx)
            _endy_coord.append(endy)

        return _startx_coord, _starty_coord, _endx_coord, _endy_coord


    def draw_match(self, frame, max_val, thresh_max, number, articlename):
        """ Picks the brightest pixel out of the set of bright pixels and draws bounding box """

        startx_coord = self.startx_coord[number]
        starty_coord = self.starty_coord[number]
        endx_coord = self.endx_coord[number]
        endy_coord = self.endy_coord[number]


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

            cv2.rectangle(frame, (startx_coord[index_of_max], starty_coord[index_of_max]), (endx_coord[
                index_of_max], endy_coord[index_of_max]), (0, 0, 255), 2)
            cv2.putText(frame, articlename, (startx_coord[index_of_max], starty_coord[index_of_max] - 3),
                        Config.font, 0.9, (0, 0, 255), 1, cv2.LINE_AA)

        Config.fps.stop()
        cv2.putText(frame, "Elapsed time: {:.2f}".format(Config.fps.elapsed()), Config.position_elapsed,
                    Config.font, Config.fontScale, Config.fontColor, Config.lineType)
        cv2.putText(frame, "FPS: {:.2f}".format(Config.fps.fps()),
                    Config.position_fps, Config.font, Config.fontScale,
                    Config.fontColor, Config.lineType)

        cv2.imshow("Result", frame)
        print("\rFPS: {:.2f}".format(Config.fps.fps()), end='\r')
        return is_drawn, index_of_max, frame
