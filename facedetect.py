# import the required package
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import os
import sys

#initialize the camera object that will allow us to play with the Raspberry Pi camera. 
#We set the resolution at (640, 480) and frame rate at 30 fps
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

#PiRGBArray() gives us a 3-dimensional RGB array organized(rows, columns, colors) 
# from an unencoded RGB capture. PiRGBArray’s advantage is its ability to read 
# the frames from Raspberry Pi camera as NumPy arrays making it compatible with OpenCV
#It avoids the conversion from JPEG format to OpenCV format which would slow our process
rawCapture = PiRGBArray(camera, size=(640, 480))

#Load a cascade file for detecting faces
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#Ask the user for a name. If a directory with that name is already there,
# it will respond with “Name already exists” and will exit the code. 
#If a directory with this name isn’t there, it will create the directory 
# and images will be saved with this name
name = input("What's his/her Name? ")
dirName = "./images/" + name
print(dirName)
if not os.path.exists(dirName):
	os.makedirs(dirName)
	print("Directory Created")
else:
	print("Name already exists")
	sys.exit()

count = 1
#The format in which we want to read each frame since OpenCV expects the image to be in 
# the BGR format rather than the RGB so we specify the format to be BGR
#use_video_port=True means we are treating as a stream video
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	if count > 30:
		break
	
	#Once we have the frame, we can access the raw NumPy array via the .array attribute. 
	#After accessing, we convert this frame to grayscale
	frame = frame.array
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	#Call our classifier function to detect faces in the frame. The first argument we pass
	# is the grayscale image. The second argument is the parameter specifying how much 
	# the image size is reduced at each image scale. The third argument is a parameter 
	# specifying how many neighbors each candidate rectangle should have to retain it. 
	#A higher number gives lower false positive
	faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
	
	#Show the cropped face and created a rectangle on the original frame.
	#The code will collect 30 image
	for (x, y, w, h) in faces:
		roiGray = gray[y:y+h, x:x+w]
		fileName = dirName + "/" + name + str(count) + ".jpg"
		cv2.imwrite(fileName, roiGray)
		cv2.imshow("face", roiGray)
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		count += 1
	
	#Show the original frame on the output window. cv2.waitkey() is a keyboard binding function.
	#It waits for a specified millisecond for any keyboard event. It takes one argument and 
	# this argument is the time in milliseconds. If the key is pressed in that time then 
	# the program will continue. Passing 0 means it will wait infinitely for a key
	cv2.imshow('frame', frame)
	key = cv2.waitKey(1)
	
	#Clear the stream in preparation for the next frame by calling truncate(0) between captures
	rawCapture.truncate(0)

	if key == 27:
		break

cv2.destroyAllWindows()