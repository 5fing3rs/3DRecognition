''' Module to initialize the objects in the scene '''

import logging
import time
import datetime
import yaml

class Item(object):
    def __init__(self):
        self.identication = None
        self.x_abscissa = None
        self.y_ordinate = None
        self.type = None
        self.yaml_file_name = None

    def log_position(self):
        time_stamp = time.time()
        time_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "x" : self.x_abscissa,
            "y" : self.y_ordinate,
            "time_stamp" : time_stamp
        }
        with open(self.yaml_file_name, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)
        pass
