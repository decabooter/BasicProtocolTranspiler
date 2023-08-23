# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:03:13 2023

@author: decabooter
"""

import Constants
import TokenClass as tok

######################
# Lexer
#####################

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
                      
        token = Constants.ARGUMENTS.get(result, tok.Token(Constants.ID, result))
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
                    case 'plan': tokenType = Constants.PLAN
                    case 'configuration': tokenType = Constants.CONFIG
                    case 'liquid' : tokenType = Constants.LIQUID
                    case 'labware' : tokenType = Constants.LABWARE
                    case 'protocol' : tokenType = Constants.PROTOCOL
                    case 'step' : tokenType = Constants.STEP
                    case 'transfer' : tokenType = Constants.TRANSFER
                    case _ : tokenType = Constants.RESWORD
                                      
                return tok.Token(tokenType, matchValue)
            
            if self.current_char == ')':
                self.advance()
                return tok.Token(Constants.DONE, ')')
            
            if self.current_char == '"':
                return tok.Token(Constants.STRING, self.getString())
            
            if self.current_char == ':':
                return tok.Token(Constants.LOCATION, self.getLocation())
            
            if self.current_char == '[':
                self.advance()
                return tok.Token(Constants.STARTARR, '[')
            
            if self.current_char == ']':
                self.advance()
                return tok.Token(Constants.ENDARR, ']')
            
            if self.current_char == '=':
                self.advance()
                return tok.Token(Constants.ASSIGN, '=')
            
            if self.current_char.isdigit():
                return tok.Token(Constants.INTEGER, self.getInteger())
            
            self.error()
            
        return tok.Token(Constants.EOF, None)


################
# LexerLister
#
# This is some code that will extract and print the results of the lexer so you can see the resulting tokens
################

class LexerLister(object):
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
        while self.current_token.type != Constants.EOF:
            token = self.current_token
            print(repr(self.current_token))
            match token.type:
                case _:
                    self.eat(Constants.EOF)
                    #print(repr(self.current_token))
                    