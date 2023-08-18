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
RPAREN = 'EOTERM'
RESWORD = 'RESWORD'
STRING = 'STRING'
INTEGER = 'INTEGER'
LOCATION = 'LOCATION'
ARGUMENT = 'ARGUMENT'
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
    
    def getArgument(self):
        result = []
        term = ''
        while self.current_char is not None:
            term += self.current_char
            self.advance()
            if self.current_char == '=':
                result.append(term)
                term = ''
                self.advance() #advance past the equals sign; resume loop for arg value
            if self.current_char.isspace() or self.current_char == ')':
                #detects the end of an argument
                break
        result.append(term)  #add argument value to the argument list
        return result
            
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
            
            if self.current_char == '(':
                return Token(RESWORD, self.reservedWord())
            
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            if self.current_char == '"':
                return Token(STRING, self.getString())
            
            if self.current_char == ':':
                return Token(LOCATION, self.getLocation())
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.getInteger())
            
            if not self.current_char.isspace():
                return Token(ARGUMENT, self.getArgument())
            
            self.error()
            
        return Token(EOF, None)

################
# Parser
################
class AST(object):
    pass

class Plan(AST):
    def __init(self, token, children):
        self.token = token
        self.value = token.value
        self.children = []

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
        self.current_token = self.lexer.get_next_token()
        
    

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
    interpreter = Interpreter(lexer)
    result = interpreter.expr()
    print(result)
    
if __name__ == '__main__':
    main()

#print(lexemeList)