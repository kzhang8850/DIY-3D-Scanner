#Interfaces with an Arduino board to receive data about the Pan-Tilt Scanner 
#we built and gives XYZ coordinates for 3D Imaging.

import serial
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import time
import sys, select, os

def StartUp():
	"""
	Sets up Serial to communicate with Arduino
	"""


	ser = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=1)
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
	print s
	

	if s is not None and len(s) > 0:
		print s

		data = s.split(', ')

		if len(data) >= 2:

			data[-1] = data[-1][:-2]
			print data

			if all(len(item) > 0 for item in data):

				for i in range(len(data)):
					data[i] = float(data[i])

				return data

	return None


def Spherical2Cartesian(r, theta, phi):
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




def Plot3DCoordinates():
	"""
	Creates a 3D plot and starts up plotting functionality
	"""

	plt.ion()
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.set_xlabel('X Axis')
	ax.set_ylabel('Y Axis')
	ax.set_zlabel('Z Axis')

	ax.set_xlim3d(0, 20)
	ax.set_ylim3d(0, 20)
	ax.set_zlim3d(0, 20)

	ax.scatter(0, 0, 0, c='g', marker='o')
	plt.show()

	return ax

def Update3DPlot(graph, x,y,z, xarray, yarray, zarray):
	"""
	Updates the 3D plot based on the continual readings from Arduino.
	"""
	if len(xarray) < 180*180:
		xarray.append(x)
	else:
		xarray = xarray[1:]
		xarray.append(x)

	if len(yarray) < 180*180:
		yarray.append(y)
	else:
		yarray = yarray[1:]
		yarray.append(y)

	if len(zarray) < 180*180:
		zarray.append(z)
	else:
		zarray = zarray[1:]
		zarray.append(z)

 	if len(xarray) % 180 == 0:
		graph.scatter(xarray, yarray, zarray, c='g', marker='o')

		plt.draw()
		plt.pause(.01)


def Plot2DCoordinates():
	"""
	Creates a 2D plot and starts up plotting functionality
	"""

	plt.ion()
	fig = plt.figure()

	plt.scatter(0, 0, c = 'g', alpha = 0.5)
	plt.show()

def Update2DPlot(x, y, xarray, yarray):
	"""
	Updates the 2D plot based on the continual readings from Arduino.
	"""
	if len(xarray) < 180*2:
		xarray.append(x)
	else:
		xarray = xarray[1:]
		xarray.append(x)

	if len(yarray) < 180*2:
		yarray.append(y)
	else:
		yarray = yarray[1:]
		yarray.append(y)	

	if len(xarray) % 180 == 0:	

		plt.scatter(xarray, yarray, c='g', alpha=.5)

		plt.draw()
		plt.pause(.01)




if __name__ == "__main__":

	print "Doing the Arduino Thing."
	dim = raw_input('We doing 2D or 3D?\n\n')


	if dim == "3d":
		graph = Plot3DCoordinates()
	elif dim == '2d':
		Plot2DCoordinates()	


	xarray = []
	yarray = []
	zarray = []

	ser = StartUp()
	print ser

	while True:

		if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			break		

		datapoint = ReadArduino(ser)

		if datapoint is not None:

			if dim == "3d":
				coordinates = Spherical2Cartesian(datapoint[0], datapoint[1], datapoint[2])
				Update3DPlot(graph, coordinates[0], coordinates[1], coordinates[2], xarray, yarray, zarray)

			elif dim == '2d':	
				coordinates = Polar2Cartesian(datapoint[0], datapoint[1])
				Update2DPlot(coordinates[0], coordinates[1], xarray, yarray)
	print ser.isOpen()
	ser.close()
	print ser.isOpen()








