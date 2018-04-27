# -*- coding: utf-8 -*-

"""

Created on Thu Feb  1 10:46:04 2018



@author: anm16

"""



#%% IMPORT PATH NAME for modules

#import sys

#import os

import numpy as np
import math
import matplotlib.pyplot as plt
import time
from itertools import cycle


#snspd_measurement_code_dir = r'C:\Library\Documents\Python Scripts\amcc-measurement'

#dir1 = os.path.join(snspd_measurement_code_dir,'instruments')

#dir2 = os.path.join(snspd_measurement_code_dir,'useful_functions')

#dir3 = os.path.join(snspd_measurement_code_dir,'measurement')

#

#if snspd_measurement_code_dir not in sys.path:

#    sys.path.append(snspd_measurement_code_dir)

#    sys.path.append(dir1)

#    sys.path.append(dir2)

#    sys.path.append(dir3)



#%%import modules



#from instruments.srs_sim970 import SIM970

#from instruments.srs_sim928 import SIM928



from srs_sim928 import SIM928

from srs_sim970 import SIM970



class runTrial(object):

    """docstring for ."""

    def __init__(self, voltage_resistance, count, voltmeter, source1):
        self.voltage_resistance = int(voltage_resistance)
        self.count = count
        self.voltmeter = voltmeter
        self.source1 = source1
        self.setup()
        self.doTest()
        self.finishTest()

    def setup(self):
        self.volt_channel = 1
        self.set_voltage = np.linspace(0,5,self.count)
        #source2 = SIM928('GPIB0::4', 4)
        self.voltmeter.set_impedance(True,self.volt_channel)
        self.source1.set_voltage(voltage = 0)
        #source2.set_voltage(voltage = 0)
        self.volts_read = []
        self.volts_exp = []
        self.output_current = []
        self.resistance = []
        self.unc = []
        self.source1.set_output(True)
        #source2.set_output(True)

    def doTest(self):
        self.source1.set_voltage(0.00)
        time.sleep(1)
        self.source1.set_output(True)
        for ind, volt in enumerate(self.set_voltage):
            self.source1.set_voltage(voltage = volt)
            time.sleep(0.45)
        #    source2.set_voltage(voltage = volt)
            self.volts_read.append(self.voltmeter.read_voltage(self.volt_channel))
            self.output_current.append(volt/self.voltage_resistance)
            self.volts_exp.append(self.output_current[ind] * self.voltage_resistance)
            if self.output_current[ind] != 0:
                self.resistance.append(self.volts_read[ind] / self.output_current[ind])
            self.unc.append(math.sqrt(math.pow(self.volts_read[ind],2)+math.pow(self.volts_exp[ind],2)))
    
        self.source1.set_output(False)

    def plotGraph(self):
        plt.errorbar(self.output_current,self.volts_read,0,0.0001, ecolor='g', capthick=2, fmt = '.', elinewidth=1)
        #plt.plot(output_current, volts_read)
        plt.ylabel("Voltage")
        plt.xlabel("Current")
        plt.title("4 Point Measurement Test")
    
    def getUncertainty(self):
        self.source1.set_output(True)
        self.source1.set_voltage(voltage = 2.53)
        time.sleep(1.5)
        self.readings=[]
        for measurement in range(0,40):
            self.readings.append(voltmeter.read_voltage(self.volt_channel))
            time.sleep(0.3)
           
        self.uncertainty = np.std(self.readings)
        self.source1.set_voltage(voltage = 0.00)
        self.source1.set_output(False)
        return self.uncertainty;
 
    def finishTest(self):
        self.source1.set_voltage(voltage = 0.0)
        #source2.set_voltage(voltage = 0.0)
        self.source1.set_output(False)
        #source2.set_output(False)



    #%% end testing

dataPoints = 10
allData = []
resistances = []
voltmeter = SIM970('GPIB0::9::INSTR',6)
source1 = SIM928('GPIB0::9::INSTR', 1)
uncertainty = 0
first = True

while True:
    nextr = input('Next series Resistance (in Ohms) or type q to quit and make the graph: \n')

    if nextr == 'q':
        break
    else:
        print("Trial Running with R = ",nextr)
        trial = runTrial(nextr, dataPoints, voltmeter, source1)
        allData.append([[x * 100000 for x in trial.output_current],[x * 1000 for x in trial.volts_read]]) #change units to microamps and millivolts
        resistances.append(np.mean(trial.resistance))
        print("Resistance: ",np.mean(trial.resistance))


x = input("Now collect the uncertainty. Wire SIM928 directly into SIM970. Hit enter when ready")
uncertainty = trial.getUncertainty()
first = False

colors = cycle(["aqua", "black", "blue", "fuchsia", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
unccolors = cycle(["lightskyblue","gray","cornflowerblue","palevioletred","darkseagreen","palegreen","lightcoral","slategray","darkkhaki","mediumorchid","indianred","lightgrey","powderblue","palegoldenrod"])
fig = plt.figure()
ax = fig.add_subplot(111)
for i,item in enumerate(allData):
    ax.errorbar(item[0],item[1],uncertainty,uncertainty, label="R= "+str(resistances[i]), color = next(colors), ecolor=next(unccolors), capsize=4, elinewidth=0.3, capthick=0.3)


ax.set_xlabel("Current(μA)", fontsize=12)
ax.set_ylabel("Voltage (mV)", fontsize=12)
ax.set_title("4 Point Measurement", fontsize = 18)
ax.legend(loc="best")
ax.margins(0.1)
fig.tight_layout()

 # plt.savefig("mwe.png")

# plt.errorbar(trials[0].output_current, trials[0].volts_read, 'b')

