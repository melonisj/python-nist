# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 11:00:39 2018

@author: jlm7
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import os

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
channels_allowed = [1,2,3,4,5,6]
full_path = os.path.expanduser('~\Documents\Tc Check Data\Original\RampT Test\\2018_03_16_17_22_16.csv')
#full_path = os.path.expanduser('~\Documents\Tc Check Data\Modified\Full Cooldown\\2018_03_15_10_50_53.csv')
#full_path = os.path.expanduser('~\Documents\Tc Check Data\Original\Full Cooldown\\2018_02_23_13_37_51.csv')
#

#%% read data from CSV file
with open(full_path, "r", newline='') as output:
            reader = csv.reader(output,delimiter=',')
            for row in reader:
                if '#' not in row[0]:
                    if(float(row[3]) < 2000 and float(row[3]) > -2000):
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
    if((i+1) in channels_allowed):
        ax.plot(temp[i],res[i], label="Ch " + str(i+1), color = next(colors))
ax.legend(loc="best")
ax.set_xlabel("Temp(K)", fontsize=12)
ax.set_ylabel("Resistance(Ω)", fontsize=12)
ax.set_title("Resistance over time", fontsize = 18)

#%% Calculate RRR


#
#for x in range(6):
#    while(val in temp[x] > 280):
#        




#%% Calculate Tc

ch1_resistance = np.array(res[1], dtype=np.float)
ch1_slope = np.gradient(ch1_resistance)