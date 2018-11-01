import io
import hashlib
import logging
import os
import struct
import random

from HintList import getHint, getHintGroup, Hint
from ItemList import eventlocations
from Messages import update_message_by_id
from TextBox import lineWrap
from Utils import random_choices

gossipLocations = {
    0x0401: 'Zoras Fountain (Fairy)',
    0x0402: 'Zoras Fountain (Jabu)',
    0x0403: 'Lake Hylia (Lab)',
    0x0404: 'Death Mountain Trail (Biggoron)',
    0x0405: 'Death Mountain Crater (Bombable Wall)',
    0x0406: 'Temple of Time (Left)',
    0x0407: 'Temple of Time (Left-Center)',
    0x0408: 'Lake Hylia (Southwest Corner)',
    0x0409: 'Zoras Domain (Mweep)',
    0x040A: 'Graveyard (Shadow Temple)',
    0x040B: 'Hyrule Castle (Rock Wall)',
    0x040C: 'Zoras River (Waterfall)',
    0x040D: 'Zoras River (Plateau)',
    0x040E: 'Temple of Time (Right-Center)',
    0x040F: 'Lake Hylia (Southeast Corner)',
    0x0410: 'Temple of Time (Right)',
    0x0411: 'Gerudo Valley (Waterfall)',
    0x0412: 'Hyrule Castle (Malon)',
    0x0413: 'Hyrule Castle (Storms Grotto)',
    0x0414: 'Dodongos Cavern (Bombable Wall)',
    0x0415: 'Goron City (Maze)',
    0x0416: 'Sacred Forest Meadow (Maze Lower)',
    0x0417: 'Sacred Forest Meadow (Maze Upper)',
    0x0418: 'Generic Grotto',
    0x0419: 'Goron City (Medigoron)',
    0x041A: 'Desert Colossus (Spirit Temple)',
    0x041B: 'Hyrule Field (Hammer Grotto)',
    0x041C: 'Sacred Forest Meadow (Saria)',
    0x041D: 'Lost Woods (Bridge)',
    0x041E: 'Kokiri Forest (Storms)',
    0x041F: 'Kokiri Forest (Deku Tree Left)',
    0x0420: 'Kokiri Forest (Deku Tree Right)'
}

def buildHintString(hintString):
    if len(hintString) < 77:
        hintString = "They say that " + hintString
    elif len(hintString) < 82:
        hintString = "They say " + hintString
    # captitalize the sentance
    hintString = hintString[:1].upper() + hintString[1:]

    return hintString


def getItemGenericName(item):
    if item.type == 'Map' or item.type == 'Compass' or item.type == 'BossKey' or item.type == 'SmallKey' or item.type == 'FortressSmallKey':
        return item.type
    else:
        return item.name


def isRestrictedDungeonItem(dungeon, item):
    if (item.map or item.compass) and dungeon.world.shuffle_mapcompass == 'dungeon':
        return item in dungeon.dungeon_items
    if item.smallkey and dungeon.world.shuffle_smallkeys == 'dungeon':
        return item in dungeon.small_keys
    if item.bosskey and dungeon.world.shuffle_bosskeys == 'dungeon':
        return item in dungeon.boss_key
    return False


def add_hint(world, id, text):
    world.spoiler.hints[id] = lineWrap(text)


def writeGossipStoneHintsHints(world, messages):
    for id,text in world.spoiler.hints.items():
        update_message_by_id(messages, id, get_raw_text(text))

def filterTrailingSpace(text):
    if text.endswith('& '):
        return text[:-1]
    else:
        return text

hintPrefixes = [
    'a few ',
    'some ',
    'plenty of ',
    'a ',
    'an ',
    'the ',
    '',
]

def getSimpleHintNoPrefix(item):
    hint = getHint(item.name, True).text

    for prefix in hintPrefixes:
        if hint.startswith(prefix):
            # return without the prefix
            return hint[len(prefix):]

    # no prefex
    return hint

def colorText(text, color):
    colorMap = {
        'White':      '\x40',
        'Red':        '\x41',
        'Green':      '\x42',
        'Blue':       '\x43',
        'Light Blue': '\x44',
        'Pink':       '\x45',
        'Yellow':     '\x46',
        'Black':      '\x47',
    }

    colorTags = False
    while True:
        splitText = text.split('#', 2)
        if len(splitText) == 3:
            splitText[1] = '\x05' + colorMap[color] + splitText[1] + '\x05\x40'
            text = ''.join(splitText)
            colorTags = True
        else:
            text = '#'.join(splitText)
            break

    if not colorTags:
        for prefix in hintPrefixes:
            if text.startswith(prefix):
                text = text[:len(prefix)] + '\x05' + colorMap[color] + text[len(prefix):] + '\x05\x40'
                break

    return text


