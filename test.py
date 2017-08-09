import unittest

import PIL
import timeit
from PIL import Image
from libs.pb_image import *

imgPath = './dataTest'

background_small = Image.open(imgPath + '/black_762.jpg')
background_big = Image.open(imgPath + '/black_big_7638.jpg')
image1 = Image.open(imgPath + '/white.jpg')
image2 = Image.open(imgPath + '/red.jpg')
image3 = Image.open(imgPath + '/blue.jpg')
image4 = Image.open(imgPath + '/green.jpg')

def test_combineResize():
	combined_image = pb_resizeAndMergeImages(background_small, 246, 246 / 10, 246 / 2, image1, image2, image3, image4)
	combined_image.save(imgPath + '/combined_testResult_resized.jpg', 'JPEG', quality=100)
	#print("total width: ", pb_getSquarePixelResolution(246, 246 / 10, 246 / 2))
	#print("offset2: ", pb_getOffset2(246, 246 / 10, 246 / 2))

def test_combineNoResize():
	offset1 = 2464 / 2
	offset2 = 3942
	combined_image = pb_mergeImages(background_big, image1, image2, image3, image4, offset1, offset2)
	combined_image.save(imgPath + '/combined_testResult_not_resized.jpg', 'JPEG', quality=100)
	#print("total width: ", pb_getSquarePixelResolution(2464, 2464 / 10, 2464 / 2))
	#print("offset2: ", pb_getOffset2(2464, 2464 / 10, 2464 / 2))

class TestCombineImages(unittest.TestCase):
	def test_combine_no_resize_timed(self):
		time = timeit.timeit(test_combineNoResize, number=1)
		print("time without resize: ", time)
		self.assertLess(time, 8)
	def test_combine_resize_timed(self):
		time = timeit.timeit(test_combineResize, number=1)
		print("time with resize: ", time)
		self.assertLess(time, 8)

if __name__ == '__main__':
	unittest.main()

