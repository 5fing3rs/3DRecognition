import cv2
import threading

class Detector(object):
    def __init__(self, thresh_max, thresh_min):
        self.item_threads = []
        self.item_list = []
        self.max_val = []
        self.max_loc = []
        self.thresh_max = thresh_max
        self.thresh_min = thresh_min

    def multi_match(self, ratio, edged, template, method, i, j):
        result = cv2.matchTemplate(
            edged, template, method)
        (ret_minval, ret_maxval, _, ret_maxloc) = cv2.minMaxLoc(result)

        self.item_list[j].max_val[i] = (ret_maxval)
        self.item_list[j].max_loc[i] = (ret_maxloc)

        if self.item_list[j].found[i] is None or self.item_list[j].max_val[i] > self.item_list[j].found[i][0]:
            self.item_list[j].found[i] = (self.item_list[j].max_val[i], self.item_list[j].max_loc[i], ratio)

    def match_templates(self, ratio, edged, templates, found, j, method=cv2.TM_CCOEFF_NORMED):
        """ Gets the brightest and the dimmest pixel from the matched matrix """

        self.item_list[j].max_loc = []
        self.item_list[j].max_val = []
        threads = []

        for i, template in enumerate(templates):
            self.item_list[j].max_val.append(1)
            self.item_list[j].max_loc.append(1)
            threads.append(threading.Thread(target=self.multi_match, args=(ratio, edged, template, method, i, j,)))
        for i in threads:
            i.start()
        for i in threads:
            i.join()

        return self.item_list[j].max_val, self.item_list[j].max_loc

    def item_threading(self, ratio, edged, templates, found, i):

        ret_maxval, ret_maxloc = self.match_templates(ratio,
                                                edged,
                                                templates,
                                                found,
                                                i,
                                                cv2.TM_CCOEFF_NORMED)

        self.max_val[i] = ret_maxval
        self.max_loc[i] = ret_maxloc

    def reset_item_threads(self):
        self.item_threads = []
        
    def reset_max_loc_val(self):
        self.max_loc = []
        self.max_val = []

    def spawn_item_threads(self):
        for i in self.item_threads:
            i.start()
        for i in self.item_threads:
            i.join()