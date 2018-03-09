# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 12:25:11 2018

@author: jlm7
"""

from phidl import Device, Layer, quickplot
import math
import phidl.geometry as pg

top = Layer(name = 'top', gds_layer = 1, gds_datatype = 0,
                 description = 'Top layer copper', color="red")
bottom = Layer(name = 'bottom', gds_layer = 2, gds_datatype = 0,
                 description = 'bottom layer copper', color="blue")
vias = Layer(name = 'vias', gds_layer = 3, gds_datatype = 0,
                 description = 'Top layer copper', color="orange")
pads = Layer(name = 'pads', gds_layer = 0, gds_datatype = 0,
                 description = 'Top layer copper', color="green")

def via_iterable(via_spacing, wire_width, wiring1_layer, wiring2_layer, via_layer, via_width):
    VI = Device('Via Route')
    wire1 = VI.add_ref(pg.compass(size=(via_spacing, wire_width), layer=wiring1_layer))
    wire2 = VI.add_ref(pg.compass(size=(via_spacing, wire_width), layer=wiring2_layer))
    via1 = VI.add_ref(pg.compass(size=(via_width, via_width), layer=via_layer))
    via2 = VI.add_ref(pg.compass(size=(via_width, via_width), layer=via_layer))
    wire1.connect(port='E', destination = wire2.ports['W'], overlap=wire_width)
    via1.connect(port='W', destination = wire1.ports['E'], overlap = (wire_width + via_width)/2)
    via2.connect(port='W', destination = wire2.ports['E'], overlap = (wire_width + via_width)/2)
    VI.add_port(name='W', port = wire1.ports['W'])
    VI.add_port(name='E', port = wire2.ports['E'])
    VI.add_port(name='S', midpoint = [(1*wire_width)+ wire_width/2,-wire_width/2], width = wire_width, orientation = -90)
    VI.add_port(name='N', midpoint = [(1*wire_width)+ wire_width/2,wire_width/2], width = wire_width, orientation = 90)

    return VI

def via_route(num_vias, pad_size = (300,300), wire_width=10, via_spacing = 40, min_pad_spacing = 0, pad_layer = 0, wiring1_layer = 1, wiring2_layer = 2, via_layer = 3):
    """
    total requested vias (num_vias) -> this needs to be even
    pad size (pad_size) -> given in a pair (width, height)
    wire_width -> how wide each wire should be
    pad_layer -> GDS layer number of the pads
    wiring1_layer -> GDS layer number of the top wiring
    wiring2_layer -> GDS layer number of the bottom wiring
    via_layer -> GDS layer number of the vias
    """
    
    VR = Device('Via Route')
    pad1 = VR.add_ref(pg.rectangle(size=pad_size, layer=pad_layer))
    pad2 = VR.add_ref(pg.rectangle(size=pad_size, layer=pad_layer))
    nub = VR.add_ref(pg.compass(size=(3*wire_width,wire_width),layer=wiring1_layer))
    head = VR.add_ref(pg.compass(size=(wire_width,wire_width),layer=wiring1_layer))
    tail = VR.add_ref(pg.compass(size=(wire_width,wire_width),layer=wiring1_layer))
    nub.ymax = pad1.ymax-5
    nub.xmin = pad1.xmax
    head.connect(port = "W", destination = nub.ports["E"])

    old_port = head.ports['S']
    count = 0
    width_via_iter = 2*via_spacing - 2*wire_width
    max_via_rows = math.ceil(pad_size[1]/width_via_iter)

    pad2.xmin = pad1.xmax + min_pad_spacing
    bottom = False
    top = False
    obj_old = head
    while( count <= num_vias):
        obj = VR.add_ref(via_iterable(via_spacing, wire_width, wiring1_layer, wiring2_layer, via_layer, wire_width*1.25))
        obj.connect(port = 'W', destination = old_port, overlap = wire_width)
        old_port = obj.ports['E']
        if(obj.ymax > pad1.ymax):
            print("top")
            obj.connect(port = 'W', destination = obj_old.ports['S'], overlap = wire_width)
            old_port = obj.ports['S']

        elif(obj.ymin < pad1.ymin):
            print("bottom")
            obj.connect(port = 'W', destination = obj_old.ports['N'], overlap = wire_width)
            old_port = obj.ports['N']
        count = count + 2
        obj_old = obj


#
    #
    min_via_iters_per_row = math.floor((min_pad_spacing-10) / width_via_iter)
    print(width_via_iter)
    print(min_via_iters_per_row)

    

#    if(max_via_rows % 2 == 0):
#        max_via_rows = max_via_rows-1
#    vias_per_row = math.ceil(num_vias / (max_via_rows))
#    old_port = head.ports['E']
#    print(vias_per_row)
#    print(max_via_rows)
#    count = 0;
#    
    
    
    
    
#    for y in range(math.floor(max_via_rows/2)):
#        for x in range(math.ceil(vias_per_row / 2)):
#            obj = VR.add_ref(via_iterable(via_spacing, wire_width, wiring1_layer, wiring2_layer, via_layer, wire_width*1.25))
#            obj.connect(port = 'W', destination = old_port, overlap = wire_width)
#            old_port = obj.ports['E']
#            count = count + 2
#        old_port = obj.ports['S']
#        obj = VR.add_ref(via_iterable(via_spacing, wire_width, wiring1_layer, wiring2_layer, via_layer, wire_width*1.25))
#        obj.connect(port = 'W', destination = old_port, overlap = wire_width)
#        old_port = obj.ports['S']
#        count = count + 2
#        for x in range(math.ceil(vias_per_row / 2)):
#            obj = VR.add_ref(via_iterable(via_spacing, wire_width, wiring1_layer, wiring2_layer, via_layer, wire_width*1.25))
#            obj.connect(port = 'W', destination = old_port, overlap = wire_width)
#            old_port = obj.ports['E']
#            count = count + 2
#        old_port = obj.ports['N']
#        obj = VR.add_ref(via_iterable(via_spacing, wire_width, wiring1_layer, wiring2_layer, via_layer, wire_width*1.25))
#        obj.connect(port = 'W', destination = old_port, overlap = wire_width)
#        old_port = obj.ports['N']
#        count = count + 2
#    for x in range(math.ceil((num_vias - count)/2)):
#        obj = VR.add_ref(via_iterable(via_spacing, wire_width, wiring1_layer, wiring2_layer, via_layer, wire_width*1.25))
#        obj.connect(port = 'W', destination = old_port, overlap = wire_width)
#        old_port = obj.ports['E']
#    
#    final_wire = VR.add_ref(pg.compass(size=(int(width_via_iter * (vias_per_row - (num_vias-count))/2),wire_width), layer=wiring1_layer))
#    final_wire.connect(port = 'W', destination=old_port, overlap = wire_width)
#    tail.connect(port = 'W', destination = final_wire.ports['E'])
#    pad2.xmin = tail.xmax
#    pad2.ymin = pad1.ymin
#    
    

    

    
    
    
    return VR
    
quickplot(via_route(34, min_pad_spacing=300))

    