#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/proj/MFRC522-python/')
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("Hold a tag near the reader")

try:
	id, text = reader.read()
	print(text.strip() + "," + str(id))

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	print("Keyboard interrupt")

finally:
	GPIO.cleanup()
	sys.exit()
