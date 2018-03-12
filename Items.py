import logging

from BaseClasses import Item


def ItemFactory(items):
    ret = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in item_table:
            advancement, priority, type, code = item_table[item]
            ret.append(Item(item, advancement, priority, type, code))
        else:
            logging.getLogger('').warning('Unknown Item: %s', item)
            return None

    if singleton:
        return ret[0]
    return ret


# Format: Name: (Advancement, Priority, Type, ItemCode)
item_table = {'Bow': (True, False, None, 0x0080),
              'Hammer': (True, False, None, 0x01A0),
              'Slingshot': (True, False, None, 0x00A0),
              'Boomerang': (True, False, None, 0x00C0),
              'Bomb Bag': (True, False, None, 0x0640),
              'Dins Fire': (True, False, None, 0x0B80),
              'Farores Wind': (False, True, None, 0x0BA0),
              'Fairy Ocarina': (True, False, None, 0x0760),
              'Ocarina of Time': (True, False, None, 0x0180),
              'Bottle': (True, False, None, 0x01E0),
              'Kokiri Sword': (True, False, None, 0x04E0),
              'Master Sword': (True, False, None, None),
              'Deku Shield': (False, True, None, 0x0520),
              'Hylian Shield': (False, True, None, 0x0540),
              'Goron Bracelet': (True, False, None, 0x0A80),
              'Silver Scale': (True, False, None, 0x06E0),
              'Piece of Heart': (False, True, None, 0x07C0),
              'Recovery Heart': (False, False, None, 0x0900),
              'Bombs (5)': (False, False, None, 0x0020),
              'Rupee (1)': (False, False, None, 0x0980),
              'Rupees (5)': (False, False, None, 0x09A0),
              'Rupees (20)': (False, False, None, 0x09C0),
              'Rupees (50)': (False, False, None, 0x0AA0),
              'Rupees (200)': (False, False, None, 0x0AC0),
              'Map': (False, False, 'Map', 0x0820),
              'Compass': (False, False, 'Compass', 0x0800),
              'Boss Key': (False, False, 'BossKey', 0x07E0),
              'Small Key': (False, False, 'SmallKey', 0x0840),
              'Map (Deku Tree)': (False, False, 'Map', 0x0820),
              'Compass (Deku Tree)': (False, False, 'Compass', 0x0800),
              'Map (Dodongos Cavern)': (False, False, 'Map', 0x0820),
              'Compass (Dodongos Cavern)': (False, False, 'Compass', 0x0800),
              'Map (Jabu Jabus Belly)': (False, False, 'Map', 0x0820),
              'Compass (Jabu Jabus Belly)': (False, False, 'Compass', 0x0800),
              'Zeldas Letter': (True, False, None, None),
              'Zeldas Lullaby': (True, False, 'Song', 0x0A),
              'Suns Song': (True, False, 'Song', 0x0B),
              'Sarias Song': (True, False, 'Song', 0x08),
              'Song of Time': (True, False, 'Song', 0x0C),
              'Bottle with Letter': (True, False, 'Event', 0x02A0),
              'Magic Meter': (True, False, 'Event', None),
              'Darunia is Sad Event': (True, False, 'Event', None),
              'Kokiri Emerald': (True, False, 'Event', None),
              'Goron Ruby': (True, False, 'Event', None),
              'Zora Sapphire': (True, False, 'Event', None),
              'Triforce': (True, False, 'Event', None)}