# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 15:00:53 2023

@author: decabooter
"""

import SymbolBed as bench
import numpy as np

class MakeTrackmanCSV (object):
    def __init__(self):
        self.protocol = []
        
    def makeCSV(self):
        CSVVersion = 7
        NumSteps = len(bench.STEPS)
        NumColumns = 12
        self.CSVHeader(CSVVersion, NumSteps, NumColumns)
        showDestination = True
        for stepID, step in bench.STEPS.items():
            self.CSVPipetting(step, NumColumns, showDestination)
        return self.protocol
    
    def CSVHeader(self, version, numSteps, numColumns):
        header = ['' for i in range (numColumns)]
        header[0] = version
        header[1] = numSteps
        self.protocol.append(header)
    
    def BlankLine(self):
        blankline = []
        self.protocol.append(blankline)
    
    def CSVPipetting(self, step, numColumns, showDestination):
        self.CSVPipHeader('step '+str(step.stepID), [8,12], 6, 6, 12)
        # the for loop below assumes destinations are the same.
        # extend by adding support for showDestination (could show source) and
        # adding support for splitting actions in a step with different labware
        
        # This code is initializing the labware array for the CSV
        # Note: since we're not tracking liquids, we don't need to worry about
        #   initial contents in the wells, so are just zero'ing them out
        labwareName = step.actionList[0].destinationLabware
        labwareType = bench.INITBED[labwareName].model
        labwareShape = np.array(bench.LabwareMapping[labwareType])
        #print ("Array Dimension: ", labwareShape.shape[0], " , ", labwareShape.shape[1])
        labware = np.array([["" for j in range(labwareShape.shape[1])] 
                                for i in range(labwareShape.shape[0])],
                                dtype='object')
        # Load the liquids into the labware array
        for action in step.actionList:
            # Continues to assume all the steps are transfers...
            # Future work: Determine liquid name from source well
            liquidName = action.sourceLabware + ":" + str(action.sourceLocation)
            liquidVolume = action.volume
            liquidCell = liquidName + ' / ' + str(liquidVolume)
            row = action.destinationLocation[0]
            column = action.destinationLocation[1]
            labware[row, column] = str(liquidCell)
        columnIndex = ['']
        for j in range(labwareShape.shape[1]):
            columnIndex.append(str(j))
        self.protocol.append(columnIndex)
        for i in range(labwareShape.shape[0]):
            rowIndex = chr(65+i)
            rowValue = np.insert(labware[i],0,rowIndex)
            self.protocol.append(rowValue.tolist())
        self.BlankLine()
        
    def CSVPipHeader(self, stepName, lwDim, aspSpeed, dispSpeed, numColumns):
        default = ['' for i in range (16)]
        header1 = default
        header1[0] = 'Pipetting step'
        header1[1] = stepName
        header1[2] = lwDim[0]
        header1[3] = lwDim[1]
        header1[4] = 'Standard'
        header1[5] = 'Color'
        header1[7] = aspSpeed
        header1[8] = dispSpeed
        header1[9] = 'Normal'
        header1[10] = 'Multi-channel'
        header1[11] = 'No'
        header1[12] = 'No'
        header1[13] = 'By labware order'
        header1[14] = 'Vertical'
        self.protocol.append(header1)
        
        header2 = ['' for i in range (13)]
        header2[11] = 'Per well'
        header2[12] = 'On source'
        self.protocol.append(header2)
        
        