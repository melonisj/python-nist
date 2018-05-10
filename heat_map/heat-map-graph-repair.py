# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 10:07:42 2018

@author: jlm7
"""

import csv
from itertools import cycle
import matplotlib.pyplot as plt
temp_4K = []
temp_40K = []
power_4K = []
power_40K = []
power_4K_set = []
power_40K_set = []
row_count = 0
filename = "heat_map_data.csv"

        
temp_4K_2 = []
temp_40K_2 = []
power_4K_2 = []
power_40K_2 = []
power_4K_set_2 = []
power_40K_set_2 = []

temp_4K_3 = []
temp_40K_3 = []
power_4K_3 = []
power_40K_3 = []

temp_4K_4 = []
temp_40K_4 = []
power_4K_4 = []
power_40K_4 = []
with open(filename, "r", newline='') as output:
    reader = csv.reader(output,delimiter=',')
    for row in reader:
        if(row_count < 65 and row_count > 0): #heatmap_test3a
            temp_4K_4.append(float(row[10]))
            temp_40K_4.append(float(row[5]))
            power_4K_4.append(float(row[9]))
            power_40K_4.append(float(row[4]))
        if(row_count > 68 and row_count < 133): #heatmap_test4
            temp_4K.append(float(row[10]))
            temp_40K.append(float(row[5]))
            power_4K.append(float(row[9]))
            power_40K.append(float(row[4]))
        if(row_count > 132 and row_count < 197):
            temp_4K_2.append(float(row[10]))
            temp_40K_2.append(float(row[5]))
            power_4K_2.append(float(row[9]))
            power_40K_2.append(float(row[4]))
        if(row_count > 196 and row_count < 261):
            temp_4K_3.append(float(row[10]))
            temp_40K_3.append(float(row[5]))
            power_4K_3.append(float(row[9]))
            power_40K_3.append(float(row[4]))
#        if(row_count > 260 and row_count < 325):
#            temp_4K_2.append(float(row[10]))
#            temp_40K_2.append(float(row[5]))
#            power_4K_2.append(float(row[9]))
#            power_40K_2.append(float(row[4]))
#        if(row_count > 324 and row_count < 389):
#            temp_4K.append(float(row[10]))
#            temp_40K.append(float(row[5]))
#            power_4K.append(float(row[9]))
#            power_40K.append(float(row[4]))
#        if(row_count > 388 and row_count < 453):
#            temp_4K.append(float(row[10]))
#            temp_40K.append(float(row[5]))
#            power_4K.append(float(row[9]))
#            power_40K.append(float(row[4]))
        row_count = row_count +1      
            

#Fix data Points that God messed Up
temp_4K[36] = temp_4K[28]
temp_4K[62] = temp_4K_2[62]
temp_4K[14] = temp_4K_2[14]
temp_4K[31] = temp_4K_2[31]
temp_4K[47] = temp_4K_4[47]
#
temp_40K[62] = temp_40K_2[62]
temp_40K[14] = temp_40K_2[14]
temp_40K[31] = temp_40K_2[31]


#temp_40K = temp_40K_2
#power_4K = power_4K_2
#power_40K = power_40K_2

#Fix Labels that got messed up
power_4K[62] = power_4K_2[62]
power_4K[14] = power_4K_2[14]
power_4K[36] = power_4K_2[36]
power_4K[31] = power_4K_2[39]
power_4K[47] = power_4K_2[39]



def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def better_graph(rows, cols):
    temp_40K_col = chunkIt(temp_40K, cols)
    temp_4K_col = chunkIt(temp_4K, cols)
#    power_40K_col = chunkIt(power_40K_data, cols)
#    power_4K_col = chunkIt(power_4K_data, cols)
    

    
    width_4K = len(temp_4K)
#    print(width_4K)
    temps_40K_overlay = []
    temps_4K_overlay = []
    for i, x in enumerate(temp_4K):
        temps_40K_overlay.append(temp_40K[rows*i%(width_4K-1)])
        temps_4K_overlay.append(temp_4K[rows*i%(width_4K-1)])
    temps_4K_overlay[len(temps_4K_overlay)-1] = temp_4K[len(temp_4K)-1]
    temps_40K_overlay[len(temps_40K_overlay)-1] = temp_40K[len(temp_40K)-1]

    temp_40K_row = chunkIt(temps_40K_overlay, rows)
    temp_4K_row = chunkIt(temps_4K_overlay, rows)
#    power_40K_row = chunkIt(temps_40K_overlay, rows)
#    power_4K_row = chunkIt(temps_4K_overlay, rows)
    

    
    colors = cycle(["aqua", "black", "blue", "fuchsia", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
#        ax2 = fig.add_subplot(111)
    for i, x in enumerate(temp_40K_col):
        ax1.plot(temp_40K_col[i], temp_4K_col[i], '-r')
    for i, x in enumerate(temp_40K_row):
        ax1.plot(temp_40K_row[i], temp_4K_row[i], '-b')
    ax1.set_xlabel('Temp in 40K Stage')
    ax1.set_ylabel('Temp in 4K Stage')
    ax1.set_title('Heat Map')
    
    power_string= []
    for i, x in enumerate(power_40K):
            power_string.append(str(round(abs(power_4K[i]),2)) + ", " + str(round(abs(power_40K[i]),2)))
    for i, txt in enumerate(power_string):
        ax1.annotate(txt, (temp_40K[i],temp_4K[i]), fontsize = 11)
    fig.show()
    plt.savefig("reformed.png")
    
better_graph(rows = 8, cols = 8)