def get_woth_hint(world, checked):
    locations = world.spoiler.required_locations[world.id]
    locations = list(filter(lambda location: location.name not in checked, locations))
    if not locations:
        return None

    location = random.choice(locations)
    checked.append(location.name)

    if location.parent_region.dungeon:
        return buildHintString(colorText(getHint(location.parent_region.dungeon.name, world.clearer_hints).text, 'Light Blue') + \
            " is on the way of the hero.")
    else:
        return buildHintString(colorText(location.hint, 'Light Blue') + " is on the way of the hero.")


def get_good_loc_hint(world, checked):
    locations = getHintGroup('location', world)
    locations = list(filter(lambda hint: hint.name not in checked, locations))
    if not locations:
        return None

    hint = random.choice(locations)
    location = world.get_location(hint.name)
    checked.append(location)

    return buildHintString(colorText(getHint(location.name, world.clearer_hints).text, 'Green') + " " + \
                colorText(getHint(getItemGenericName(location.item), world.clearer_hints).text, 'Red') + ".")


def get_good_item_hint(world, checked):
    locations = [location for location in world.get_locations() 
            if not location.name in checked and \
            location.item.majoritem and \
            not location.locked]
    if not locations:
        return None

    location = random.choice(locations)
    checked.append(location.name)

    if location.parent_region.dungeon:
        return buildHintString(colorText(getHint(location.parent_region.dungeon.name, world.clearer_hints).text, 'Green') + \
            " hoards " + colorText(getHint(getItemGenericName(location.item), world.clearer_hints).text, 'Red') + ".")
    else:
        return buildHintString(colorText(getHint(getItemGenericName(location.item), world.clearer_hints).text, 'Red') + \
            " can be found at " + colorText(location.hint, 'Green') + ".")


def get_overworld_hint(world, checked):
    locations = [location for location in world.get_locations()
            if not location.name in checked and \
            location.item.type != 'Event' and \
            location.item.type != 'Shop' and \
            not location.locked and \
            not location.parent_region.dungeon]
    if not locations:
        return None

    location = random.choice(locations)
    checked.append(location.name)

    return buildHintString(colorText(getHint(getItemGenericName(location.item), world.clearer_hints).text, 'Red') + \
        " can be found at " + colorText(location.hint, 'Green') + ".")


def get_dungeon_hint(world, checked):
    dungeons = list(filter(lambda dungeon: dungeon.name not in checked, world.dungeons))
    if not dungeons:
        return None

    dungeon = random.choice(dungeons)
    checked.append(dungeon.name)

    # Choose a random dungeon location that is a non-dungeon item
    locations = [location for region in dungeon.regions for location in region.locations
        if location.name not in checked and \
           location.item.type != 'Event' and \
           location.item.type != 'Shop' and \
           not isRestrictedDungeonItem(dungeon, location.item) and \
           not location.locked]
    if not locations:
        return get_dungeon_hint(world, checked)

    location = random.choice(locations)
    checked.append(location.name)

    return buildHintString(colorText(getHint(dungeon.name, world.clearer_hints).text, 'Green') + " hoards " + \
        colorText(getHint(getItemGenericName(location.item), world.clearer_hints).text, 'Red') + ".")


def get_junk_hint(world, checked):
    hints = getHintGroup('junkHint', world)
    hints = list(filter(lambda hint: hint.name not in checked, hints))
    if not hints:
        return None

    hint = random.choice(hints)
    checked.append(hint.name)
    
    return hint.text


hint_func = {
    'woth': get_woth_hint,
    'loc': get_good_loc_hint,
    'item': get_good_item_hint,
    'ow': get_overworld_hint,
    'dungeon': get_dungeon_hint,
    'junk': get_junk_hint,
}


#builds out general hints based on location and whether an item is required or not
def buildGossipHints(world):

    stoneIDs = list(gossipLocations.keys())

    # Don't repeat hints
    checkedLocations = []

    #shuffles the stone addresses for randomization, always locations will be placed first
    random.shuffle(stoneIDs)

    # Add trial hints
    if world.trials < 6 and world.trials > 3:
        for trial,skipped in world.skipped_trials.items():
            if skipped:
                add_hint(world, stoneIDs.pop(0), buildHintString("the " + colorText(trial + " Trial", 'Yellow') + " was dispelled by Sheik."))
    elif world.trials <= 3 and world.trials > 0:
        for trial,skipped in world.skipped_trials.items():
            if not skipped:
                add_hint(world, stoneIDs.pop(0), buildHintString("the " + colorText(trial + " Trial", 'Pink') + " protects Ganon's Tower."))

    # Add required location hints
    alwaysLocations = getHintGroup('alwaysLocation', world)
    for hint in alwaysLocations:
        location = world.get_location(hint.name)
        checkedLocations.append(hint.name)   
        add_hint(world, stoneIDs.pop(0), buildHintString(colorText(getHint(location.name, world.clearer_hints).text, 'Green') + " " + \
            colorText(getHint(getItemGenericName(location.item), world.clearer_hints).text, 'Red') + "."))


    hint_types = list(hint_func.keys())
    hint_dist = [1,1,1,1,1,1]

    while stoneIDs:
        [hint_type] = random_choices(hint_types, weights=hint_dist)

        hint = hint_func[hint_type](world, checkedLocations)
        if hint != None:
            add_hint(world, stoneIDs.pop(0), hint)


