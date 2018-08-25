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
item_table = {'Bow': (True, False, None, 0x0620, 0x31),
              'Hookshot': (True, False, None, 0x0120, 0x09),
              'Bomb Bag': (True, False, None, 0x0680, 0x34),
              'Lens of Truth': (True, False, None, 0x0140, 0x0A),
              'Fire Arrows': (True, False, None, 0x0B00, 0x58),
              'Ice Arrows': (True, False, None, 0x0B20, 0x59),
              'Light Arrows': (True, False, None, 0x0B40, 0x5A),
              'Ocarina of Time': (True, False, None, 0x0180, 0x0C),
              'Bottle': (True, False, None, None, None),
              'Bottle with Red Potion': (True, False, None, None, None),
              'Bottle with Gold Dust': (True, False, None, None, None),
              'Bottle with Milk': (True, False, None, None, None),
              'Bottle with Chateau Romani': (True, False, None, None, None),
              'Kokiri Sword': (True, False, None, 0x04E0, 0x27),
              'Gilded Sword': (True, False, None, 0x04E0, 0x27),
              'Hylian Shield': (False, False, None, 0x0540, 0x2A),
              'Mirror Shield': (True, False, None, 0x0560, 0x2B),
              'Goron Mask': (True, False, None, 0x0580, 0x2C),
              'Zora Mask': (True, False, None, 0x05A0, 0x2D),
              'Progressive Wallet': (True, False, None, 0x08C0, 0x46),
              'Piece of Heart': (False, False, None, 0x07C0, 0x3E),
              #'Recovery Heart': (False, True, None, 0x0900, 0x48),
              'Arrows (5)': (False, True, None, 0x0920, 0x49),
              'Arrows (10)': (False, True, None, 0x0940, 0x4A),
              'Arrows (30)': (False, True, None, 0x0960, 0x4B),
              'Bombs (5)': (False, True, None, 0x0020, 0x01),
              'Bombs (10)': (False, True, None, 0x0CC0, 0x66),
              'Bombs (20)': (False, True, None, 0x0CE0, 0x67),
              'Bombchus (5)': (False, False, None, 0x0D40, 0x6A),
              'Bombchus (10)': (False, False, None, 0x0060, 0x03),
              'Bombchus (20)': (False, False, None, 0x0D60, 0x6B),
              'Deku Nuts (5)': (False, True, None, 0x0040, 0x02),
              'Deku Nuts (10)': (False, True, None, 0x0C80, 0x64),
              'Rupee (1)': (False, False, None, 0x0980, 0x4C),
              'Rupees (5)': (False, False, None, 0x09A0, 0x4D),
              'Rupees (20)': (False, False, None, 0x09C0, 0x4E),
              'Rupees (50)': (False, False, None, 0x0AA0, 0x55),
              'Rupees (100)': (False, False, None, 0x0AC0, 0x56),
              'Rupees (200)': (False, False, None, 0x0AC0, 0x56),
              'Ice Trap': (False, True, None, 0x0F80, 0x7C),
              'Magic Bean': (True, False, None, 0x02C0, 0x16),
              'Map': (False, False, 'Map', 0x0820, 0x41),
              'Compass': (False, False, 'Compass', 0x0800, 0x40),
              'Boss Key': (False, False, 'BossKey', 0x07E0, 0x3F),
              'Small Key': (False, False, 'SmallKey', 0x0840, 0x42),
              'Map (Woodfall Temple)': (False, False, 'Map', 0x0820, 0x41),
              'Compass (Woodfall Temple)': (False, False, 'Compass', 0x0800, 0x40),
              'Boss Key (Woodfall Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
              'Small Key (Woodfall Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
              'Map (Snowhead Temple)': (False, False, 'Map', 0x0820, 0x41),
              'Compass (Snowhead Temple)': (False, False, 'Compass', 0x0800, 0x40),
              'Boss Key (Snowhead Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
              'Small Key (Snowhead Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
              'Map (Great Bay Temple)': (False, False, 'Map', 0x0820, 0x41),
              'Compass (Great Bay Temple)': (False, False, 'Compass', 0x0800, 0x40),
              'Boss Key (Great Bay Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
              'Small Key (Great Bay Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
              'Map (Stone Tower Temple)': (False, False, 'Map', 0x0820, 0x41),
              'Compass (Stone Tower Temple)': (False, False, 'Compass', 0x0800, 0x40),
              'Boss Key (Stone Tower Temple)': (False, False, 'BossKey', 0x07E0, 0x3F),
              'Small Key (Stone Tower Temple)': (False, False, 'SmallKey', 0x0840, 0x42),
              'Eponas Song': (True, False, 'Song', None, None),
              'Song of Time': (True, False, 'Song', None, None),
              'Song of Storms': (True, False, 'Song', None, None),
              'Magic Meter': (True, False, 'Event', None, None),
              'Epona': (True, False, 'Event', None, None),
              'Stray Fairy Pickup': (True, False, 'Event', None, None),
              'Odolwas Remains': (True, False, 'Event', None, None),
              'Majoras Mask': (True, False, 'Event', None, None)}

