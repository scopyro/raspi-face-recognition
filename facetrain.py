#This code creates a trainer.yml and labels files that we use in the recognition code.
#The labels give us confidence and label ID (how much confidence the recognizer is in relation to this match). 
#If the face matches, the servo will turn on
import os
import numpy as np 
from PIL import Image 
import cv2
import pickle

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#Use the LBPH (LOCAL BINARY PATTERNS HISTOGRAMS) face recognizer, included on the OpenCV package
recognizer = cv2.face.LBPHFaceRecognizer_create()

#Get the path of the current working directory and we move to the directory where 
# the image directories are present
baseDir = os.path.dirname(os.path.abspath(__file__))
imageDir = os.path.join(baseDir, "images")

currentId = 1
labelIds = {}
yLabels = []
xTrain = []

#Move into each image directory and look for the images. If the image is present,
# we convert it into the NumPy array
for root, dirs, files in os.walk(imageDir):
	print(root, dirs, files)
	for file in files:
		print(file)
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root, file)
			label = os.path.basename(root)
			print(label)

			if not label in labelIds:
				labelIds[label] = currentId
				print(labelIds)
				currentId += 1

			id_ = labelIds[label]
			pilImage = Image.open(path).convert("L")
			imageArray = np.array(pilImage, "uint8")
			
			#Perform the face detection again to make sure we have the right images
			# and then we prepare the training data
			faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)

			for (x, y, w, h) in faces:
				roi = imageArray[y:y+h, x:x+w]
				xTrain.append(roi)
				yLabels.append(id_)

#Store the dictionary which contains the directory names and label IDs
with open("labels", "wb") as f:
	pickle.dump(labelIds, f)
	f.close()

#Train the data and save the file
recognizer.train(xTrain, np.array(yLabels))
recognizer.save("trainer.yml")
print(labelIds)