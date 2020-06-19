from bluetooth import *
from pushbullet import PushBullet
from databaseUtil import DatabaseUtil
import MySQLdb
from BluetoothID import BluetoothID

from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
from QRCodeScanner import QRCodeScanner

if __name__ == '__main__':
	"""
	Task B

	Written by: Jason

	Entry point for the bluetooth identification program
	"""
	print("************Bluetooth Identification**************")
	choice = input("A: Bluetooth\nB: QR Scanner\nPlease enter your choice: ")

	if choice == "A" or choice == "a":
		objBluetooth = BluetoothID()

		print("Performing Inquiry")

		#Looking for nearby devices
		nearby_devices = discover_devices(lookup_names = True)

		print ("found %d devices" %len(nearby_devices))

		#Print out all the nearby devices
		for name in nearby_devices:
			print( "%s -%s" % (name))

		#Fetching the mac address registered in the database
		obj = DatabaseUtil()
		phone = obj.getDeviceID("Altis")

		#split tuple so we get just the mac addr
		(addr, ownder) = name

		objBluetooth.Verify(addr, phone)
	elif choice == "B" or choice == "b":
		"""
		Main entry point of the program
		"""
		obj = QRCodeScanner()

		arguments = obj.argumentParser()

		# initialize the camera
		print("Starting Camera")
		camera = VideoStream(src=0).start()
		time.sleep(2.0)

		# open the output CSV file for writing and initialize the set of
		# barcodes found thus far
		csv = open(arguments["output"], "w")
		found = set()

		# loop over the frames from the video stream
		obj.iterateVideoFrames(camera, found, csv)

		# closing the program by destroying all windows
		print("Closing")
		csv.close()
		cv2.destroyAllWindows()
		camera.stop()