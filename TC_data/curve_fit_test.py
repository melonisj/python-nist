# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 11:06:14 2018

@author: jlm7
"""

from curve_fitting import determine_tc
import csv
import os

full_path = os.path.expanduser('H:\Documents\Tc Measurement Data\RampT\Raw Data\\2018_04_12_12_42_26.csv')
txt_file = os.path.expanduser('H:\Documents\Tc Measurement Data\RampT\Graph\\2018_04_12.txt')
graph_file = os.path.expanduser('H:\Documents\Tc Measurement Data\RampT\Graph\\2018_04_12.png')
channel = 6
time = [[],[],[],[],[],[]]
temp = [[],[],[],[],[],[]]
res = [[],[],[],[],[],[]]
tc_guess = [0,0,0,0,0,0] # set one of these to a non zero value if the fit line doesn't fit well. Default is 6
tc_negative = [0,0,0,0,0,1] # set one of these to 1 if the data is negative for some reason
tc_offset = [0,0,0,0,0,-10] #set one of these to the value need to get the superconducting to 0. This is probably needed if something is negative

#%% read data from CSV file
with open(full_path, "r", newline='') as output:
            reader = csv.reader(output,delimiter=',')
            for row in reader:
                if '#' not in row[0]:
                    time[int(row[1])-1].append(float(row[0]))
                    temp[int(row[1])-1].append(float(row[2]))
                    if(tc_negative[int(row[1])-1]):
                        res[int(row[1])-1].append(-1*float(row[3]) + tc_offset[int(row[1])-1])
                    else:
                        res[int(row[1])-1].append(float(row[3]) + tc_offset[int(row[1])-1])

                    

tc_data = [[],[],[],[],[],[],[]]
for l in range (6):
    print("====================================\n\n\nChannel :", l+1)
    if(tc_guess[l] != 0):
        tc_data[l] = determine_tc(temp[l], res[l],(l+1),txt_file, graph_file, tc_guess[l])
    else:
        tc_data[l] = determine_tc(temp[l], res[l],(l+1),txt_file, graph_file)
    if(tc_data[l].valid == True):
        tc_data[l].calc_all()
    else:
        print("No Data for Channel ", (l+1))
