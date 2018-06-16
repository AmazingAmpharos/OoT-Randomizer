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

# builds boss reward text that is displayed at the temple of time altar for child and adult, pull based off of item in a fixed order.
def buildBossRewardHints(world, rom):
    bossRewardsSpiritualStones = ['Kokiri Emerald', 'Goron Ruby', 'Zora Sapphire']
    bossRewardsMedallions = ['Forest Medallion', 'Fire Medallion', 'Water Medallion', 'Shadow Medallion', 'Spirit Medallion', 'Light Medallion']

    # text that appears at altar as a child.
    Block_code = []
    Block_code = getBytes(getHint('Spiritual Stone Text Start').text)
    for reward in bossRewardsSpiritualStones:
        buildBossString(Block_code, reward, world)

    Block_code = setRewardColor(Block_code)
    Block_code.extend(getBytes(getHint('Spiritual Stone Text End').text))
    Block_code.extend([0x0B])
    endText(Block_code)
    rom.write_bytes(0x95ED95, Block_code)

    # text that appears at altar as an adult.
    Block_code = []    
    for reward in bossRewardsMedallions:
        buildBossString(Block_code, reward, world)

    Block_code = setRewardColor(Block_code)
    Block_code.extend(getBytes(getHint('Medallion Text End').text))
    Block_code.extend([0x0B])
    endText(Block_code)
    rom.write_bytes(0x95DB94, Block_code)
    
    return rom

# pulls text string from hintlist for reward after sending the location to hintlist.
def buildBossString(Block_code, reward, world):
    for location in world.get_locations():
        if location.item.name == reward:
            Block_code.extend([0x08])
            Block_code.extend(getBytes(getHint(location.name).text))

    return Block_code

# alternates through color set commands in child and adult boss reward hint strings setting the colors at the start of the string to correspond with the reward found at the location.
# skips over color commands at the end of stings to set color back to white.
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

# fun new lines for Ganon during the final battle
def buildGanonText(world, rom):
    # reorganize text header files to make space for text
    rom.write_bytes(0xB884B1, [0x03, 0x41, 0xED])
    rom.write_bytes(0xB884B9, [0x03, 0x41, 0xEE])
    rom.write_bytes(0xB884C1, [0x03, 0x41, 0xEF])
    rom.write_bytes(0xB884C9, [0x03, 0x42, 0x99])

    # clear space for new text
    for address in range(0x9611EC, 0x961349):
        rom.write_byte(address, 0x08)

    Block_code = []
    # lines before battle, 160 characters max
    ganonLines = getHintGroup('ganonLine')
    random.shuffle(ganonLines)
    Block_code = getBytes(ganonLines.pop().text)
    endText(Block_code)
    rom.write_bytes(0x9611F1, Block_code)

    if world.fast_ganon:
        for location in world.get_locations():
            if location.item.name == 'Light Arrows':
                Block_code = getBytes(getHint('Light Arrow Location').text)
                Block_code.extend(getBytes(location.hint))
                Block_code.extend(getBytes('!'))
                break
        endText(Block_code)
    else:
        Block_code = getBytes(getHint('Validation Line').text)
        for location in world.get_locations():
            if location.name == 'Ganons Tower Boss Key Chest':
                Block_code.extend(getBytes((getHint(location.item.name).text)))
        endText(Block_code)
    
    rom.write_bytes(0x96129D, Block_code)

    return rom

#sets the end of text byte in the text box.
def endText(byteArray):
    return byteArray.extend([0x02])

# reads array of characters and converts them to an array of bytes.
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
        
