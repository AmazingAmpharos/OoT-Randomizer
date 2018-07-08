# text details: https://wiki.cloudmodding.com/oot/Text_Format

import random

TABLE_START = 0xB849EC
TEXT_START = 0x92D000

SHOP_ITEM_START = 0xC022CC

# name of type, followed by number of additional bytes to read, follwed by a function that prints the code
CONTROL_CODES = {
    0x00: ('pad', 0, lambda _: '<pad>' ),
    0x01: ('line-break', 0, lambda _: '\n' ),
    0x02: ('end', 0, lambda _: '' ),
    0x04: ('box-break', 0, lambda _: '\n▼\n' ),
    0x05: ('color', 1, lambda d: '<color ' + "{:02x}".format(d) + '>' ),
    0x06: ('gap', 1, lambda d: '<' + str(d) + 'px gap>' ),
    0x07: ('goto', 2, lambda d: '<goto ' + "{:04x}".format(d) + '>' ),
    0x08: ('instant', 0, lambda _: '<allow instant text>' ),
    0x09: ('un-instant', 0, lambda _: '<disallow instant text>' ),
    0x0A: ('keep-open', 0, lambda _: '<keep open>' ),
    0x0B: ('event', 0, lambda _: '<event>' ),
    0x0C: ('box-break-delay', 1, lambda d: '\n▼<wait ' + str(d) + ' frames>\n' ),
    0x0E: ('fade-out', 1, lambda d: '<fade after ' + str(d) + ' frames?>' ),
    0x0F: ('name', 0, lambda _: '<name>' ),
    0x10: ('ocarina', 0, lambda _: '<ocarina>' ),
    0x12: ('sound', 2, lambda d: '<play SFX ' + "{:04x}".format(d) + '>' ),
    0x13: ('icon', 1, lambda d: '<icon ' + "{:02x}".format(d) + '>' ),
    0x14: ('speed', 1, lambda d: '<delay each character by ' + str(d) + ' frames>' ),
    0x15: ('background', 3, lambda d: '<set background to ' + "{:06x}".format(d) + '>' ),
    0x16: ('marathon', 0, lambda _: '<marathon time>' ),
    0x17: ('race', 0, lambda _: '<race time>' ),
    0x18: ('points', 0, lambda _: '<points>' ),
    0x19: ('skulltula', 0, lambda _: '<skulltula count>' ),
    0x1A: ('unskippable', 0, lambda _: '<text is unskippable>' ),
    0x1B: ('two-choice', 0, lambda _: '<start two choice>' ),
    0x1C: ('three-choice', 0, lambda _: '<start three choice>' ),
    0x1D: ('fish', 0, lambda _: '<fish weight>' ),
    0x1E: ('high-score', 1, lambda d: '<high-score ' + "{:02x}".format(d) + '>' ),
    0x1F: ('time', 0, lambda _: '<current time>' ),
}

SPECIAL_CHARACTERS = {
    0x96: 'é',
    0x9F: '[A]',
    0xA0: '[B]',
    0xA1: '[C]',
    0xA2: '[L]',
    0xA3: '[R]',
    0xA4: '[Z]',
    0xA5: '[C Up]',
    0xA6: '[C Down]',
    0xA7: '[C Left]',
    0xA8: '[C Right]',
    0xA9: '[Triangle]',
    0xAA: '[Control Stick]',
}

GOSSIP_STONE_MESSAGES = list( range(0x0401, 0x0421) ) # ids of the actual hints
GOSSIP_STONE_MESSAGES += [0x2053, 0x2054] # shared initial stone messages
TEMPLE_HINTS_MESSAGES = [0x7057, 0x707A] # dungeon reward hints from the temple of time pedestal
LIGHT_ARROW_HINT = [0x70CC] # ganondorf's light arrow hint line

