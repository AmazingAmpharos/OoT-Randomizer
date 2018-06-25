# text details: https://wiki.cloudmodding.com/oot/Text_Format

import random

TABLE_START = 0xB849EC
TEXT_START = 0x92D000

# reads len bytes from the rom starting at offset
def read_bytes(rom, offset, len):
    return rom.buffer[offset : offset + len]

# name of type, followed by number of additional bytes to read, follwed by a function that prints the code
CONTROL_CODES = {
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
            bytes_to_write = int.to_bytes(self.data, extra_bytes, byteorder='big', signed=False)
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
        meta_data = ["#" + str(self.count),
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
                    data = int.from_bytes(self.raw_text[index : index + extra_bytes], byteorder='big', signed=False)
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
    def write(self, rom, index, offset, replace_ending=False, ending=None, always_allow_skip=True):

        # construct the table entry
        id_bytes = int.to_bytes(self.id, 2, byteorder='big', signed=False)
        offset_bytes = int.to_bytes(offset, 3, byteorder='big', signed=False)
        entry = id_bytes + bytes([self.opts, 0x00, 0x07]) + offset_bytes
        # write it back
        entry_offset = TABLE_START + 8 * index
        rom.write_bytes(entry_offset, entry)

        ending_codes = [0x02, 0x07, 0x0A, 0x0B, 0x0E, 0x10]

        # write the message
        for code in self.text_codes:
            # ignore ending codes if it's going to be replaced
            if replace_ending and code.code in ending_codes:
                pass
            # ignore the "make unskippable flag"
            elif always_allow_skip and code.code == 0x1A:
                pass
            else:
                offset = code.write(rom, offset)

        if replace_ending:
            if ending:
                offset = ending.write(rom, offset) # write special ending
            offset = Text_Code(0x02, 0).write(rom, offset) # write end code

        return offset

    # read a single message
    def __init__(self, rom, index):

        entry_offset = TABLE_START + 8 * index
        entry = read_bytes(rom, entry_offset, 8)
        next = read_bytes(rom, entry_offset + 8, 8)
        self.opts = entry[2]

        self.count = index
        self.id = int.from_bytes(entry[0:2], byteorder='big', signed=False)
        self.box_type = (self.opts & 0xF0) >> 4
        self.position = (self.opts & 0x0F)
        self.offset = int.from_bytes(entry[5:8], byteorder='big', signed=False)
        self.length = int.from_bytes(next[5:8], byteorder='big', signed=False) - self.offset

        self.has_goto = False
        self.has_keep_open = False
        self.has_event = False
        self.has_fade = False
        self.has_ocarina = False
        self.has_two_choice = False
        self.has_three_choice = False
        self.ending = None

        self.raw_text = read_bytes(rom, TEXT_START + self.offset, self.length)
        self.parse_text()

    __str__ = __repr__ = display

# reads each of the game's messages into a list of Message objects
def read_messages(rom):

    table_offset = TABLE_START
    index = 0
    messages = []
    while True:
        entry = read_bytes(rom, table_offset, 8)
        id = int.from_bytes(entry[0:2], byteorder='big', signed=False)

        if id == 0xFFFD:
            table_offset += 8
            continue # this is only here to give an ending offset
        if id == 0xFFFF:
            break # this marks the end of the table

        messages.append( Message(rom, index) )

        index += 1
        table_offset += 8

    return messages

# wrtie the messages back
def repack_messages(rom, messages, permutation, always_allow_skip=True):

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
    entry = bytes([0xFF, 0xFD, 0x00, 0x00, 0x07]) + int.to_bytes(offset, 3, byteorder='big', signed=False)
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
        exempt_as_hint = ( except_hints and m.id in (GOSSIP_STONE_MESSAGES + TEMPLE_HINTS_MESSAGES + LIGHT_ARROW_HINT) )
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
            permutation[group[index_to].count] = group[index_from].count

    # need to use 'list' to force 'map' to actually run through
    list( map( shuffle_group, [
        have_goto + have_keep_open + have_event + have_fade + basic_messages,
        have_ocarina,
        have_two_choice,
        have_three_choice,
    ]))

    # write the messages back
    repack_messages(rom, messages, permutation, always_allow_skip)