#Interfaces with an Arduino board to receive data about the Pan-Tilt Scanner 
#we built and gives XYZ coordinates for 3D Imaging. Loads to a csv file for better visualization
#in MATLAB or some other program.

import serial
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import time
import csv


def StartUp():
	"""
	Sets up Serial to communicate with Arduino
	"""

	ser = serial.Serial('/dev/cu.usbmodem1421', 9600, timeout=1)

	#resets the serial port and prints a statement to ensure it's working
	ser.close()
	time.sleep(1)
	ser.open()
	print ser.isOpen()

	return ser


def ReadArduino(ser):
	"""
	Reads Arduino inputs and converts them to a usable form
	"""

	s = ser.readline()

	#ensures the the data is real and isn't corrupted.
	if s is not None and len(s) > 0:

		data = s.split(', ')

		#checks if the data has enough points to be considered valid
		if len(data) >= 2:

			#formatting
			data[-1] = data[-1][:-2]
			print data

			#checks that infrared sensor works properly (broken will return nothing or empty strings)
			if all(len(item) > 0 for item in data):

				for i in range(len(data)):
					data[i] = float(data[i])

				return data

	#will return None if data is bad, which will prompt the while loop to close
	return None


def Spherical2Cartesian(r, phi, theta):
	"""
	Converts from Spherical Coordinates to Cartesian Coordinates
	Assumes phi and theta are in degrees
	"""

	x = r * np.sin(np.radians(phi)) * np.cos(np.radians(theta))
	y = r * np.sin(np.radians(phi)) * np.sin(np.radians(theta))
	z = r * np.cos(np.radians(phi)) 

	return x, y, z


def Polar2Cartesian(r, theta):
	"""
	Converts from Polar Coordinates to Cartesian Coordinates
	Assumes phi and theta are in degrees	
	"""

	x = r * np.cos(np.radians(theta))
	y = r * np.sin(np.radians(theta))

	return x, y


def Update3DData(x,y,z, xarray, yarray, zarray):
	"""
	Updates the 3D data based on the continual readings from Arduino.
	"""

	xarray.append(x)
	yarray.append(y)
	zarray.append(z)

	return xarray, yarray, zarray


def Update2DData(x, y, xarray, yarray):
	"""
	Updates the 2D plot based on the continual readings from Arduino.
	"""

	xarray.append(x)
	yarray.append(y)	

	return xarray, yarray


if __name__ == "__main__":

	dim = raw_input('We doing 2D or 3D?\n\n')

	#data arrays
	xarray = []
	yarray = []
	zarray = []

	#counter which checks to see if sufficient time has passed before exiting while loop
	stop_counter = 0

	#keeps the loop looping
	start = True

	#starts up serial port, and sends a command to begin Arduino processes
	ser = StartUp()
	time.sleep(2)
	ser.write('start')

	while start:	

		#reads a datapoint
		datapoint = ReadArduino(ser)

		if datapoint is not None:

			#decides if 3D or 2D, and updates data arrays accordingly
			if dim == "3d":
				coordinates = Spherical2Cartesian(datapoint[0], datapoint[1], datapoint[2])
				xarray, yarray, zarray = Update3DData(coordinates[0], coordinates[1], coordinates[2], xarray, yarray, zarray)

			elif dim == '2d':	
				coordinates = Polar2Cartesian(datapoint[0], datapoint[1])
				xarray, yarray = Update2DData(coordinates[0], coordinates[1], xarray, yarray)

		#stops the loop once data stops coming through
		else:
			stop_counter += 1
			if stop_counter > 5:
				start = False


	#decides if 3D or 2D, and writes to a csv file accordingly
	if dim == "3d":

		file = open('test3d.csv','wb')

		writer = csv.writer(file, delimiter=',')

		writer.writerow(xarray)
		writer.writerow(yarray)
		writer.writerow(zarray)

		file.close()

	if dim == "2d":
		file = open('test2d.csv','wb')

		writer = csv.writer(file, delimiter=',')

		writer.writerow(xarray)
		writer.writerow(yarray)

		file.close()

	#ensures closure of the serial port
	ser.close()







