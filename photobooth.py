# Raspberry Pi - Photo Booth
#
# Copyright (c) 2014, John Croucher - www.jcroucher.com
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this 
# list of conditions and the following disclaimer in the documentation and/or other 
# materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may 
# be used to endorse or promote products derived from this software without specific 
# prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
# THE POSSIBILITY OF SUCH DAMAGE.


import RPi.GPIO as GPIO
import time
from threading import Thread
import picamera
import PIL
from PIL import Image
import cups
import os
import sys
import pygame
import random
import select

from libs.pb_image import *

slideshowRunning = True
basewidth = 246 # Used for merging the photos onto one
printPhoto = False
imgPath = './images/tmp'

# Push button for starting the photo sequence
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Display surface
pygame.init()

pygame.mouse.set_visible(0)

w = pygame.display.Info().current_w
h = pygame.display.Info().current_h

maxSquareSize = min(w, h);

screenSize = (w, h)

screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN) # Full screen the display with no window


# Used for loading a random photo for the slideshow
def random_file(dir):
	files = [os.path.join(path, filename)
		for path, dirs, files in os.walk(dir)
		for filename in files]

	return random.choice(files)


def displayImage(file):
	screen.fill((0,0,0))

	img = pygame.image.load(file) 
	img = pygame.transform.scale(img,(maxSquareSize,maxSquareSize)) # Make the image full screen
	screen.blit(img,((w - maxSquareSize) / 2,0))
	pygame.display.flip() # update the display


# Display a random image
def slideshow():
	while True:

		if slideshowRunning == True:
	
			checkEvents()

			randomFile = random_file('./images/')
			
			displayImage(randomFile)
	
			time.sleep(2) # pause 

def quit():
	slideshowRunning = False
	pygame.quit()
	sys.exit()



# Handle events like keypress
def checkEvents():
	for event in pygame.event.get():
		# Shutdown the application if quit event or escape key is pressed
		if event.type == pygame.QUIT or ( event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE ):
			quit()
		if event.type is pygame.KEYDOWN and event.key == pygame.K_f: # Switch the display mode between full screen and windowed
			if screen.get_flags() & pygame.FULLSCREEN:
				pygame.display.set_mode(screenSize)
			else:
				pygame.display.set_mode(screenSize,pygame.FULLSCREEN)
		if event.type is pygame.KEYDOWN and event.key == pygame.K_p:
			return True
	while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
		line = sys.stdin.readline()
		print(line)
		if line:
			if line == "p\n":
				return True
			if line == "q\n":
				quit()	
	return False

# On screen text message
def displayStatus(status):
	screen.fill((0,0,0))
	
	font = pygame.font.SysFont("monospace",72)
	text = font.render(status,True,(255,255,255))

	# Display in the center of the screen
	textrect = text.get_rect()
	textrect.centerx = screen.get_rect().centerx
	textrect.centery = screen.get_rect().centery

	screen.blit(text,textrect)
	
	pygame.display.flip() # update the display
	

# Merge all photos onto one ready for printing
def combineImages():
	displayStatus('Please wait. Processing Images')
	background = Image.open('blank.jpg')
	image1 = Image.open(imgPath + '/image1.jpg')		
	image2 = Image.open(imgPath + '/image2.jpg')
	image3 = Image.open(imgPath + '/image3.jpg')
	image4 = Image.open(imgPath + '/image4.jpg')
	offset1 = 246 / 2
	offset2 = 393
	combined_image = pb_resizeAndMergeImages(background, 246, 246 / 10, 246 / 2, image1, image2, image3, image4)
	combined_image.save(imgPath + '/combined.jpg', 'JPEG', quality=100)


# Print the photo
def printPhoto():
	if printPhoto == True:
		displayStatus('Printing')

		conn = cups.Connection()
		printers = conn.getPrinters()
		printer_name = printers.keys()[0]
		conn.printFile(printer_name, imgPath + '/combined.jpg',"TITLE",{})

		time.sleep(2)

# Thread for the slideshow
t = Thread(target=slideshow)
t.start()

with picamera.PiCamera() as camera:
        camera.resolution = (2464, 2464)
	camera.annotate_text_size = 160
	while True:
		time.sleep(0.1);	
		input_state = checkEvents() # Needed to check for keypresses and close signals

		# Putton press to start the photo sequence
		input_state = False if input_state else GPIO.input(18)
		if input_state == False:
			print("stop slideshow")
			# Stop the slideshow
			slideshowRunning = False

			# Start the camera preview
			camera.start_preview()

			# Make the destination path for the photos
			if not os.path.exists(imgPath):
				os.mkdir(imgPath)

			# Loop through the 4 photo taking sequences
			for pNum in range (1,5):
				camera.annotate_text = 'Photo ' + str(pNum) + ' of 4'
				time.sleep(1)

				for countDown in range (3,0,-1):
					camera.annotate_text = str(countDown)
					time.sleep(1)
	
				camera.annotate_text = ''
				camera.capture( imgPath + '/image' + str(pNum) + '.jpg')

			# Stop the camera preview so we can return to the pygame surface
			camera.stop_preview()

			combineImages()

			printPhoto()

			displayImage( imgPath + '/combined.jpg' ) # Display a preview of the combined image

			time.sleep(5)

			# Move the temp files to a new dir based on the current timestamp so they can be retrieved later
			os.rename(imgPath, './images/' + str(int(time.time())))

			# Restart the slideshow
			slideshowRunning = True

			
			
