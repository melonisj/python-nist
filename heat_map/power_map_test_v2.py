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
from tqdm import tqdm
#%%
# Expected Paramters
# set_voltage    : 1 V    |3 V     |4.3 V    |6 V    | 8.5 V  | 12 V   | 14.7 V  | 17 V   | 19 V   | 20.8 V  |
# expected_power : 0.01 V |0.125W  |0.25 V   | 0.5 W | 1 W    | 2 W    | 3 W     | 4 W    | 5 W    | 6 W     |
#
#
#%%

# SEE THIS LINK FOR USEFUL INSRUCTIONS
#https://qittlab-nuc-01.campus.nist.gov/wordpress/wp-admin/post.php?post=5878&action=edit

class power_meas(object):
    """
        This function allows heat map measurement to be made in Adam's Cryostat. 
        Things you may want to change:
            
        
        
        
        To set up object:
            Need to supply:
                Voltage Source object from ka3305p
                voltmeter object from srs_sim970
                resistance of series resistor next to voltage source (10 Ohms)
                CSV file name to save data to.
        
        To run a sample:
            Need to supply 2 arrays of equal size: 
                one array for the requested Power (in watts) in the 40K stage,
                one array for the requested Power (in watts) in the 4K stage.
            Also need to tell whether or not the 40K value changed since the last measurement
        
        See example at bottom of this file for how all of these work. 
    """
    def __init__(self, voltage_source, voltmeter,series_resistance,csv_file_name):
        """
        This function simply creates the object and calls the setup function to initialize the variables
        
        Nothing should need to be changed in here to run the file with your settings.
        """
        self.source = voltage_source
        self.voltmeter = voltmeter
        self.series_resistance = series_resistance # this should be 10 ohm
        self.csv_file_name = csv_file_name
        self.setup()
    
    def setup(self):
        """
        This function creates the variables that will be used and establishes
        which voltmeter channels will be used.
        
        Nothing should need to be changed in here to run the file with your settings.
        """
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
    
    def test_source(self, voltage):
        """
        This function is just for testing. It will just turn the voltage source
        on and off to see if a delay is necessary. If the source does not turn on
        and off, try increasing the time.sleep delay.
        
        This function does not automatically run. To run it, uncomment it in the 
        __main__ section below.
        """
        self.source.set_voltage(channel=1, voltage=voltage)
        time.sleep(0.01)
        self.source.set_voltage(channel=2, voltage=voltage)
        
        
    def data_to_csv(self, series_I_40K, series_V_40K, p_resistor_V_40K, temp_40K, power_40K, series_I_4K, series_V_4K, p_resistor_V_4K, temp_4K, power_4K):
        """
        This function simply saves all the data in a long table format to the file 
        specified when the init function was called. 
        
        Nothing should need to be changed in here to run the file with your settings.
        """
        with open("heat_map_data.csv", "r", newline='') as output:
            reader = csv.reader(output,delimiter=',')
            count = len(list(reader))
            
        now = datetime.datetime.now()
        datenow = now.strftime("%Y-%m-%d %H:%M")
        
        #%%
        data = [count,series_I_40K, series_V_40K, p_resistor_V_40K, power_40K, temp_40K, series_I_4K, series_V_4K, p_resistor_V_4K, power_4K, temp_4K,datenow]
        with open(self.csv_file_name, "a", newline='') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(data)
    
    
    def graph_helper(self, seq, num):
        """
        This function just reorders some of the data for the graph so that the 
        heat map graph has an actaul mesh look to it instead of just a bunch 
        of disconnected lines.
        
        Nothing should need to be changed in here to run the file with your settings.
        """
        avg = len(seq) / float(num)
        out = []
        last = 0.0
    
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
    
        return out
            
    def make_graph(self,rows,cols):
        """
        This function will take the data generated from the measurements and make 
        a graph. It uses the graph helper function to actaully make a mesh appearance
        for the heat map.
        
        Nothing should need to changed in here to run the file with your settings.
        """
        temp_40K_col = self.graph_helper(self.temps_40K_array, cols)
        temp_4K_col = self.graph_helper(self.temps_4K_array, cols)
        
        width_4K = len(self.temps_4K_array)
        temps_40K_overlay = []
        temps_4K_overlay = []
        for i, x in enumerate(self.temps_4K_array):
            temps_40K_overlay.append(self.temps_40K_array[rows*i%(width_4K-1)])
            temps_4K_overlay.append(self.temps_4K_array[rows*i%(width_4K-1)])
        temps_4K_overlay[len(temps_4K_overlay)-1] = self.temps_4K_array[len(self.temps_4K_array)-1]
        temps_40K_overlay[len(temps_40K_overlay)-1] = self.temps_40K_array[len(self.temps_40K_array)-1]
        
        temp_40K_row = self.graph_helper(temps_40K_overlay, rows)
        temp_4K_row = self.graph_helper(temps_4K_overlay, rows)
        
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        for i, x in enumerate(temp_40K_col):
            ax1.plot(temp_40K_col[i], temp_4K_col[i], '-r')
        for i, x in enumerate(temp_40K_row):
            ax1.plot(temp_40K_row[i], temp_4K_row[i], '-b')
        ax1.set_xlabel('Temp in 40K Stage')
        ax1.set_ylabel('Temp in 4K Stage')
        ax1.set_title('Heat Map')
        
        power_string= []
        for i, x in enumerate(self.powers_40K_array):
                power_string.append(str(round(self.powers_4K_set[i],2)) + ", " + str(round(self.powers_4K_set[i],2)))
        for i, txt in enumerate(power_string):
            ax1.annotate(txt, (self.temps_40K_array[i],self.temps_4K_array[i]))
        fig.show()
        now = datetime.datetime.now()
        datenowstring = now.strftime("%Y-%m-%d %H:%M")
        string = "heatmap" + datenowstring + ".png"
        plt.savefig(string)
        
            
    def run_sample(self, power_40K, power_4K,new_40K , settling_time_4K = 500, settling_time_40K = 5000):
        """
        THIS IS WHERE THE TEST IS ACTAULLY RUN!
        This function uses some of the helper functions above to create a heat 
        map for the cryostat.
        Each time this runs, 1 data point will be collected and saved but the 
        graph is not automatically generated. See the example in the __main__ 
        section for usage.
        
        Nothing should need to changed in here to run the file with your settings.
        """
        #Setup (DON'T NEED TO CHANGE ANYTHING HERE)
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
        time.sleep(3)

        # Set the voltage source to the given voltage to get the requested power
        source.clear_serial_buffer()
        self.source.set_voltage(channel=1, voltage=round(set_voltage_40K,2))
        time.sleep(3)
        source.clear_serial_buffer()
        self.source.set_voltage(channel=2, voltage=round(set_voltage_4K,2))
        time.sleep(3)
        source.clear_serial_buffer()
        self.source.set_output(on=True)
        time.sleep(3)
        
        #Give it time for the temperature to settle
        if(new_40K):
            print("\nTemperature Settling...please wait")
            for wait_var in range(settling_time_40K): #wait time in 40K stage 
                time.sleep(1)
        else:
            print("\nTemperature Settling...please wait")
            for wait_var in range(settling_time_4K): #wait time in 4K stage
                time.sleep(1)


        #Run a few samples and average each
        for x in range(5):
            time.sleep(1)
            #40K stage measurements
            series_voltage_40K.append(voltmeter.read_voltage(channel = 1))
            power_resistor_voltage_40K.append(voltmeter.read_voltage(channel = 2))
            series_current_40K.append((set_voltage_40K - series_voltage_40K[x]) / self.series_resistance)
            
            #4K stage measurements
            series_voltage_4K.append(voltmeter.read_voltage(channel = 3))
            power_resistor_voltage_4K.append(voltmeter.read_voltage(channel = 4))
            series_current_4K.append((set_voltage_4K - series_voltage_4K[x]) / self.series_resistance)
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


