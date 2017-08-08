import unittest

import PIL
from PIL import Image
from libs.pb_image import *

imgPath = './dataTest'

class TestCombineImages(unittest.TestCase):
	def test_combineNormal(self):
		background = Image.open(imgPath + '/black.jpg')
		image1 = Image.open(imgPath + '/white.jpg')		
		image2 = Image.open(imgPath + '/red.jpg')
		image3 = Image.open(imgPath + '/blue.jpg')
		image4 = Image.open(imgPath + '/green.jpg')
		offset1 = 191
		offset2 = 537
		combined_image = pb_combineImages(background, image1, image2, image3, image4, offset1, offset2)
		combined_image.save(imgPath + '/combined_testResult.jpg', 'JPEG', quality=100)

if __name__ == '__main__':
	unittest.main()

