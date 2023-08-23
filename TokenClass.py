# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 16:48:11 2023

@author: decabooter
"""

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
    