#////////////////////////
#   EXAMPLE USAGE      //
#////////////////////////
    
                
if(__name__ == "__main__"):
    # Step 0: create the voltage source and voltmeter objects
    source = ka3305p('COM8')
    voltmeter = SIM970('GPIB0::4',7)
    # Step 1: create the heat_map_testing object
    heat_map = power_meas(voltage_source = source, voltmeter = voltmeter, series_resistance = 10, csv_file_name = "heat_map_data.csv")
    # Step 2: define the requested powers you want measured (these are in watts)
    # CHANGE THESE VALUES TO GET WHAT YOU WANT MEASURED. MAX IS ~12.5 W
    powers_in_4K = [0,0.5,1,2,3,4,5,6]
    powers_in_40K = [0,0.5,1,2,3,4,5,6]
    # Step 3: create a loop to run through those arrays and take a sample for each one
    for k in range(0,3):
        for i in tqdm(range(len(powers_in_40K)),desc="40 K Temp Status"):
            # Each time the 40K value is changed we must wait a long time. Set new_40K to true when this happens
            new_40K = True
            for j in tqdm(range(len(powers_in_4K)),desc="4 K Temp Status"):
                print("\n\n===================================\nHeating 40K with ", powers_in_40K[i], " W\nHeating 4K with  ",powers_in_4K[j]," W\n===================================")
                heat_map.run_sample(powers_in_40K[i], powers_in_4K[j], new_40K)
                new_40K = False
        if(k!=4):
            time.sleep(3600)
     
