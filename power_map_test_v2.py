# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 13:37:30 2018

@author: jlm7
"""

from ka3305p import ka3305p
from srs_sim970 import SIM970
import numpy as np
import time
import csv
import client
import datetime
import math
import matplotlib.pyplot as plt
#%%
# Expected Paramters
# set_voltage    : 1 V    |3 V     |4.3 V    |6 V    | 8.5 V  | 12 V   | 14.7 V  | 17 V   | 19 V   | 20.8 V  |
# expected_power : 0.01 V |0.125W  |0.25 V   | 0.5 W | 1 W    | 2 W    | 3 W     | 4 W    | 5 W    | 6 W     |
#
#
#%%

class power_meas(object):
    def __init__(self, voltage_source, voltmeter,series_resistance,csv_file_name):
        self.source = voltage_source
        self.voltmeter = voltmeter
        self.series_resistance = series_resistance # this should be 10 ohm
        self.csv_file_name = csv_file_name
        self.setup()
    
    def setup(self):

        self.voltmeter.set_impedance(True,channel=1)
        self.voltmeter.set_impedance(True,channel=2)
        self.voltmeter.set_impedance(True,channel=3)
        self.voltmeter.set_impedance(True,channel=4)
        
        self.powers_40K_array = []
        self.powers_4K_array = []
        self.temps_40K_array = []
        self.temps_4K_array = []
        
        self.powers_40K_set = []
        self.powers_4K_set = []
        
    def run_sample(self, power_40K, power_4K):
        #Setup
        set_voltage_40K = 1.2*math.sqrt(50 * power_40K)
        set_voltage_4K = 1.2*math.sqrt(50 * power_4K)
        
        series_current_40K = []
        series_voltage_40K = []
        power_resistor_voltage_40K = []
        temp_40K = []
        
        series_current_4K = []
        series_voltage_4K = []
        power_resistor_voltage_4K = []
        temp_4K = []

        self.source.set_voltage(channel=1, voltage=round(set_voltage_40K,2))
#        time.sleep(1)
        self.source.set_voltage(channel=2, voltage=round(set_voltage_4K,2))
        
#        time.sleep(1)
        

        self.source.set_output(on=True)
        #Run a few samples and average each
        for x in range(3):
            time.sleep(1)
            #40K stage measurements
            series_voltage_40K.append(voltmeter.read_voltage(channel = 1))
            power_resistor_voltage_40K.append(voltmeter.read_voltage(channel = 2))
            series_current_40K.append((set_voltage_40K - series_voltage_40K[x]) / self.series_resistance)
        #        delivered_power_40K.append(series_current_40K*power_resistor_voltage_40K)
            
            #4K stage measurements
            series_voltage_4K.append(voltmeter.read_voltage(channel = 3))
            power_resistor_voltage_4K.append(voltmeter.read_voltage(channel = 4))
            series_current_4K.append((set_voltage_4K - series_voltage_4K[x]) / self.series_resistance)
        #        delivered_power_4K.append(series_current_4K*power_resistor_voltage_4K)
#            time.sleep(5)
            all_temps = client.client('132.163.53.67',50326,'getall').decode('ascii').split(',')
            temp_4K.append(float(all_temps[5]))
            temp_40K.append(float(all_temps[6]))
            
        #Collect Average values
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
        
        source.set_output(on = False)
        
        #Save important variables for graph making
        self.powers_40K_array.append(avg_power_40K)
        self.powers_4K_array.append(avg_power_4K)
        self.temps_40K_array.append(avg_temp_40K)
        self.temps_4K_array.append(avg_temp_4K)
        self.powers_40K_set.append(power_40K)
        self.powers_4K_set.append(power_4K)
        
        
        #Save all data to CSV
        self.data_to_csv(avg_series_current_40K, avg_series_voltage_40K, avg_power_resistor_voltage_40K, avg_temp_40K, avg_power_40K, avg_series_current_4K, avg_series_voltage_4K, avg_power_resistor_voltage_4K, avg_temp_4K, avg_power_4K)

    def data_to_csv(self, series_I_40K, series_V_40K, p_resistor_V_40K, temp_40K, power_40K, series_I_4K, series_V_4K, p_resistor_V_4K, temp_4K, power_4K):
        with open("heat_map_data.csv", "r", newline='') as output:
            reader = csv.reader(output,delimiter=',')
            count = len(list(reader))
            
        now = datetime.datetime.now()
        now.strftime("%Y-%m-%d %H:%M")
        
        #%%
        data = [count,series_I_40K, series_V_40K, p_resistor_V_40K, power_40K, temp_40K, series_I_4K, series_V_4K, p_resistor_V_4K, power_4K, temp_4K,now]
        with open(self.csv_file_name, "a", newline='') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(data)
            
    def create_graph(self, rows, cols):
        print(rows, cols)
        fig = plt.figure()
        power_string = []
#        width_4K = len(self.powers_4K_array)
#        print(width_4K)
#        powers_40K_overlay = []
#        powers_4K_overlay = []
#        for i, x in enumerate(self.powers_4K_array):
#            powers_40K_overlay.append(self.temps_40K_array[rows*i%(width_4K-1)])
#            powers_4K_overlay.append(self.temps_4K_array[rows*i%(width_4K-1)])
#        
        for i, x in enumerate(self.powers_40K_array):
            power_string.append(str(round(self.powers_4K_set[i],2)) + ", " + str(round(self.powers_40K_set[i],2)))
        ax1 = fig.add_subplot(111)
#        ax2 = fig.add_subplot(111)
        ax1.plot(self.temps_40K_array, self.temps_4K_array, '-ro')
        ax1.set_xlabel('Temp in 40K Stage')
        ax1.set_ylabel('Temp in 4K Stage')
        ax1.set_title('Heat Map')
        
        for i, txt in enumerate(power_string):
            ax1.annotate(txt, (self.temps_40K_array[i],self.temps_4K_array[i]))
#        ax2.plot(powers_40K_overlay, powers_4K_overlay, '-b')

        fig.show()
        
    def test_source(self, voltage):
        self.source.set_voltage(channel=1, voltage=voltage)
        time.sleep(0.01)
        self.source.set_voltage(channel=2, voltage=voltage)
        
if(__name__ == "__main__"):
    source = ka3305p('COM8')
    voltmeter = SIM970('GPIB0::4',7)
    heat_map = power_meas(voltage_source = source, voltmeter = voltmeter, series_resistance = 10, csv_file_name = "heat_map_data.csv")
    powers_in_4K = [0.25,0.5]
    powers_in_40K = [0.25,0.5]
    
    for power40 in powers_in_40K:
        for power4 in powers_in_4K:
            heat_map.run_sample(power40, power4)
#    heat_map.test_source(7.32)
    heat_map.create_graph(rows = len(powers_in_40K), cols = len(powers_in_4K))
    source.close()