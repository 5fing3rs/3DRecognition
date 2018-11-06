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