#    heat_map.test_source(7.32)
    # Step 4: Make a graph
    heat_map.make_graph(rows = len(powers_in_40K), cols = len(powers_in_4K))
    source.close()
    
    
    
    
    

    
    
#%% BELOW HERE IS THE CODE GRAVEYARD. THESE LINES OF CODE ONCE HAD A PURPOSE BUT 
#   AS TIME WORE ON, THEY REFUSED TO CHANGE AND SOON BECAME OBSOLETE. ALL THAT IS
#   LEFT OF THEM IS THIS TRIBUTE (IN CASE SOMETHING ELSE GOES WRONG)
#    
#    
#    
#      ,-=-.       ,-=-.      ,-=-.      ,-=-.      ,-=-. 
#     |  +  \     |  +  \    |  +  \    |  +  \    |  +  \   
#     | ~~~ |     | ~~~ |    | ~~~ |    | ~~~ |    | ~~~ | 
#     |R.I.P|     |R.I.P|    |R.I.P|    |R.I.P|    |R.I.P|
#     |_____|     |_____|    |_____|    |_____|    |_____|
##    
#    
#    
    
#    def create_graph(self, rows, cols):
#        print(rows, cols)
#        fig = plt.figure()
#        power_string = []
##        width_4K = len(self.powers_4K_array)
##        print(width_4K)
##        powers_40K_overlay = []
##        powers_4K_overlay = []
##        for i, x in enumerate(self.powers_4K_array):
##            powers_40K_overlay.append(self.temps_40K_array[rows*i%(width_4K-1)])
##            powers_4K_overlay.append(self.temps_4K_array[rows*i%(width_4K-1)])
##        
#        for i, x in enumerate(self.powers_40K_array):
#            power_string.append(str(round(self.powers_4K_set[i],2)) + ", " + str(round(self.powers_40K_set[i],2)))
#        ax1 = fig.add_subplot(111)
##        ax2 = fig.add_subplot(111)
#        ax1.plot(self.temps_40K_array, self.temps_4K_array, '-ro')
#        ax1.set_xlabel('Temp in 40K Stage')
#        ax1.set_ylabel('Temp in 4K Stage')
#        ax1.set_title('Heat Map')
#        
#        for i, txt in enumerate(power_string):
#            ax1.annotate(txt, (self.temps_40K_array[i],self.temps_4K_array[i]))
##        ax2.plot(powers_40K_overlay, powers_4K_overlay, '-b')
#
#        fig.show()
#        plt.savefig('heatmap_test6.png')