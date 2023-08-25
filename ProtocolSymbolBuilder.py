# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:17:22 2023

@author: decabooter
"""

import SymbolBed as bench
import LHToolLibrary as tools

#######################
# Interpreter
#
# This section will take the parsed tree and translate it into results
# For this initial case, the interpreter will output a CSV that can be imported
# into Gilson's PipettePilot (CSV version 7)
#######################

class NodeVisitor(object):
    # visit is set up to be a "universal" call--it will determine from the type
    # of node passed in which specific visit call is required.
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception('no visit_{} method'.format(type(node).__name__))

# This class inherits from NodeVisitor to do all of the specific stuff for our
# specific language
class SymbolBuilder(NodeVisitor):
    
    def __init__(self, parser):
        self.parser = parser
        
    def visit_Plan(self, node):
        print("Creating plan", node.name.value, "ver", node.version.value)
        CSVVersion = 7
        NumSteps = 0
        planCSV = str(CSVVersion) + "," + str(NumSteps) + ",,,,,,,,,,\n"
        self.visit(node.config)
        self.visit(node.protocol)
        return planCSV
    
    def visit_Configuration(self, node):
        for declaration in node.declarationList:
            self.visit(declaration)
        
    def visit_Liquid(self, node):
        liquidName = self.visit(node.liquidName)
        argList = {}
        for arg in node.argList:
            argument = self.visit(arg)
            argList[argument[0]] = argument[1]
        bench.LIQUIDS[liquidName] = argList
        
    #Labware Visitor
    #This visitor reads in the labware information, initializes any wells with defined liquids
    #Checks are done to ensure the liquids have already been defined.
    #Labware is then added to the "symbolic benchtop"
    def visit_Labware(self, node):
        labwareName = self.visit(node.labwareName)
        labwareModel = 'reservoir'
        argList = {}
        for arg in node.argList:
            argument = self.visit(arg)
            if argument[0] == 'LWTYPE':
                labwareModel = argument[1]
            else:
                argList[argument[0]] = argument [1]
        labware = bench.Labware(labwareName, labwareModel)
        labware.initWells(labwareModel)
        lwDims = labware.wells.shape
        for count,initVolume in enumerate(node.initVolumes):
            if count < labware.wells.size: #Kludge: taking out the 3rd dimension in calculation of array size
                val = bench.LIQUIDS.get(initVolume.value)
                if val is None:
                    raise Exception('Liquid not defined:', initVolume.value)
                else:
                    labware.wells[count%lwDims[0], count//lwDims[0]].liquid = initVolume.value
            else:
                raise Exception('Initial volume assignment out of range.  Expected: ',
                                labware.wells.size, ' Actual: ', count+1)
        bench.INITBED[labwareName] = labware
        
    def visit_Protocol(self, node):
        print("Got to Protocol")
        for count, step in enumerate(node.stepList):
            symbolStep = self.visit(step)
            bench.STEPS[count] = symbolStep
            
    def visit_Step(self, node):
        step = bench.ProtocolStep(self.visit(node.stepID))
        for stepAction in node.stepActionList:
            step.actionList.append(self.visit(stepAction))       
        return step
            
    def visit_StepAction(self, node):
        action = self.visit(node.action)
        checkVal = bench.INITBED.get(self.visit(node.sourceLabware))
        if checkVal is None:
            raise Exception('Labware not defined:', self.visit(node.sourceLabware))
        else:
            sourceLabware = self.visit(node.sourceLabware)
        sourceLocation = tools.A1to00(self.visit(node.sourceLocation))
        checkVal = bench.INITBED.get(self.visit(node.destinationLabware))
        if checkVal is None:
            raise Exception('Labware not defined:', self.visit(node.destinationLabware))
        destinationLabware = self.visit(node.destinationLabware)
        destinationLocation = tools.A1to00(self.visit(node.destinationLocation))
        volume = self.visit(node.volume)
        stepAction = bench.ProtocolAction(action, sourceLabware, sourceLocation,
                                          destinationLabware, destinationLocation,
                                          volume)
        print(stepAction)
        return stepAction
        
    def visit_Assign(self,node):
        print(node.arg.value, '=', node.assignment.value)
        assignment = [node.arg.value, node.assignment.value]
        return assignment
    
    def visit_Variable(self, node):
        #print("Variable", node.value)
        return node.value
    
    def interpret(self):
        tree = self.parser.parse()
        print("####################")
        print("Done with the parser")
        print("####################")
        return self.visit(tree)
