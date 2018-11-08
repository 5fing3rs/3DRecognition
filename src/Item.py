''' Module to initialize the objects in the scene '''

import logging
import time
import datetime
import os
import json
import csv
import cv2
import numpy as np
class Item(object):
    def __init__(self, article, identification):
        self.templates = []
        self.height = []
        self.width = []
        self.found = []
        self.max_val = []
        self.min_val = []
        self.max_loc = []
        self.identification = identification
        self.x_abscissa = None
        self.y_ordinate = None
        self.article = article
        self.csv_file = None
        self.set_file_name()


    def set_file_name(self):
        _time_stamp = time.time()
        _time_stamp = datetime.datetime.fromtimestamp(_time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        self.csv_file = "../output/%s/log_%s.csv" % (self.article, _time_stamp)
        exists = os.path.isfile(self.csv_file)
        with open(self.csv_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y', 'Time Stamp'])

    def log_position(self):
        """Log position of the article into a csv
        file."""
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

    def template_processing(self, template_directory):
        """Extracts templates from template_directory &
           does some preprocessing on it"""

        for filename in os.listdir(template_directory):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                self.templates.append(cv2.imread(template_directory + '/' + filename))
                self.templates[-1] = cv2.cvtColor(self.templates[-1], cv2.COLOR_BGR2GRAY)
                self.templates[-1] = cv2.Canny(self.templates[-1], 50, 100)
                # self.templates[-1]= cv2.dilate(self.templates[-1], None, iterations=1)
                # self.templates[-1] = cv2.erode(self.templates[-1], None, iterations=1)   #Experiment
                tempH, tempW = self.templates[-1].shape[:2]
                self.height.append(tempH)
                self.width.append(tempW)
                # cv2.imshow("Template" + str(len(self.templates)) + template_directory, self.templates[-1])
            else:
                pass
