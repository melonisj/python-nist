# -*- coding: utf-8 -*-

"""

Created on Tue Feb  6 14:59:51 2018



@author: jlm7

"""



import numpy as np

import math

import matplotlib.pyplot as plt

import time



from srs_sim928 import SIM928

from srs_sim970 import SIM970



volt_channel = 1

volts_read = []

times = []

volts_read_high = []

times_high = []

voltmeter = SIM970('GPIB0::4',7)

source1 = SIM928('GPIB0::4', 1)

source1.set_output(False)





voltmeter.set_impedance(True,volt_channel)

source1.set_voltage(voltage = 2.23)



source1.set_output(True)



for x in range(0,50):

    volts_read.append(voltmeter.read_voltage(volt_channel))

    times.append(0.001*x)

    time.sleep(0.001)





source1.set_voltage(voltage = 0.0)

time.sleep(5)

source1.set_voltage(voltage = 4.117)

for x in range(0,50):

    volts_read_high.append(voltmeter.read_voltage(volt_channel))

    times_high.append(0.001*x)

    time.sleep(0.001)





plt.plot(times, volts_read,'r', times_high,volts_read_high,'b')
plt.xlabel("Time (s)")
plt.ylabel("Measured Voltage")



source1.set_output(False)