# builds boss reward text that is displayed at the temple of time altar for child and adult, pull based off of item in a fixed order.
def buildBossRewardHints(world, messages):
    bossRewardsSpiritualStones = ['Kokiri Emerald', 'Goron Ruby', 'Zora Sapphire']
    bossRewardsMedallions = ['Forest Medallion', 'Fire Medallion', 'Water Medallion', 'Shadow Medallion', 'Spirit Medallion', 'Light Medallion']

    # text that appears at altar as a child.
    text = '\x08'
    text += get_raw_text(getHint('Spiritual Stone Text Start', world.clearer_hints).text)
    for reward in bossRewardsSpiritualStones:
        text += buildBossString(reward, world)

    text = setRewardColor(text)
    text += get_raw_text(getHint('Spiritual Stone Text End', world.clearer_hints).text)
    text += '\x0B'

    update_message_by_id(messages, 0x707a, text, 0x20)


    # text that appears at altar as an adult.
    start = '\x08When evil rules all, an awakening\x01voice from the Sacred Realm will\x01call those destined to be Sages,\x01who dwell in the \x05\x41five temples\x05\x40.\x04'
    text = ''
    for reward in bossRewardsMedallions:
        text += buildBossString(reward, world)

    text = setRewardColor(text)
    text += get_raw_text(getHint('Medallion Text End', world.clearer_hints).text)
    text += '\x0B'

    update_message_by_id(messages, 0x7057, start + text, 0x20)

# pulls text string from hintlist for reward after sending the location to hintlist.
def buildBossString(reward, world):
    text = ''
    for location in world.get_locations():
        if location.item.name == reward:
            text += '\x08' + get_raw_text(getHint(location.name, world.clearer_hints).text)
    return text

# alternates through color set commands in child and adult boss reward hint strings setting the colors at the start of the string to correspond with the reward found at the location.
# skips over color commands at the end of stings to set color back to white.
def setRewardColor(text):
    rewardColors = ['\x42', '\x41', '\x43', '\x45', '\x46', '\x44']

    colorWhite = True
    for i, char in enumerate(text):
        if char == '\x05' and colorWhite:
            text = text[:i + 1] + rewardColors.pop(0) + text[i + 2:]
            colorWhite = False 
        elif char == '\x05' and not colorWhite:
            colorWhite = True
        
    return text

# fun new lines for Ganon during the final battle
def buildGanonText(world, messages):
    # empty now unused messages to make space for ganon lines
    update_message_by_id(messages, 0x70C8, " ")
    update_message_by_id(messages, 0x70C9, " ")
    update_message_by_id(messages, 0x70CA, " ")

    # lines before battle
    text = '\x08'
    ganonLines = getHintGroup('ganonLine', world)
    random.shuffle(ganonLines)
    text = get_raw_text(ganonLines.pop().text)
    update_message_by_id(messages, 0x70CB, text)

    # light arrow hint or validation chest item
    text = '\x08'
    if world.trials == 0:
        for location in world.get_locations():
            if location.item.name == 'Light Arrows':
                text = get_raw_text(getHint('Light Arrow Location', world.clearer_hints).text)
                location_hint = location.hint.replace('Ganon\'s Castle', 'my castle')
                location_hint = location.hint.replace('Ganon\'s Tower', 'my tower')
                text += get_raw_text(location_hint)
                text += '!'
                break
    else:
        text = get_raw_text(getHint('Validation Line', world.clearer_hints).text)
        for location in world.get_locations():
            if location.name == 'Ganons Tower Boss Key Chest':
                text += get_raw_text(getHint(getItemGenericName(location.item), world.clearer_hints).text)
                text += '!'
                break
    
    update_message_by_id(messages, 0x70CC, text)
        
def get_raw_text(string):
    text = ''
    for char in string:
        if char == '^':
            text += '\x04' # box break
        elif char == '&':
            text += '\x01' #new line
        elif char == '@':
            text += '\x0F' #print player name
        elif char == '#':
            text += '\x05\x40' #sets color to white
        else:
            text += char
    return text