# messages for keysanity item pickup
# ids are in the space freed up by move_shop_item_messages()
KEYSANITY_MESSAGES = {
    0x06: '\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09',
    0x1c: '\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09',
    0x1d: '\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09',
    0x1e: '\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09',
    0x2a: '\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09',
    0x61: '\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for \x05\x47Ganon\'s Castle\x05\x40!\x09',
    0x62: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x42Deku Tree\x05\x40!\x09',
    0x63: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for \x05\x41Dodongo\'s Cavern\x05\x40!\x09',
    0x64: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for \x05\x43Jabu Jabu\'s Belly\x05\x40!\x09',
    0x65: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09',
    0x7c: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09',
    0x7d: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09',
    0x7e: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09',
    0x7f: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09',
    0xa2: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09',
    0x87: '\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x44Ice Cavern\x05\x40!\x09',
    0x88: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x42Deku Tree\x05\x40!\x09',
    0x89: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for \x05\x41Dodongo\'s Cavern\x05\x40!\x09',
    0x8a: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for \x05\x43Jabu Jabu\'s Belly\x05\x40!\x09',
    0x8b: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09',
    0x8c: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09',
    0x8e: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09',
    0x8f: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09',
    0xa3: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09',
    0xa5: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09',
    0x92: '\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x44Ice Cavern\x05\x40!\x09',
    0x93: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09',
    0x94: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09',
    0x95: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09',
    0xa6: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09',
    0xa9: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09',
    0x9b: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09',
    0x9f: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Gerudo Training\x01Grounds\x05\x40!\x09',
    0xa0: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Gerudo Fortress\x05\x40!\x09',
    0xa1: '\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for \x05\x47Ganon\'s Castle\x05\x40!\x09',
}

# convert byte array to an integer
def bytes_to_int(bytes, signed=False):
    return int.from_bytes(bytes, byteorder='big', signed=signed)

# convert int to an array of bytes of the given width
def int_to_bytes(num, width, signed=False):
    return int.to_bytes(num, width, byteorder='big', signed=signed)

def display_code_list(codes):
    message = ""
    for code in codes:
        message += str(code)
    return message

# holds a single character or control code of a string
class Text_Code():

    def display(self):
        if self.code in CONTROL_CODES:
            return CONTROL_CODES[self.code][2](self.data)
        elif self.code in SPECIAL_CHARACTERS:
            return SPECIAL_CHARACTERS[self.code]
        elif self.code >= 0x7F:
            return '?'
        else:
            return chr(self.code)

    # writes the code to the given offset, and returns the offset of the next byte
    def write(self, rom, offset):
        rom.write_byte(TEXT_START + offset, self.code)

        extra_bytes = 0
        if self.code in CONTROL_CODES:
            extra_bytes = CONTROL_CODES[self.code][1]
            bytes_to_write = int_to_bytes(self.data, extra_bytes)
            rom.write_bytes(TEXT_START + offset + 1, bytes_to_write)

        return offset + 1 + extra_bytes

    def __init__(self, code, data):
        self.code = code
        if code in CONTROL_CODES:
            self.type = CONTROL_CODES[code][0]
        else:
            self.type = 'character'
        self.data = data

    __str__ = __repr__ = display

