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
            advancement, priority, type, code, index = item_table[item]
            ret.append(Item(item, advancement, priority, type, code, index))
        else:
            logging.getLogger('').warning('Unknown Item: %s', item)
            return None

    if singleton:
        return ret[0]
    return ret


# Format: Name: (Advancement, Priority, Type, ItemCode, Index)
item_table = {'Bow': (True, False, None, 0x0080, 0x01),
              'Progressive Hookshot': (True, False, None, 0x0120, 0x09),
              'Hammer': (True, False, None, 0x01A0, 0x0D),
              'Slingshot': (True, False, None, 0x00A0, 0x05),
              'Boomerang': (True, False, None, 0x00C0, 0x06),
              'Bomb Bag': (True, False, None, 0x0640, 0x34),
              'Dins Fire': (True, False, None, 0x0B80, 0x5C),
              'Farores Wind': (False, True, None, 0x0BA0, 0x5D),
              'Fairy Ocarina': (True, False, None, 0x0760, 0x3B),
              'Ocarina of Time': (True, False, None, 0x0180, 0x0C),
              'Bottle': (True, False, None, 0x01E0, 0x0F),
              'Kokiri Sword': (True, False, None, 0x04E0, 0x27),
              'Master Sword': (True, False, None, None, None),
              'Deku Shield': (False, True, None, 0x0520, 0x29),
              'Hylian Shield': (False, True, None, 0x0540, 0x2A),
              'Progressive Strength Upgrade': (True, False, None, 0x06C0, 0x36),
              'Progressive Scale': (True, False, None, 0x0700, 0x38),
              'Piece of Heart': (False, True, None, 0x07C0, 0x3E),
              'Recovery Heart': (False, False, None, 0x0900, 0x48),
              'Arrows (5)': (False, False, None, 0x0920, 0x49),
              'Arrows (10)': (False, False, None, 0x0940, 0x4A),
              'Arrows (30)': (False, False, None, 0x0960, 0x4B),
              'Bombs (5)': (False, False, None, 0x0020, 0x01),
              'Rupee (1)': (False, False, None, 0x0980, 0x4C),
              'Rupees (5)': (False, False, None, 0x09A0, 0x4D),
              'Rupees (20)': (False, False, None, 0x09C0, 0x4E),
              'Rupees (50)': (False, False, None, 0x0AA0, 0x55),
              'Rupees (200)': (False, False, None, 0x0AC0, 0x56),
              'Map': (False, False, 'Map', 0x0820, 0x41),
              'Compass': (False, False, 'Compass', 0x0800, 0x40),
              'Boss Key': (False, False, 'BossKey', 0x07E0, 0x3F),
              'Small Key': (False, False, 'SmallKey', 0x0840, 0x42),
              'Map (Deku Tree)': (False, False, 'Map', 0x0820, 0x41),
              'Compass (Deku Tree)': (False, False, 'Compass', 0x0800, 0x40),
              'Map (Dodongos Cavern)': (False, False, 'Map', 0x0820, 0x41),
              'Compass (Dodongos Cavern)': (False, False, 'Compass', 0x0800, 0x40),
              'Map (Jabu Jabus Belly)': (False, False, 'Map', 0x0820, 0x41),
              'Compass (Jabu Jabus Belly)': (False, False, 'Compass', 0x0800, 0x40),
              'Map (Forest Temple)': (False, False, 'Map', 0x0820, 0x41),
              'Compass (Forest Temple)': (False, False, 'Compass', 0x0800, 0x40),
              'Boss Key (Forest Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
              'Small Key (Forest Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
              'Zeldas Letter': (True, False, None, None, None),
              'Zeldas Lullaby': (True, False, 'Song', 0x0A, 0x5),
              'Eponas Song': (True, False, 'Song', 0x09, 0x4),
              'Suns Song': (True, False, 'Song', 0x0B, 0x2),
              'Sarias Song': (True, False, 'Song', 0x08, 0x3),
              'Song of Time': (True, False, 'Song', 0x0C, 0x1),
              'Song of Storms': (True, False, 'Song', 0x0D, 0x0),
              'Minuet of Forest': (True, False, 'Song', 0x02, 0xB),
              'Prelude of Light': (True, False, 'Song', 0x07, 0x6),
              'Bottle with Letter': (True, False, 'Event', 0x02A0, None),
              'Magic Meter': (True, False, 'Event', None, None),
              'Kokiri Emerald': (True, False, 'Event', None, None),
              'Goron Ruby': (True, False, 'Event', None, None),
              'Zora Sapphire': (True, False, 'Event', None, None),
              'Forest Medallion': (True, False, 'Event', None, None),
              'Triforce': (True, False, 'Event', None, None)}