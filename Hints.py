import io
import hashlib
import logging
import os
import struct
import random

from HintList import getHint, getHintGroup, Hint
from Utils import local_path
from Items import ItemFactory
from ItemList import eventlocations

requiredganonitems = [
    'Bottle',
    'Bottle with Milk',
    'Bottle with Red Potion',
    'Bottle with Green Potion',
    'Bottle with Blue Potion',
    'Bottle with Fairy',
    'Bottle with Fish',
    'Bottle with Blue Fire',
    'Bottle with Bugs',
    'Bottle with Poe',
    'Hammer',
    'Goron Tunic',
    'Progressive Strength Upgrade',
    'Bomb Bag',
    'Progressive Hookshot',
    'Mirror Shield',
    'Magic Meter',
    'Bow',
    'Light Arrows',
]

gooditems = [
    'Bow',
    'Progressive Hookshot',
    'Hammer',
    'Slingshot',
    'Boomerang',
    'Bomb Bag',
    'Lens of Truth',
    'Dins Fire',
    'Farores Wind',
    'Nayrus Love',
    'Fire Arrows',
    'Ice Arrows',
    'Light Arrows',
    'Bottle',
    'Bottle with Letter',
    'Bottle with Milk',
    'Bottle with Red Potion',
    'Bottle with Green Potion',
    'Bottle with Blue Potion',
    'Bottle with Fairy',
    'Bottle with Fish',
    'Bottle with Blue Fire',
    'Bottle with Bugs',
    'Bottle with Poe',
    'Pocket Egg',
    'Pocket Cucco',
    'Cojiro',
    'Odd Mushroom',
    'Odd Potion',
    'Poachers Saw',
    'Broken Sword',
    'Prescription',
    'Eyeball Frog',
    'Eyedrops',
    'Claim Check',
    'Kokiri Sword',
    'Biggoron Sword',
    'Deku Shield',
    'Hylian Shield',
    'Mirror Shield',
    'Goron Tunic',
    'Zora Tunic',
    'Iron Boots',
    'Hover Boots',
    'Progressive Strength Upgrade',
    'Progressive Scale',
    'Progressive Wallet',
    'Deku Stick Capacity',
    'Deku Nut Capacity',
    'Magic Meter',
    'Double Defense',
    'Stone of Agony',
    'Zeldas Lullaby',
    'Eponas Song',
    'Suns Song',
    'Sarias Song',
    'Song of Time',
    'Song of Storms',
    'Minuet of Forest',
    'Prelude of Light',
    'Bolero of Fire',
    'Serenade of Water',
    'Nocturne of Shadow',
    'Requiem of Spirit',
]


# build a formatted string with linebreaks appropriate textboxes
def buildHintString(hintString):
    formatString = ""
    splitHintString = hintString.split()
    lineLength = 0

    if len(hintString) < 77:
        hintString = "They say that " + hintString
    elif len(hintString) < 82:
        hintString = "They say " + hintString
    elif len(hintString) > 91:
        print('Too many characters in hint')
        hintString = hintString[:91]

    for word in splitHintString:
        # let's assume words are not 35 or more char long
        if lineLength + len(word) + 1 <= 35:
            # add a space if line is not empty
            if lineLength != 0:
                lineLength = lineLength + 1
                formatString = formatString + ' '

            # append word
            formatString = formatString + word
            lineLength = lineLength + len(word)
        else:
            # word won'd fit, add to a new line
            formatString = formatString + '&' + word
            lineLength = len(word)

    return formatString


def getItemGenericName(item):
    if item.type == 'Map' or item.type == 'Compass' or item.type == 'BossKey' or item.type == 'SmallKey':
        return item.type
    else:
        return item.name

def isDungeonItem(item):
    return item.type == 'Map' or item.type == 'Compass' or item.type == 'BossKey' or item.type == 'SmallKey'


#builds out general hints based on location and whether an item is required or not
def buildGossipHints(world, rom):
    stoneAddresses = [0x938e4c, 0x938EA8, 0x938F04, 0x938F60, 0x938FBC, 0x939018, 0x939074, 0x9390D0, 0x93912C, 0x939188,
                      0x9391E4, 0x939240, 0x93929C, 0x9392F8, 0x939354, 0x9393B0, 0x93940C, 0x939468, 0x9394C4, 0x939520,
                      0x93957C, 0x9395D8, 0x939634, 0x939690, 0x9396EC, 0x939748, 0x9397A4, 0x939800, 0x93985C, 0x9398B8,
                      0x939914, 0x939970] #address for gossip stone text boxes, byte limit is 92


    # get list of required items that are not events or needed for Ganon's Castle
    requiredItems = [(location, item) for _,sphere in world.spoiler.playthrough.items() for location,item in sphere.items() 
        if ItemFactory(item).type != 'Event' and not location in eventlocations and not item in requiredganonitems]

    # add required non-ganon items for hints (good hints)
    for location,item in random.sample(requiredItems, random.randint(2,4)):
        if random.choice([True, False]):
            print(item)
        else:
            print(location)

    # Don't repeat hints
    checkedLocations = []

    # Add required location hints
    alwaysLocations = getHintGroup('alwaysLocation')
    for hint in alwaysLocations:
        for locationWorld in world.get_locations():
            if hint.name == locationWorld.name:
                checkedLocations.append(hint.name)    
                print(locationWorld.name, ',', locationWorld.item.name)

    # Add good location hints
    sometimesLocations = getHintGroup('location')
    for _ in range(0, random.randint(9,11) - len(alwaysLocations)):
        hint = random.choice(sometimesLocations)
        # Repick if location isn't new
        while hint.name in checkedLocations or hint.name in alwaysLocations:
            hint = random.choice(sometimesLocations)

        for locationWorld in world.get_locations():
            if hint.name == locationWorld.name:
                checkedLocations.append(locationWorld.name)    
                print(locationWorld.name, ',', locationWorld.item.name)

    # add bad dungeon locations hints
    for dungeon in random.sample(world.dungeons, random.randint(3,5)):
        # Choose a randome dungeon location that is a non-dungeon item
        locationWorld = random.choice([location for region in dungeon.regions for location in world.get_region(region).locations
            if location.item.type != 'Event' and \
            not location.name in eventlocations and \
            not isDungeonItem(location.item) and \
            location.item.name != 'Gold Skulltulla Token' and\
            location.item.type != 'Song'])

        checkedLocations.append(locationWorld.name)
        print(dungeon.name, ",", locationWorld.item.name)

    # add bad overworld locations hints
    # only choose location if it is new and a proper item from the overworld
    overworldlocations = [locationWorld for locationWorld in world.get_locations()
            if not locationWorld.name in checkedLocations and \
            not locationWorld.name in alwaysLocations and \
            not locationWorld.name in sometimesLocations and \
            locationWorld.item.type != 'Event' and \
            not locationWorld.name in eventlocations and \
            locationWorld.item.name != 'Gold Skulltulla Token' and \
            not locationWorld.parent_region.dungeon and \
            not locationWorld.name in checkedLocations]
    for locationWorld in random.sample(overworldlocations, random.randint(4,6)):
        checkedLocations.append(locationWorld.name)
        print(locationWorld.parent_region.name, ',', locationWorld.item.name)

    
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

