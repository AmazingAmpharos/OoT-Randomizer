import io
import hashlib
import logging
import os
import struct
import random

from HintList import getHint, getHintGroup, Hint
from Utils import local_path

#builds out general hints based on location and whether an item is required or not
def buildGossipHints(world, rom):
    stoneAddresses = [0x938e4c, 0x938EA8, 0x938F04, 0x938F60, 0x938FBC, 0x939018, 0x939074, 0x9390D0, 0x93912C, 0x939188,
                      0x9391E4, 0x939240, 0x93929C, 0x9392F8, 0x939354, 0x9393B0, 0x93940C, 0x939468, 0x9394C4, 0x939520,
                      0x93957C, 0x9395D8, 0x939634, 0x939690, 0x9396EC, 0x939748, 0x9397A4, 0x939800, 0x93985C, 0x9398B8,
                      0x939914, 0x939970] #address for gossip stone text boxes, byte limit is 92


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

    #hopefully fixes weird VC error where the last character from a previous text box would sometimes spill over into the next box.
    for address in range(stoneAddresses[0], 0x9399D8):
        rom.write_byte(address, 0x08)

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

        if len(Block_code) > 92:
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

def buildDungeonRewardHints(world, rom):
    dungeonRewardsSpiritualStones = ['Kokiri Emerald', 'Goron Ruby', 'Zora Sapphire']
    dungeonRewardsMedallions = ['Forest Medallion', 'Fire Medallion', 'Water Medallion', 'Shadow Medallion', 'Spirit Medallion', 'Light Medallion']

    Block_code = []
    Block_code = getBytes(getHint('Spiritual Stone Text Start').text)
    for reward in dungeonRewardsSpiritualStones:
        buildDungeonString(Block_code, reward, world)

    Block_code = setRewardColor(Block_code)
    Block_code.extend(getBytes(getHint('Spiritual Stone Text End').text))
    Block_code.extend([0x0B])
    endText(Block_code)
    rom.write_bytes(0x95ED95, Block_code)

    Block_code = []    
    for reward in dungeonRewardsMedallions:
        buildDungeonString(Block_code, reward, world)

    Block_code = setRewardColor(Block_code)
    Block_code.extend(getBytes(getHint('Medllion Text End').text))
    Block_code.extend([0x0B])
    endText(Block_code)
    rom.write_bytes(0x95DB94, Block_code)
    
    return rom

def buildDungeonString(Block_code, reward, world):
    for location in world.get_locations():
        if location.item.name == reward:
            Block_code.extend([0x08])
            Block_code.extend(getBytes(getHint(location.name).text))

    return Block_code

def setRewardColor(Block_code):
    rewardColors = [0x42, 0x41, 0x43, 0x45, 0x46, 0x44]

    colorWhite = True
    for i, byte in enumerate(Block_code):
        if byte == 0x05 and colorWhite:
            Block_code[i + 1] = rewardColors.pop(0)
            colorWhite = False 
        elif byte == 0x05 and not colorWhite:
            colorWhite = True
        
    return Block_code

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
        elif char == '#':
            byteCode.extend([0x05, 0x40]) #sets color to white
        else:
            char = char.encode('utf-8')
            char = char.hex()
            byte = int('0x' + char, 16)
            byteCode.extend([byte])
    return byteCode
        
