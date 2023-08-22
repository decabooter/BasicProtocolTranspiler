# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:58:18 2023

@author: decabooter

Building my little compiler based on a tutorial from 
ruslanspivak.com/lsbasi-part1
"""

import sys
import re

inFile = sys.argv[1] if len(sys.argv) >= 2 else 'simpleProtocol.txt'

with open (inFile) as protocolFile:
#    lines = protocolFile.readlines()
    fileText = protocolFile.read()
    
print(fileText)

    
"""
This section takes the protocol string and breaks it down into a list of lexemes
"""
"""
lexemeList = []
baseString = ""
stringField = False

for i in range(len(fileText)):
    if fileText[i] == "(" :
        lexemeList.append(fileText[i])
    elif fileText[i] == ")" :
        if len(baseString) != 0 :
            lexemeList.append(baseString)
            baseString = ""
        lexemeList.append(fileText[i])
    elif fileText[i].isspace() & ~stringField:
        if len(baseString) != 0 :
            lexemeList.append(baseString)
            baseString = ""
    else:
        baseString = baseString + fileText[i]
        if fileText[i] == '"':
            stringField = ~stringField
"""
"""
This section translates the lexeme list into an abstract syntax tree
"""

"""
Start of work based on architecture defined by ruslanspivak.com demo

Token Types
EOF (end-of-file) token is used to indicate that there is no more input left for lexical analysis
"""
"""PLAN, LPAREN, RPAREN, CONFIGURATION, STEP, ACTION, STRING, INTEGER, 
EOF, RESWORD, LOCATION = (
    'PLAN', '(', ')', 'CONFIG', 'STEP', 'ACTION', 'STRING', 
    'INTEGER', 'EOF', 'RESWORD', 'LOCATION'
    )
"""
DONE = 'DONE'
RESWORD = 'RESWORD'
PLAN = 'PLAN'
CONFIG = 'CONFIG'
LIQUID = 'LIQUID'
LABWARE = 'LABWARE'
PROTOCOL = 'PROTOCOL'
STEP = 'STEP'
TRANSFER = 'TRANSFER'
STRING = 'STRING'
INTEGER = 'INTEGER'
LOCATION = 'LOCATION'
ARGUMENT = 'ARGUMENT'
STARTARR = 'STARTARR'
ENDARR = 'ENDARR'
ID = 'ID'
ASSIGN = 'ASSIGN'
EOF = 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def __str__(self):
        """String representation of the class instance.
        
        Examples:
            Token(INTEGER, 3)
        """
        return 'Token({type}, {value})'.format(
            type =self.type,
            value=repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()
    
ARGUMENTS = {
    'aspSpeed' : Token('aspSpeed', 'ASPSPEED'),
    'dispSpeed' : Token('dispSpeed', 'DISPSPEED'),
    'lwType' : Token('lwType', 'LWTYPE'),
}

    
class Lexer(object):
    def __init__(self, text):
        #client string input
        self.text = text
        #self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
        
    def error(self):
        raise Exception('Invalid character')
        
    def advance(self):
        #advance the 'pos' pointer and sent the 'current_char' variable.
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None #Indicates end of input
        else:
            self.current_char = self.text[self.pos]
            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def reservedWord(self):
        result = ''
        self.advance() #advance past the '('
        while self.current_char is not None and not self.current_char.isspace():
            result += self.current_char
            self.advance()
        return result
    
    def getString(self):
        result = ''
        self.advance() #advance past the first "
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance() #advance past the second "
        return str(result)
    
    def getLocation(self):
        result = ''
        self.advance() # advance past the colon
        while self.current_char is not None and not self.current_char.isspace():
            result += self.current_char
            self.advance()
        return str(result)
    
    def getInteger(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def getAssignment(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
                      
        token = ARGUMENTS.get(result, Token(ID, result))
        return token
            
    def get_next_token(self):
        """
        Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence apart into tokens
        One token at a time
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isalpha():
                return self.getAssignment()
            
            if self.current_char == '(':
                matchValue = self.reservedWord()
                match matchValue:
                    case 'plan': tokenType = PLAN
                    case 'configuration': tokenType = CONFIG
                    case 'liquid' : tokenType = LIQUID
                    case 'labware' : tokenType = LABWARE
                    case 'protocol' : tokenType = PROTOCOL
                    case 'step' : tokenType = STEP
                    case 'transfer' : tokenType = TRANSFER
                    case _ : tokenType = RESWORD
                                      
                return Token(tokenType, matchValue)
            
            if self.current_char == ')':
                self.advance()
                return Token(DONE, ')')
            
            if self.current_char == '"':
                return Token(STRING, self.getString())
            
            if self.current_char == ':':
                return Token(LOCATION, self.getLocation())
            
            if self.current_char == '[':
                self.advance()
                return Token(STARTARR, '[')
            
            if self.current_char == ']':
                self.advance()
                return Token(ENDARR, ']')
            
            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.getInteger())
            
            self.error()
            
        return Token(EOF, None)

################
# Parser
################
class AST(object):
    pass

class Plan(AST):
    def __init__(self, name, version, config, protocol):
        self.name = name
        self.version = version
        self.config = config
        self.protocol = protocol
        
class Configuration(AST):
    def __init__(self):
        self.declarationList = []
        
class Liquid(AST):
    def __init__(self, liquidName):
        self.liquidName = liquidName
        self.argList = []
        
class Labware(AST):
    def __init__(self, labwareName):
        self.labwareName = labwareName
        self.initVolumes = []
        self.argList = []
        
