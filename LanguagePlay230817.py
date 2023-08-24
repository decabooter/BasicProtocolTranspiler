# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:58:18 2023

@author: decabooter

Building my little compiler based on a tutorial from 
ruslanspivak.com/lsbasi-part1
"""

import sys
import re
import ProtocolLexer as lex
import ProtocolParser as par
import SymbolBed as bench
import Constants



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
class Interpreter(NodeVisitor):
    
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
        print (bench.LIQUIDS)
        print (bench.BED)
        
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
            if count < labware.wells.size//2: #Kludge: taking out the 3rd dimension in calculation of array size
                val = bench.LIQUIDS.get(initVolume.value)
                if val is None:
                    raise Exception('Liquid not defined:', initVolume.value)
                else:
                    labware.wells[count%lwDims[0], count//lwDims[0], 0] = initVolume.value
            else:
                raise Exception('Initial volume assignment out of range.  Expected: ',
                                labware.wells.size//2, ' Actual: ', count+1)
        bench.BED[labwareName] = labware
        
    def visit_Protocol(self, node):
        print("Got to Protocol")
        
    def visit_Assign(self,node):
        print(node.arg.value, '=', node.assignment.value)
        assignment = [node.arg.value, node.assignment.value]
        return assignment
    
    def visit_Variable(self, node):
        print("Variable", node.value)
        return node.value
    
    def interpret(self):
        tree = self.parser.parse()
        print("####################")
        print("Done with the parser")
        print("####################")
        return self.visit(tree)

###############
# Main Section
#
# Gets run if the file is run on its own
###############

def main():
    inFile = sys.argv[1] if len(sys.argv) >= 2 else 'simpleProtocol.txt'

    with open (inFile) as protocolFile:
    #    lines = protocolFile.readlines()
        fileText = protocolFile.read()
        
    print(fileText)
    
    lexer = lex.Lexer(fileText)
    lexerList = lex.LexerLister(lexer)
    result = lexerList.expr()

    lexer = lex.Lexer(fileText)    
    parser = par.Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(result)
    
if __name__ == '__main__':
    main()

#print(lexemeList)