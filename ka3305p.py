# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:32:12 2018

@author: jlm7
"""

import serial

class ka3305p(object):
    """Python class for Korad KA3305p programmable Voltage/Current Source, written by Jacob Melonis"""
    def __init__(self, comport):
        self.ser = serial.Serial(comport)
        self.ser.timeout = 5 #5 second timeout
        
        
    def close(self):
        self.ser.close()
         
    def set_current(self, current, channel):
        write_string = 'ISET' + str(channel) + ':' + str(current)
        self.ser.write(write_string.encode())
        
    def set_voltage(self, voltage, channel):
        write_string = 'VSET' + str(channel) + ':' + str(voltage)
        self.ser.write(write_string.encode())
        
    def set_output(self, on):
        if(on):
            self.ser.write(b'OUT1')
        else:
            self.ser.write(b'OUT0')
        
    def save_settings(self, memory_spot):
        write_string = 'SAV' + str(memory_spot)
        self.ser.write(write_string.encode())
        
    def recall_settings(self, memory_spot):
        write_string = 'RCL' + str(memory_spot)
        self.ser.write(write_string.encode())     
        
    def set_over_voltage_protection(self, channel, voltage):
        write_string = 'OVPSTE' + str(channel) + ':' + str(voltage)
        self.ser.write(write_string.encode())
        
    def set_over_current_protection(self, channel, current):
        write_string = 'OCPSTE' + str(channel) + ':' + str(current)
        self.ser.write(write_string.encode())
            
    def enable_ovp(self, ovp_on):
        if(ovp_on):
            self.ser.write(b'OVP1')
        else:
            self.ser.write(b'OVP0')
            
    def enable_ocp(self, ocp_on):
        
        if(ocp_on):
            self.ser.write(b'OCP1')
        else:
            self.ser.write(b'OCP0')
            
    def tracking_mode(self, mode):
        if(mode == 0): #independant mode
            self.ser.write(b'TRACK0')
        elif(mode == 1):#ser mode
            self.ser.write(b'TRACK1')
        elif(mode == 2):#para mode
            self.ser.write(b'TRACK2')
            
    def identify(self):
        self.ser.write(b'*IDN?')
        return(self.ser.read(30))
        
        #TODO: get rid of the 'b' at the beginning of the returned strings
    def status(self):
        self.ser.write(b'STATUS?')
        byte = self.ser.read()
        status_object = {'channel1':'', 'channel2':'', 'output':False}
        print(byte)
        if(byte == '\x00'):
            status_object = {'channel1':'CC', 'channel2':'CC', 'output':False}
        elif (byte == '\x01'):
            status_object = {'channel1':'CV', 'channel2':'CC', 'output':False}
        elif (byte == '\x02'):
            status_object = {'channel1':'CC', 'channel2':'CV', 'output':False} 
        elif (byte == '\x03'):        
            status_object = {'channel1':'CV', 'channel2':'CV', 'output':False}
        elif (byte == '\x40'):
            status_object = {'channel1':'CC', 'channel2':'CC', 'output':True}
        elif (byte == '\x41'):
            status_object = {'channel1':'CV', 'channel2':'CC', 'output':True}
        elif (byte == '\x42'):
            status_object = {'channel1':'CC', 'channel2':'CV', 'output':True}
        elif (byte == '\x43'):
            status_object = {'channel1':'CV', 'channel2':'CV', 'output':True}
        return status_object
            
    def enable_beep(self, beep_on):
        if(beep_on):
            self.ser.write(b'BEEP1')
        else:
            self.ser.write(b'BEEP0')
        
    def read_output_current(self, channel):
        write_string = 'IOUT' + str(channel) + '?'
        self.ser.write(write_string.encode())
        return float(self.ser.read(5))
    
    def read_output_voltage(self, channel):
        write_string = 'VOUT' + str(channel) + '?'
        self.ser.write(write_string.encode())
        return float(self.ser.read(5))
    
    def read_set_current(self, channel):
        write_string = 'ISET' + str(channel) + '?'
        self.ser.write(write_string.encode())
        return float(self.ser.read(5))
        
    def read_set_voltage(self, channel):
        write_string = 'VSET' + str(channel) + '?'
        self.ser.write(write_string.encode())
        return float(self.ser.read(5))
        