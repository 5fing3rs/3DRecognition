import os
from PIL import Image
import pytest
import Item
import csv
import sys
import video_utils
import cv2

def test_video_resolution_change():
    ccap = cv2.VideoCapture("../data/heart/training_video/heart1.avi")
    test_cap = video_utils.make_480p(ccap)
    # vcap = cv2.VideoCapture(test_cap)
    if test_cap.isOpened():
        test_width = test_cap.get(3)
        test_height = test_cap.get(4)
    assert(test_width == 960)
    assert(test_height == 540)

def test_rescaling():
    cap = cv2.VideoCapture("../data/heart/training_video/heart1.avi")
    ret, frame = cap.read()
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    test_frame = video_utils.rescale_frame(frame, 50)
    assert(test_frame.shape[0] == 0.50*frame_height)
    assert(test_frame.shape[1] == 0.50*frame_width)