# holds a single message, and all its data
class Message():

    def display(self):
        meta_data = ["#" + str(self.index),
         "ID: 0x" + "{:04x}".format(self.id),
         "Offset: 0x" + "{:06x}".format(self.offset),
         "Length: 0x" + "{:04x}".format(self.unpadded_length) + "/0x" + "{:04x}".format(self.length),
         "Box Type: " + str(self.box_type),
         "Postion: " + str(self.position)]
        return ', '.join(meta_data) + '\n' + self.text

    # check if this is an unused message that just contains it's own id as text
    def is_id_message(self):
        if self.unpadded_length == 5:
            for i in range(4):
                code = self.text_codes[i].code
                if not (code in range(ord('0'),ord('9')+1) or code in range(ord('A'),ord('F')+1) or code in range(ord('a'),ord('f')+1) ):
                    return False
            return True
        return False

    def parse_text(self):
        self.text_codes = []

        index = 0
        while index < self.length:
            next_char = self.raw_text[index]
            data = 0
            index += 1
            if next_char in CONTROL_CODES:
                extra_bytes = CONTROL_CODES[next_char][1]
                if extra_bytes > 0:
                    data = bytes_to_int(self.raw_text[index : index + extra_bytes])
                    index += extra_bytes
            text_code = Text_Code(next_char, data)
            self.text_codes.append(text_code)
            if next_char == 0x02: # message end code
                break
            if next_char == 0x07: # goto
                self.has_goto = True
                self.ending = text_code
            if next_char == 0x0A: # keep-open
                self.has_keep_open = True
                self.ending = text_code
            if next_char == 0x0B: # event
                self.has_event = True
                self.ending = text_code
            if next_char == 0x0E: # fade out
                self.has_fade = True
                self.ending = text_code
            if next_char == 0x10: # ocarina
                self.has_ocarina = True
                self.ending = text_code
            if next_char == 0x1B: # two choice
                self.has_two_choice = True
            if next_char == 0x1C: # three choice
                self.has_three_choice = True
        self.text = display_code_list(self.text_codes)
        self.unpadded_length = index

    def is_basic(self):
        return not (self.has_goto or self.has_keep_open or self.has_event or self.has_fade or self.has_ocarina or self.has_two_choice or self.has_three_choice)

    # writes a Message back into the rom, using the given index and offset to update the table
    # returns the offset of the next message
    def write(self, rom, index, offset, replace_ending=False, ending=None, always_allow_skip=True, speed_up_text=True):

        # construct the table entry
        id_bytes = int_to_bytes(self.id, 2)
        offset_bytes = int_to_bytes(offset, 3)
        entry = id_bytes + bytes([self.opts, 0x00, 0x07]) + offset_bytes
        # write it back
        entry_offset = TABLE_START + 8 * index
        rom.write_bytes(entry_offset, entry)

        ending_codes = [0x02, 0x07, 0x0A, 0x0B, 0x0E, 0x10]
        box_breaks = [0x04, 0x0C]
        slows_text = [0x09, 0x14]

        # speed the text
        if speed_up_text:
            offset = Text_Code(0x08, 0).write(rom, offset) # allow instant

        # write the message
        for code in self.text_codes:
            # ignore ending codes if it's going to be replaced
            if replace_ending and code.code in ending_codes:
                pass
            # ignore the "make unskippable flag"
            elif always_allow_skip and code.code == 0x1A:
                pass
            # ignore anything that slows down text
            elif speed_up_text and code.code in slows_text:
                pass
            elif speed_up_text and code.code in box_breaks:
                offset = Text_Code(0x04, 0).write(rom, offset) # un-delayed break
                offset = Text_Code(0x08, 0).write(rom, offset) # allow instant
            else:
                offset = code.write(rom, offset)

        if replace_ending:
            if ending:
                offset = ending.write(rom, offset) # write special ending
            offset = Text_Code(0x02, 0).write(rom, offset) # write end code


        while offset % 4 > 0:
            offset = Text_Code(0x00, 0).write(rom, offset) # pad to 4 byte align

        return offset

    def __init__(self, raw_text, index, id, opts, offset, length):

        self.raw_text = raw_text

        self.index = index
        self.id = id
        self.opts = opts
        self.box_type = (self.opts & 0xF0) >> 4
        self.position = (self.opts & 0x0F)
        self.offset = offset
        self.length = length

        self.has_goto = False
        self.has_keep_open = False
        self.has_event = False
        self.has_fade = False
        self.has_ocarina = False
        self.has_two_choice = False
        self.has_three_choice = False
        self.ending = None

        self.parse_text()

    # read a single message from rom
    @classmethod
    def from_rom(cls, rom, index):

        entry_offset = TABLE_START + 8 * index
        entry = rom.read_bytes(entry_offset, 8)
        next = rom.read_bytes(entry_offset + 8, 8)

        id = bytes_to_int(entry[0:2])
        opts = entry[2]
        offset = bytes_to_int(entry[5:8])
        length = bytes_to_int(next[5:8]) - offset

        raw_text = rom.read_bytes(TEXT_START + offset, length)

        return cls(raw_text, index, id, opts, offset, length)

    @classmethod
    def from_string(cls, text, id=0, opts=0x00):
        bytes = list(text.encode('utf-8')) + [0x02]

        return cls(bytes, 0, id, opts, 0, len(bytes) + 1)

    __str__ = __repr__ = display

# wrapper for updating the text of a message, given its message id
# if the id does not exist in the list, this will silently do nothing
def update_message_by_id(messages, id, text, opts=None):
    # get the message index
    index = next( (m.index for m in messages if m.id == id), -1)
    # update if it was found
    if index >= 0:
        update_message_by_index(messages, index, text, opts)

# wrapper for updating the text of a message, given its index in the list
def update_message_by_index(messages, index, text, opts=None):
    if opts is None:
        opts = messages[index].opts
    messages[index] = Message.from_string(text, messages[index].id, opts)

# wrapper for adding a string message to a list of messages
def add_message(messages, text, id=0, opts=0x00):
    messages.append( Message.from_string(text, id, opts) )
    messages[-1].index = len(messages) - 1

