# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 13:46:22 2018

@author: jlm7
"""

from ka3305p import ka3305p
from srs_sim970 import SIM970
import time
import matplotlib.pyplot as plt
import client
import math
import numpy as np
from tqdm import tqdm


source = ka3305p('COM8')
voltmeter = SIM970('GPIB0::4',7)
 
voltmeter.set_impedance(True,channel=1)
voltmeter.set_impedance(True,channel=2)
voltmeter.set_impedance(True,channel=3)
voltmeter.set_impedance(True,channel=4)
source.set_output(on=False)

temp_4K = []
temp_40K = []
series_voltage_40K = []
power_resistor_voltage_40K = []
series_current_40K = []
avg_powers = []
time_array = []
cur_time = -10 #waits this long before turning on the heater. -10 means it waits 10 seconds and then turns on the heater
power_wanted = 2
set_voltage = 1.2*math.sqrt(50 * power_wanted)

time.sleep(2)
source.set_voltage(channel=1, voltage=round(set_voltage,2))
time.sleep(2)

print("Begin Data collection no heat")
pbar = tqdm(total=10/0.46)
while (cur_time < 0):
    all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
    temp_4K.append(float(all_temps[5]))
    temp_40K.append(float(all_temps[6]))
    cur_time += 0.46
    time_array.append(cur_time)
    pbar.update(0.46)
    
    
source.set_output(on=True)
print("\n\nBegin heating Loop")
run_time = 6600 #seconds to measure
pbar = tqdm(total=run_time) # CHANGE THIS TO ADJUST TOTAL MEASUREMENT TIME
while (cur_time < run_time):
    all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
    temp_4K.append(float(all_temps[5]))
    temp_40K.append(float(all_temps[6]))
    cur_time += 0.7
    time_array.append(cur_time)
    
    series_v_read = voltmeter.read_voltage(channel = 1)
    r_voltage = voltmeter.read_voltage(channel = 2)
    s_current = (set_voltage - series_v_read) / 10
    series_voltage_40K.append(series_v_read)
    power_resistor_voltage_40K.append(r_voltage)
    series_current_40K.append(s_current)
    avg_powers.append(s_current * r_voltage)
    pbar.update(0.7)
    
source.set_output(on=False)

print("Avg Power: ", np.mean(avg_powers))
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(time_array, temp_4K, '-ro')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Temperature in 40K(K)",color='r')
ax1.set_title("Temperature Applied in 40K")
ax2.plot(time_array, temp_40K, '-bo')
ax2.set_ylabel("Temperature in 40K(K)", color='b')
ax1.legend(loc="best")
ax1.margins(0.1)
fig.tight_layout()

source.close()