# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 12:26:41 2018

@author: jlm7
"""

from phidl import Device, Layer, quickplot
import phidl.geometry as pg
import numpy as np

padb_layer = Layer(name = 'padbottom', gds_layer = 0, gds_datatype = 0,
                 description = 'bottom layer copper', color="red")
padt_layer = Layer(name = 'padtop', gds_layer = 1, gds_datatype = 0,
                 description = 'Top layer copper', color="blue")
wire_layer = Layer(name = 'pads', gds_layer = 2, gds_datatype = 0,
                 description = 'Top layer copper', color="green")

def wire_step4(thick_width = 10, thin_width = 1):
    WS4 = Device('Optimal Wire Step Symmetric')
    wire_stepa = WS4.add_ref(pg.optimal_step(thick_width/2, thin_width/2, layer=wire_layer))
    wire_stepb = WS4.add_ref(pg.optimal_step(thin_width/2, thick_width/2, layer=wire_layer))
    wire_stepc = WS4.add_ref(pg.optimal_step(thick_width/2, thin_width/2, layer=wire_layer))
    wire_stepd = WS4.add_ref(pg.optimal_step(thin_width/2, thick_width/2, layer=wire_layer))
    wire_stepb.rotate(180)
    wire_stepb.xmin = wire_stepa.xmin
    wire_stepc.rotate(180)
    wire_stepc.xmin = wire_stepa.xmax
    wire_stepd.xmin = wire_stepc.xmin
    return WS4


#def optimal_ic_step(pad_size=(200,200), total_width = 1200, total_height = 600, thick_width = 20, narrow_width = 2, padb_layer = 0, padt_layer = 1, wire_layer=2):
#    ICS = Device('Critical Current Step')
#    translation = 0
#    padb = ICS.add_ref(pg.rectangle(size=(total_width, pad_size[1]), layer=wire_layer))
#    padb_overlay = ICS.add_ref(pg.rectangle(size=(total_width*9/10, pad_size[1]*9/10), layer=padb_layer))
#    padb_overlay.center = padb.center
#    padb_overlay.ymin = padb.ymin
#    while(translation < total_width):
#        padt = ICS.add_ref(pg.rectangle(pad_size, wire_layer))
#        padt.xmin = padb.xmin + translation
#        padt.ymax = total_height
#        padt_overlay = ICS.add_ref(pg.rectangle(size=(pad_size[0]*9/10, pad_size[1]*9/10), layer=padt_layer))
#        padt_overlay.center = padt.center
#        padt_overlay.ymax = padt.ymax
#        difference = padt.ymin-padb.ymax
#        wire_step = ICS.add_ref(wire_step4(thick_width, narrow_width))
#        wire_step.rotate(90)
#        wire_step.center = (padt.center[0], padb.ymax + difference/2)
#        translation = translation + pad_size[1]*12/10 
#        conn_wire_top = ICS.add_ref(pg.rectangle(size=(thick_width, padt.ymin-wire_step.ymax), layer=wire_layer))
#        conn_wire_bottom = ICS.add_ref(pg.rectangle(size=(thick_width, wire_step.ymin-padb.ymax), layer=wire_layer))
#        conn_wire_top.ymax = padt.ymin
#        conn_wire_top.xmin = wire_step.xmin
#        conn_wire_bottom.ymin = padb.ymax
#        conn_wire_bottom.xmin = wire_step.xmin
#    return ICS


def optimal_ic_step2(pad_size=(200,200), step_width_growth_factor = 5, thick_width = [], narrow_width = [0.5,1,2,4,5], padb_layer = 0, padt_layer = 1, wire_layer=2):
    ICS = Device('Critical Current Step')
    if(np.size(thick_width) == 0):
        for i, val in enumerate(narrow_width):
            thick_width.append(step_width_growth_factor * narrow_width[i])
    translation = 0
    padb = ICS.add_ref(pg.rectangle(size=(np.size(narrow_width) * (pad_size[0]*6/5), pad_size[1]), layer=wire_layer))
    padb_overlay = ICS.add_ref(pg.rectangle(size=((np.size(narrow_width) * (pad_size[0]*6/5))*9/10, pad_size[1]*9/10), layer=padb_layer))
    padb_overlay.center = padb.center
    padb_overlay.ymin = padb.ymin
    for i, x in enumerate(thick_width):
        padt = ICS.add_ref(pg.rectangle(pad_size, wire_layer))
        padt.xmin = padb.xmin + translation
        padt.ymax = pad_size[1]*3
        padt_overlay = ICS.add_ref(pg.rectangle(size=(pad_size[0]*9/10, pad_size[1]*9/10), layer=padt_layer))
        padt_overlay.center = padt.center
        padt_overlay.ymax = padt.ymax
        difference = padt.ymin-padb.ymax
        wire_step = ICS.add_ref(wire_step4(thick_width[i], narrow_width[i]))
        wire_step.rotate(90)
        wire_step.center = (padt.center[0], padb.ymax + difference/2)
        translation = translation + pad_size[1]*12/10 
        conn_wire_top = ICS.add_ref(pg.rectangle(size=(thick_width[i], padt.ymin-wire_step.ymax), layer=wire_layer))
        conn_wire_bottom = ICS.add_ref(pg.rectangle(size=(thick_width[i], wire_step.ymin-padb.ymax), layer=wire_layer))
        conn_wire_top.ymax = padt.ymin
        conn_wire_top.xmin = wire_step.xmin
        conn_wire_bottom.ymin = padb.ymax
        conn_wire_bottom.xmin = wire_step.xmin
    return ICS
    

D = Device('test')
D.add_ref(optimal_ic_step2())
#D.write_gds('step_test.gds')
quickplot(D)


D2 = Device('test2')
D2.add_ref(optimal_ic_step2(thick_width = [5,10,10,10,10]))
#D.write_gds('step_test.gds')
quickplot(D2)