# holds a row in the shop item table (which contains pointers to the description and purchase messages)
class Shop_Item():

    def display(self):
        meta_data = ["#" + str(self.index),
         "Item: 0x" + "{:04x}".format(self.get_item_id),
         "Price: " + str(self.price),
         "Amount: " + str(self.pieces),
         "Object: 0x" + "{:04x}".format(self.object),
         "Model: 0x" + "{:04x}".format(self.model),
         "Description: 0x" + "{:04x}".format(self.description_message),
         "Purchase: 0x" + "{:04x}".format(self.purchase_message),]
        func_data = [
         "func1: 0x" + "{:08x}".format(self.func1),
         "func2: 0x" + "{:08x}".format(self.func2),
         "func3: 0x" + "{:08x}".format(self.func3),
         "func4: 0x" + "{:08x}".format(self.func4),]
        return ', '.join(meta_data) + '\n' + ', '.join(func_data)

    # write the shop item back
    def write(self, rom, index):

        entry_offset = SHOP_ITEM_START + 0x20 * index

        bytes = []
        bytes += int_to_bytes(self.object, 2)
        bytes += int_to_bytes(self.model, 2)
        bytes += int_to_bytes(self.func1, 4)
        bytes += int_to_bytes(self.price, 2)
        bytes += int_to_bytes(self.pieces, 2)
        bytes += int_to_bytes(self.description_message, 2)
        bytes += int_to_bytes(self.purchase_message, 2)
        bytes += [0x00, 0x00]
        bytes += int_to_bytes(self.get_item_id, 2)
        bytes += int_to_bytes(self.func2, 4)
        bytes += int_to_bytes(self.func3, 4)
        bytes += int_to_bytes(self.func4, 4)

        rom.write_bytes(entry_offset, bytes)

    # read a single message
    def __init__(self, rom, index):

        entry_offset = SHOP_ITEM_START + 0x20 * index
        entry = rom.read_bytes(entry_offset, 0x20)

        self.index = index
        self.object = bytes_to_int(entry[0x00:0x02])
        self.model = bytes_to_int(entry[0x02:0x04])
        self.func1 = bytes_to_int(entry[0x04:0x08])
        self.price = bytes_to_int(entry[0x08:0x0A])
        self.pieces = bytes_to_int(entry[0x0A:0x0C])
        self.description_message = bytes_to_int(entry[0x0C:0x0E])
        self.purchase_message = bytes_to_int(entry[0x0E:0x10])
        # 0x10-0x11 is always 0000 padded apparently
        self.get_item_id = bytes_to_int(entry[0x12:0x14])
        self.func2 = bytes_to_int(entry[0x14:0x18])
        self.func3 = bytes_to_int(entry[0x18:0x1C])
        self.func4 = bytes_to_int(entry[0x1C:0x20])

    __str__ = __repr__ = display

# reads each of the shop items
def read_shop_items(rom):
    shop_items = []

    for index in range(0x032):
        shop_items.append( Shop_Item(rom, index) )

    return shop_items

# writes each of the shop item back into rom
def write_shop_items(rom, shop_items):
    for s in shop_items:
        s.write(rom, s.index)

# these are unused shop items, and contain text ids that are used elsewhere, and should not be moved
SHOP_ITEM_EXCEPTIONS = [0x0A, 0x0B, 0x11, 0x12, 0x13, 0x14, 0x29]

# returns a set of all message ids used for shop items
def get_shop_message_id_set(shop_items):
    ids = set()
    for shop in shop_items:
        if shop.index not in SHOP_ITEM_EXCEPTIONS:
            ids.add(shop.description_message)
            ids.add(shop.purchase_message)
    return ids

# remove all messages that easy to tell are unused to create space in the message index table
def remove_unused_messages(messages):
    messages[:] = [m for m in messages if not m.is_id_message()]
    for index, m in enumerate(messages):
        m.index = index

