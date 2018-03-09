# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 12:24:50 2018

@author: jlm7
"""

from __future__ import division, print_function, absolute_import


from phidl import Device, Layer, quickplot
import math


class via_router(object):
    """
    The following parameters are required:  total sample height (total_height), 
                                            total sample width (total_width), 
                                            number of requested vias (num_vias)
    Can be passed with any of the following optional parameters:pad_height (height of pad in um)
                                                                pad_width (width of pad in um)
                                                                via_height (via height in um)
                                                                via_width (via width in um)
                                                                wire_height (wire height between vias in um)
                                                                wire_width (wire length between vias in um)
                                                                overlap (how much vias and wire will overlap)
                                                                top_layer (gds layer of the top surfaces)
                                                                bottom_layer (gds layer of the bottom surfaces)
                                        

# """
    def __init__(self, total_height, total_width, num_vias, pad_height = None, pad_width = None, via_height = None, via_width = None, wire_height = None, wire_width = None, overlap = None, top_layer = None, bottom_layer = None, via_layer = None, vias_per_row = None, num_rows = None):
        if(pad_height == None):
            self.pad_height = total_height;
        else:
            self.pad_height = pad_height
            
        if(pad_width == None):
            self.pad_width = pad_height/2;
        else:
            self.pad_width = pad_width
            
        remaining_width = total_width - pad_width *2
        
        ratio = remaining_width / total_height
#        area = remaining_width * total_height
        
        if(num_rows == None):
            self.num_rows = (math.ceil(math.sqrt(num_vias/ratio)))
            if(self.num_rows % 2 == 0):
                self.num_rows = self.num_rows+1
        else:
            self.num_rows = num_rows
            
    
        if(vias_per_row == None):
            self.vias_per_row = (math.ceil(num_vias/self.num_rows))
