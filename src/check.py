import sys
import time
import os

def check_output_dir(args):
    """ Check existence of output directory """
    if not os.path.isdir("../output"):
        os.makedirs("../output")
        os.makedirs("../output/output_video")
        for i in range(0, len(args.tempdirs)):
            object_name = args.tempdirs[i].split('/')
            os.makedirs("../output/{}".format(object_name[2]))


def check_output_video_dir():
    """ Check existence of output video directory """
    if not os.path.isdir("../output/output_video"):
        os.makedirs("../output/output_video")


def check_data_dir():
    """ Check existence of data directory """
    if not os.path.isdir("../data"):
        os.makedirs("../data")


def check_TemplateDir_corresponsingObject(object_name):
    """ Check existence of object template directory """
    if not os.path.isdir("../data/{}/templates".format(object_name)):
        os.makedirs("../data/{}/templates".format(object_name))


def check_query_video_path(path):
    """ Check validity of video file path """
    if path is not None:
        if not os.path.isfile(path):
            raise IOError("Query Video file {} does not exist.".format(path))


def check_init(args):
    check_data_dir()
    check_output_dir(args)
    check_output_video_dir()
    check_query_video_path(args.videofile)

    for i in range(0, len(args.tempdirs)):
        object_name = args.tempdirs[i].split('/')
        check_TemplateDir_corresponsingObject(object_name[2])
