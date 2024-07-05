	# Reading and Saving Serial Data from MCU
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import os
import numpy as np

## CONSTANTS
PATH = '/Users/Sreela/Documents/Personal/homeTemperatureUnit/DataCollected/' # change this to your path!
PORT_NAME = "/dev/cu.usbmodem14101" # change this to Arduino/teeny's port
BAUD_RATE = 9600
RUNTIME_LENGTH = 60 # seconds


START_TIME = datetime.datetime(2024, 7, 4, 13, 50, 0, 0)

#DIRECTORY
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = PATH +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)

mcu = serial.Serial(port=PORT_NAME, baudrate=BAUD_RATE, timeout=.1)
f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
g = open(p + 'processed_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)
writer2 = csv.writer(g)
writer.writerow([START_TIME])

date = []
temp = []
# Read in serial data and save in csv
endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)

#while (datetime.datetime.now() < endTime):

nLines = 0
while (nLines < 3):
	value = mcu.readline()
	value = str(value, "utf-8").split(", ")
	if (len(value) == 3):
		raw = [j.rstrip() for j in value]

		if ((raw[2] == 'NAN') or (raw[2] == 0)):
			break
		else:
			d1 = START_TIME + datetime.timedelta(seconds=int(raw[1])/1000)
			t = float(raw[2])
			date.append(d1)
			temp.append(t)

			nLines = nLines + 1
			print(raw)
			print('{}, {}'.format(str(d1), str(t)))
			writer.writerow(raw)
			writer2.writerow([d1, t])
f.close()
g.close()