#            vias_per_row_raw = (2*ratio + (math.sqrt(math.pow(2*ratio,2)+4*ratio*area)))/(2*ratio)
#            print (vias_per_row_2)

            
#            self.vias_per_row = math.ceil(vias_per_row_raw)
            self.wire_width = (total_height /(self.num_rows-1)) / (0.8 + 0.2/(self.num_rows-1))
            self.wire_height = self.wire_width/5
        else:
            self.vias_per_row = vias_per_row
            
        
    

        if(via_height == None):
            self.via_height = self.wire_height * 1.75
        else:
            self.via_height = via_height
            
        if(via_width == None):
            self.via_width = self.via_height
        else:
            self.via_width = via_width

        if(overlap == None):
            self.overlap = self.wire_height
        else:
            self.overlap = overlap
            
        if(top_layer == None):
            self.top_layer = 3
        else:
            self.top_layer = top_layer
            
        if(bottom_layer == None):
            self.bottom_layer = 4
        else:
            self.bottom_layer = bottom_layer
            
        if(via_layer == None):
            self.via_layer = 5
        else:
            self.via_layer = via_layer   
        self.num_vias = num_vias
        
    
    def waveguide(self,width = 10, height = 1, layer=3):
        WG = Device('waveguide')
        WG.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)], layer=layer)
        WG.add_port(name = 'wgport1', midpoint = [0,height/2], width = height, orientation = 180)
        WG.add_port(name = 'wgport2', midpoint = [width,height/2], width = height, orientation = 0)
        return WG

    def make_pad(self,height, width,layer):
        p = Device('Pad')
        p.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)], layer=layer)
        p.add_port(name = 1, midpoint = [0,self.wire_height/2], width = self.wire_height, orientation = 180)
        return p
    
    def via(self,width = 2, height = 2):
        WG = Device('via')
        WG.add_polygon( [(0, 0), (width, 0), (width, height), (0, height)], layer=5 )
        WG.add_port(name = 'viaport1', midpoint = [0,height/2], width = height, orientation = 180)
        WG.add_port(name = 'viaport2', midpoint = [width,height/2], width = height, orientation = 0)
        return WG
    
        
    def iterate_make_row(self,count = 2):
        ROW = Device('Row')
        wg = []
        v = []
        for x in range(count):
            if(x % 2 == 0):
                wg.append(ROW.add_ref(self.waveguide(width=self.wire_width, height = self.wire_height, layer=self.bottom_layer)))
            else:
                wg.append(ROW.add_ref(self.waveguide(width=self.wire_width, height = self.wire_height, layer=self.top_layer)))
            if(x > 0):
                v.append(ROW.add_ref(self.via(width=self.via_width, height=self.via_height)))
                wg[x].connect(port = 'wgport1', destination = wg[x-1].ports['wgport2'], overlap = self.overlap)
                v[x-1].connect(port = 'viaport1', destination = wg[x-1].ports['wgport2'], overlap = self.overlap+((self.via_width-self.overlap)/2))
        ROW.add_port(name = 1, port = wg[0].ports['wgport1'])
        ROW.add_port(name = 2, port = wg[x].ports['wgport2'])
    
        return ROW
            
                
    def make_corner(self, top = True):
        CT = Device('Corner Top')
        via1 = self.via(width=self.via_width, height=self.via_height)
        via2 = self.via(width=self.via_width, height=self.via_height)
        VIA1 = CT.add_ref(via1).rotate(90)
        VIA2 = CT.add_ref(via2).rotate(90)
        if(top):
            wire = self.waveguide(width=self.wire_width, height = self.wire_height, layer=3)
        else:
            wire = self.waveguide(width=self.wire_width, height = self.wire_height, layer=4)
        WIRE = CT.add_ref(wire)
        VIA1.connect(port = 'viaport1', destination = WIRE.ports['wgport2'], overlap = self.overlap+((self.via_width-self.overlap)/2))
        VIA2.connect(port = 'viaport2', destination = WIRE.ports['wgport1'], overlap = self.overlap+((self.via_width-self.overlap)/2))
        VIA2.rotate(90).movex(self.overlap)
        VIA1.rotate(270, (self.wire_width-self.overlap,0)).movey(self.overlap)
        CT.add_port(name = 1, port = VIA1.ports['viaport2'])
        CT.add_port(name = 2, port = VIA2.ports['viaport1'])
        return CT
                
                
    
    def make_end(self, top = True, add_via = True):
        END = Device('Head/Tail')
        
        if(top):
            wire = self.waveguide(width=self.wire_width, height = self.wire_height, layer=3)
        else:
            wire = self.waveguide(width=self.wire_width, height = self.wire_height, layer=4)
        WIRE = END.add_ref(wire)
        if(add_via == True):
            via1 = self.via(width=self.via_width, height=self.via_height)
            VIA1 = END.add_ref(via1)    
            VIA1.connect(port = 'viaport2', destination = WIRE.ports['wgport1'], overlap = self.overlap+((self.via_width-self.overlap)/2))
            END.add_port(port = VIA1.ports['viaport1'], name = 1)
        else:
            END.add_port(port = WIRE.ports['wgport1'], name = 1)
    
    
        END.add_port(port = WIRE.ports['wgport2'], name = 2)
        return END
    
    def last_row(self, remaining_vias, starting_layer):
        if(remaining_vias % 2 != 0):
            remaining_vias = remaining_vias+1
        LR = Device('Last Row')
        ir = LR.add_ref(self.iterate_make_row(remaining_vias))
        wg = LR.add_ref(self.waveguide(width = (self.vias_per_row-remaining_vias) * (self.wire_width-self.overlap), height = self.wire_height, layer=3))
        wg.connect(port='wgport1', destination = ir.ports[2])
        LR.add_port(name=1, port=ir.ports[1])
        LR.add_port(name=2, port = wg.ports['wgport2'])
        return LR
        

    def generate_path(self):
        self.E = Device('Via Path Loop')        
        
        ##Create Layers
        top = Layer(name = 'top', gds_layer = self.top_layer, gds_datatype = 0,
                         description = 'Top layer copper', color="red")
        bottom = Layer(name = 'bottom', gds_layer = self.bottom_layer, gds_datatype = 0,
                         description = 'bottom layer copper', color="blue")
        vias = Layer(name = 'vias', gds_layer = self.via_layer, gds_datatype = 0,
                         description = 'Top layer copper', color="green")
        #Create pads and beginning/end paths
        
        PAD1 = self.E.add_ref(self.make_pad(self.pad_height,self.pad_width,3)).rotate(180,(self.pad_width/2,self.pad_height/2))
        if(self.vias_per_row % 2 == 0):
            TAIL = self.E.add_ref(self.make_end(True, False))
        else: 
            TAIL = self.E.add_ref(self.make_end(True, True))
        PAD2 = self.E.add_ref(self.make_pad(self.pad_height,self.pad_width,3))
        HEAD = self.E.add_ref(self.make_end(True, True))
        HEAD.connect(port = 2, destination = PAD1.ports[1])
        
        ROW_ARR = []
        COR_ARR = []
        
        for x in range(self.num_rows):
            if(x < self.num_rows-1):
                ROW_ARR.append(self.E.add_ref(self.iterate_make_row(self.vias_per_row)))
                if(x % 2 == 0 and self.vias_per_row % 2 == 0):   
                    COR_ARR.append(self.E.add_ref(self.make_corner(False)))
                else:
                    COR_ARR.append(self.E.add_ref(self.make_corner(True)))
            else:
                ROW_ARR.append(self.E.add_ref(self.last_row((self.num_vias % self.vias_per_row+1)-(self.num_rows), self.top_layer)))
            if(x == 0):
                ROW_ARR[x].connect(port = 1, destination = HEAD.ports[1],overlap = self.overlap+((self.via_width-self.overlap)/2))
            else:
                if(x % 2 == 0):
                    ROW_ARR[x].connect(port = 1, destination = COR_ARR[x-1].ports[2],overlap = self.overlap+((self.via_width-self.overlap)/2))
                else:
                    ROW_ARR[x].connect(port = 2, destination = COR_ARR[x-1].ports[1],overlap = self.overlap+((self.via_width-self.overlap)/2))
            if(x < self.num_rows-1):
                if(x % 2 == 0):
                    COR_ARR[x].connect(port = 2, destination=ROW_ARR[x].ports[2],overlap = self.overlap+((self.via_width-self.overlap)/2))
                else:
                    COR_ARR[x].connect(port = 1, destination=ROW_ARR[x].ports[1],overlap = self.overlap+((self.via_width-self.overlap)/2))
            
            TAIL.connect(port = 1, destination = ROW_ARR[x].ports[2],overlap = self.overlap+((self.via_width-self.overlap)/2))
            PAD2.connect(port = 1, destination = TAIL.ports[2])
        
        quickplot(self.E)
        
    
        self.E.write_gds('Via-Path.gds')



if(__name__ == "__main__"):
    new_params = via_router(total_height=130, total_width=400, pad_width=50, num_vias=90)
    new_params.generate_path()
    
Device()