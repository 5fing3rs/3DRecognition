import os
import template_generator
from PIL import Image
import pytest

def test_template_generation():
	template_generator.generate_template("../data/syringe/training_video/syringe_body_1.avi", 45)
	if(os.path.exists("../data/syringe/templates/syringe_body_2_0.jpg") == 1):
		test_var3 = 1
	else:
		test_var3 = 0
	assert(test_var3) == 1

def test_rezise():
	basewidth = 500
	initial_image = Image.open("../data/syringe/templates/syringe_body_2_0.jpg")
	initial_image_height = initial_image.size[1]
	initial_image_width = initial_image.size[0]
	template_generator.resize_image("../data/syringe/templates/syringe_body_2_0.jpg", basewidth) #angle 0 always exists
	test_image = Image.open("../data/syringe/templates/syringe_body_2_0.jpg") 
	test_var2 = test_image.size[0]
	test_var3 = test_image.size[1]
	assert(test_var2) == 500
	assert(test_var3) == initial_image_height*(500/initial_image_width)

def test_check_path():
	test_var4 = template_generator.get_template_path("../data/syringe/training_video/syringe_body_1.avi", 0)
	assert(test_var4 == "../data/syringe/templates/syringe_1_0.jpg")


#found error for this test case, there's nothing like path.is_file. Import os.path and use os.path.isfile instead
def test_path_validation():
	vald = template_generator.validate_path("../data/syringe/training_video/syringe_body_1.avi")
	assert(vald == 1)