item_data = {'Bow': [0x4C, 0x80, 0x17, 0xEE, 0x00, 0xBE],
              'Progressive Hookshot': [0x0B, 0x80, 0x2E, 0xD7, 0x00, 0xDD],
              'Bomb Bag': [0x4F, 0x80, 0x1A, 0xD8, 0x00, 0xBF],
              'Lens of Truth': [0x0F, 0x80, 0x36, 0x39, 0x00, 0xEA],
              'Fire Arrows': [0x04, 0x80, 0x60, 0x70, 0x01, 0x58],
              'Ice Arrows': [0x0C, 0x80, 0x61, 0x71, 0x01, 0x58],
              'Light Arrows': [0x12, 0x80, 0x62, 0x72, 0x01, 0x58],
              'Bottle': [0x14, 0x80, 0x01, 0x42, 0x00, 0xC6],
              'Bottle with Red Potion': [0x1B, 0x80, 0x45, 0x99, 0x01, 0x0B],
              'Bottle with Milk': [0x1A, 0x80, 0x30, 0x98, 0x00, 0xDF],
              'Kokiri Sword': [0x3B, 0x80, 0x74, 0xA4, 0x01, 0x8D],
              'Hylian Shield': [0x3F, 0xA0, 0xD4, 0x4D, 0x00, 0xDC],
              'Mirror Shield': [0x40, 0x80, 0x3A, 0x4E, 0x00, 0xEE],
              'Goron Mask': [0x42, 0xA0, 0x3C, 0x50, 0x00, 0xF2],
              'Zora Mask': [0x43, 0xA0, 0x3D, 0x51, 0x00, 0xF2],
              'Progressive Wallet': [0x57, 0x80, 0x23, 0xE9, 0x00, 0xD1],
              'Piece of Heart': [0x7A, 0x80, 0x14, 0xC2, 0x00, 0xBD],
              'Recovery Heart': [0x83, 0x80, 0x09, 0x55, 0x00, 0xB7],
              'Arrows (5)': [0x92, 0x48, 0xDB, 0xE6, 0x00, 0xD8],
              'Arrows (10)': [0x93, 0x4A, 0xDA, 0xE6, 0x00, 0xD8],
              'Arrows (30)': [0x94, 0x4A, 0xD9, 0xE6, 0x00, 0xD8],
              'Bombs (5)': [0x8E, 0x59, 0xE0, 0x32, 0x00, 0xCE],
              'Bombs (10)': [0x8F, 0x59, 0xE0, 0x32, 0x00, 0xCE],
              'Bombs (20)': [0x90, 0x59, 0xE0, 0x32, 0x00, 0xCE],
              'Bombchus (5)': [0x96, 0x80, 0xD8, 0x33, 0x00, 0xD9],
              'Bombchus (10)': [0x09, 0x80, 0xD8, 0x33, 0x00, 0xD9],
              'Bombchus (20)': [0x97, 0x80, 0xD8, 0x33, 0x00, 0xD9],
              'Deku Nuts (1)': [0x8C, 0x0C, 0xEE, 0x34, 0x00, 0xBB],
              'Deku Nuts (10)': [0x8D, 0x0C, 0xEE, 0x34, 0x00, 0xBB],
              'Rupee (1)': [0x84, 0x00, 0x93, 0x6F, 0x01, 0x7F],
              'Rupees (5)': [0x85, 0x01, 0x92, 0xCC, 0x01, 0x7F],
              'Rupees (20)': [0x86, 0x02, 0x91, 0xF0, 0x01, 0x7F],
              'Rupees (50)': [0x87, 0x14, 0x8F, 0xF1, 0x01, 0x7F],
              'Rupees (100)': [0x88, 0x13, 0x8E, 0xF2, 0x01, 0x7F],
              'Rupees (200)': [0x88, 0x13, 0x8E, 0xF2, 0x01, 0x7F],
              'Ice Trap': [0x85, 0x01, 0x92, 0xCC, 0x01, 0x7F], # Ice Trap in special spots will become a blue rupee.
              'Eponas Song': 0xD2,
              'Song of Time': 0xD5,
              'Song of Storms': 0xD6,
              'Odolwas Remains': 0xDE,
              'Gohts Remains': 0xDE,
              'Gyorgs Remains': 0xDE,
              'Twinmolds Remains': 0xDE}
