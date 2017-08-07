import unittest

import PIL
from PIL import Image
from libs.pb_image import *

imgPath = './testData'

class TestCombineImages(unittest.TestCase):
	def test_combineNormal(self):
		background = Image.open('blank.jpg')
		image1 = Image.open(imgPath + '/image1.jpg')		
		image2 = Image.open(imgPath + '/image2.jpg')
		image3 = Image.open(imgPath + '/image3.jpg')
		image4 = Image.open(imgPath + '/image4.jpg')
		offset1 = 179
		offset2 = 519
		combined_image = pb_combineImages(background, image1, image2, image3, image4, offset1, offset2)
		combined_image.save(imgPath + '/combined_testResult.jpg', 'JPEG', quality=100)

if __name__ == '__main__':
	unittest.main()

