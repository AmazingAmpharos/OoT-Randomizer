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
    stoneAddresses = [0x938E4C, 0x938E90, 0x938F0C, 0x938F54, 0x938F9C, 0x939000, 0x939058, 0x9390D0, 0x939138, 0x93919C, 0x9391E0,
                      0x939248, 0x9392B0, 0x939308, 0x939378, 0x9393E8, 0x93943C, 0x939488, 0x9394FC, 0x939554, 0x939590, 0x9395D8,
                      0x939630, 0x9396A0, 0x9396EC, 0x939758, 0x9397DC, 0x939834, 0x93988C, 0x9398DC, 0x939954, 0x939994] #address for gossip stone text boxes, byte limit is 60


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
        if currentLoc.item.type == 'Map' or currentLoc.item.type == 'Compass' or currentLoc.item.type == 'Boss Key' or currentLoc.item.type == 'Small Key':
            Block_code.extend(getBytes((getHint(currentLoc.item.type).text)))
        else:
            Block_code.extend(getBytes((getHint(currentLoc.item.name).text)))
        endText(Block_code)

        if len(Block_code) > 60:
            print('Too many characters in hint')
            Block_code = getBytes("I am Error.")
            Block_code.extend(getBytes(currentLoc.name))
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
        
