# -*- coding: utf8 -*-
#!/usr/bin/python
#
   
#****************************************************************************
#*                                                                          *
#* generic class for generating SMD DIP switch models in STEP AP214         *
#*                                                                          *
#* This is part of FreeCAD & cadquery tools                                 *
#* to export generated models in STEP & VRML format.                        *
#*   Copyright (c) 2017                                                     *
#* Terje Io / Io Engineering                                                *
#*                                                                          *
#* All trademarks within this guide belong to their legitimate owners.      *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Lesser General Public License (LGPL)     *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc.,                                                      *
#*   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA           *
#*                                                                          *
#****************************************************************************

## base parametes & model

from cq_base_model import part
from cq_parameters import CASE_THT_TYPE, CASE_SMD_TYPE

## model generators

from cq_model_smd_switch import *

class dip_switch_omron_a6h (dip_smd_switch):

    def __init__(self, params):
        dip_smd_switch.__init__(self, params)
        self.make_me = self.make_me and self.num_pins >= 4 and self.num_pins <= 20 
        self.rotation = 90

        self.pin_pitch  = 1.27
        self.pin_length = 3.2
        self.pin_thickness = 0.15
        self.pin_width = 0.4
        self.pin_bottom_length = 0.6

        self.body_width = 4.5
        self.body_overall_width = 6.7
        self.body_height = 1.45
        self.body_length = self.num_pins * self.pin_pitch / 2.0 + 1.23
        self.body_board_distance = 0.1

        self.button_width = 0.5
        self.button_length = 0.6
        self.button_base = 2.25
        self.button_heigth = 0.4
        self.button_pocket_dept = 0.5

        self.color_keys[1] = "gold pins"

    def make_modelname(self, genericName):
        return 'SW_DIP_x' + '{:d}'.format(self.num_pins / 2) + '_W6.15mm_Slide_Omron_A6H'

    def _make_switchpockets(self):

        # create first pocket

        x0 = self._first_pin_pos()
        z0 = self.body_height - self.button_pocket_dept
        
        pocket = cq.Workplane("XY", origin=(x0, 0.0, z0))\
                   .rect(self.button_width, self.button_base).extrude(self.button_pocket_dept)

        BS = cq.selectors.BoxSelector

        w2 = self.button_base / 2.0
        x2 = self.button_width / 2.0
        
        case = pocket.edges(BS((x0 + x2 + 0.1, -w2 - 0.1, z0-0.1), (x0 - x2 - 0.1, -w2 + 0.1, z0 + 0.1))).chamfer(self.button_pocket_dept - 0.01)
        case = pocket.edges(BS((x0 + x2 + 0.1, w2 - 0.1, z0-0.1), (x0 - x2 - 0.1, w2 + 0.1, z0 + 0.1))).chamfer(self.button_pocket_dept - 0.01)
                   
        return self.make_rest(pocket)

    def _make_cornerpockets(self):
        width = 0.5
        depth = -0.2
        pocket = cq.Workplane("XY", origin=(self.body_length / 2 - 0.5, self.body_width / 2.0 - 0.25, self.body_height))\
                   .rect(width, width).extrude(depth)\
                   .faces(">Z").center(0.0, -width / 2.0).circle(width / 2.0).extrude(depth)
        
        pockets = pocket.union(pocket.translate((-self.body_length + 1.0, 0, 0)))

        return pockets.union(pockets.rotate((0,0,0), (0,0,1), 180))

    def _make_buttonsrecess(self):
        depth = -0.2
        return cq.Workplane("XY")\
                   .workplane(offset=self.body_height)\
                   .rect(self.body_length - 1.6, self.body_width - self.button_base).extrude(depth)\
                   .faces("<Z").edges().chamfer(-depth-0.01)

    def make_body(self):
        body = dip_smd_switch.make_body(self, 0.2, 0.0).cut(self._make_buttonsrecess())\
                                                       .cut(self._make_cornerpockets())

        self.body_edge_upper = self.body_edge_upper + 0.15 # move pin mark a bit

        return body

    def make_buttons(self):

        button = cq.Workplane("XY", origin=(self._first_pin_pos(), 0.0, self.body_height - self.button_pocket_dept - 0.1))\
                   .rect(self.button_width, self.button_base).extrude(0.1)\
                   .faces(">Z").center(0, -self.button_base / 2.0 + self.button_length / 2.0 + self.button_pocket_dept)\
                   .rect(self.button_width, self.button_length).extrude(self.button_heigth + 0.1)

        return self.make_rest(button)

### EOF ###
