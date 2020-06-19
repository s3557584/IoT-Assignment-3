"""
Task C

Written By: Lin

This class contains the code for the QRCode scanner part of the assignment
"""
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
class QRCodeScanner:
	
	def __init__(self):
		"""
		Empty Constructor

		Parameters:
			None
		
		Returns:
			None
		"""
		pass

	def argumentParser(self):
		"""
		Function to parse arguments for the csv file

		Parameters:
			None
		
		Returns:
			arguments(dict): Contains the arguments for the csv file
		"""
		# construct the argument parser and parse the arguments
		parseArgument = argparse.ArgumentParser()
		parseArgument.add_argument("-o", "--output", type=str, default="qrCodesResults.csv",
		help="path to output CSV file containing QRCodes")
		arguments = vars(parseArgument.parse_args())
		return arguments

	def detectQR(self, QRCodes, frame, found, csv):
		"""
		This function mainly extract the data from detected QRCodes and writes them into the csv file

		Parameters:
			QRCodes(list): List of QR codes
			frame: Camera frame configurations data
			found(list): List of QR codes data
			csv: The csv file
		
		Returns:
			None
		"""
		for i in QRCodes:
			# extract the bounding box location of the barcode and draw
			# the bounding box surrounding the barcode on the image
			(x, y, w, h) = i.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			# the barcode data is a bytes object so if we want to draw it
			# on our output image we need to convert it to a string first
			barcodeData = i.data.decode("utf-8")
			barcodeType = i.type
			# draw the barcode data and barcode type on the image
			text = "{} ({})".format(barcodeData, barcodeType)
			cv2.putText(frame, text, (x, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			# if the barcode text is currently not in our CSV file, write
			# the timestamp + barcode to disk and update the set
			if barcodeData not in found:
				csv.write("{},{}\n".format(datetime.datetime.now(),
					barcodeData))
				csv.flush()
				found.add(barcodeData)
				print(barcodeData)

	def iterateVideoFrames(self, camera, found, csv):
		"""
		This functions mainly iterate through the video frame by frame to detect the QR codes

		Parameters:
			camera: Readings from the camera
			found(list): List of QR code data
			csv: The csv file
		
		Returns:
			None
		"""
		while True:
			frame = camera.read()
			frame = imutils.resize(frame, width=400)
			# find the barcodes in the frame and decode each of the barcodes
			QRCodes = pyzbar.decode(frame)

			# loop over the detected barcodes
			self.detectQR(QRCodes, frame, found, csv)
			# shows the frame in the display
			cv2.imshow("QRCode Scanner", frame)
			quit = cv2.waitKey(1) & 0xFF
		
			# Quit the program if 'q' is pressed
			if quit == ord("q"):
				break


