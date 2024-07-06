	# Reading and Saving Serial Data from MCU
# Written by: Sreela Kodali (kodali@stanford.edu) 

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import serial
import datetime
import csv
import os
import numpy as np
import sys, getopt
import pandas as pd

def graph(s, p, time, temp):
	fig, ax1 = plt.subplots()
	plt.suptitle("Temperature Data vs Time", name='Arial', weight='bold')
	ax1.set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Temperature (F)", name='Arial',)
	#ax1.scatter(time, force)
	l1 = ax1.plot(time, temp, 'r', linewidth=1.75, label='Force')
	ax1.yaxis.label.set_color('r')
	ax1.tick_params(axis='y', color='r')
	#ax1.set_ylim(-2,10)
	#ax1.set_ylim(0,2)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig")
	plt.show()

PATH = '/Users/Sreela/Documents/Personal/homeTemperatureUnit/DataCollected/' # change this to your path!
directories = ['2024-07-04_13-46', '2024-07-04_19-12', '2024-07-06_00-55']

headers = ['datetime', 'temp']
dtypes = {'datetime': 'str', 'temp': 'float'}
parse_dates = ['datetime']


#allData = pd.DataFrame()

if (len(directories) >= 1):
	for i in range(0,len(directories)):
		if (i == 0):
			data = pd.read_csv(PATH + directories[i] + '/processed_' + directories[i] + '.csv', delimiter = ",", header=None, names=headers, dtype=dtypes, parse_dates=parse_dates)
		else:
			data2 = pd.read_csv(PATH + directories[i] + '/processed_' + directories[i] + '.csv', delimiter = ",", header=None, names=headers, dtype=dtypes, parse_dates=parse_dates)
			data = data.append(data2, ignore_index=True)


time = data['datetime']
temp = data['temp']
print(data)

graph(0, PATH, time, temp)

