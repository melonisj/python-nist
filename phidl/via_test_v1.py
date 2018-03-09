# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:40:06 2018

@author: jlm7
"""

from __future__ import division, print_function, absolute_import
import numpy as np


from phidl import Device, Layer, quickplot, make_device
import phidl.geometry as pg
import phidl.routing as pr

def test_via_chain(num_vias, num_rows, via_spacing, via_size, wire_width, layer_wiring1, layer_wiring2, layer_via, pad_size):
    print ("hello")
    total_width = 1000
    total_height = 1000
    usable_width = total_width-pad_size[0]
    usable_height = pad_size[1]
    edge_threshold = 5
    wire_length = (usable_width-2*edge_threshold)*num_rows + 2*edge_threshold
    

    #begin by assuming there will be a divisible number of rows
    vias_per_row = num_vias/num_rows
    if(via_spacing == None):
        #calculate via spacing
        
        
    if(via_spacing/2 <= via_size):
        print("vias too big")
        #throw error
    
    if(vias_per_row * via_spacing > usable_width):
        print("too wide")
        #Throw error
