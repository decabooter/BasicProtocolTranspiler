# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 06:22:09 2023

@author: decab
"""
import numpy as np

LIQUIDS = {}
BED = {}

DefaultWell = [None,0]
LabwareMapping = {
    'plate96': np.full(shape=(8,12,2),fill_value=DefaultWell),
    'reservoir': np.full(shape=(1,1,2),fill_value=DefaultWell)
    }

class Labware(object):
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.wells = []
        self.initVolumes = []
    
    def __str__(self):
        return 'Labware({name}, {model}, {wells}'.format(
            name = self.name,
            model = self.model,
            wells = self.wells
        )
    
    def __repr__(self):
        return self.__str__()
        
    def initWells(self,model):
        self.wells = LabwareMapping[model]
