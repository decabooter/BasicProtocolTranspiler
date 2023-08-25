# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 11:55:41 2023

@author: decabooter
"""

def A1to00 (wellLoc):
    rowAlpha = wellLoc[0]
    rowNum = ord(rowAlpha) - 65
    try:
        colNum = int(wellLoc[1:])-1
    except:
        colNum = 10000
    #print(rowNum, colNum)
    location = [rowNum, colNum]
    return(location)

#######################
# Tests
#######################
def test_A1to00():
    assert A1to00("A1") == [0,0], "should be [0,0]"
    assert A1to00("Q15") == [16,14], "should be [16,14]"
    assert not(A1to00("11") == [0,0]), "error case"
    assert not(A1to00("~12") == [0,0]), "error case"
    assert not(A1to00("12A") == [0,0]), "error case"

if __name__ == "__main__":
    test_A1to00()
    print("Everything passed")