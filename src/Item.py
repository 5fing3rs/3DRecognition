''' Module to initialize the objects in the scene '''

import logging
import time
import datetime
import os
import json

class Item(object):
    def __init__(self, article, identification):
        self.identification = None
        self.x_abscissa = None
        self.y_ordinate = None
        self.article = None
        self.json_file_name = "../output/%s/%d/log.json" % (article, identification)
        exists = os.path.isfile(self.json_file_name)
        if exists:
            os.remove(self.json_file_name)
        with open(self.json_file_name, mode = 'w', encoding= 'utf-8') as f:
            json.dump([],f)


    def log_position(self):
        time_stamp = time.time()
        time_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "x" : self.x_abscissa,
            "y" : self.y_ordinate,
            "time_stamp" : time_stamp
        }
        feeds = [] 
        with open(self.json_file_name, mode = 'r', encoding= 'utf-8') as feedsjson:
            feeds=json.load(feedsjson)
        with open(self.json_file_name, mode = 'w', encoding= 'utf-8') as feedsjson:
            entry = data
            feeds.append(entry)
            json.dump(feeds, feedsjson,indent=4)


