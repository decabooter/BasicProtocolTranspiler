# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 15:00:53 2023

@author: decabooter
"""

class MakeTrackmanCSV (object):
    def __init__(self, liquids, bed, steps):
        self.liquids = liquids
        self.bed = bed
        self.steps = steps
        self.protocol = []
        
    def makeCSV(self):
        CSVVersion = 7
        NumSteps = len(self.steps)
        NumColumns = 12
        self.CSVHeader(CSVVersion, NumSteps, NumColumns)
        for step in self.steps:
            self.CSVPipetting(step, NumColumns)
        return self.protocol
    
    def CSVHeader(self, version, numSteps, numColumns):
        header = ['' for i in range (numColumns)]
        header[0] = version
        header[1] = numSteps
        self.protocol.append(header)
    
    def BlankLine(self):
        blankline = []
        self.protocol.append(blankline)
    
    def CSVPipetting(self, step, numColumns):
        constant = [1 for i in range (numColumns)]
        print(step.stepID)
        self.CSVPipHeader('step'+str(step.stepID), [8,12], 6, 6, 12)
        self.protocol.append(constant)
        self.protocol.append(self.BlankLine())
        
    def CSVPipHeader(self, lwDim, stepName, aspSpeed, dispSpeed, numColumns):
        default = [1 for i in range (16)]
        header1 = default
        header1[0] = 'Pipetting step'
        header1[1] = stepName
        header1[2] = lwDim[0]
        header1[3] = lwDim[1]
        header1[4] = 'Standard'
        header1[5] = Color
        header1[7] = aspSpeed
        header1[8] = dispSpeed
        header1[9] = 'Normal'
        header1[10] = 'Multi-channel'
        header1[11] = 'No'
        header1[12] = 'No'
        header1[13] = 'By labware order'
        header1[14] = 'Vertical'
        self.protocol.append(header1)
        
        default = [1 for i in range (13)]
        header2[11] = 'Per well'
        header2[12] = 'On source'
        self.protocol.append(header2)
        
        