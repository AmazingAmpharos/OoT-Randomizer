import io
import hashlib
import logging
import os
import struct
import random

from Utils import local_path
from Items import ItemFactory


JAP10HASH = '03a63945398191337e896e5771f77173'
RANDOMIZERBASEHASH = 'dc5840f0d1ef7b51009c5625a054b3dd'


class LocalRom(object):

    def __init__(self, file, patch=True):
        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        if patch:
            self.patch_base_rom()

    def write_byte(self, address, value):
        self.buffer[address] = value

    def write_bytes(self, startaddress, values):
        for i, value in enumerate(values):
            self.write_byte(startaddress + i, value)

    def write_int16_to_rom(self, address, value):
        self.write_bytes(address, int16_as_bytes(value))

    def write_int32_to_rom(self, address, value):
        self.write_bytes(address, int32_as_bytes(value))

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def patch_base_rom(self):
        # verify correct checksum of baserom
        basemd5 = hashlib.md5()
        basemd5.update(self.buffer)
#        if JAP10HASH != basemd5.hexdigest():
        if JAP10HASH != JAP10HASH:
            logging.getLogger('').warning('Supplied Base Rom does not match known MD5 for JAP(1.0) release. Will try to patch anyway.')

        # extend to 2MB
#        self.buffer.extend(bytearray([0x00] * (2097152 - len(self.buffer))))

        # verify md5
        patchedmd5 = hashlib.md5()
        patchedmd5.update(self.buffer)
#        if RANDOMIZERBASEHASH != patchedmd5.hexdigest():
        if RANDOMIZERBASEHASH != RANDOMIZERBASEHASH:
            raise RuntimeError('Provided Base Rom unsuitable for patching. Please provide a JAP(1.0) "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc" rom to use as a base.')

def read_rom(stream):
    "Reads rom into bytearray"
    buffer = bytearray(stream.read())
    return buffer


def int16_as_bytes(value):
    value = value & 0xFFFF
    return [value & 0xFF, (value >> 8) & 0xFF]

def int32_as_bytes(value):
    value = value & 0xFFFFFFFF
    return [value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF]

def patch_rom(world, rom):

    # Can always return to youth
    rom.write_byte(0xCB6844, 0x35)

    # patch items
    for location in world.get_locations():
        itemid = location.item.code
        locationaddress = location.address

        if itemid is None or location.address is None:
            continue
        if location.type == 'Song':
            secondaryaddress = location.default
            rom.write_byte(locationaddress, itemid)
            itemid = itemid + 0x0D
            rom.write_byte(secondaryaddress, itemid)
            if location.name == 'Impa at Castle':
                impa_fix = 0x65 - location.item.index
                rom.write_byte(0xD12ECB, impa_fix)
                impa_fix = 0x8C34 - (location.item.index * 4)
                impa_fix_high = impa_fix >> 8
                impa_fix_low = impa_fix & 0x00FF
                rom.write_bytes(0xB063FE, [impa_fix_high, impa_fix_low])
            elif location.name == 'Song from Malon':
                malon_fix = 0x8C34 - (location.item.index * 4)
                malon_fix_high = malon_fix >> 8
                malon_fix_low = malon_fix & 0x00FF
                rom.write_bytes(0xD7E142, [malon_fix_high, malon_fix_low])
#                rom.write_bytes(0xD7E8D6, [malon_fix_high, malon_fix_low]) # I don't know what this does, may be useful?
                rom.write_bytes(0xD7E786, [malon_fix_high, malon_fix_low])
            elif location.name == 'Song from Composer Grave':
                sun_fix = 0x8C34 - (location.item.index * 4)
                sun_fix_high = sun_fix >> 8
                sun_fix_low = sun_fix & 0x00FF
                rom.write_bytes(0xE09F66, [sun_fix_high, sun_fix_low])
            elif location.name == 'Song from Saria':
                saria_fix = 0x8C34 - (location.item.index * 4)
                saria_fix_high = saria_fix >> 8
                saria_fix_low = saria_fix & 0x00FF
                rom.write_bytes(0xE29382, [saria_fix_high, saria_fix_low])
            elif location.name == 'Song at Windmill':
                windmill_fix = 0x65 - location.item.index
                rom.write_byte(0xE42ABF, windmill_fix)
            elif location.name == 'Sheik Forest Song':
                minuet_fix = 0x65 - location.item.index
                rom.write_byte(0xC7BAA3, minuet_fix)
            elif location.name == 'Sheik at Temple':
                prelude_fix = 0x65 - location.item.index
                rom.write_byte(0xC8060B, prelude_fix)
        elif location.type == 'NPC':
            rom.write_byte(locationaddress, location.item.index)
        else:
            locationdefault = location.default & 0xF01F
            itemid = itemid | locationdefault
            itemidhigh = itemid >> 8
            itemidlow = itemid & 0x00FF

            rom.write_bytes(locationaddress, [itemidhigh, itemidlow])

    if world.open_forest:
        rom.write_byte(0x2081153, 0x00)
        rom.write_byte(0x20811A5, 0x63)
        rom.write_bytes(0x20811B2, [0xFF, 0x01])

    return rom