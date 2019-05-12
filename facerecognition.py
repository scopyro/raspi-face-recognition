import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import pickle
import RPi.GPIO as GPIO
from time import sleep

relay_pin = [26]
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, 0)

#Load the pickle file which contains the dictionary
with open('labels', 'rb') as f:
	dicti = pickle.load(f)
	f.close()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

#Load the classifier that will detect the faces and the recognizer that will
# predict the faces and the trained data
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

font = cv2.FONT_HERSHEY_SIMPLEX

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	frame = frame.array
	
	#read the frame, convert it to grayscale, and look for the faces in the image. 
	#If any faces are there, we will extract the face region and use the recognizer 
	# to recognize the image
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
	for (x, y, w, h) in faces:
		roiGray = gray[y:y+h, x:x+w]

		id_, conf = recognizer.predict(roiGray)

		#look in the dictionary for the name assigned to this label ID
		for name, value in dict.items():
			if value == id_:
				print(name)
		
		#check whether we have enough confidence to open the door lock. 
		#If the confidence is less than 70, the door will open. Otherwise, it will remain closed
		if conf <= 70:
			#GPIO.output(relay_pin, 1)
			print("Opening the door../")
			
			#Create a rectangle in the original image and write this name on top of the rectangle
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			cv2.putText(frame, name + str(conf), (x, y), font, 2, (0, 0 ,255), 2,cv2.LINE_AA)

		else:
			#GPIO.output(relay_pin, 0)
			print("You shall not pass!")
			
	cv2.imshow('frame', frame)
	key = cv2.waitKey(1)

	rawCapture.truncate(0)

	if key == 27:
		break

cv2.destroyAllWindows()