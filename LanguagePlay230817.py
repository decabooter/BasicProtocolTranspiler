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
    for index, step in bench.STEPS:
        print(index, ": ", step)
    ##################
    # At this point, an abstract model of the full protocol has been created.
    # Next step will be to generate device-specific protocol data.
    # First target will be the CSV format for PipettePilot
    ##################
    protocol = tn.MakeTrackmanCSV(bench.LIQUIDS, bench.INITBED, bench.STEPS)
    outputProtocol = protocol.makeCSV()
    print(outputProtocol)
    #print(result)
    #print (bench.LIQUIDS)
    #print (bench.INITBED)
    
if __name__ == '__main__':
    main()

#print(lexemeList)