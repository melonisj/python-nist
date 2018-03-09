# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:02:07 2018

@author: jlm7
"""

from __future__ import division, print_function, absolute_import
import numpy as np


from phidl import Device, Layer, quickplot, make_device
import phidl.geometry as pg
import phidl.routing as pr

via_height = 1.5
via_width = 1.5
wire_height = 1
wire_width = 5
overlap = 1
pad_height = 10
pad_width = 5
wg = []
v = []


def waveguide(width = 10, height = 1, layer=3):
    WG = Device('waveguide')
    WG.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)], layer=layer)
    WG.add_port(name = 'wgport1', midpoint = [0,height/2], width = height, orientation = 180)
    WG.add_port(name = 'wgport2', midpoint = [width,height/2], width = height, orientation = 0)
    return WG

def make_pad(height, width):
    p = Device('Pad')
    p.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)])
    p.add_port(name = 'padport1', midpoint = [0,wire_height/2], width = wire_height, orientation = 180)
    p.add_port(name = 'padport2', midpoint = [width,height-wire_height/2], width = wire_height, orientation = 0)
    return p

def via(width = 2, height = 2):
    WG = Device('via')
    WG.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)], layer=5 )
    WG.add_port(name = 'viaport1', midpoint = [0,height/2], width = height, orientation = 180)
    WG.add_port(name = 'viaport2', midpoint = [width,height/2], width = height, orientation = 0)
    return WG

def iterate_make_row(count = 2):
        for x in range(0,count):
            if(x % 2 == 0):
                wg.append(E.add_ref(waveguide(width=wire_width, height = wire_height, layer=3)))
            else:
                wg.append(E.add_ref(waveguide(width=wire_width, height = wire_height, layer=4)))
            if(x > 0):
                v.append(E.add_ref(via(width=via_width, height=via_height)))

        
def connect_row_l2r(start = 0, end = 6):
    for x in range(start,end):
        if(x > 0):
            wg[x].connect(port = 'wgport1', destination = wg[x-1].ports['wgport2'], overlap = overlap)
            v[x-1].connect(port = 'viaport1', destination = wg[x-1].ports['wgport2'], overlap = overlap+((via_width-overlap)/2))
            
def connect_row_r2l(start = 0, end = 6):
    for x in range(start,end):
        if(x > 0):
            wg[x].connect(port = 'wgport2', destination = wg[x-1].ports['wgport1'], overlap = overlap)
            v[x-1].connect(port = 'viaport2', destination = wg[x-1].ports['wgport1'], overlap = overlap+((via_width-overlap)/2))
        

#D = Device('Via Path')
E = Device('Via Path Loop')

##Create Layers
top = Layer(name = 'top', gds_layer = 3, gds_datatype = 0,
                 description = 'Top layer copper', color="red")
bottom = Layer(name = 'bottom', gds_layer = 4, gds_datatype = 0,
                 description = 'bottom layer copper', color="blue")
vias = Layer(name = 'vias', gds_layer = 5, gds_datatype = 0,
                 description = 'vias', color = "green")
    

w1 = waveguide(5,1,3)
w2 = waveguide(4,1,3)
W1 = E.add_ref(w1)
W2 = E.add_ref(w2)
W1.connect(port = 'wgport1', destination = W2.ports['wgport2'])

##Create Objects
#
#wg1 = D.add_ref(waveguide(width=wire_width, height = wire_height, layer=3))
#wg2 = D.add_ref(waveguide(width=wire_width, height = wire_height, layer=4))
#wg3 = D.add_ref(waveguide(width=wire_width, height = wire_height, layer=3))
#
#v1 = D.add_ref(via(width=via_width, height=via_height))
#v2 = D.add_ref(via(width=via_width, height=via_height))
#
##Position Objects
#
##Connect Objects
#wg2.connect(port = 'wgport1', destination = wg1.ports['wgport2'], overlap = overlap)
#v1.connect(port = 'viaport1', destination = wg1.ports['wgport2'], overlap = overlap+((via_width-overlap)/2))
#
#wg3.connect(port = 'wgport1', destination = wg2.ports['wgport2'], overlap = overlap)
#v2.connect(port = 'viaport1', destination = wg2.ports['wgport2'], overlap = overlap+((via_width-overlap)/2))
#
##Plot Objects
#quickplot(D)

#iterate_make_row(6)
#connect_row_l2r(0,6)
quickplot(E)