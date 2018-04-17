# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 11:06:14 2018

@author: jlm7
"""

from curve_fitting import determine_tc
import csv
import os

full_path = os.path.expanduser('~\Documents\Tc Check Data\Original\RampT Test\\2018_02_23_14_43_37.csv')
channel = 6
time = [[],[],[],[],[],[]]
temp = [[],[],[],[],[],[]]
res = [[],[],[],[],[],[]]

#%% read data from CSV file
with open(full_path, "r", newline='') as output:
            reader = csv.reader(output,delimiter=',')
            for row in reader:
                if '#' not in row[0]:
                    time[int(row[1])-1].append(float(row[0]))
                    temp[int(row[1])-1].append(float(row[2]))
                    res[int(row[1])-1].append(float(row[3]))
                    

tc_data = [[],[],[],[],[],[],[]]
for l in range (6):
    print("====================================\n\n\nChannel :", l+1)
    tc_data[l] = determine_tc(temp[l], res[l],(l+1))
    tc_data[l].calc_all()