# takes all messages used for shop items, and moves messages from the 00xx range into the unused 80xx range
def move_shop_item_messages(messages, shop_items):
    # checks if a message id is in the item message range
    def is_in_item_range(id):
        bytes = int_to_bytes(id, 2)
        return bytes[0] == 0x00
    # get the ids we want to move
    ids = set( id for id in get_shop_message_id_set(shop_items) if is_in_item_range(id) )
    # update them in the message list
    for id in ids:
        # should be a singleton list, but in case something funky is going on, handle it as a list regardless
        relevant_messages = [message for message in messages if message.id == id]
        for message in relevant_messages:
            message.id |= 0x8000
    # update them in the shop item list
    for shop in shop_items:
        if is_in_item_range(shop.description_message):
            shop.description_message |= 0x8000
        if is_in_item_range(shop.purchase_message):
            shop.purchase_message |= 0x8000


# add the keysanity messages
# make sure to call this AFTER move_shop_item_messages()
def add_keysanity_messages(messages):
    for id, text in KEYSANITY_MESSAGES.items():
        add_message(messages, text, id, 0x23)

# run all keysanity related patching to add messages for dungeon specific items
def message_patch_for_dungeon_items(rom, messages, shop_items):
    move_shop_item_messages(messages, shop_items)
    add_keysanity_messages(messages)

# reads each of the game's messages into a list of Message objects
def read_messages(rom):

    table_offset = TABLE_START
    index = 0
    messages = []
    while True:
        entry = rom.read_bytes(table_offset, 8)
        id = bytes_to_int(entry[0:2])

        if id == 0xFFFD:
            table_offset += 8
            continue # this is only here to give an ending offset
        if id == 0xFFFF:
            break # this marks the end of the table

        messages.append( Message.from_rom(rom, index) )

        index += 1
        table_offset += 8

    return messages

# wrtie the messages back
def repack_messages(rom, messages, permutation=None, always_allow_skip=True):

    if permutation is None:
        permutation = range(len(messages))

    # repack messages
    offset = 0
    for old_index, new_index in enumerate(permutation):
        old_message = messages[old_index]
        new_message = messages[new_index]
        remember_id = new_message.id 
        new_message.id = old_message.id
        offset = new_message.write(rom, old_index, offset, True, old_message.ending, always_allow_skip)
        new_message.id = remember_id

    # end the table
    table_index = len(messages)
    entry = bytes([0xFF, 0xFD, 0x00, 0x00, 0x07]) + int_to_bytes(offset, 3)
    entry_offset = TABLE_START + 8 * table_index
    rom.write_bytes(entry_offset, entry)
    table_index += 1
    entry_offset = TABLE_START + 8 * table_index
    rom.write_bytes(entry_offset, [0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

# shuffles the messages in the game, making sure to keep various message types in their own group
def shuffle_messages(rom, except_hints=True, always_allow_skip=True):

    messages = read_messages(rom)

    permutation = [i for i, _ in enumerate(messages)]

    def is_not_exempt(m):
        exaempt_as_id = m.is_id_message()
        exempt_as_hint = ( except_hints and m.id in (GOSSIP_STONE_MESSAGES + TEMPLE_HINTS_MESSAGES + LIGHT_ARROW_HINT + list(KEYSANITY_MESSAGES.keys()) ) )
        return not ( exaempt_as_id or exempt_as_hint )
    
    have_goto =         list( filter( lambda m: is_not_exempt(m) and m.has_goto, messages) )
    have_keep_open =    list( filter( lambda m: is_not_exempt(m) and m.has_keep_open, messages) )
    have_event =        list( filter( lambda m: is_not_exempt(m) and m.has_event, messages) )
    have_fade =         list( filter( lambda m: is_not_exempt(m) and m.has_fade, messages) )
    have_ocarina =      list( filter( lambda m: is_not_exempt(m) and m.has_ocarina, messages) )
    have_two_choice =   list( filter( lambda m: is_not_exempt(m) and m.has_two_choice, messages) )
    have_three_choice = list( filter( lambda m: is_not_exempt(m) and m.has_three_choice, messages) )
    basic_messages =    list( filter( lambda m: is_not_exempt(m) and m.is_basic(), messages) )


    def shuffle_group(group):
        group_permutation = [i for i, _ in enumerate(group)]
        random.shuffle(group_permutation)

        for index_from, index_to in enumerate(group_permutation):
            permutation[group[index_to].index] = group[index_from].index

    # need to use 'list' to force 'map' to actually run through
    list( map( shuffle_group, [
        have_goto + have_keep_open + have_event + have_fade + basic_messages,
        have_ocarina,
        have_two_choice,
        have_three_choice,
    ]))

    # write the messages back
    repack_messages(rom, messages, permutation, always_allow_skip)
