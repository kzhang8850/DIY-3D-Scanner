#Interfaces with an Arduino board to receive data about the Pan-Tilt Scanner 
#we built and gives XYZ coordinates for 3D Imaging.

import serial
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import time
import sys, select, os
import csv


def StartUp():
	"""
	Sets up Serial to communicate with Arduino
	"""


	ser = serial.Serial('/dev/cu.usbmodem1421', 9600, timeout=1)
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
		xarray.append(x*100)
	else:
		xarray = xarray[1:]
		xarray.append(x*100)

	if len(yarray) < 180*180:
		yarray.append(y*100)
	else:
		yarray = yarray[1:]
		yarray.append(y*100)

	if len(zarray) < 180*180:
		zarray.append(z*100)
	else:
		zarray = zarray[1:]
		zarray.append(z*100)


	return xarray, yarray, zarray




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

	return xarray, yarray




if __name__ == "__main__":

	print "Doing the Arduino Thing."
	dim = raw_input('We doing 2D or 3D?\n\n')

	if dim == "3d":
		graph = Plot3DCoordinates()
	elif dim == '2d':
		Plot2DCoordinates()	


	if dim == "a":
		csv.field_size_limit(sys.maxsize)

		ifile = open('ttest.csv', 'rb')
		reader = csv.reader(ifile)
		temp = []
		for row in reader:
			temp.append(row)
		xarray = temp[0]
		yarray = temp[1]
		zarray = temp[2]

		xarray = xarray[0].split('\t')
		yarray = yarray[0].split('\t')
		zarray = zarray[0].split('\t')
		print len(xarray)
		print len(yarray)
		print len(zarray)

		xarray = [float(item[1:-1]) for item in xarray]
		yarray = [float(item[1:-1]) for item in yarray]
		zarray = [float(item[1:-1]) for item in zarray]
		print xarray[-1]
		print yarray[-1]
		print zarray[-1]

		graph = Plot3DCoordinates()
		plt.ion()


		graph.scatter(xarray, yarray, zarray, c='g', marker='o')
		plt.pause(.0001)

		plt.show(block=True)	

		ifile.close()

		sys.exit()



	xarray = []
	yarray = []
	zarray = []
	stop_counter = 0
	start = True

	ser = StartUp()
	print ser
	time.sleep(2)
	ser.write('start')

	while start:

		if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			break		

		datapoint = ReadArduino(ser)

		if datapoint is not None:

			if dim == "3d":
				coordinates = Spherical2Cartesian(datapoint[0], datapoint[1], datapoint[2])
				xarray, yarray, zarray = Update3DPlot(graph, coordinates[0], coordinates[1], coordinates[2], xarray, yarray, zarray)

			elif dim == '2d':	
				coordinates = Polar2Cartesian(datapoint[0], datapoint[1])
				xarray, yarray = Update2DPlot(coordinates[0], coordinates[1], xarray, yarray)

		else:
			stop_counter += 1
			if stop_counter > 10:
				start = False


	if dim == "3d":

		file = open('test2.csv','wb')

		writer = csv.writer(file, delimiter=',')

		writer.writerow(xarray)
		writer.writerow(yarray)
		writer.writerow(zarray)

		file.close()
		graph.scatter(xarray, yarray, zarray, c='g', marker='o')

		plt.show(block=True)	

	if dim == "2d":
		plt.scatter(xarray, yarray, c='g', alpha=.5)

		plt.show(block=True)


	print ser.isOpen()
	ser.close()
	print ser.isOpen()








