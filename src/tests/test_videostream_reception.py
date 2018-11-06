import os
import main2
from PIL import Image
import pytest

def video_reception():
	sys.argv.append("-td")
	sys.argv = ["../data/syringe/templates"]
	sys.argv.append("")