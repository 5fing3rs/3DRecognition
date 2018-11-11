'''this test checks if the log entry is being correctly made on the entry and exit of 
the object. Here, I use a test video in which the object is introduced into the frame and then taken out of the 
frame. Then I check if a log entry exists against the time of entry and also check that a log entry
should not exist after the object has exited'''
import os
import main2
import detector
from PIL import Image
import pytest
import Item
import csv
import time 
import datetime
from datetime import timedelta
import glob

def test_logging():
    check = 0

    #calling main
    os.system("python3 main.py -td ../data/heart/templates -v ../data/test_logging.mp4")
    # time_entry = time_entry.replace(year=0, month=0, day=0, hour=0, minute=0, second=0)
    time_entry = datetime.datetime.now() - timedelta(seconds = 3)
    time_entry = '{0:%Y-%m-%d %H:%M:%S}'.format(time_entry)
    print(time_entry) 

    #finding the latest folder in the directory
    folder = "../output/heart/"
    files_path = os.path.join(folder, '*')
    files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 

    #checking for the log entry
    with open(files[0]) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if time_entry == row[2]:
                if row[0] != '':
                    check = 1
    assert(check == 1)
           

def test_logging_exit():
    check = 0

    #calling main
    os.system("python3 main2.py -td ../data/heart/templates -v ../data/test_logging.mp4")
    # time_entry = time_entry.replace(year=0, month=0, day=0, hour=0, minute=0, second=0)
    time_entry = datetime.datetime.now() - timedelta(seconds = 3)
    time_entry = '{0:%Y-%m-%d %H:%M:%S}'.format(time_entry)
    print(time_entry) 

    #finding the latest folder in the directory
    folder = "../output/heart/"
    files_path = os.path.join(folder, '*')
    files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 

    #checking for the log entry
    with open(files[0]) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if time_entry == row[2]:
                if row[0] == '':
                    check = 1
    assert(check == 1)