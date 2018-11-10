from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import cv2

class OutputVideoWriter(object):
    def __init__(self, file_name, fps, height, width, is_color):
        self.file_name = file_name
        self.height = height
        self.width = width
        self.is_color = is_color
        self.fps = fps
        self.dimension = width, height
        print(type(file_name))
        print(type(fps))
        print(type(self.dimension))
        print(type(is_color))


        self.video = VideoWriter(file_name,VideoWriter_fourcc(*"XVID"), fps, self.dimension , is_color)

    def write(self, frame):
        self.video.write(frame)
        print("Written")

    def set_dimension(self, width, height):
        self.height = height
        self.width = width

    def release_video(self):
        self.video.release()
        
