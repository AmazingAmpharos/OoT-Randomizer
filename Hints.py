import io
import hashlib
import logging
import os
import struct
import random

from HintList import getHint, getHintGroup, Hint
from Utils import local_path

#builds out general hints based on location and whether an item is required or not
def buildHints(world, rom):
    stoneAddresses = [0x938e4c, 0x938ea7, 0x938f02, 0x938f5d, 0x938fb8, 0x939013, 0x93906e, 0x9390c9, 0x939124, 0x93917f,
                      0x9391da, 0x939235, 0x939290, 0x9392eb, 0x939346, 0x9393a1, 0x9393fc, 0x939457, 0x9394b2, 0x93950d,
                      0x939568, 0x9395c3, 0x93961e, 0x939679, 0x9396d4, 0x93972f, 0x93978a, 0x9397e5, 0x939840, 0x93989b,
                      0x9398f6, 0x939951] #address for gossip stone text boxes, byte limit is 91


    alwaysLocations = getHintGroup('alwaysLocation')#These location will always have a hint somewhere in the world.
    
    sometimesSpace = (int((len(stoneAddresses) - len(alwaysLocations)*2)/2))
    sometimesLocations = getHintGroup('location')#A random selection of these locations will be in the hint pool.
    random.shuffle(sometimesLocations)
    sometimesLocations = sometimesLocations[0:sometimesSpace]
    hintList = alwaysLocations
    hintList.extend(alwaysLocations)
    hintList.extend(sometimesLocations)

    locationData = []
    for hint in  hintList:
        for locationWorld in world.get_locations():
            if hint.name == locationWorld.name:
                locationData.extend([locationWorld])         
            
    #shuffles the stone addresses for randomization, always locations will be placed first and twice
    random.shuffle(stoneAddresses)

    #loops through shuffled locations and addresses and builds hint.
    while locationData:
        currentLoc = locationData.pop(0)
        Block_code = getBytes((getHint(currentLoc.name).text))
        if currentLoc.item.type == 'Map' or currentLoc.item.type == 'Compass' or currentLoc.item.type == 'BossKey' or currentLoc.item.type == 'SmallKey':
            Block_code.extend(getBytes((getHint(currentLoc.item.type).text)))
        else:
            Block_code.extend(getBytes((getHint(currentLoc.item.name).text)))
        endText(Block_code)

        if len(Block_code) > 91:
            print('Too many characters in hint')
            Block_code = getBytes("I am Error.")
            Block_code.extend(getBytes(currentLoc.name))
            Block_code.extend(getBytes('&'))
            Block_code.extend(getBytes(currentLoc.item.name))
            
        rom.write_bytes(stoneAddresses.pop(0), Block_code)

    junkHints = getHintGroup('junkHint')
    random.shuffle(junkHints)
    while stoneAddresses:
        junkHint = junkHints.pop()
        Block_code = getBytes(junkHint.text)
        endText(Block_code)
        rom.write_bytes(stoneAddresses.pop(0), Block_code)
        
    return rom

def endText(byteArray):
    return byteArray.extend([0x02])

def getBytes(string):
    byteCode = []
    for char in string:
        if char == '^':
            byteCode.extend([0x04])#box break
        elif char == '&':
            byteCode.extend([0x01])#new line
        elif char == '@':
            byteCode.extend([0x0F])#print player name
        else:
            char = char.encode('utf-8')
            char = char.hex()
            byte = int('0x' + char, 16)
            byteCode.extend([byte])
    return byteCode
        
