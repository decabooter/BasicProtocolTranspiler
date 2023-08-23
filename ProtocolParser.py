# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:06:46 2023

@author: decabooter
"""
import Constants

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
    def __init__(self, stepID):
        self.stepID = stepID
        self.stepActionList = []
        
class Assign(AST):
    def __init__(self, arg, assignment):
        self.arg = arg
        self.assignment = assignment
        
class StepAction(AST):
    def __init__(self, action, srcLabware, srcLoc, destLabware, destLoc, volume):
        self.action = action
        self.sourceLabware = srcLabware
        self.sourceLocation = srcLoc
        self.destinationLabware = destLabware
        self.destinationLocation = destLoc
        self.volume = volume
        
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
        self.eat(Constants.PLAN)
        planName = self.variable()
        print (planName.value)
        version = self.variable()
        print (version.value)
        configuration = self.configuration()
        protocol = self.protocol()
        self.eat(Constants.DONE)
        node = Plan(planName, version, configuration, protocol)
        return node
    
    #######################
    # Configuration section
    def configuration(self):
        print ("entering configuration")
        self.eat(Constants.CONFIG)
        declarations = self.declList()
        root = Configuration()
        for declaration in declarations:
            root.declarationList.append(declaration)
        print("end of configuration")
        self.eat(Constants.DONE)
        return root
    
    #################
    # List of declarations
    # Currently, we have two:  liquid and labware    
    def declList (self):
        print ("entering declList")
        node = self.decl()
        results = [node]
        while self.current_token.type != Constants.DONE:
            results.append(self.decl())
        return results
    
    def decl(self):
        print(self.current_token.value)
        if self.current_token.type == Constants.LIQUID:
            node = self.liquid()
        elif self.current_token.type == Constants.LABWARE:
            node = self.labware()
        else:
            print("I'm here!")
            self.error()
        return node
    
    def liquid(self):
        self.eat(Constants.LIQUID)
        liquidName = self.variable()
        liquidRoot = Liquid(liquidName)
        arguments = self.argList()
        for argument in arguments:
            liquidRoot.argList.append(argument)
        self.eat(Constants.DONE)
        return liquidRoot
    
    def labware(self):
        self.eat(Constants.LABWARE)
        labwareName = self.variable()
        labwareRoot = Labware(labwareName)
        self.eat(Constants.STARTARR)
        initVols = self.initVolumes()
        self.eat(Constants.ENDARR)
        for initVol in initVols:
            labwareRoot.initVolumes.append(initVol)
        arguments = self.argList()
        for argument in arguments:
            labwareRoot.argList.append(argument)
        self.eat(Constants.DONE)
        print("end of labware")
        return labwareRoot
        
    def initVolumes(self):
        initVols = []
        while self.current_token.type != Constants.ENDARR:
            initVols.append(self.initVolume())
        return initVols
    
    def initVolume(self):
        node = self.variable()
        print ("volume: ", node.value)
        return node
    
    def argList(self):
        arguments = []
        while self.current_token.type != Constants.DONE:
            arguments.append(self.argument())
        return arguments
            
    def argument(self):
        arg = self.argName()
        self.eat(Constants.ASSIGN)
        argValue = self.variable()
        print("argValue: ", argValue.value)
        node = Assign(arg, argValue)
        return node
                
    def argName(self):
        print("argName:", self.current_token.value)
        if Constants.ARGUMENTS.get(self.current_token.type) != None:
            node = Variable(self.current_token)
            self.eat(self.current_token.type)
            return node
        else:
            self.error()
    
    ######################
    # Protocol definition section
    def protocol(self):
        print ("entering protocol")
        self.eat(Constants.PROTOCOL)
        steps = self.stepList()
        root = Protocol()
        for step in steps:
            root.stepList.append(step)
        print("end of protocol")
        self.eat(Constants.DONE)
        return root        
    
    def stepList(self):
        print ("entering stepList")
        node = self.step()
        results = [node]
        while self.current_token.type != Constants.DONE:
            results.append(self.step())
        return results        
    
    def step(self):
        print ("entering step")
        self.eat(Constants.STEP)
        stepID = self.variable()
        node = Step(stepID)
        while self.current_token.type != Constants.DONE:
            node.stepActionList.append(self.stepAction())
        self.eat(Constants.DONE)
        return node
        
    def stepAction(self):
        print ("entering stepAction")
        action = self.action()
        sourceLabware = self.variable()
        sourceLocation = self.location()
        destinationLabware = self.variable()
        destinationLocation = self.location() 
        volume = self.variable()
        node = StepAction(action, sourceLabware, sourceLocation, destinationLabware, 
                          destinationLocation, volume)
        self.eat(Constants.DONE)
        return node
    
    def action(self):
        node = Variable(self.current_token)
        self.eat(Constants.TRANSFER)
        print("action")
        return node
    
    def location(self):
        node = Variable(self.current_token)
        self.eat(Constants.LOCATION)
        return node
        
    ####################
    # Generic parsing blocks
    def variable(self):
        node = Variable(self.current_token)
        if node.token.type == Constants.STRING:
            self.eat(Constants.STRING)
        elif node.token.type == Constants.INTEGER:
            self.eat(Constants.INTEGER)
        elif node.token.type == Constants.ID:  #This is a hack:  I'm getting argument values showing up as IDs
            self.eat(Constants.ID)
            node.token.type = Constants.STRING
        return node
            
    def empty(self):
        """An empty production"""
        return NoOp()
        
    def parse(self):
        node = self.plan()
        if self.current_token.type != Constants.EOF:
            self.error()
        return (node)
    
