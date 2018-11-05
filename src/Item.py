''' Module to initialize the objects in the scene '''

import logging
import time
import datetime
import os
import json
import csv
import cv2

class Item(object):
    def __init__(self, article, identification):
        self.templates = []
        self.height = []
        self.width = []
        self.found = []
        self.identification = identification
        self.x_abscissa = None
        self.y_ordinate = None
        self.article = article
        self.json_file_name = "../output/%s/%d/log.json" % (article, identification)
        self.csv_file = "../output/%s/log.csv" % (article)
        exists = os.path.isfile(self.json_file_name)
        if exists:
            os.remove(self.json_file_name)
        with open(self.json_file_name, mode = 'w', encoding= 'utf-8') as f:
            json.dump([],f)
        with open(self.csv_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y', 'Time Stamp'])



    def log_position(self):
        time_stamp = time.time()
        time_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        data = [
            self.x_abscissa,
            self.y_ordinate,
            time_stamp
        ]
        with open(self.csv_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)

        # data = {
        #     "x" : self.x_abscissa,
        #     "y" : self.y_ordinate,
        #     "time_stamp" : time_stamp
        # }
        # feeds = []
        # with open(self.json_file_name, mode = 'r', encoding= 'utf-8') as feedsjson:
        #     feeds=json.load(feedsjson)
        # with open(self.json_file_name, mode = 'w', encoding= 'utf-8') as feedsjson:
        #     entry = data
        #     feeds.append(entry)
        #     json.dump(feeds, feedsjson,indent=4)





# extracting templates from template_directory to use it for match template


    def template_processing(self, template_directory):
        """Extracts templates from template_directory &
           does some preprocessing on it"""

        for filename in os.listdir(template_directory):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                self.templates.append(cv2.imread(template_directory + '/' + filename))
                self.templates[-1] = cv2.cvtColor(self.templates[-1], cv2.COLOR_BGR2GRAY)
                self.templates[-1] = cv2.Canny(self.templates[-1], 50, 100)
                tempH, tempW = self.templates[-1].shape[:2]
                self.height.append(tempH)
                self.width.append(tempW)
                cv2.imshow("Template" + str(len(self.templates)) + template_directory, self.templates[-1])
            else:
                pass
