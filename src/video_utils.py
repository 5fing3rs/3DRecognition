import cv2

def make_1080p(cap):
    """ Convert Input Video
    to 1080p """
    cap.set(3, 1920)
    cap.set(4, 1080)
    return cap


def make_720p(cap):
    """ Convert Input Video
    to 720p """
    cap.set(3, 1280)
    cap.set(4, 720)
    return cap


def make_480p(cap):
    """ Convert Input Video
    to 480p """
    cap.set(3, 640)
    cap.set(4, 480)
    return cap


def make_240p(cap):
    """ Convert Input Video
    to 240p """
    cap.set(3, 352)
    cap.set(4, 240)
    return cap

def rescale_frame(frame, percent):
    """ Rescaling frame of video """
    scale_percent = percent
    width =  int(frame.shape[1]*percent/100)
    height = int(frame.shape[0]*percent/100)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def write_video(video, frame):
    """ Write to video """
    video.write(frame)
