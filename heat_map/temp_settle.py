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
import datetime



# SEE THIS LINK FOR USEFUL INSTRUCTIONS
# https://qittlab-nuc-01.campus.nist.gov/wordpress/wp-admin/post.php?post=5878&action=edit
#%% INITIALIZATION AND SETUP

#Create objects for the voltage source and voltmeter
source = ka3305p('COM8')
voltmeter = SIM970('GPIB0::4',7)

#Set impedence for the voltmeter channels being used 
voltmeter.set_impedance(True,channel=1)
voltmeter.set_impedance(True,channel=2)
#voltmeter.set_impedance(True,channel=3)
#voltmeter.set_impedance(True,channel=4)
source.set_output(on=False)

#%%Initialize variables with what will be used. 

#******************************************************************************
# NOTE: NOTHING HERE NEEDS TO BE CHANGED. HOWEVER...
#       YOU CAN CHANGE THE POWER DELIVERED TO THE STAGE WITH THE power_wanted VARIABLE HOWEVER IT CAN BE LEFT AT 2
#       YOU CAN ALSO CHANGE THE WAIT TIME BEFORE THE HEATER TURNS ON WITH cur_time HOWEVER IT CAN BE LEFT AT -10 
#       YOU CAN ALSO CHANGE THE run_time VARIABLE WHICH SETS HOW LONG THE TEMPERATURE WILL BE MESAURED FOR
#       YOU CAN ALSO CHANGE THE CHANNEL FOR THE VOLTAGE SOURCE OR VOLTMETER MEASUREMENTS
#       YOU CAN ALSO CHANGE THE VALUE OF THE SERIES RESISTOR ON YOUR CIRCUIT WITH series_resistance
#******************************************************************************

pre_heat_time = 10 #waits this long before turning on the heater. 10 means it waits 10 seconds and then turns on the heater
power_wanted = 2 #this is the watts delivered to the heater
run_time = 10000 #this is the number of seconds the test will run for (note, it will go this long to heat, and this long to cool) total test = 2* runtime
voltage_source_channel = 1 # this is the channel on the voltmeter you plugged the heater resistor into
voltmeter_series_voltage_channel = 1 # this is the voltmeter channel connected to the series resistor (NOT TO THE CRYOSTAT)
voltmeter_resistor_voltage_channel = 2 # this is the voltmeter channel connected to the resistor in the cryostat
series_resistance = 10 # this is the value of the resistor connected in series to the voltage source(should be 10 ohm)

# DON'T CHANGE ANY OF THESE VARIABLES
temp_4K = []
temp_40K = []
series_voltage_40K = []
power_resistor_voltage_40K = []
series_current_40K = []
avg_powers = []
time_array = []
set_voltage = 1.2*math.sqrt(50 * power_wanted)
cur_time = 0

#%% TURN ON THE VOLTAGE SOURCE -> NOTHING NEEDS TO BE CHANGED IN HERE FOR YOUR SETTINGS
time.sleep(2)
source.set_voltage(channel=voltage_source_channel, voltage=round(set_voltage,2))
time.sleep(2)

#%% BEGIN MEASURING TEMP DATA BEFORE THE HEATER TURNS ON -> NOTHING NEEDS TO BE CHANGED IN HERE FOR YOUR SETTINGS

print("Begin Data collection no heat")
start_time = time.time()
# Make a status bar for the user to follow
with tqdm(total=pre_heat_time, unit="s") as pbar:
    cur_time = time.time()
    while (cur_time < start_time + pre_heat_time):
        all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
        temp_4K.append(float(all_temps[5]))
        temp_40K.append(float(all_temps[6]))
        time_array.append(cur_time - start_time)
        prev_time = cur_time
        cur_time = time.time()
        pbar.update(cur_time - prev_time)


    
#%% BEGIN MEAUREING TEMP DATA AFTER THE HEATER TURNS ON -> NOTHING NEEDS TO BE CHANGED IN HERE FOR YOUR SETTINGS
source.set_output(on=True)
print("\n\nBegin heating Loop")
with tqdm(total=run_time, unit="s") as pbar: # CHANGE THIS TO ADJUST TOTAL MEASUREMENT TIME
    cur_time = time.time()
    while (cur_time < start_time + pre_heat_time + run_time):
        all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
        temp_4K.append(float(all_temps[5]))
        temp_40K.append(float(all_temps[6]))
        #this is incremented due to the average run time of each of these loops
        time_array.append(cur_time - start_time)
        series_v_read = voltmeter.read_voltage(channel = voltmeter_series_voltage_channel)
        r_voltage = voltmeter.read_voltage(channel = voltmeter_resistor_voltage_channel)
        s_current = (set_voltage - series_v_read) / series_resistance
        series_voltage_40K.append(series_v_read)
        power_resistor_voltage_40K.append(r_voltage)
        series_current_40K.append(s_current)
        avg_powers.append(s_current * r_voltage)
        prev_time = cur_time
        cur_time = time.time()
        pbar.update(cur_time - prev_time)

    
source.set_output(on=False)
off_time = time.time() - start_time

# Now run the cooling loop
print("\n\nBegin Cooling Loop")
with tqdm(total=run_time, unit="s") as pbar: # CHANGE THIS TO ADJUST TOTAL MEASUREMENT TIME
    cur_time = time.time()
    while (cur_time < off_time + start_time + run_time):
        all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
        temp_4K.append(float(all_temps[5]))
        temp_40K.append(float(all_temps[6]))
        #this is incremented due to the average run time of each of these loops
        time_array.append(cur_time - start_time)
        series_v_read = voltmeter.read_voltage(channel = voltmeter_series_voltage_channel)
        r_voltage = voltmeter.read_voltage(channel = voltmeter_resistor_voltage_channel)
        s_current = (set_voltage - series_v_read) / series_resistance
        series_voltage_40K.append(series_v_read)
        power_resistor_voltage_40K.append(r_voltage)
        series_current_40K.append(s_current)
        avg_powers.append(s_current * r_voltage)
        prev_time = cur_time
        cur_time = time.time()
        pbar.update(cur_time - prev_time)

#%% CREATE THE GRAPH WHICH WILL SHOW THE TEMPEREATURE DATA vs TIME -> MAKE SURE TO CHANGE THE GRAPH LABEL DEPENDING ON WHERE THE POWER WAS APPLIED
#*****************************************************************************
# NOTE:
#       CHANGE THE TITLE TO CORRESPOND TO WHERE THE POWER WAS APPLIED
#       DONT CHANGE THE Y LABELS

#*****************************************************************************

print("Avg Power: ", np.mean(avg_powers))
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(time_array, temp_4K, '-ro')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Temperature in 4K(K)",color='r')
ax1.set_title("Temperature Applied in 40K")
ax2.plot(time_array, temp_40K, '-bo')
plt.axvline(x = off_time, color='k', linestyle='--')
plt.text(off_time+1, 4.5, "Power Off", rotation=90)
ax2.set_ylabel("Temperature in 40K(K)", color='b')
ax1.legend(loc="best")
ax1.margins(0.1)
fig.tight_layout()
now = datetime.datetime.now()
string = "images/" + now.strftime("%Y-%m-%d-%H-%M") + ".png"
plt.savefig(string)

source.close()