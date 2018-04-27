# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:32:12 2018

@author: jlm7
"""

import serial
import time

class ka3305p(object):
    """Python class for Korad KA3305p programmable Voltage/Current Source, written by Jacob Melonis"""
    def __init__(self, comport):
        self.ser = serial.Serial(comport)
        self.ser.timeout = 5 #5 second timeout
        self.sleep_time = 1
        
        
    def close(self):
        self.ser.close()
         
    def set_current(self, channel, current):
        time.sleep(self.sleep_time)
        write_string = 'ISET' + str(channel) + ':' + str(current)
        self.ser.write(write_string.encode())
        
    def set_voltage(self, channel, voltage):
        time.sleep(self.sleep_time)
        write_string = 'VSET' + str(channel) + ':' + str(voltage)
        self.ser.write(write_string.encode())
        
    def set_output(self, on):
        if(on):
            self.ser.write(b'OUT1')
        else:
            self.ser.write(b'OUT0')
        
    def save_settings(self, memory_spot):
        time.sleep(self.sleep_time)
        write_string = 'SAV' + str(memory_spot)
        self.ser.write(write_string.encode())
        
    def recall_settings(self, memory_spot):
        time.sleep(self.sleep_time)
        write_string = 'RCL' + str(memory_spot)
        self.ser.write(write_string.encode())     
        
    def set_over_voltage_protection(self, channel, voltage):
        time.sleep(self.sleep_time)
        write_string = 'OVPSTE' + str(channel) + ':' + str(voltage)
        self.ser.write(write_string.encode())
        
    def set_over_current_protection(self, channel, current):
        time.sleep(self.sleep_time)
        write_string = 'OCPSTE' + str(channel) + ':' + str(current)
        self.ser.write(write_string.encode())
            
    def enable_ovp(self, ovp_on):
        time.sleep(self.sleep_time)
        if(ovp_on):
            self.ser.write(b'OVP1')
        else:
            self.ser.write(b'OVP0')
            
    def enable_ocp(self, ocp_on):
        time.sleep(self.sleep_time)
        if(ocp_on):
            self.ser.write(b'OCP1')
        else:
            self.ser.write(b'OCP0')
            
    def tracking_mode(self, mode):
        time.sleep(self.sleep_time)
        if(mode == 0): #independant mode
            self.ser.write(b'TRACK0')
        elif(mode == 1):#series mode (channel 1 and 2 in series) ch2=master, ch1=slave
            self.ser.write(b'TRACK1')
        elif(mode == 2):#parallel mode (channel 1 and 2 in parallel) ch2=master, ch1=slave
            self.ser.write(b'TRACK2')
            
    def identify(self):
        time.sleep(self.sleep_time)
        write_string = '*IDN?'
        self.ser.write(write_string.encode())
        return(self.ser.read(30).decode('UTF-8'))
        
        #TODO: get rid of the 'b' at the beginning of the returned strings
    def status(self):
        time.sleep(self.sleep_time)
        self.ser.write(b'STATUS?')
        byte = self.ser.read()
        status_object = {'channel1':'', 'channel2':'', 'output':False}
        print(byte)
        if(byte == b'\x00'):
            status_object = {'channel1':'CC', 'channel2':'CC', 'output':False}
        elif (byte == b'\x01'):
            status_object = {'channel1':'CV', 'channel2':'CC', 'output':False}
        elif (byte == b'\x02'):
            status_object = {'channel1':'CC', 'channel2':'CV', 'output':False} 
        elif (byte == b'\x03'):        
            status_object = {'channel1':'CV', 'channel2':'CV', 'output':False}
        elif (byte == b'\xc0'):
            status_object = {'channel1':'CC', 'channel2':'CC', 'output':True}
        elif (byte == b'\xc1'):
            status_object = {'channel1':'CV', 'channel2':'CC', 'output':True}
        elif (byte == b'\xc2'):
            status_object = {'channel1':'CC', 'channel2':'CV', 'output':True}
        elif (byte == b'\xc3'):
            status_object = {'channel1':'CV', 'channel2':'CV', 'output':True}
        return status_object
            
    def enable_beep(self, beep_on):
        time.sleep(self.sleep_time)
        if(beep_on):
            self.ser.write(b'BEEP1')
        else:
            self.ser.write(b'BEEP0')
        
    def read_output_current(self, channel):
        time.sleep(self.sleep_time)
        write_string = 'IOUT' + str(channel) + '?'
        self.ser.write(write_string.encode())
        return float(self.ser.read(5))
    
    def read_output_voltage(self, channel):
        time.sleep(self.sleep_time)
        write_string = 'VOUT' + str(channel) + '?'
        self.ser.write(write_string.encode())
        return float(self.ser.read(5))
    
    def read_set_current(self, channel):
        time.sleep(self.sleep_time)
        write_string = 'ISET' + str(channel) + '?'
        self.ser.write(write_string.encode())
        return float(self.ser.read(5))
        
    def read_set_voltage(self, channel):
        time.sleep(self.sleep_time)
        write_string = 'VSET' + str(channel) + '?'
        self.ser.write(write_string.encode())
        return float(self.ser.read(5))
    
    def lock_control_panel(self, lock):
        time.sleep(self.sleep_time)
        if(lock):
            self.ser.write(b'LOCK1')
        else:
            self.ser.write(b'LOCK0')
        