"""
Task B

Written by: Jason

BluetoothID Class

This class contains the code for the bluetooth verification part of the assignment
"""
from bluetooth import *
from pushbullet import PushBullet
from databaseUtil import DatabaseUtil
import MySQLdb

class BluetoothID:
	
	def __init__(self):
		"""
		Constructor of the class

		Parameters: 
		    None

		Returns:
		    None
		"""
		pass
	
	def Verify(self, addr, phone):
		"""
		Verify function. Takes in the mac address of the device and compare it with the database

		Parameters: 
		    addr(str): Mac address from the detected phone
		    phone(str): Mac address information from the database

		Returns:
		    None
		"""
		if addr == phone:
			print("Authorised, Vehicle Unlocked!!!")
			apiKey = "o.spfQSePwyGKGMeZG8DZxXZRJIMmSli0X"
			p = PushBullet(apiKey)
			dev = p.get_device('HUAWEI TAS-L29')
			push = dev.push_note("NOTICE: ", "Vehicle Unlocked!!")
		else:
			print("Unauthorised!!!")

