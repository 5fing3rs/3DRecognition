''' Module to initialize the objects in the scene '''

import logging
import time
import datetime
import yaml

class Item(object):
    def __init__(self, identification, article):
        self.identification = None
        self.x_abscissa = None
        self.y_ordinate = None
        self.article = None

    def log_position(self):
        time_stamp = time.time()
        time_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "x" : self.x_abscissa,
            "y" : self.y_ordinate,
            "time_stamp" : time_stamp
        }
