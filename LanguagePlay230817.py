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

inFile = sys.argv[1] if len(sys.argv) >= 2 else 'simpleProtocol.txt'

with open (inFile) as protocolFile:
#    lines = protocolFile.readlines()
    fileText = protocolFile.read()
    
print(fileText)


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
        return planCSV
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

###############
# Main Section
#
# Gets run if the file is run on its own
###############

def main():
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