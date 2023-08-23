# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 16:44:32 2023

@author: decabooter
"""

from TokenClass import Token

#############
# Token Types
#############

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

    
ARGUMENTS = {
    'aspSpeed' : Token('aspSpeed', 'ASPSPEED'),
    'dispSpeed' : Token('dispSpeed', 'DISPSPEED'),
    'lwType' : Token('lwType', 'LWTYPE'),
}