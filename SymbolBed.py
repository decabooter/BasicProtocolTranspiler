# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 06:22:09 2023

@author: decab
"""
import numpy as np

LIQUIDS = {}
INITBED = {}
STEPS = {}

class Well(object):
    def __init__(self, liquid, volume):
        self.liquid = liquid
        self.volume = volume
        
LabwareMapping = {
    'plate96' : np.array([[Well(None, 0) for j in range(12)] for i in range(8)]),
    'reservoir' : np.array([[Well(None, 0) for j in range(1)] for i in range(1)])
    }

class Labware(object):
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.wells = []
        self.initVolumes = []
    
    def __str__(self):
        wellList = ""
        for i in range (self.wells.shape[0]):
            if i == 0:
                wellList += ('[')
            for j in range (self.wells.shape[1]):
                if j == 0:
                    wellList += ('[')
                wellList += ('[{liquid}, {volume}]'.format(
                    liquid = self.wells[i,j].liquid, 
                    volume = self.wells[i,j].volume))
                if j < self.wells.shape[1]-1:
                    wellList += (',')
                else:
                    wellList += (']')
            if i < self.wells.shape[0]-1:
                wellList += (',\n')
            else:
                wellList += (']\n')
                
            
        return 'Labware({name}, {model}\n {wells}'.format(
            name = self.name,
            model = self.model,
            wells = wellList
        )
    
    def __repr__(self):
        return self.__str__()
        
    def initWells(self,model):
        self.wells = LabwareMapping[model]
        
class ProtocolStep(object):
    def __init__(self, stepID):
        self.stepID = stepID
        self.actionList = []
        
    def __str__(self):
        stepPrint = "Step {stepNum}:\n".format(
            stepNum = str(self.stepID))
        for count, action in enumerate(self.actionList):
            stepPrint += repr(action)
        return stepPrint
    
    def __repr__(self):
        return self.__str__()
        
class ProtocolAction(object):
    def __init__(self, action, srcLabware, srcLoc, destLabware, destLoc, volume):
        self.action = action
        self.sourceLabware = srcLabware
        self.sourceLocation = srcLoc
        self.destinationLabware = destLabware
        self.destinationLocation = destLoc
        self.volume = volume
    
    def __str__(self):
        return 'Action({name}: {volume} uL from {srcLW}:{srcLoc} to {destLW}:{destLoc}\n'.format(
            name = self.action,
            volume = self.volume,
            srcLW = self.sourceLabware,
            srcLoc = self.sourceLocation,
            destLW = self.destinationLabware,
            destLoc = self.destinationLocation
            )
    
    def __repr__(self):
        return self.__str__()