class Protocol(AST):
    def __init__(self):
        self.stepList = []
        
class Step(AST):
    def __init__(self):
        self.stepActionList = []
        
class Assign(AST):
    def __init__(self, arg, assignment):
        self.arg = arg
        self.assignment = assignment
        
class StepAction(AST):
    def __init__(self, srcLabware, srcLoc, destLabware, destLoc):
        self.sourceLabware = srcLabware
        self.sourceLocation = srcLoc
        self.destinationLabware = destLabware
        self.destinationLocation = destLoc
        
class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
class NoOp(AST):
    pass

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        
    def error(self):
        raise Exception('Invalid syntax')
        
    def eat(self, token_type):
        #Note:  I don't use the token_type, so can probably trim this out
        #but...it could be a way to add another layer of checks in if I wanted
        #to have a more "rigid" parsing approach
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    #################
    # Top Level of Plan
    def plan(self):
        print ("entering plan")
        self.eat(PLAN)
        planName = self.variable()
        print (planName.value)
        version = self.variable()
        print (version.value)
        configuration = self.configuration()
        protocol = self.protocol()
        self.eat(DONE)
        node = Plan(planName, version, configuration, protocol)
        return node
    
    #######################
    # Configuration section
    def configuration(self):
        print ("entering configuration")
        self.eat(CONFIG)
        declarations = self.declList()
        root = Configuration()
        for declaration in declarations:
            root.declarationList.append(declaration)
        print("end of configuration")
        self.eat(DONE)
        return root
    
    #################
    # List of declarations
    # Currently, we have two:  liquid and labware    
    def declList (self):
        print ("entering declList")
        node = self.decl()
        results = [node]
        while self.current_token.type != DONE:
            results.append(self.decl())
        return results
    
    def decl(self):
        print(self.current_token.value)
        if self.current_token.type == LIQUID:
            node = self.liquid()
        elif self.current_token.type == LABWARE:
            node = self.labware()
        else:
            print("I'm here!")
            self.error()
        return node
    
    def liquid(self):
        self.eat(LIQUID)
        liquidName = self.variable()
        liquidRoot = Liquid(liquidName)
        arguments = self.argList()
        for argument in arguments:
            liquidRoot.argList.append(argument)
        self.eat(DONE)
        return liquidRoot
    
    def labware(self):
        self.eat(LABWARE)
        labwareName = self.variable()
        labwareRoot = Labware(labwareName)
        self.eat(STARTARR)
        initVols = self.initVolumes()
        self.eat(ENDARR)
        for initVol in initVols:
            labwareRoot.initVolumes.append(initVol)
        arguments = self.argList()
        for argument in arguments:
            labwareRoot.argList.append(argument)
        self.eat(DONE)
        print("end of labware")
        return labwareRoot
        
    def initVolumes(self):
        initVols = []
        while self.current_token.type != ENDARR:
            initVols.append(self.initVolume())
        return initVols
    
    def initVolume(self):
        node = self.variable()
        print ("volume: ", node.value)
        return node
    
    def argList(self):
        arguments = []
        while self.current_token.type != DONE:
            arguments.append(self.argument())
        return arguments
            
    def argument(self):
        arg = self.argName()
        self.eat(ASSIGN)
        argValue = self.variable()
        print("argValue: ", argValue.value)
        node = Assign(arg, argValue)
        return node
                
    def argName(self):
        print("argName:", self.current_token.value)
        if ARGUMENTS.get(self.current_token.type) != None:
            node = Variable(self.current_token)
            self.eat(self.current_token.type)
            return node
        else:
            self.error()
    
    ######################
    # Protocol definition section
    def protocol(self):
        print ("entering protocol")
        self.eat(CONFIG)
        steps = self.stepList()
        root = Protocol()
        for step in steps:
            root.stepList.append(step)
        print("end of protocol")
        self.eat(DONE)
        return root        
    
    def steps(self):
        print ("entering stepList")
        node = self.step()
        results = [node]
        while self.current_token.type != DONE:
            results.append(self.step())
        return results        
        
    ####################
    # Generic parsing blocks
    def variable(self):
        node = Variable(self.current_token)
        if node.token.type == STRING:
            self.eat(STRING)
        elif node.token.type == INTEGER:
            self.eat(INTEGER)
        elif node.token.type == ID:  #This is a hack:  I'm getting argument values showing up as IDs
            self.eat(ID)
            node.token.type = STRING
        return node
            
    def empty(self):
        """An empty production"""
        return NoOp()
        
    def parse(self):
        node = self.plan()
        if self.current_token.type != EOF:
            self.error()
        return (node)
    

################
# Interpreter
################

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer #set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()
        
    def error(self):
        raise Exception('Invalid syntax')
        
    def eat(self, token_type):
        #compare the current token type with the passed token type and if they
        #match then "eat" the current token and assign the next token to the 
        #self.current_token, otherwise, raise an exception.
        #if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        #else:
            #self.error()
            
    def expr(self):
        """list out the tokens"""
        while self.current_token.type != EOF:
            token = self.current_token
            print(repr(self.current_token))
            match token.type:
                case _:
                    self.eat(EOF)
                    #print(repr(self.current_token))

def main():
    lexer = Lexer(fileText)
    parser = Parser(lexer)
    result = parser.parse()
#    interpreter = Interpreter(lexer)
#    result = interpreter.expr()
    print(result)
    
if __name__ == '__main__':
    main()

#print(lexemeList)