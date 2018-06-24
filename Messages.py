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
         "Length: 0x" + "{:04x}".format(self.length),
         "Box Type: " + str(self.box_type),
         "Postion: " + str(self.position)]
        return ', '.join(meta_data) + '\n' + self.text

    def parse_text(self):
        self.text_codes = []

        index = 0
        while index < self.length:
            next_char = self.raw_text[index]
            data = next_char
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
            if next_char == 0x0A: # keep-open
                self.has_keep_open = True
            if next_char == 0x0B: # event
                self.has_event = True
            if next_char == 0x0E: # fade out
                self.has_fade = True
            if next_char == 0x10: # ocarina
                self.has_ocarina = True
            if next_char == 0x1B: # two choice
                self.has_two_choice = True
            if next_char == 0x1C: # three choice
                self.has_three_choice = True
        self.text = display_code_list(self.text_codes)

    def is_basic(self):
        return not (self.has_goto or self.has_keep_open or self.has_event or self.has_fade or self.has_ocarina or self.has_two_choice or self.has_three_choice)

    # read a single message
    def __init__(self, rom, offset, count):

        entry = read_bytes(rom, offset, 8)
        next = read_bytes(rom, offset + 8, 8)
        opts = entry[2]

        self.count = count
        self.id = int.from_bytes(entry[0:2], byteorder='big', signed=False)
        self.box_type = (opts & 0xF0) >> 4
        self.position = (opts & 0x0F)
        self.offset = int.from_bytes(entry[5:8], byteorder='big', signed=False)
        self.length = int.from_bytes(next[5:8], byteorder='big', signed=False) - self.offset

        self.has_goto = False
        self.has_keep_open = False
        self.has_event = False
        self.has_fade = False
        self.has_ocarina = False
        self.has_two_choice = False
        self.has_three_choice = False

        self.raw_text = read_bytes(rom, TEXT_START + self.offset, self.length)
        self.parse_text()

    __str__ = __repr__ = display

# reads each of the game's messages into a list of Message objects
def read_messages(rom):

    offset = TABLE_START
    count = 0
    messages = []
    while True:
        entry = read_bytes(rom, offset, 8)
        id = int.from_bytes(entry[0:2], byteorder='big', signed=False)

        if id == 0xFFFD:
            offset += 8
            continue # this is only here to give an ending offset
        if id == 0xFFFF:
            break # this marks the end of the table

        messages.append( Message(rom, offset, count) )

        count += 1
        offset += 8

    return messages

# shuffles the messages in the game, making sure to keep various message types in their own group
def shuffle_messages(rom, except_hints=True):

    messages = read_messages(rom)

    def is_not_exempt(m):
        exempt_as_too_short = (m.length < 4)
        exempt_as_hint = ( except_hints and m.id in (GOSSIP_STONE_MESSAGES + TEMPLE_HINTS_MESSAGES) )
        return not ( exempt_as_too_short or exempt_as_hint )
    
    have_goto =         list( filter( lambda m: is_not_exempt(m) and m.has_goto, messages) ) # not shuffled yet
    have_keep_open =    list( filter( lambda m: is_not_exempt(m) and m.has_keep_open, messages) )
    have_event =        list( filter( lambda m: is_not_exempt(m) and m.has_event, messages) )
    have_fade =         list( filter( lambda m: is_not_exempt(m) and m.has_fade, messages) )
    have_ocarina =      list( filter( lambda m: is_not_exempt(m) and m.has_ocarina, messages) )
    have_two_choice =   list( filter( lambda m: is_not_exempt(m) and m.has_two_choice, messages) )
    have_three_choice = list( filter( lambda m: is_not_exempt(m) and m.has_three_choice, messages) )
    basic_messages =    list( filter( lambda m: is_not_exempt(m) and m.is_basic(), messages) )


    def shuffle_group(group):
        permutation = list( range( len(group) ) )
        random.shuffle(permutation)

        for index_from, index_to in enumerate(permutation):
            message_id = group[index_from].id
            rom_location = TABLE_START + 8 * group[index_to].count
            # print('0x' + "{:04x}".format(message_id) + " at #" + str(group[index_to].count) + " -> 0x" + "{:06x}".format(rom_location) )
            id_bytes = [(message_id >> 8) & 0xFF, message_id & 0xFF]
            rom.write_bytes(rom_location, id_bytes)

    # need to use 'list' to force 'map' to actually run through
    list( map( shuffle_group, [
        have_keep_open,
        have_event,
        have_fade,
        have_ocarina,
        have_two_choice,
        have_three_choice,
        basic_messages,
    ]))