# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 14:29:42 2018

@author: jlm7
"""

from phidl import Device, Layer, quickplot, make_device
import phidl.geometry as pg
import phidl.routing as pr

padr_layer = Layer(name = 'bottom', gds_layer = 0, gds_datatype = 0,
                 description = 'bottom layer copper', color="orange")
padlt_layer = Layer(name = 'vias', gds_layer = 1, gds_datatype = 0,
                 description = 'Top layer copper', color="green")
comb_layer = Layer(name = 'pads', gds_layer = 2, gds_datatype = 0,
                 description = 'Top layer copper', color="blue")
zig_layer = Layer(name = 'top', gds_layer = 3, gds_datatype = 0,
                 description = 'Top layer copper', color="purple")
padb_layer = Layer(name = 'top', gds_layer = 4, gds_datatype = 0,
                 description = 'Top layer copper', color="red")

def test_comb(pad_size = (200,200), wire_width = 1, wire_gap = 3,
              comb_layer = 0, overlap_zigzag_layer = 1,
              comb_pad_layer = None, comb_gnd_layer = None, overlap_pad_layer = None):
    """
    Usage:
    
    Call comb_insulation_test_structure() with any of the
    parameters shown below which you'd like to change. You
    only need to supply the parameters which you intend on
    changing You can alternatively call it with no parameters
    and it will take all the default alues shown below.
    Ex:
        comb_insulation_test_structure(pad_size=(175,175), wire_width=2, wire_gap=5)
        - or -
        comb_insulation_test_structure()
    """ 
    CI = Device("test_comb")

    if comb_pad_layer is None:  comb_pad_layer = comb_layer
    if comb_gnd_layer is None:  comb_gnd_layer = comb_layer
    if overlap_pad_layer is None:  overlap_pad_layer = overlap_zigzag_layer
    if wire_gap < wire_width : wire_gap = wire_width*2

    #%% pad overlays
    overlay_padb = CI.add_ref(rectangle(size=(pad_size[0]*9/10,pad_size[1]*9/10), layer=overlap_pad_layer))
    overlay_padl = CI.add_ref(rectangle(size=(pad_size[0]*9/10,pad_size[1]*9/10), layer=comb_pad_layer ) )
    overlay_padt = CI.add_ref(rectangle(size=(pad_size[0]*9/10,pad_size[1]*9/10), layer=comb_pad_layer ) )
    overlay_padr = CI.add_ref(rectangle(size=(pad_size[0]*9/10,pad_size[1]*9/10), layer=comb_gnd_layer))
    
    overlay_padl.xmin = 0
    overlay_padl.ymin = 0
    overlay_padb.ymax = 0
    overlay_padb.xmin = overlay_padl.xmax + pad_size[1]/5
    overlay_padr.ymin = overlay_padl.ymin
    overlay_padr.xmin = overlay_padb.xmax + pad_size[1]/5
    overlay_padt.xmin = overlay_padl.xmax + pad_size[1]/5
    overlay_padt.ymin = overlay_padl.ymax
    
    #%% pads
    padl = CI.add_ref(rectangle(size=pad_size, layer=comb_layer))
    padt = CI.add_ref(rectangle(size=pad_size, layer=comb_layer))
    padr = CI.add_ref(rectangle(size=pad_size, layer=comb_layer))
    padb = CI.add_ref(rectangle(size=pad_size, layer=overlap_zigzag_layer))
    padl_nub = CI.add_ref(rectangle(size=(pad_size[0]/4,pad_size[1]/2), layer=comb_layer))
    padr_nub = CI.add_ref(rectangle(size=(pad_size[0]/4,pad_size[1]/2), layer=comb_layer))
    
    padl.xmin = overlay_padl.xmin
    padl.center = [padl.center[0],overlay_padl.center[1]]
    padt.ymax = overlay_padt.ymax
    padt.center = [overlay_padt.center[0],padt.center[1]]
    padr.xmax = overlay_padr.xmax
    padr.center = [padr.center[0],overlay_padr.center[1]]
    padb.ymin = overlay_padb.ymin
    padb.center = [overlay_padb.center[0],padb.center[1]]
    padl_nub.xmin = padl.xmax
    padl_nub.center = [padl_nub.center[0],padl.center[1]]
    padr_nub.xmax = padr.xmin
    padr_nub.center = [padr_nub.center[0],padr.center[1]]
    
    #%% connected zig
    
    head = CI.add_ref(pg.compass(size=(pad_size[0]/12, wire_width), layer=comb_layer))
    head.xmin = padl_nub.xmax
    head.ymax = padl_nub.ymax
    connector = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=comb_layer))
    connector.connect(port = 'W', destination=head.ports['E'])
    old_port = connector.ports['S']
    top = True
    obj = connector
    while(obj.xmax + pad_size[0]/12 < padr_nub.xmin):
        obj = CI.add_ref(pg.compass(size=(pad_size[1]/2 - 2*wire_width, wire_width), layer=comb_layer))
        obj.connect(port = 'W', destination=old_port)
        old_port = obj.ports['E']
        if(top):
            obj = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=comb_layer))
            obj.connect(port = 'N', destination=old_port)
            top = False
        else:
            obj = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=comb_layer))
            obj.connect(port = 'S', destination=old_port)
            top = True
            comb = CI.add_ref(pg.rectangle(size=((padt.ymin-head.ymax)+pad_size[1]/2 - (wire_gap + wire_width)/2, wire_width), layer=comb_layer))
            comb.rotate(90)
            comb.ymax = padt.ymin
            comb.xmax = obj.xmax - (wire_gap+wire_width)/2
        old_port = obj.ports['E']
        obj = CI.add_ref(pg.compass(size=(wire_gap, wire_width), layer=comb_layer))
        obj.connect(port = 'W', destination=old_port)
        old_port = obj.ports['E']
        obj = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=comb_layer))
        obj.connect(port = 'W', destination=old_port)
        if(top):
            old_port = obj.ports['S']
        else:
            old_port = obj.ports['N']
    old_port = obj.ports['E']
    if(padr_nub.xmin-obj.xmax > 0):
        tail = CI.add_ref(pg.compass(size=(padr_nub.xmin-obj.xmax, wire_width), layer=comb_layer))
    else:
        tail = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=comb_layer))
    tail.connect(port = 'W', destination=old_port)

    #%% disconnected zig
    
    dhead = CI.add_ref(pg.compass(size=(padr_nub.ymin -padb.ymax - wire_width, wire_width), layer=overlap_zigzag_layer))
    dhead.rotate(90)
    dhead.ymin = padb.ymax
    dhead.xmax = tail.xmin-(wire_gap+wire_width)/2
    connector = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=overlap_zigzag_layer))
    connector.connect(port = 'S', destination=dhead.ports['E'])
    old_port = connector.ports['N']
    right = True
    obj = connector
    while(obj.ymax + wire_gap + wire_width < head.ymax):
        obj = CI.add_ref(pg.compass(size=(wire_gap, wire_width), layer=overlap_zigzag_layer))
        obj.connect(port = 'W', destination=old_port)
        old_port = obj.ports['E']
        if(right):
            obj = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=overlap_zigzag_layer))
            obj.connect(port = 'W', destination=old_port)
            right = False
        else:
            obj = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=overlap_zigzag_layer))
            obj.connect(port = 'E', destination=old_port)
            right = True
        old_port = obj.ports['N']
        obj = CI.add_ref(pg.compass(size=(dhead.xmin-(head.xmax+head.xmin+wire_width)/2, wire_width), layer=overlap_zigzag_layer))
        obj.connect(port = 'E', destination=old_port)
        old_port = obj.ports['W']
        obj = CI.add_ref(pg.compass(size=(wire_width, wire_width), layer=overlap_zigzag_layer))
        obj.connect(port = 'S', destination=old_port)
        if(right):
            old_port = obj.ports['W']
        else:
            old_port = obj.ports['E']
    
    return CI

#%% Usage:
D2 = Device("final object")
D2.add_ref(test_comb(wire_width=2))
D2.write_gds('comb_test.gds')
quickplot(D2)