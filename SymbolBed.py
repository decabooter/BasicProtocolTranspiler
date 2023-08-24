# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 06:22:09 2023

@author: decab
"""

LIQUIDS = {}
BED = {}

LabwareMapping = {
    'plate96': [[0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0]],
    'reservoir': [0]
    }

class Labware(object):
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.wells = []
        
    def initWells(self,model):
        self.wells = LabwareMapping[model]
