# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 14:31:04 2018

@author: jlm7
"""

from ka3305p import ka3305p
from srs_sim970 import SIM970
import numpy as np
import time
import csv
import client
import datetime

#%%
# Expected Paramters
# set_voltage    : 1 V    |3 V     |4.3 V    |6 V    | 8.5 V  | 12 V   | 14.7 V  | 17 V   | 19 V   | 20.8 V  |
# expected_power : 0.01 V |0.125W  |0.25 V   | 0.5 W | 1 W    | 2 W    | 3 W     | 4 W    | 5 W    | 6 W     |
#
#
#%%
set_voltage = 6.0
series_resistance = 10

series_current_40K = []
series_voltage_40K = []
power_resistor_voltage_40K = []
temp_40K = []

series_current_4K = []
series_voltage_4K = []
power_resistor_voltage_4K = []
temp_4K = []

source = ka3305p('COM8')
voltmeter = SIM970('GPIB0::4',7)

voltmeter.set_impedance(True,channel=1)
voltmeter.set_impedance(True,channel=2)
voltmeter.set_impedance(True,channel=3)
voltmeter.set_impedance(True,channel=4)


source.set_voltage(channel=1, voltage=set_voltage)
source.set_voltage(channel=2, voltage=set_voltage)
time.sleep(1)

source.set_output(on=True)

#%%

for x in range(3):
    time.sleep(1)
    #40K stage measurements
    series_voltage_40K.append(voltmeter.read_voltage(channel = 1))
    power_resistor_voltage_40K.append(voltmeter.read_voltage(channel = 2))
    series_current_40K.append((set_voltage - series_voltage_40K[x]) / series_resistance)
#        delivered_power_40K.append(series_current_40K*power_resistor_voltage_40K)
    
    #4K stage measurements
    series_voltage_4K.append(voltmeter.read_voltage(channel = 3))
    power_resistor_voltage_4K.append(voltmeter.read_voltage(channel = 4))
    series_current_4K.append((set_voltage - series_voltage_4K[x]) / series_resistance)
#        delivered_power_4K.append(series_current_4K*power_resistor_voltage_4K)
    
    all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
    temp_4K.append(float(all_temps[5]))
    temp_40K.append(float(all_temps[6]))

    
avg_series_current_40K = np.mean(series_current_40K)
avg_series_voltage_40K = np.mean(series_voltage_40K)
avg_power_resistor_voltage_40K = np.mean(power_resistor_voltage_40K)
avg_temp_40K = np.mean(temp_40K)

avg_series_current_4K = np.mean(series_current_4K)
avg_series_voltage_4K = np.mean(series_voltage_4K)
avg_power_resistor_voltage_4K = np.mean(power_resistor_voltage_4K)
avg_temp_4K = np.mean(temp_4K)

avg_power_40K = avg_power_resistor_voltage_40K * avg_series_current_40K
avg_power_4K = avg_power_resistor_voltage_4K * avg_series_current_4K
print("Average Power 40K: ",avg_power_40K," W")
print("Average Power 4K: ",avg_power_4K," W")

source.set_output(on=False)

#%%


with open("heat_map_data.csv", "r", newline='') as output:
    reader = csv.reader(output,delimiter=',')
    count = len(list(reader))
    
now = datetime.datetime.now()
now.strftime("%Y-%m-%d %H:%M")

#%%
data = [count,avg_series_current_40K, avg_series_voltage_40K, avg_power_resistor_voltage_40K, avg_power_40K, avg_temp_40K, avg_series_current_4K, avg_series_voltage_4K, avg_power_resistor_voltage_4K, avg_power_4K, avg_temp_4K,now]
with open("heat_map_data.csv", "a", newline='') as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(data)

#%%
source.close()
