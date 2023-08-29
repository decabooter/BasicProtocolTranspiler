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
import ProtocolSymbolBuilder as symbldr
import SymbolBed as bench
import TrackmanCSV as tn
import LHToolLibrary as tools
import Constants
import csv




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
    symbolBuild = symbldr.SymbolBuilder(parser)
    symbolBedSetup = symbolBuild.interpret()
    print ("Length of the step list: ", len(bench.STEPS))
    for count, symbolStep in bench.STEPS.items():
        print(count, ": ")
        print(repr(symbolStep))
    ##################
    # At this point, an abstract model of the full protocol has been created.
    # Next step will be to generate device-specific protocol data.
    # First target will be the CSV format for PipettePilot
    ##################
    protocol = tn.MakeTrackmanCSV()
    outputProtocol = protocol.makeCSV()
    print(outputProtocol)
    print(type(outputProtocol))
    with open('./generatedCSV/banana.csv', 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerows(outputProtocol)
    
if __name__ == '__main__':
    main()

#print(lexemeList)