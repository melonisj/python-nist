# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 12:47:16 2018

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
pad_height = 17
pad_width = 4
top_layer = 3
bottom_layer = 4
vias_per_row = 7


def waveguide(width = 10, height = 1, layer=3):
    WG = Device('waveguide')
    WG.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)], layer=layer)
    WG.add_port(name = 'wgport1', midpoint = [0,height/2], width = height, orientation = 180)
    WG.add_port(name = 'wgport2', midpoint = [width,height/2], width = height, orientation = 0)
    return WG


def make_pad(height, width,layer):
    p = Device('Pad')
    p.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)], layer=layer)
    p.add_port(name = 1, midpoint = [0,wire_height/2], width = wire_height, orientation = 180)
    return p


def via(width = 2, height = 2):
    WG = Device('via')
    WG.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)], layer=5 )
    WG.add_port(name = 'viaport1', midpoint = [0,height/2], width = height, orientation = 180)
    WG.add_port(name = 'viaport2', midpoint = [width,height/2], width = height, orientation = 0)
    return WG


    
def iterate_make_row(count = 2):
    ROW = Device('Row')
    wg = []
    v = []
    for x in range(count):
        if(x % 2 == 0):
            wg.append(ROW.add_ref(waveguide(width=wire_width, height = wire_height, layer=bottom_layer)))
        else:
            wg.append(ROW.add_ref(waveguide(width=wire_width, height = wire_height, layer=top_layer)))
        if(x > 0):
            v.append(ROW.add_ref(via(width=via_width, height=via_height)))
            wg[x].connect(port = 'wgport1', destination = wg[x-1].ports['wgport2'], overlap = overlap)
            v[x-1].connect(port = 'viaport1', destination = wg[x-1].ports['wgport2'], overlap = overlap+((via_width-overlap)/2))
    ROW.add_port(name = 1, port = wg[0].ports['wgport1'])
    ROW.add_port(name = 2, port = wg[x].ports['wgport2'])

    return ROW
        
            
def make_corner(top = True):
    CT = Device('Corner Top')
    via1 = via(width=via_width, height=via_height)
    via2 = via(width=via_width, height=via_height)
    VIA1 = CT.add_ref(via1).rotate(90)
    VIA2 = CT.add_ref(via2).rotate(90)
    if(top):
        wire = waveguide(width=wire_width, height = wire_height, layer=3)
    else:
        wire = waveguide(width=wire_width, height = wire_height, layer=4)
    WIRE = CT.add_ref(wire)
    VIA1.connect(port = 'viaport1', destination = WIRE.ports['wgport2'], overlap = overlap+((via_width-overlap)/2))
    VIA2.connect(port = 'viaport2', destination = WIRE.ports['wgport1'], overlap = overlap+((via_width-overlap)/2))
    VIA2.rotate(90).movex(overlap)
    VIA1.rotate(270, (wire_width-overlap,0)).movey(overlap)
    CT.add_port(name = 1, port = VIA1.ports['viaport2'])
    CT.add_port(name = 2, port = VIA2.ports['viaport1'])
    return CT
            
            
            
#
#    v[lenwg-2].rotate(90)
#    v[lenwg-1].rotate(90)

def make_end(top = True, add_via = True):
    END = Device('Head/Tail')
    
    if(top):
        wire = waveguide(width=wire_width, height = wire_height, layer=3)
    else:
        wire = waveguide(width=wire_width, height = wire_height, layer=4)
    WIRE = END.add_ref(wire)
    if(add_via != True):
        via1 = via(width=via_width, height=via_height)
        VIA1 = END.add_ref(via1)    
        VIA1.connect(port = 'viaport2', destination = WIRE.ports['wgport1'], overlap = overlap+((via_width-overlap)/2))
        END.add_port(port = VIA1.ports['viaport1'], name = 1)
    else:
        END.add_port(port = WIRE.ports['wgport1'], name = 1)


    END.add_port(port = WIRE.ports['wgport2'], name = 2)
    return END

      
#D = Device('Via Path')
E = Device('Via Path Loop')


##Create Layers
top = Layer(name = 'top', gds_layer = 3, gds_datatype = 0,
                 description = 'Top layer copper', color="red")
bottom = Layer(name = 'bottom', gds_layer = 4, gds_datatype = 0,
                 description = 'bottom layer copper', color="blue")
vias = Layer(name = 'vias', gds_layer = 5, gds_datatype = 0,
                 description = 'Top layer copper', color="green")
 

PAD1 = E.add_ref(make_pad(pad_height,pad_width,3))
HEAD = E.add_ref(make_end(True,False))
HEAD.connect(port = 2, destination = PAD1.ports[1])

ROW1 = E.add_ref(iterate_make_row(vias_per_row))
ROW1.connect(port = 1, destination = HEAD.ports[1],overlap = overlap+((via_width-overlap)/2))
COR1 = E.add_ref(make_corner(True))
COR1.connect(port = 2, destination=ROW1.ports[2],overlap = overlap+((via_width-overlap)/2))

ROW2 = E.add_ref(iterate_make_row(vias_per_row))
ROW2.connect(port = 2, destination = COR1.ports[1],overlap = overlap+((via_width-overlap)/2))
COR2 = E.add_ref(make_corner(False))
COR2.connect(port = 1, destination=ROW2.ports[1],overlap = overlap+((via_width-overlap)/2))

ROW3 = E.add_ref(iterate_make_row(vias_per_row))
ROW3.connect(port = 1, destination = COR2.ports[2],overlap = overlap+((via_width-overlap)/2))
COR3 = E.add_ref(make_corner(True))
COR3.connect(port = 2, destination=ROW3.ports[2],overlap = overlap+((via_width-overlap)/2))

ROW4 = E.add_ref(iterate_make_row(vias_per_row))
ROW4.connect(port = 2, destination = COR3.ports[1],overlap = overlap+((via_width-overlap)/2))
COR4 = E.add_ref(make_corner(False))
COR4.connect(port = 1, destination=ROW4.ports[1],overlap = overlap+((via_width-overlap)/2))

ROW5 = E.add_ref(iterate_make_row(vias_per_row))
ROW5.connect(port = 1, destination = COR4.ports[2],overlap = overlap+((via_width-overlap)/2))


PAD2 = E.add_ref(make_pad(pad_height,pad_width,3))
TAIL = E.add_ref(make_end(top = True,add_via=False))
TAIL.connect(port = 1, destination = ROW5.ports[2],overlap = overlap+((via_width-overlap)/2))
PAD2.connect(port = 1, destination = TAIL.ports[2])


quickplot(E)