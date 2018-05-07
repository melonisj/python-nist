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

pre_heat_time = 10
run_time = 2000 #seconds to measure
series_resistance = 10
voltmeter_channel_1 = 1
voltmeter_channel_2 = 2
voltage_source_channel = 1
power_wanted = 2 


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

cur_time = 0
set_voltage = 1.2*math.sqrt(50 * power_wanted)
time.sleep(2)
source.set_voltage(channel=voltage_source_channel, voltage=round(set_voltage,2))
time.sleep(2)
start_time = time.time()

print("Begin Data collection no heat")
pbar = tqdm(total=pre_heat_time)
while (cur_time < start_time + pre_heat_time):
    all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
    temp_4K.append(float(all_temps[5]))
    temp_40K.append(float(all_temps[6]))
    cur_time = time.time()
    time_array.append(cur_time)
    pbar.update(cur_time - start_time)
    
#reset time
source.set_output(on=True)
print("\n\nBegin heating Loop")
pbar = tqdm(total=run_time) 
while (cur_time < run_time + start_time + pre_heat_time):
    all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
    temp_4K.append(float(all_temps[5]))
    temp_40K.append(float(all_temps[6]))
    time_array.append(cur_time - start_time)
    
    series_v_read = voltmeter.read_voltage(channel = voltmeter_channel_1)
    r_voltage = voltmeter.read_voltage(channel = voltmeter_channel_2)
    s_current = (set_voltage - series_v_read) / series_resistance
    series_voltage_40K.append(series_v_read)
    power_resistor_voltage_40K.append(r_voltage)
    series_current_40K.append(s_current)
    avg_powers.append(s_current * r_voltage)
    cur_time =time.time()

    pbar.update(cur_time - start_time - pre_heat_time)
    
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