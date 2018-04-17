# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:08:43 2018

@author: jlm7
"""
from itertools import cycle
import matplotlib.pyplot as plt



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
    print(temp_40K_row)
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
    for i, x in enumerate(power_40K_data):
            power_string.append(str(round(power_4K_set[i],2)) + ", " + str(round(power_40K_set[i],2)))
    for i, txt in enumerate(power_string):
        ax1.annotate(txt, (temp_40K[i],temp_4K[i]))
    fig.show()
    
better_graph(rows = len(powers_in_40K), cols = len(powers_in_4K))