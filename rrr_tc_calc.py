# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 11:00:39 2018

@author: jlm7
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

#%% setup
ch1 = []
ch2 = []
ch3 = []
ch4 = []
ch5 = []
ch6 = []
time = [[],[],[],[],[],[]]
temp = [[],[],[],[],[],[]]
res = [[],[],[],[],[],[]]
count = 0


#%% read data from CSV file
with open("test-channel-measurements.csv", "r", newline='') as output:
            reader = csv.reader(output,delimiter=',')
            for row in reader:
                if '#' not in row[0]:
                    time[int(row[1])-1].append(float(row[0]))
                    temp[int(row[1])-1].append(float(row[2]))
                    res[int(row[1])-1].append(float(row[3]))
                    count = count + 1
                    

#%% Initial Plot

colors = cycle(["aqua", "black", "blue", "fuchsia", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
#unccolors = cycle(["lightskyblue","gray","cornflowerblue","palevioletred","darkseagreen","palegreen","lightcoral","slategray","darkkhaki","mediumorchid","indianred","lightgrey","powderblue","palegoldenrod"])
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(6):
    ax.plot(time[i],res[i], label="Ch " + str(i), color = next(colors))
ax.legend(loc="best")
ax.set_xlabel("Time(s)", fontsize=12)
ax.set_ylabel("Resistance(Ω)", fontsize=12)
ax.set_title("Resistance over time", fontsize = 18)

#%% Calculate RRR



for x in range(6):
    while(val in temp[x] > 280):
        




#%% Calculate Tc

ch1_resistance = np.array(res[1], dtype=np.float)
ch1_slope = np.gradient(ch1_resistance)