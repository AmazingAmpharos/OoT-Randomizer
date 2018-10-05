import io
import json
import logging
import os
import platform
import struct
import subprocess
import random
import copy

from Hints import writeGossipStoneHintsHints, buildBossRewardHints, buildGanonText, getSimpleHintNoPrefix
from Utils import local_path, default_output_path, random_choices
from Items import ItemFactory, item_data
from Messages import *
from OcarinaSongs import Song, str_to_song, replace_songs
from MQ import patch_files, File, update_dmadata, insert_space, add_relocations

TunicColors = {
    "Custom Color": [0, 0, 0], 
    "Kokiri Green": [0x1E, 0x69, 0x1B],
    "Goron Red": [0x64, 0x14, 0x00],
    "Zora Blue": [0x00, 0x3C, 0x64],
    "Black": [0x30, 0x30, 0x30],
    "White": [0xF0, 0xF0, 0xFF],
    "Azure Blue": [0x13, 0x9E, 0xD8],
    "Vivid Cyan": [0x13, 0xE9, 0xD8],
    "Light Red": [0xF8, 0x7C, 0x6D],
    "Fuchsia":[0xFF, 0x00, 0xFF],
    "Purple": [0x95, 0x30, 0x80],
    "MM Purple": [0x50, 0x52, 0x9A],
    "Twitch Purple": [0x64, 0x41, 0xA5],
    "Purple Heart": [0x8A, 0x2B, 0xE2],
    "Persian Rose": [0xFF, 0x14, 0x93],
    "Dirty Yellow": [0xE0, 0xD8, 0x60],
    "Blush Pink": [0xF8, 0x6C, 0xF8],
    "Hot Pink": [0xFF, 0x69, 0xB4],
    "Rose Pink": [0xFF, 0x90, 0xB3],
    "Orange": [0xE0, 0x79, 0x40],
    "Gray": [0xA0, 0xA0, 0xB0],
    "Gold": [0xD8, 0xB0, 0x60],
    "Silver": [0xD0, 0xF0, 0xFF],
    "Beige": [0xC0, 0xA0, 0xA0],
    "Teal": [0x30, 0xD0, 0xB0],
    "Blood Red": [0x83, 0x03, 0x03],
    "Blood Orange": [0xFE, 0x4B, 0x03],
    "Royal Blue": [0x40, 0x00, 0x90],
    "Sonic Blue": [0x50, 0x90, 0xE0],
    "NES Green": [0x00, 0xD0, 0x00],
    "Dark Green": [0x00, 0x25, 0x18],
    "Lumen": [80, 140, 240],
}

NaviColors = {
    "Custom Color": [0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00], 
    "Gold": [0xFE, 0xCC, 0x3C, 0xFF, 0xFE, 0xC0, 0x07, 0x00],
    "White": [0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0x00],
    "Green": [0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0x00],
    "Light Blue": [0x96, 0x96, 0xFF, 0xFF, 0x96, 0x96, 0xFF, 0x00],
    "Yellow": [0xFF, 0xFF, 0x00, 0xFF, 0xC8, 0x9B, 0x00, 0x00],
    "Red": [0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00],
    "Magenta": [0xFF, 0x00, 0xFF, 0xFF, 0xC8, 0x00, 0x9B, 0x00],
    "Black": [0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00],
    "Tatl": [0xFF, 0xFF, 0xFF, 0xFF, 0xC8, 0x98, 0x00, 0x00],
    "Tael": [0x49, 0x14, 0x6C, 0xFF, 0xFF, 0x00, 0x00, 0x00],
    "Fi": [0x2C, 0x9E, 0xC4, 0xFF, 0x2C, 0x19, 0x83, 0x00],
    "Ciela": [0xE6, 0xDE, 0x83, 0xFF, 0xC6, 0xBE, 0x5B, 0x00],
    "Epona": [0xD1, 0x49, 0x02, 0xFF, 0x55, 0x1F, 0x08, 0x00],
    "Ezlo": [0x62, 0x9C, 0x5F, 0xFF, 0x3F, 0x5D, 0x37, 0x00],
    "King of Red Lions": [0xA8, 0x33, 0x17, 0xFF, 0xDE, 0xD7, 0xC5, 0x00],
    "Linebeck": [0x03, 0x26, 0x60, 0xFF, 0xEF, 0xFF, 0xFF, 0x00],
    "Loftwing": [0xD6, 0x2E, 0x31, 0xFF, 0xFD, 0xE6, 0xCC, 0x00],
    "Midna": [0x19, 0x24, 0x26, 0xFF, 0xD2, 0x83, 0x30, 0x00],
    "Phantom Zelda": [0x97, 0x7A, 0x6C, 0xFF, 0x6F, 0x46, 0x67, 0x00],
}

def get_tunic_colors():
    return list(TunicColors.keys())

def get_tunic_color_options():
    return ["Random Choice", "Completely Random"] + get_tunic_colors()

def get_navi_colors():
    return list(NaviColors.keys())

def get_navi_color_options():
    return ["Random Choice", "Completely Random"] + get_navi_colors()

def patch_rom(world, rom):
    with open(local_path('data/rom_patch.txt'), 'r') as stream:
        for line in stream:
            address, value = [int(x, 16) for x in line.split(',')]
            rom.write_byte(address, value)
    
    # Write Randomizer title screen logo
    with open(local_path('data/title.bin'), 'rb') as stream:
        titleBytes = stream.read()
        rom.write_bytes(0x01795300, titleBytes)

    # Increase the instance size of Bombchus prevent the heap from becoming corrupt when
    # a Dodongo eats a Bombchu. Does not fix stale pointer issues with the animation
    rom.write_int32(0xD6002C, 0x1F0)

    # Can always return to youth
    rom.write_byte(0xCB6844, 0x35)
    rom.write_byte(0x253C0E2, 0x03) # Moves sheik from pedestal

    # Fix child shooting gallery reward to be static
    rom.write_bytes(0xD35EFC, [0x00, 0x00, 0x00, 0x00])

    # Fix target in woods reward to be static
    rom.write_bytes(0xE59CD4, [0x00, 0x00, 0x00, 0x00])

    # Fix GS rewards to be static
    rom.write_bytes(0xEA3934, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xEA3940 , [0x10, 0x00])

    # Fix horseback archery rewards to be static
    rom.write_byte(0xE12BA5, 0x00)
    rom.write_byte(0xE12ADD, 0x00)

    # Fix adult shooting gallery reward to be static
    rom.write_byte(0xD35F55, 0x00)

    # Fix deku theater rewards to be static
    rom.write_bytes(0xEC9A7C, [0x00, 0x00, 0x00, 0x00]) #Sticks
    rom.write_byte(0xEC9CD5, 0x00) #Nuts

    # Fix deku scrub who sells stick upgrade
    rom.write_bytes(0xDF8060, [0x00, 0x00, 0x00, 0x00])

    # Fix deku scrub who sells nut upgrade
    rom.write_bytes(0xDF80D4, [0x00, 0x00, 0x00, 0x00])

    # Fix rolling goron as child reward to be static
    rom.write_bytes(0xED2960, [0x00, 0x00, 0x00, 0x00])

    # Fix proximity text boxes (Navi) (Part 1)
    rom.write_bytes(0xDF8B84, [0x00, 0x00, 0x00, 0x00])

    # Fix final magic bean to cost 99
    rom.write_byte(0xE20A0F, 0x63)
    rom.write_bytes(0x94FCDD, [0x08, 0x39, 0x39])
    
    # Remove intro cutscene
    rom.write_bytes(0xB06BBA, [0x00, 0x00])

    # Remove locked door to Boss Key Chest in Fire Temple
    if not world.keysanity and not world.dungeon_mq['FiT']:
        rom.write_byte(0x22D82B7, 0x3F)

    # Change Bombchi Shop to be always open
    rom.write_int32(0xC6CEDC, 0x240B0001) # li t3, 1

    if world.bombchus_in_logic:
        # Change Bowling Alley check to bombchus (Part 1)
        rom.write_bytes(0x00E2D714, [0x81, 0xEF, 0xA6, 0x4C])
        rom.write_bytes(0x00E2D720, [0x24, 0x18, 0x00, 0x09, 0x11, 0xF8, 0x00, 0x06])

        # Change Bowling Alley check to bombchus (Part 2)
        rom.write_bytes(0x00E2D890,  [0x81, 0x6B, 0xA6, 0x4C, 0x24, 0x0C, 0x00, 0x09, 0x51, 0x6C, 0x00, 0x0A])

        # Cannot buy bombchu refills without Bombchus
        rom.write_int32s(0xC01078, 
            [0x3C098012,    # lui     t1, 0x8012
             0x812AA64C,    # lb      t2, -0x59B4(t1)    ; bombchu item (SAVE_CONTEXT + 0x7C)
             0x340B0009,    # li      t3, 9
             0x114B0002,    # beq     t2, t3, @@return  ; if has bombchu, return 1 (can buy)
             0x34020000,    # li      v0, 0
             0x34020002])   # li      v0, 2             ; else, return 2 (can't buy)
    else:
        # Change Bowling Alley check to Bomb Bag (Part 1)
        rom.write_bytes(0x00E2D716, [0xA6, 0x72])
        rom.write_byte(0x00E2D723, 0x18)

        # Change Bowling Alley check to Bomb Bag (Part 2)
        rom.write_bytes(0x00E2D892, [0xA6, 0x72])
        rom.write_byte(0x00E2D897, 0x18)

        # Cannot buy bombchu refills without Bomb Bag
        rom.write_int32s(0xC01078,
            [0x3C098012,    # lui     t1, 0x8012
             0x812AA673,    # lb      t2, -0x598D(t1)    ; bombbag size (SAVE_CONTEXT + 0xA3)
             0x314A0038,    # andi    t2, t2, 0x38
             0x15400002,    # bnez    t2, @@return       ; If has bombbag, return 1 (can buy)
             0x24020000,    # li      v0, 0
             0x24020002])   # li      v0, 2              ; else, return 2, (can't buy)

    # Change Bazaar check to Bomb Bag (Child?)
    rom.write_bytes(0x00C0082A, [0x00, 0x18])
    rom.write_bytes(0x00C0082C, [0x00, 0x0E, 0X74, 0X02])
    rom.write_byte(0x00C00833, 0xA0)

    # Change Bazaar check to Bomb Bag (Adult?)
    rom.write_bytes(0x00DF7A8E, [0x00, 0x18])
    rom.write_bytes(0x00DF7A90, [0x00, 0x0E, 0X74, 0X02])
    rom.write_byte(0x00DF7A97, 0xA0)

    # Change Goron Shop check to Bomb Bag
    rom.write_bytes(0x00C6ED86, [0x00, 0xA2])
    rom.write_bytes(0x00C6ED8A, [0x00, 0x18])

    # Change graveyard graves to not allow grabbing on to the ledge
    rom.write_byte(0x0202039D, 0x20)
    rom.write_byte(0x0202043C, 0x24)

    # Fix Link the Goron to always work
    rom.write_bytes(0xED2FAC, [0x80, 0x6E, 0x0F, 0x18])
    rom.write_bytes(0xED2FEC, [0x24, 0x0A, 0x00, 0x00])
    rom.write_bytes(0xAE74D8, [0x24, 0x0E, 0x00, 0x00])

    # Fix King Zora Thawed to always work
    rom.write_bytes(0xE55C4C, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xE56290, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xE56298, [0x00, 0x00, 0x00, 0x00])

    # Fix Castle Courtyard to check for meeting Zelda, not Zelda fleeing, to block you
    rom.write_bytes(0xCD5E76, [0x0E, 0xDC])
    rom.write_bytes(0xCD5E12, [0x0E, 0xDC])

    # Cutscene for all medallions never triggers when leaving shadow or spirit temples(hopefully stops warp to colossus on shadow completion with boss reward shuffle)
    rom.write_byte(0xACA409, 0xAD)
    rom.write_byte(0xACA49D, 0xCE)
    
    # Speed Zelda's Letter scene
    rom.write_bytes(0x290E08E, [0x05, 0xF0])
    rom.write_byte(0xEFCBA7, 0x08)
    rom.write_byte(0xEFE7C7, 0x05)
    #rom.write_byte(0xEFEAF7, 0x08)
    #rom.write_byte(0xEFE7C7, 0x05)
    rom.write_bytes(0xEFE938, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xEFE948, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xEFE950, [0x00, 0x00, 0x00, 0x00])

    # Speed Zelda escaping from Hyrule Castle
    Block_code = [0x00, 0x00, 0x00, 0x01, 0x00, 0x21, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02]
    rom.write_bytes(0x1FC0CF8, Block_code)

    # Speed learning Zelda's Lullaby
    rom.write_int32s(0x02E8E90C, [0x000003E8, 0x00000001]) # Terminator Execution
    if world.shuffle_song_items:
        rom.write_int16s(None, [0x0073, 0x001, 0x0002, 0x0002]) # ID, start, end, end  
    else:
        rom.write_int16s(None, [0x0073, 0x003B, 0x003C, 0x003C]) # ID, start, end, end  


    rom.write_int32s(0x02E8E91C, [0x00000013, 0x0000000C]) # Textbox, Count
    if world.shuffle_song_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0010, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x0017, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2        
    rom.write_int16s(None, [0x00D4, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    # Speed learning Sun's Song
    if world.shuffle_song_items:
        rom.write_int32(0x0332A4A4, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x0332A4A4, 0x0000003C) # Header: frame_count      

    rom.write_int32s(0x0332A868, [0x00000013, 0x00000008]) # Textbox, Count
    rom.write_int16s(None, [0x0018, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x00D3, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    # Speed learning Saria's Song
    if world.shuffle_song_items:
        rom.write_int32(0x020B1734, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x020B1734, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x20B1DA8, [0x00000013, 0x0000000C]) # Textbox, Count
    rom.write_int16s(None, [0x0015, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x00D1, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x020B19C0, [0x0000000A, 0x00000006]) # Link, Count
    rom.write_int16s(0x020B19C8, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int16s(0x020B19F8, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????
    rom.write_int32s(None,         [0x80000000,                          # ???
                                     0x00000000, 0x000001D4, 0xFFFFF731,  # start_XYZ
                                     0x00000000, 0x000001D4, 0xFFFFF712]) # end_XYZ

    # Speed learning Epona's Song
    rom.write_int32s(0x029BEF60, [0x000003E8, 0x00000001]) # Terminator Execution
    if world.shuffle_song_items:
        rom.write_int16s(None, [0x005E, 0x0001, 0x0002, 0x0002]) # ID, start, end, end  
    else:
        rom.write_int16s(None, [0x005E, 0x000A, 0x000B, 0x000B]) # ID, start, end, end         

    rom.write_int32s(0x029BECB0, [0x00000013, 0x00000002]) # Textbox, Count
    if world.shuffle_song_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0009, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x00D2, 0x0000, 0x0009, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0xFFFF, 0x000A, 0x003C, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    # Speed learning Song of Time
    rom.write_int32s(0x0252FB98, [0x000003E8, 0x00000001]) # Terminator Execution
    if world.shuffle_song_items:
        rom.write_int16s(None, [0x0035, 0x0001, 0x0002, 0x0002]) # ID, start, end, end  
    else:
        rom.write_int16s(None, [0x0035, 0x003B, 0x003C, 0x003C]) # ID, start, end, end          

    rom.write_int32s(0x0252FC80, [0x00000013, 0x0000000C]) # Textbox, Count
    if world.shuffle_song_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0010, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x0019, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2        
    rom.write_int16s(None, [0x00D5, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32(0x01FC3B84, 0xFFFFFFFF) # Other Header?: frame_count

    # Speed learning Song of Storms
    if world.shuffle_song_items:
        rom.write_int32(0x03041084, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x03041084, 0x0000000A) # Header: frame_count

    rom.write_int32s(0x03041088, [0x00000013, 0x00000002]) # Textbox, Count
    rom.write_int16s(None, [0x00D6, 0x0000, 0x0009, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0xFFFF, 0x00BE, 0x00C8, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    # Speed learning Minuet of Forest
    if world.shuffle_song_items:
        rom.write_int32(0x020AFF84, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x020AFF84, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x020B0800, [0x00000013, 0x0000000A]) # Textbox, Count
    rom.write_int16s(None, [0x000F, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0073, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x020AFF88, [0x0000000A, 0x00000005]) # Link, Count
    rom.write_int16s(0x020AFF90, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int16s(0x020AFFC1, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x020B0488, [0x00000056, 0x00000001]) # Music Change, Count
    rom.write_int16s(None, [0x003F, 0x0021, 0x0022, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x020B04C0, [0x0000007C, 0x00000001]) # Music Fade Out, Count
    rom.write_int16s(None, [0x0004, 0x0000, 0x0000, 0x0000]) #action, start, end, ????

    # Speed learning Bolero of Fire
    if world.shuffle_song_items:
        rom.write_int32(0x0224B5D4, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x0224B5D4, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x0224D7E8, [0x00000013, 0x0000000A]) # Textbox, Count
    rom.write_int16s(None, [0x0010, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0074, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x0224B5D8, [0x0000000A, 0x0000000B]) # Link, Count
    rom.write_int16s(0x0224B5E0, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int16s(0x0224B610, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x0224B7F0, [0x0000002F, 0x0000000E]) # Sheik, Count
    rom.write_int16s(0x0224B7F8, [0x0000]) #action
    rom.write_int16s(0x0224B828, [0x0000]) #action
    rom.write_int16s(0x0224B858, [0x0000]) #action
    rom.write_int16s(0x0224B888, [0x0000]) #action

    # Speed learning Serenade of Water
    if world.shuffle_song_items:
        rom.write_int32(0x02BEB254, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x02BEB254, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x02BEC880, [0x00000013, 0x00000010]) # Textbox, Count
    rom.write_int16s(None, [0x0011, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0075, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x02BEB258, [0x0000000A, 0x0000000F]) # Link, Count
    rom.write_int16s(0x02BEB260, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int16s(0x02BEB290, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x02BEB530, [0x0000002F, 0x00000006]) # Sheik, Count
    rom.write_int16s(0x02BEB538, [0x0000, 0x0000, 0x018A, 0x0000]) #action, start, end, ????
    rom.write_int32s(None,         [0x1BBB0000,                          # ???
                                     0xFFFFFB10, 0x8000011A, 0x00000330,  # start_XYZ
                                     0xFFFFFB10, 0x8000011A, 0x00000330]) # end_XYZ

    rom.write_int32s(0x02BEC848, [0x00000056, 0x00000001]) # Music Change, Count
    rom.write_int16s(None, [0x0059, 0x0021, 0x0022, 0x0000]) #action, start, end, ????

    # Speed learning Nocturne of Shadow
    rom.write_int32s(0x01FFE458, [0x000003E8, 0x00000001]) # Other Scene? Terminator Execution
    rom.write_int16s(None, [0x002F, 0x0001, 0x0002, 0x0002]) # ID, start, end, end  

    rom.write_int32(0x01FFFDF4, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x02000FD8, [0x00000013, 0x0000000E]) # Textbox, Count
    if world.shuffle_song_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0010, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x0013, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0077, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x02000128, [0x000003E8, 0x00000001]) # Terminator Execution
    if world.shuffle_song_items:
        rom.write_int16s(None, [0x0032, 0x0001, 0x0002, 0x0002]) # ID, start, end, end  
    else:
        rom.write_int16s(None, [0x0032, 0x003A, 0x003B, 0x003B]) # ID, start, end, end  

    # Speed learning Requiem of Spirit
    rom.write_int32(0x0218AF14, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x0218C574, [0x00000013, 0x00000008]) # Textbox, Count
    if world.shuffle_song_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0010, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2       
    else:
        rom.write_int16s(None, [0x0012, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2       
    rom.write_int16s(None, [0x0076, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x0218B478, [0x000003E8, 0x00000001]) # Terminator Execution
    if world.shuffle_song_items:
        rom.write_int16s(None, [0x0030, 0x0001, 0x0002, 0x0002]) # ID, start, end, end  
    else:
        rom.write_int16s(None, [0x0030, 0x003A, 0x003B, 0x003B]) # ID, start, end, end  

    rom.write_int32s(0x0218AF18, [0x0000000A, 0x0000000B]) # Link, Count
    rom.write_int16s(0x0218AF20, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int32s(None,         [0x40000000,                          # ???
                                     0xFFFFFAF9, 0x00000008, 0x00000001,  # start_XYZ
                                     0xFFFFFAF9, 0x00000008, 0x00000001,  # end_XYZ
                                     0x0F671408, 0x00000000, 0x00000001]) # normal_XYZ
    rom.write_int16s(0x0218AF50, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????

    # Speed learning Prelude of Light
    if world.shuffle_song_items:
        rom.write_int32(0x0252FD24, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x0252FD24, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x02531320, [0x00000013, 0x0000000E]) # Textbox, Count
    rom.write_int16s(None, [0x0014, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0078, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x0252FF10, [0x0000002F, 0x00000009]) # Sheik, Count
    rom.write_int16s(0x0252FF18, [0x0006, 0x0000, 0x0000, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x025313D0, [0x00000056, 0x00000001]) # Music Change, Count
    rom.write_int16s(None, [0x003B, 0x0021, 0x0022, 0x0000]) #action, start, end, ????

    # Speed scene after Deku Tree
    rom.write_bytes(0x2077E20, [0x00, 0x07, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])
    rom.write_bytes(0x2078A10, [0x00, 0x0E, 0x00, 0x1F, 0x00, 0x20, 0x00, 0x20])
    Block_code = [0x00, 0x80, 0x00, 0x00, 0x00, 0x1E, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 
                  0xFF, 0xFF, 0x00, 0x1E, 0x00, 0x28, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    rom.write_bytes(0x2079570, Block_code)

    # Speed scene after Dodongo's Cavern
    rom.write_bytes(0x2221E88, [0x00, 0x0C, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0x2223308, [0x00, 0x81, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])

    # Speed scene after Jabu Jabu's Belly
    rom.write_bytes(0xCA3530, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x2113340, [0x00, 0x0D, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0x2113C18, [0x00, 0x82, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])
    rom.write_bytes(0x21131D0, [0x00, 0x01, 0x00, 0x00, 0x00, 0x3C, 0x00, 0x3C])

    # Speed scene after Forest Temple
    rom.write_bytes(0xD4ED68, [0x00, 0x45, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD4ED78, [0x00, 0x3E, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])
    rom.write_bytes(0x207B9D4, [0xFF, 0xFF, 0xFF, 0xFF])

    # Speed scene after Fire Temple
    rom.write_bytes(0x2001848, [0x00, 0x1E, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])
    rom.write_bytes(0xD100B4, [0x00, 0x62, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD10134, [0x00, 0x3C, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])

    # Speed scene after Water Temple
    rom.write_bytes(0xD5A458, [0x00, 0x15, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD5A3A8, [0x00, 0x3D, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])
    rom.write_bytes(0x20D0D20, [0x00, 0x29, 0x00, 0xC7, 0x00, 0xC8, 0x00, 0xC8])

    # Speed scene after Shadow Temple
    rom.write_bytes(0xD13EC8, [0x00, 0x61, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD13E18, [0x00, 0x41, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])

    # Speed scene after Spirit Temple
    rom.write_bytes(0xD3A0A8, [0x00, 0x60, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD39FF0, [0x00, 0x3F, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])

    # Speed Nabooru defeat scene
    rom.write_bytes(0x2F5AF84, [0x00, 0x00, 0x00, 0x05])
    rom.write_bytes(0x2F5C7DA, [0x00, 0x01, 0x00, 0x02])
    rom.write_bytes(0x2F5C7A2, [0x00, 0x03, 0x00, 0x04])
    rom.write_byte(0x2F5B369, 0x09)
    rom.write_byte(0x2F5B491, 0x04)
    rom.write_byte(0x2F5B559, 0x04)
    rom.write_byte(0x2F5B621, 0x04)
    rom.write_byte(0x2F5B761, 0x07)

    # Speed scene with all medallions
    rom.write_bytes(0x2512680, [0x00, 0x74, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])

    # Speed collapse of Ganon's Tower
    rom.write_bytes(0x33FB328, [0x00, 0x76, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])

    # Speed Phantom Ganon defeat scene
    rom.write_bytes(0xC944D8, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xC94548, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xC94730, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xC945A8, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xC94594, [0x00, 0x00, 0x00, 0x00])

    # Speed Twinrova defeat scene
    rom.write_bytes(0xD678CC, [0x24, 0x01, 0x03, 0xA2, 0xA6, 0x01, 0x01, 0x42])
    rom.write_bytes(0xD67BA4, [0x10, 0x00])
    
    # Speed scenes during final battle
    # Ganondorf battle end
    rom.write_byte(0xD82047, 0x09)
    # Zelda descends
    rom.write_byte(0xD82AB3, 0x66)
    rom.write_byte(0xD82FAF, 0x65)
    rom.write_bytes(0xD82D2E, [0x04, 0x1F])
    rom.write_bytes(0xD83142, [0x00, 0x6B])
    rom.write_bytes(0xD82DD8, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xD82ED4, [0x00, 0x00, 0x00, 0x00])
    rom.write_byte(0xD82FDF, 0x33)
    # After tower collapse
    rom.write_byte(0xE82E0F, 0x04)
    # Ganon intro
    rom.write_bytes(0xE83D28, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xE83B5C, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xE84C80, [0x10, 0x00])
    
    # Speed completion of the trials in Ganon's Castle
    rom.write_bytes(0x31A8090, [0x00, 0x6B, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02]) #Forest
    rom.write_bytes(0x31A9E00, [0x00, 0x6E, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02]) #Fire
    rom.write_bytes(0x31A8B18, [0x00, 0x6C, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02]) #Water
    rom.write_bytes(0x31A9430, [0x00, 0x6D, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02]) #Shadow
    rom.write_bytes(0x31AB200, [0x00, 0x70, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02]) #Spirit
    rom.write_bytes(0x31AA830, [0x00, 0x6F, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02]) #Light

    # Speed obtaining Fairy Ocarina
    rom.write_bytes(0x2150CD0, [0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x30])
    Block_code = [0xFF, 0xFF, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
                  0xFF, 0xFF, 0x00, 0x3C, 0x00, 0x81, 0xFF, 0xFF]
    rom.write_bytes(0x2151240, Block_code)
    rom.write_bytes(0x2150E20, [0xFF, 0xFF, 0xFA, 0x4C])

    # Speed Zelda Light Arrow cutscene
    rom.write_bytes(0x2531B40, [0x00, 0x28, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])
    rom.write_bytes(0x2532FBC, [0x00, 0x75])
    rom.write_bytes(0x2532FEA, [0x00, 0x75, 0x00, 0x80])  
    rom.write_byte(0x2533115, 0x05)
    rom.write_bytes(0x2533141, [0x06, 0x00, 0x06, 0x00, 0x10])
    rom.write_bytes(0x2533171, [0x0F, 0x00, 0x11, 0x00, 0x40])
    rom.write_bytes(0x25331A1, [0x07, 0x00, 0x41, 0x00, 0x65])
    rom.write_bytes(0x2533642, [0x00, 0x50])
    rom.write_byte(0x253389D, 0x74)
    rom.write_bytes(0x25338A4, [0x00, 0x72, 0x00, 0x75, 0x00, 0x79])
    rom.write_bytes(0x25338BC, [0xFF, 0xFF])
    rom.write_bytes(0x25338C2, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    rom.write_bytes(0x25339C2, [0x00, 0x75, 0x00, 0x76])
    rom.write_bytes(0x2533830, [0x00, 0x31, 0x00, 0x81, 0x00, 0x82, 0x00, 0x82])

    # Speed Bridge of Light cutscene
    rom.write_bytes(0x292D644, [0x00, 0x00, 0x00, 0xA0])
    rom.write_bytes(0x292D680, [0x00, 0x02, 0x00, 0x0A, 0x00, 0x6C, 0x00, 0x00])
    rom.write_bytes(0x292D6E8, [0x00, 0x27])
    rom.write_bytes(0x292D718, [0x00, 0x32])
    rom.write_bytes(0x292D810, [0x00, 0x02, 0x00, 0x3C])
    rom.write_bytes(0x292D924, [0xFF, 0xFF, 0x00, 0x14, 0x00, 0x96, 0xFF, 0xFF])

    # Remove remaining owls
    rom.write_bytes(0x1FE30CE, [0x01, 0x4B])
    rom.write_bytes(0x1FE30DE, [0x01, 0x4B])
    rom.write_bytes(0x1FE30EE, [0x01, 0x4B])
    rom.write_bytes(0x205909E, [0x00, 0x3F])
    rom.write_byte(0x2059094, 0x80)

    # Darunia won't dance
    rom.write_bytes(0x22769E4, [0xFF, 0xFF, 0xFF, 0xFF])

    # Zora moves quickly
    rom.write_bytes(0xE56924, [0x00, 0x00, 0x00, 0x00])

    # Speed Jabu Jabu swallowing Link
    rom.write_bytes(0xCA0784, [0x00, 0x18, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])

    # Ruto no longer points to Zora Sapphire
    rom.write_bytes(0xD03BAC, [0xFF, 0xFF, 0xFF, 0xFF])

    # Ruto never disappears from Jabu Jabu's Belly
    rom.write_byte(0xD01EA3, 0x00)

    # Speed up Epona race start
    rom.write_bytes(0x29BE984, [0x00, 0x00, 0x00, 0x02])
    rom.write_bytes(0x29BE9CA, [0x00, 0x01, 0x00, 0x02])
    
    # Speed start of Horseback Archery
    #rom.write_bytes(0x21B2064, [0x00, 0x00, 0x00, 0x02])
    #rom.write_bytes(0x21B20AA, [0x00, 0x01, 0x00, 0x02])

    # Speed up Epona escape
    rom.write_bytes(0x1FC8B36, [0x00, 0x2A])

    # Speed up draining the well
    rom.write_bytes(0xE0A010, [0x00, 0x2A, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])
    rom.write_bytes(0x2001110, [0x00, 0x2B, 0x00, 0xB7, 0x00, 0xB8, 0x00, 0xB8])

    # Speed up opening the royal tomb for both child and adult
    rom.write_bytes(0x2025026, [0x00, 0x01])
    rom.write_bytes(0x2023C86, [0x00, 0x01])
    rom.write_byte(0x2025159, 0x02)
    rom.write_byte(0x2023E19, 0x02)

    #Speed opening of Door of Time
    rom.write_bytes(0xE0A176, [0x00, 0x02])
    rom.write_bytes(0xE0A35A, [0x00, 0x01, 0x00, 0x02])

    # Poacher's Saw no longer messes up Deku Theater
    rom.write_bytes(0xAE72CC, [0x00, 0x00, 0x00, 0x00])

    # Learning Serenade tied to opening chest in room
    Block_code = [0x3C, 0x0F, 0x80, 0x1D, 0x81, 0xE8, 0xA1, 0xDB, 0x24, 0x19, 0x00, 0x04,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8C, 0xA2, 0x1C, 0x44,
                  0x00, 0x00, 0x00, 0x00]
    rom.write_bytes(0xC7BCF0, Block_code)

    # Dampe Chest spawn condition looks at chest flag instead of having obtained hookshot
    Block_code = [0x93, 0x18, 0xAE, 0x7E, 0x27, 0xA5, 0x00, 0x24, 0x33, 0x19, 0x00, 0x01,
                  0x00, 0x00, 0x00, 0x00]
    rom.write_bytes(0xDFEC40, Block_code)

    # Darunia sets an event flag and checks for it
    Block_code = [0x24, 0x19, 0x00, 0x40, 0x8F, 0x09, 0xB4, 0xA8, 0x01, 0x39, 0x40, 0x24,
                  0x01, 0x39, 0xC8, 0x25, 0xAF, 0x19, 0xB4, 0xA8, 0x24, 0x09, 0x00, 0x06]
    rom.write_bytes(0xCF1AB8, Block_code)

    # Change Prelude CS to check for medallion
    rom.write_bytes(0x00C805E6, [0x00, 0xA6])
    rom.write_bytes(0x00C805F2, [0x00, 0x01])

    # Change Nocturne CS to check for medallions
    rom.write_bytes(0x00ACCD8E, [0x00, 0xA6])
    rom.write_bytes(0x00ACCD92, [0x00, 0x01])
    rom.write_bytes(0x00ACCD9A, [0x00, 0x02])
    rom.write_bytes(0x00ACCDA2, [0x00, 0x04])

    # Change King Zora to move even if Zora Sapphire is in inventory
    rom.write_bytes(0x00E55BB0, [0x85, 0xCE, 0x8C, 0x3C])
    rom.write_bytes(0x00E55BB4, [0x84, 0x4F, 0x0E, 0xDA])

    # Remove extra Forest Temple medallions
    rom.write_bytes(0x00D4D37C, [0x00, 0x00, 0x00, 0x00])

    # Remove extra Fire Temple medallions
    rom.write_bytes(0x00AC9754, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x00D0DB8C, [0x00, 0x00, 0x00, 0x00])

    # Remove extra Water Temple medallions
    rom.write_bytes(0x00D57F94, [0x00, 0x00, 0x00, 0x00])

    # Remove extra Spirit Temple medallions
    rom.write_bytes(0x00D370C4, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x00D379C4, [0x00, 0x00, 0x00, 0x00])

    # Remove extra Shadow Temple medallions
    rom.write_bytes(0x00D116E0, [0x00, 0x00, 0x00, 0x00])

    # Change Mido, Saria, and Kokiri to check for Deku Tree complete flag
    # bitwise pointer for 0x80
    kokiriAddresses = [0xE52836, 0xE53A56, 0xE51D4E, 0xE51F3E, 0xE51D96, 0xE51E1E, 0xE51E7E, 0xE51EDE, 0xE51FC6, 0xE51F96, 0xE293B6, 0xE29B8E, 0xE62EDA, 0xE630D6, 0xE62642, 0xE633AA, 0xE6369E]
    for kokiri in kokiriAddresses:
        rom.write_bytes(kokiri, [0x8C, 0x0C])
    # Kokiri
    rom.write_bytes(0xE52838, [0x94, 0x48, 0x0E, 0xD4])    
    rom.write_bytes(0xE53A58, [0x94, 0x49, 0x0E, 0xD4])
    rom.write_bytes(0xE51D50, [0x94, 0x58, 0x0E, 0xD4])
    rom.write_bytes(0xE51F40, [0x94, 0x4B, 0x0E, 0xD4])
    rom.write_bytes(0xE51D98, [0x94, 0x4B, 0x0E, 0xD4])
    rom.write_bytes(0xE51E20, [0x94, 0x4A, 0x0E, 0xD4])
    rom.write_bytes(0xE51E80, [0x94, 0x59, 0x0E, 0xD4])
    rom.write_bytes(0xE51EE0, [0x94, 0x4E, 0x0E, 0xD4])
    rom.write_bytes(0xE51FC8, [0x94, 0x49, 0x0E, 0xD4])
    rom.write_bytes(0xE51F98, [0x94, 0x58, 0x0E, 0xD4])
    # Saria
    rom.write_bytes(0xE293B8, [0x94, 0x78, 0x0E, 0xD4])
    rom.write_bytes(0xE29B90, [0x94, 0x68, 0x0E, 0xD4])
    # Mido
    rom.write_bytes(0xE62EDC, [0x94, 0x6F, 0x0E, 0xD4])
    rom.write_bytes(0xE630D8, [0x94, 0x4F, 0x0E, 0xD4])
    rom.write_bytes(0xE62644, [0x94, 0x6F, 0x0E, 0xD4])
    rom.write_bytes(0xE633AC, [0x94, 0x68, 0x0E, 0xD4])
    rom.write_bytes(0xE636A0, [0x94, 0x48, 0x0E, 0xD4])

    # Change adult Kokiri Forest to check for Forest Temple complete flag
    rom.write_bytes(0xE5369E, [0xB4, 0xAC])
    rom.write_bytes(0xD5A83C, [0x80, 0x49, 0x0E, 0xDC])

    # Change adult Goron City to check for Fire Temple complete flag
    rom.write_bytes(0xED59DC, [0x80, 0xC9, 0x0E, 0xDC])

    # Change Pokey to check DT complete flag
    rom.write_bytes(0xE5400A, [0x8C, 0x4C])
    rom.write_bytes(0xE5400E, [0xB4, 0xA4])
    if world.open_forest:
        rom.write_bytes(0xE5401C, [0x14, 0x0B])

    # Fix Shadow Temple to check for different rewards for scene
    rom.write_bytes(0xCA3F32, [0x00, 0x00, 0x25, 0x4A, 0x00, 0x10])

    # Fix Spirit Temple to check for different rewards for scene
    rom.write_bytes(0xCA3EA2, [0x00, 0x00, 0x25, 0x4A, 0x00, 0x08])

    # Fix Biggoron to check a different flag.
    rom.write_byte(0xED329B, 0x72)
    rom.write_byte(0xED43E7, 0x72)
    rom.write_bytes(0xED3370, [0x3C, 0x0D, 0x80, 0x12])
    rom.write_bytes(0xED3378, [0x91, 0xB8, 0xA6, 0x42, 0xA1, 0xA8, 0xA6, 0x42])
    rom.write_bytes(0xED6574, [0x00, 0x00, 0x00, 0x00])

    # Remove the check on the number of days that passed for claim check.
    rom.write_bytes(0xED4470, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xED4498, [0x00, 0x00, 0x00, 0x00])

    # Fixed reward order for Bombchu Bowling
    rom.write_bytes(0xE2E698, [0x80, 0xAA, 0xE2, 0x64])
    rom.write_bytes(0xE2E6A0, [0x80, 0xAA, 0xE2, 0x4C])
    rom.write_bytes(0xE2D440, [0x24, 0x19, 0x00, 0x00])

    # Make fishing less obnoxious
    Block_code = [0x3C, 0x0A, 0x80, 0x12, 0x8D, 0x4A, 0xA5, 0xD4, 0x14, 0x0A, 0x00, 0x06,
                  0x31, 0x78, 0x00, 0x01, 0x14, 0x18, 0x00, 0x02, 0x3c, 0x18, 0x42, 0x30,
                  0x3C, 0x18, 0x42, 0x50, 0x03, 0xe0, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00,
                  0x14, 0x18, 0x00, 0x02, 0x3C, 0x18, 0x42, 0x10, 0x3C, 0x18, 0x42, 0x38,
                  0x03, 0xE0, 0x00, 0x08]
    rom.write_bytes(0x3480C00, Block_code)
    rom.write_bytes(0xDBF434, [0x44, 0x98, 0x90, 0x00, 0xE6, 0x52, 0x01, 0x9C])
    rom.write_bytes(0xDBF484, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xDBF4A8, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xDCBEAA, [0x42, 0x48]) #set adult fish size requirement
    rom.write_bytes(0xDCBF26, [0x42, 0x48]) #set adult fish size requirement
    rom.write_bytes(0xDCBF32, [0x42, 0x30]) #set child fish size requirement
    rom.write_bytes(0xDCBF9E, [0x42, 0x30]) #set child fish size requirement

    # Dampe always digs something up and first dig is always the Piece of Heart
    rom.write_bytes(0xCC3FA8, [0xA2, 0x01, 0x01, 0xF8])
    rom.write_bytes(0xCC4024, [0x00, 0x00, 0x00, 0x00])
    
    # Allow owl to always carry the kid down Death Mountain
    rom.write_bytes(0xE304F0, [0x24, 0x0E, 0x00, 0x01])

    # Forbid Sun's Song from a bunch of cutscenes
    Suns_scenes = [0x2016FC9, 0x2017219, 0x20173D9, 0x20174C9, 0x2017679, 0x20C1539, 0x20C15D9, 0x21A0719, 0x21A07F9, 0x2E90129, 0x2E901B9, 0x2E90249, 0x225E829, 0x225E939, 0x306D009]
    for address in Suns_scenes:
        rom.write_byte(address,0x01)

    # Remove disruptive text from Gerudo Training Grounds and early Shadow Temple (vanilla)
    Wonder_text = [0x27C00BC, 0x27C00CC, 0x27C00DC, 0x27C00EC, 0x27C00FC, 0x27C010C, 0x27C011C, 0x27C012C, 0x27CE080,
                   0x27CE090, 0x2887070, 0x2887080, 0x2887090, 0x2897070, 0x28C7134, 0x28D91BC, 0x28A60F4, 0x28AE084,
                   0x28B9174, 0x28BF168, 0x28BF178, 0x28BF188, 0x28A1144, 0x28A6104, 0x28D0094]
    for address in Wonder_text:
        rom.write_byte(address, 0xFE)

    # Speed dig text for Dampe
    rom.write_bytes(0x9532F8, [0x08, 0x08, 0x08, 0x59])
    
    # Make item descriptions into a single box
    Short_item_descriptions = [0x92EC84, 0x92F9E3, 0x92F2B4, 0x92F37A, 0x92F513, 0x92F5C6, 0x92E93B, 0x92EA12]
    for address in Short_item_descriptions:
        rom.write_byte(address,0x02)

    # Fix text for Pocket Cucco.
    rom.write_byte(0xBEEF45, 0x0B)
    rom.write_byte(0x92D41A, 0x2E)
    Block_code = [0x59, 0x6f, 0x75, 0x20, 0x67, 0x6f, 0x74, 0x20, 0x61, 0x20, 0x05, 0x41,
                  0x50, 0x6f, 0x63, 0x6b, 0x65, 0x74, 0x20, 0x43, 0x75, 0x63, 0x63, 0x6f,
                  0x2c, 0x20, 0x05, 0x40, 0x6f, 0x6e, 0x65, 0x01, 0x6f, 0x66, 0x20, 0x41,
                  0x6e, 0x6a, 0x75, 0x27, 0x73, 0x20, 0x70, 0x72, 0x69, 0x7a, 0x65, 0x64,
                  0x20, 0x68, 0x65, 0x6e, 0x73, 0x21, 0x20, 0x49, 0x74, 0x20, 0x66, 0x69,
                  0x74, 0x73, 0x20, 0x01, 0x69, 0x6e, 0x20, 0x79, 0x6f, 0x75, 0x72, 0x20,
                  0x70, 0x6f, 0x63, 0x6b, 0x65, 0x74, 0x2e, 0x02]
    rom.write_bytes(0x92D41C, Block_code)

    # Set hooks for various code
    rom.write_bytes(0xDBF428, [0x0C, 0x10, 0x03, 0x00]) #Set Fishing Hook

    configure_dungeon_info(rom, world)

    # will be populated with data to be written to initial save
    # see initial_save.asm and config.asm for more details on specifics
    # or just use the following functions to add an entry to the table
    initial_save_table = []

    # will set the bits of value to the offset in the save (or'ing them with what is already there)
    def write_bits_to_save(offset, value, filter=None):
        nonlocal initial_save_table

        if filter and not filter(value):
            return

        initial_save_table += [(offset & 0xFF00) >> 8, offset & 0xFF, 0x00, value]
        


    # will overwrite the byte at offset with the given value
    def write_byte_to_save(offset, value, filter=None):
        nonlocal initial_save_table

        if filter and not filter(value):
            return

        initial_save_table += [(offset & 0xFF00) >> 8, offset & 0xFF, 0x01, value]

    # will overwrite the byte at offset with the given value
    def write_bytes_to_save(offset, bytes, filter=None):
        for i, value in enumerate(bytes):
            write_byte_to_save(offset + i, value, filter)

    # will overwrite the byte at offset with the given value
    def write_save_table(rom):
        nonlocal initial_save_table

        table_len = len(initial_save_table)
        if table_len > 0x400:
            raise Exception("The Initial Save Table has exceeded it's maximum capacity: 0x%03X/0x400" % table_len)
        rom.write_bytes(0x3481800, initial_save_table)


    # Initial Save Data
    write_bits_to_save(0x003F, 0x02) # Some Biggoron's Sword flag?

    write_bits_to_save(0x00D4 + 0x03 * 0x1C + 0x04 + 0x0, 0x08) # Forest Temple switch flag (Poe Sisters cutscene)
    write_bits_to_save(0x00D4 + 0x05 * 0x1C + 0x04 + 0x1, 0x01) # Water temple switch flag (Ruto)
    write_bits_to_save(0x00D4 + 0x51 * 0x1C + 0x04 + 0x2, 0x08) # Hyrule Field switch flag (Owl)
    write_bits_to_save(0x00D4 + 0x55 * 0x1C + 0x04 + 0x0, 0x80) # Kokiri Forest switch flag (Owl)
    write_bits_to_save(0x00D4 + 0x56 * 0x1C + 0x04 + 0x2, 0x40) # Sacred Forest Meadow switch flag (Owl)
    write_bits_to_save(0x00D4 + 0x5B * 0x1C + 0x04 + 0x2, 0x01) # Lost Woods switch flag (Owl)
    write_bits_to_save(0x00D4 + 0x5B * 0x1C + 0x04 + 0x3, 0x80) # Lost Woods switch flag (Owl)
    write_bits_to_save(0x00D4 + 0x5C * 0x1C + 0x04 + 0x0, 0x80) # Desert Colossus switch flag (Owl)
    write_bits_to_save(0x00D4 + 0x5F * 0x1C + 0x04 + 0x3, 0x20) # Hyrule Castle switch flag (Owl)

    write_bits_to_save(0x0ED4, 0x10) # "Met Deku Tree"
    write_bits_to_save(0x0ED5, 0x20) # "Deku Tree Opened Mouth"
    write_bits_to_save(0x0ED6, 0x08) # "Rented Horse From Ingo"
    write_bits_to_save(0x0EDA, 0x08) # "Began Nabooru Battle"
    write_bits_to_save(0x0EDC, 0x80) # "Entered the Master Sword Chamber"
    write_bits_to_save(0x0EDD, 0x20) # "Pulled Master Sword from Pedestal"
    write_bits_to_save(0x0EE0, 0x80) # "Spoke to Kaepora Gaebora by Lost Woods"
    write_bits_to_save(0x0EE7, 0x20) # "Nabooru Captured by Twinrova"
    write_bits_to_save(0x0EE7, 0x10) # "Spoke to Nabooru in Spirit Temple"
    write_bits_to_save(0x0EED, 0x20) # "Sheik, Spawned at Master Sword Pedestal as Adult"
    write_bits_to_save(0x0EED, 0x01) # "Nabooru Ordered to Fight by Twinrova"
    write_bits_to_save(0x0EF9, 0x01) # "Greeted by Saria"
    write_bits_to_save(0x0F0A, 0x04) # "Spoke to Ingo Once as Adult"
    write_bits_to_save(0x0F1A, 0x04) # "Met Darunia in Fire Temple"

    write_bits_to_save(0x0ED7, 0x01) # "Spoke to Child Malon at Castle or Market"
    write_bits_to_save(0x0ED7, 0x20) # "Spoke to Child Malon at Ranch"
    write_bits_to_save(0x0ED7, 0x40) # "Invited to Sing With Child Malon"
    write_bits_to_save(0x0F09, 0x10) # "Met Child Malon at Castle or Market"
    write_bits_to_save(0x0F09, 0x20) # "Child Malon Said Epona Was Scared of You"

    write_bits_to_save(0x0F21, 0x04) # "Ruto in JJ (M3) Talk First Time"
    write_bits_to_save(0x0F21, 0x02) # "Ruto in JJ (M2) Meet Ruto"

    write_bits_to_save(0x0EE2, 0x01) # "Began Ganondorf Battle"
    write_bits_to_save(0x0EE3, 0x80) # "Began Bongo Bongo Battle"
    write_bits_to_save(0x0EE3, 0x40) # "Began Barinade Battle"
    write_bits_to_save(0x0EE3, 0x20) # "Began Twinrova Battle"
    write_bits_to_save(0x0EE3, 0x10) # "Began Morpha Battle"
    write_bits_to_save(0x0EE3, 0x08) # "Began Volvagia Battle"
    write_bits_to_save(0x0EE3, 0x04) # "Began Phantom Ganon Battle"
    write_bits_to_save(0x0EE3, 0x02) # "Began King Dodongo Battle"
    write_bits_to_save(0x0EE3, 0x01) # "Began Gohma Battle"

    write_bits_to_save(0x0EE8, 0x01) # "Entered Deku Tree"
    write_bits_to_save(0x0EE9, 0x80) # "Entered Temple of Time"
    write_bits_to_save(0x0EE9, 0x40) # "Entered Goron City"
    write_bits_to_save(0x0EE9, 0x20) # "Entered Hyrule Castle"
    write_bits_to_save(0x0EE9, 0x10) # "Entered Zora's Domain"
    write_bits_to_save(0x0EE9, 0x08) # "Entered Kakariko Village"
    write_bits_to_save(0x0EE9, 0x02) # "Entered Death Mountain Trail"
    write_bits_to_save(0x0EE9, 0x01) # "Entered Hyrule Field"
    write_bits_to_save(0x0EEA, 0x04) # "Entered Ganon's Castle (Exterior)"
    write_bits_to_save(0x0EEA, 0x02) # "Entered Death Mountain Crater"
    write_bits_to_save(0x0EEA, 0x01) # "Entered Desert Colossus"
    write_bits_to_save(0x0EEB, 0x80) # "Entered Zora's Fountain"
    write_bits_to_save(0x0EEB, 0x40) # "Entered Graveyard"
    write_bits_to_save(0x0EEB, 0x20) # "Entered Jabu-Jabu's Belly"
    write_bits_to_save(0x0EEB, 0x10) # "Entered Lon Lon Ranch"
    write_bits_to_save(0x0EEB, 0x08) # "Entered Gerudo's Fortress"
    write_bits_to_save(0x0EEB, 0x04) # "Entered Gerudo Valley"
    write_bits_to_save(0x0EEB, 0x02) # "Entered Lake Hylia"
    write_bits_to_save(0x0EEB, 0x01) # "Entered Dodongo's Cavern"
    write_bits_to_save(0x0F08, 0x08) # "Entered Hyrule Castle"
 
    # Make the Kakariko Gate not open with the MS
    if not world.open_kakariko:
        rom.write_int32(0xDD3538, 0x34190000) # li t9, 0

    # Make all chest opening animations fast
    if world.fast_chests:
        rom.write_int32(0xBDA2E8, 0x240AFFFF) # addiu   t2, r0, -1
                               # replaces # lb      t2, 0x0002 (t1)

    # Set up for Rainbow Bridge dungeons condition
    Block_code = [0x15, 0x41, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x80, 0xEA, 0x00, 0xA5,
                  0x24, 0x01, 0x00, 0x1C, 0x31, 0x4A, 0x00, 0x1C, 0x08, 0x07, 0x88, 0xD9]
    rom.write_bytes(0x3480820, Block_code)

    # Gossip stones resond to stone of agony
    Block_code = [0x3C, 0x01, 0x80, 0x12, 0x80, 0x21, 0xA6, 0x75, 0x30, 0x21, 0x00, 0x20,
                  0x03, 0xE0, 0x00, 0x08]
    # Gossip stones always respond
    if(world.hints == 'always'):
        Block_code = [0x24, 0x01, 0x00, 0x20, 0x03, 0xE0, 0x00, 0x08]
    rom.write_bytes(0x3480840, Block_code)

    # Set up Rainbow Bridge conditions
    if world.bridge == 'medallions':
        Block_code = [0x80, 0xEA, 0x00, 0xA7, 0x24, 0x01, 0x00, 0x3F,
                      0x31, 0x4A, 0x00, 0x3F, 0x00, 0x00, 0x00, 0x00]
        rom.write_bytes(0xE2B454, Block_code)
    elif world.bridge == 'open':
        write_bits_to_save(0xEDC, 0x20) # "Rainbow Bridge Built by Sages"
    elif world.bridge == 'dungeons':
        Block_code = [0x80, 0xEA, 0x00, 0xA7, 0x24, 0x01, 0x00, 0x3F,
                      0x08, 0x10, 0x02, 0x08, 0x31, 0x4A, 0x00, 0x3F]
        rom.write_bytes(0xE2B454, Block_code)

    if world.open_forest:
        write_bits_to_save(0xED5, 0x10) # "Showed Mido Sword & Shield"

    if world.open_door_of_time:
        write_bits_to_save(0xEDC, 0x08) # "Opened the Door of Time"

    # "fast-ganon" stuff
    if world.no_escape_sequence:
        rom.write_bytes(0xD82A12, [0x05, 0x17]) # Sets exit from Ganondorf fight to entrance to Ganon fight
    if world.unlocked_ganondorf:
        write_bits_to_save(0x00D4 + 0x0A * 0x1C + 0x04 + 0x1, 0x10) # Ganon's Tower switch flag (unlock boss key door)
    if world.skipped_trials['Forest']:
        write_bits_to_save(0x0EEA, 0x08) # "Completed Forest Trial"
    if world.skipped_trials['Fire']:
        write_bits_to_save(0x0EEA, 0x40) # "Completed Fire Trial"
    if world.skipped_trials['Water']:
        write_bits_to_save(0x0EEA, 0x10) # "Completed Water Trial"
    if world.skipped_trials['Spirit']:
        write_bits_to_save(0x0EE8, 0x20) # "Completed Spirit Trial"
    if world.skipped_trials['Shadow']:
        write_bits_to_save(0x0EEA, 0x20) # "Completed Shadow Trial"
    if world.skipped_trials['Light']:
        write_bits_to_save(0x0EEA, 0x80) # "Completed Light Trial"
    if world.trials == 0:
        write_bits_to_save(0x0EED, 0x08) # "Dispelled Ganon's Tower Barrier"

    # open gerudo fortress
    if world.gerudo_fortress == 'open':
        write_bits_to_save(0x00A5, 0x40) # Give Gerudo Card
        write_bits_to_save(0x0EE7, 0x0F) # Free all 4 carpenters
        write_bits_to_save(0x00D4 + 0x0C * 0x1C + 0x04 + 0x1, 0x0F) # Thieves' Hideout switch flags (started all fights)
        write_bits_to_save(0x00D4 + 0x0C * 0x1C + 0x04 + 0x2, 0x01) # Thieves' Hideout switch flags (heard yells/unlocked doors)
        write_bits_to_save(0x00D4 + 0x0C * 0x1C + 0x04 + 0x3, 0xFE) # Thieves' Hideout switch flags (heard yells/unlocked doors)
        write_bits_to_save(0x00D4 + 0x0C * 0x1C + 0x0C + 0x2, 0xD4) # Thieves' Hideout collection flags (picked up keys, marks fights finished as well)
    elif world.gerudo_fortress == 'fast':
        write_bits_to_save(0x0EE7, 0x0E) # Free 3 carpenters
        write_bits_to_save(0x00D4 + 0x0C * 0x1C + 0x04 + 0x1, 0x0D) # Thieves' Hideout switch flags (started all fights)
        write_bits_to_save(0x00D4 + 0x0C * 0x1C + 0x04 + 0x2, 0x01) # Thieves' Hideout switch flags (heard yells/unlocked doors)
        write_bits_to_save(0x00D4 + 0x0C * 0x1C + 0x04 + 0x3, 0xDC) # Thieves' Hideout switch flags (heard yells/unlocked doors)
        write_bits_to_save(0x00D4 + 0x0C * 0x1C + 0x0C + 0x2, 0xC4) # Thieves' Hideout collection flags (picked up keys, marks fights finished as well)

    # Revert change that Skips the Epona Race
    if not world.no_epona_race:
        rom.write_int32(0xA9E838, 0x03E00008)

    # skip castle guard stealth sequence
    if world.no_guard_stealth:
        # change the exit at child/day crawlspace to the end of zelda's goddess cutscene
        rom.write_bytes(0x21F60DE, [0x05, 0xF0])

    # patch mq scenes
    mq_scenes = []
    if world.dungeon_mq['DT']:
        mq_scenes.append(0)
    if world.dungeon_mq['DC']:
        mq_scenes.append(1)
    if world.dungeon_mq['JB']:
        mq_scenes.append(2)
    if world.dungeon_mq['FoT']:
        mq_scenes.append(3)
    if world.dungeon_mq['FiT']:
        mq_scenes.append(4)
    if world.dungeon_mq['WT']:
        mq_scenes.append(5)
    if world.dungeon_mq['SpT']:
        mq_scenes.append(6)
    if world.dungeon_mq['ShT']:
        mq_scenes.append(7)
    if world.dungeon_mq['BW']:
        mq_scenes.append(8)
    if world.dungeon_mq['IC']:
        mq_scenes.append(9)
    # Scene 10 has no layout changes, so it doesn't need to be patched
    if world.dungeon_mq['GTG']:
        mq_scenes.append(11)
    if world.dungeon_mq['GC']:
        mq_scenes.append(13)

    patch_files(rom, mq_scenes)

    ### Load Shop File
    # Move shop actor file to free space
    shop_item_file = File({
            'Name':'En_GirlA',
            'Start':'00C004E0',
            'End':'00C02E00',
            'RemapStart':'03485000',
        })
    shop_item_file.relocate(rom)

    # Increase the shop item table size
    shop_item_vram_start = rom.read_int32(0x00B5E490 + (0x20 * 4) + 0x08)
    insert_space(rom, shop_item_file, shop_item_vram_start, 1, 0x3C + (0x20 * 50), 0x20 * 50)

    # Add relocation entries for shop item table
    new_relocations = []
    for i in range(50, 100):
        new_relocations.append(shop_item_file.start + 0x1DEC + (i * 0x20) + 0x04)
        new_relocations.append(shop_item_file.start + 0x1DEC + (i * 0x20) + 0x14)
        new_relocations.append(shop_item_file.start + 0x1DEC + (i * 0x20) + 0x1C)
    add_relocations(rom, shop_item_file, new_relocations)

    # update actor table
    rom.write_int32s(0x00B5E490 + (0x20 * 4), 
        [shop_item_file.start, 
        shop_item_file.end, 
        shop_item_vram_start, 
        shop_item_vram_start + (shop_item_file.end - shop_item_file.start)])

    # Update DMA Table
    update_dmadata(rom, shop_item_file)

    # Create 2nd Bazaar Room
    bazaar_room_file = File({
            'Name':'shop1_room_1',
            'Start':'028E4000',
            'End':'0290D7B0',
            'RemapStart':'03489000',
        })
    bazaar_room_file.dma_key = 0x03472000
    bazaar_room_file.relocate(rom)
    # Update DMA Table
    update_dmadata(rom, bazaar_room_file)

    # Add new Bazaar Room to Bazaar Scene
    rom.write_int32s(0x28E3030, [0x00010000, 0x02000058]) #reduce position list size
    rom.write_int32s(0x28E3008, [0x04020000, 0x02000070]) #expand room list size

    rom.write_int32s(0x28E3070, [0x028E4000, 0x0290D7B0, 
                     bazaar_room_file.start, bazaar_room_file.end]) #room list
    rom.write_int16s(0x28E3080, [0x0000, 0x0001]) # entrance list
    rom.write_int16(0x28E4076, 0x0005) # Change shop to Kakariko Bazaar
    #rom.write_int16(0x3489076, 0x0005) # Change shop to Kakariko Bazaar

    # Load Message and Shop Data
    messages = read_messages(rom)
    shop_items = read_shop_items(rom, shop_item_file.start + 0x1DEC)
    remove_unused_messages(messages)

    # Set Big Poe count to get reward from buyer
    poe_points = world.big_poe_count * 100
    rom.write_int16(0xEE69CE, poe_points)
    # update dialogue
    if world.big_poe_count != 10:
        new_message = "\x1AOh, you brought a Poe today!\x04\x1AHmmmm!\x04\x1AVery interesting!\x01This is a \x05\x41Big Poe\x05\x40!\x04\x1AI'll buy it for \x05\x4150 Rupees\x05\x40.\x04On top of that, I'll put \x05\x41100\x01points \x05\x40on your card.\x04\x1AIf you earn \x05\x41%d points\x05\x40, you'll\x01be a happy man! Heh heh." % poe_points
        update_message_by_id(messages, 0x70f7, new_message)
        new_message = "\x1AWait a minute! WOW!\x04\x1AYou have earned \x05\x41%d points\x05\x40!\x04\x1AYoung man, you are a genuine\x01\x05\x41Ghost Hunter\x05\x40!\x04\x1AIs that what you expected me to\x01say? Heh heh heh!\x04\x1ABecause of you, I have extra\x01inventory of \x05\x41Big Poes\x05\x40, so this will\x01be the last time I can buy a \x01ghost.\x04\x1AYou're thinking about what I \x01promised would happen when you\x01earned %d points. Heh heh.\x04\x1ADon't worry, I didn't forget.\x01Just take this." % (poe_points, poe_points)
        update_message_by_id(messages, 0x70f8, new_message)

    # Sets hooks for gossip stone changes
    if world.hints != 'none':
        if world.hints != 'mask':
            rom.write_bytes(0xEE7B84, [0x0C, 0x10, 0x02, 0x10])
            rom.write_bytes(0xEE7B8C, [0x24, 0x02, 0x00, 0x20])
        writeGossipStoneHintsHints(world, messages)

    # build silly ganon lines
    buildGanonText(world, messages)

    # Write item overrides
    override_table = get_override_table(world)
    rom.write_bytes(0x3481000, sum(override_table, []))
    rom.write_byte(0x03481C00, world.id + 1) # Write player ID

    # Revert Song Get Override Injection
    if not world.shuffle_song_items:
        # general get song
        rom.write_int32(0xAE5DF8, 0x240200FF)
        rom.write_int32(0xAE5E04, 0xAD0F00A4)
        # requiem of spirit
        rom.write_int32s(0xAC9ABC, [0x3C010001, 0x00300821])
        # sun song
        rom.write_int32(0xE09F68, 0x8C6F00A4)
        rom.write_int32(0xE09F74, 0x01CFC024)
        rom.write_int32(0xE09FB0, 0x240F0001)
        # epona
        rom.write_int32(0xD7E77C, 0x8C4900A4)
        rom.write_int32(0xD7E784, 0x8D088C24)
        rom.write_int32s(0xD7E8D4, [0x8DCE8C24, 0x8C4F00A4])
        rom.write_int32s(0xD7E140, [0x8DCE8C24, 0x8C6F00A4])
        rom.write_int32(0xD7EBBC, 0x14410008)
        rom.write_int32(0xD7EC1C, 0x17010010)
        # song of time
        rom.write_int32(0xDB532C, 0x24050003)

    # Set default targeting option to Hold
    if world.default_targeting == 'hold':
        rom.write_byte(0xB71E6D, 0x01)

    # Set OHKO mode
    if world.difficulty == 'ohko':
        rom.write_int32(0xAE80A8, 0xA4A00030) # sh  zero,48(a1)
        rom.write_int32(0xAE80B4, 0x06000003) # bltz s0, +0003

    # Patch songs and boss rewards
    for location in world.get_locations():
        item = location.item
        itemid = copy.copy(item.code)
        locationaddress = location.address
        secondaryaddress = location.address2

        if itemid is None or location.address is None:
            continue

        if location.type == 'Song' and not world.shuffle_song_items:
            rom.write_byte(locationaddress, itemid[0])
            itemid[0] = itemid[0] + 0x0D
            rom.write_byte(secondaryaddress, itemid[0])
            if location.name == 'Impa at Castle':
                impa_fix = 0x65 - itemid[1]
                rom.write_byte(0xD12ECB, impa_fix)
                rom.write_byte(0x2E8E931, item_data[item.name]) #Fix text box
            elif location.name == 'Song from Malon':
                if item.name == 'Suns Song':
                    rom.write_byte(locationaddress, itemid[0])
                malon_fix = 0x8C34 - (itemid[1] * 4)
                malon_fix_high = malon_fix >> 8
                malon_fix_low = malon_fix & 0x00FF
                rom.write_bytes(0xD7E142, [malon_fix_high, malon_fix_low])
                rom.write_bytes(0xD7E8D6, [malon_fix_high, malon_fix_low]) # I really don't like hardcoding these addresses, but for now.....
                rom.write_bytes(0xD7E786, [malon_fix_high, malon_fix_low])
                rom.write_byte(0x29BECB9, item_data[item.name]) #Fix text box
            elif location.name == 'Song from Composer Grave':
                sun_fix = 0x8C34 - (itemid[1] * 4)
                sun_fix_high = sun_fix >> 8
                sun_fix_low = sun_fix & 0x00FF
                rom.write_bytes(0xE09F66, [sun_fix_high, sun_fix_low])
                rom.write_byte(0x332A87D, item_data[item.name]) #Fix text box
            elif location.name == 'Song from Saria':
                saria_fix = 0x65 - itemid[1]
                rom.write_byte(0xE2A02B, saria_fix)
                rom.write_byte(0x20B1DBD, item_data[item.name]) #Fix text box
            elif location.name == 'Song from Ocarina of Time':
                rom.write_byte(0x252FC95, item_data[item.name]) #Fix text box
            elif location.name == 'Song at Windmill':
                windmill_fix = 0x65 - itemid[1]
                rom.write_byte(0xE42ABF, windmill_fix)
                rom.write_byte(0x3041091, item_data[item.name]) #Fix text box
            elif location.name == 'Sheik Forest Song':
                minuet_fix = 0x65 - itemid[1]
                rom.write_byte(0xC7BAA3, minuet_fix)
                rom.write_byte(0x20B0815, item_data[item.name]) #Fix text box
            elif location.name == 'Sheik at Temple':
                prelude_fix = 0x65 - itemid[1]
                rom.write_byte(0xC805EF, prelude_fix)
                rom.write_byte(0x2531335, item_data[item.name]) #Fix text box
            elif location.name == 'Sheik in Crater':
                bolero_fix = 0x65 - itemid[1]
                rom.write_byte(0xC7BC57, bolero_fix)
                rom.write_byte(0x224D7FD, item_data[item.name]) #Fix text box
            elif location.name == 'Sheik in Ice Cavern':
                serenade_fix = 0x65 - itemid[1]
                rom.write_byte(0xC7BD77, serenade_fix)
                rom.write_byte(0x2BEC895, item_data[item.name]) #Fix text box
            elif location.name == 'Sheik in Kakariko':
                nocturne_fix = 0x65 - itemid[1]
                rom.write_byte(0xAC9A5B, nocturne_fix)
                rom.write_byte(0x2000FED, item_data[item.name]) #Fix text box
            elif location.name == 'Sheik at Colossus':
                rom.write_byte(0x218C589, item_data[item.name]) #Fix text box
        elif location.type == 'Boss':
            if location.name == 'Links Pocket':
                write_bits_to_save(item_data[item.name][1], item_data[item.name][0])
            else:
                rom.write_byte(locationaddress, itemid)
                rom.write_byte(secondaryaddress, item_data[item.name][2])
                if location.name == 'Bongo Bongo':
                    rom.write_bytes(0xCA3F32, [item_data[item.name][3][0], item_data[item.name][3][1]])
                    rom.write_bytes(0xCA3F36, [item_data[item.name][3][2], item_data[item.name][3][3]])
                elif location.name == 'Twinrova':
                    rom.write_bytes(0xCA3EA2, [item_data[item.name][3][0], item_data[item.name][3][1]])
                    rom.write_bytes(0xCA3EA6, [item_data[item.name][3][2], item_data[item.name][3][3]])

    # add a cheaper bombchu pack to the bombchu shop
    # describe
    update_message_by_id(messages, 0x80FE, '\x08\x05\x41Bombchu   (5 pieces)   60 Rupees\x01\x05\x40This looks like a toy mouse, but\x01it\'s actually a self-propelled time\x01bomb!\x09\x0A', 0x03)
    # purchase
    update_message_by_id(messages, 0x80FF, '\x08Bombchu    5 Pieces    60 Rupees\x01\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x09', 0x03)
    rbl_bombchu = shop_items[0x0018]
    rbl_bombchu.price = 60
    rbl_bombchu.pieces = 5
    rbl_bombchu.get_item_id = 0x006A
    rbl_bombchu.description_message = 0x80FE
    rbl_bombchu.purchase_message = 0x80FF

    # Reduce 10 Pack Bombchus from 100 to 99 Rupees
    shop_items[0x0015].price = 99
    shop_items[0x0019].price = 99
    shop_items[0x001C].price = 99
    update_message_by_id(messages, shop_items[0x001C].description_message, "\x08\x05\x41Bombchu  (10 pieces)  99 Rupees\x01\x05\x40This looks like a toy mouse, but\x01it's actually a self-propelled time\x01bomb!\x09\x0A")
    update_message_by_id(messages, shop_items[0x001C].purchase_message, "\x08Bombchu  10 pieces   100 Rupees\x09\x01\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40")

    shuffle_messages.shop_item_messages = []

    # kokiri shop
    shop_objs = place_shop_items(rom, world, shop_items, messages, 
        world.get_region('Kokiri Shop').locations, True)
    shop_objs |= {0x00FC, 0x00B2, 0x0101, 0x0102, 0x00FD, 0x00C5} # Shop objects
    rom.write_byte(0x2587029, len(shop_objs))
    rom.write_int32(0x258702C, 0x0300F600)
    rom.write_int16s(0x2596600, list(shop_objs))

    # kakariko bazaar
    shop_objs = place_shop_items(rom, world, shop_items, messages,  
        world.get_region('Kakariko Bazaar').locations)
    shop_objs |= {0x005B, 0x00B2, 0x00C5, 0x0107, 0x00C9, 0x016B} # Shop objects
    rom.write_byte(0x28E4029, len(shop_objs))
    rom.write_int32(0x28E402C, 0x03007A40)
    rom.write_int16s(0x28EBA40, list(shop_objs))
 
    # castle town bazaar
    shop_objs = place_shop_items(rom, world, shop_items, messages,  
        world.get_region('Castle Town Bazaar').locations)
    shop_objs |= {0x005B, 0x00B2, 0x00C5, 0x0107, 0x00C9, 0x016B} # Shop objects
    rom.write_byte(0x3489029, len(shop_objs))
    rom.write_int32(0x348902C, 0x03007A40)
    rom.write_int16s(0x3490A40, list(shop_objs))
 
    # goron shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,  
        world.get_region('Goron Shop').locations)
    shop_objs |= {0x00C9, 0x00B2, 0x0103, 0x00AF} # Shop objects
    rom.write_byte(0x2D33029, len(shop_objs))
    rom.write_int32(0x2D3302C, 0x03004340)
    rom.write_int16s(0x2D37340, list(shop_objs))

    # zora shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,  
        world.get_region('Zora Shop').locations)
    shop_objs |= {0x005B, 0x00B2, 0x0104, 0x00FE} # Shop objects
    rom.write_byte(0x2D5B029, len(shop_objs))
    rom.write_int32(0x2D5B02C, 0x03004B40)
    rom.write_int16s(0x2D5FB40, list(shop_objs))

    # kakariko potion shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,  
        world.get_region('Kakariko Potion Shop Front').locations)
    shop_objs |= {0x0159, 0x00B2, 0x0175, 0x0122} # Shop objects
    rom.write_byte(0x2D83029, len(shop_objs))
    rom.write_int32(0x2D8302C, 0x0300A500)
    rom.write_int16s(0x2D8D500, list(shop_objs))

    # market potion shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,  
        world.get_region('Castle Town Potion Shop').locations)
    shop_objs |= {0x0159, 0x00B2, 0x0175, 0x00C5, 0x010C, 0x016B} # Shop objects
    rom.write_byte(0x2DB0029, len(shop_objs))
    rom.write_int32(0x2DB002C, 0x03004E40)
    rom.write_int16s(0x2DB4E40, list(shop_objs))

    # bombchu shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,  
        world.get_region('Castle Town Bombchu Shop').locations)
    shop_objs |= {0x0165, 0x00B2} # Shop objects
    rom.write_byte(0x2DD8029, len(shop_objs))
    rom.write_int32(0x2DD802C, 0x03006A40)
    rom.write_int16s(0x2DDEA40, list(shop_objs))

    if world.shuffle_scrubs:
        # Rebuild Deku Salescrub Item Table
        scrub_items = [0x30, 0x31, 0x3E, 0x33, 0x34, 0x37, 0x38, 0x39, 0x3A, 0x77, 0x79]
        rom.seek_address(0xDF8684)
        for scrub_item in scrub_items:
            rom.write_int16(None, 10)         # Price
            rom.write_int16(None, 1)          # Count
            rom.write_int32(None, scrub_item) # Item
            rom.write_int32(None, 0x80A74FF8) # Can_Buy_Func
            rom.write_int32(None, 0x80A75354) # Buy_Func

        # update actor IDs
        set_deku_salesman_data(rom)
    else:
        # Revert Deku Scrubs changes
        rom.write_int32s(0xEBB85C, [
            0x24010002, # addiu at, zero, 2
            0x3C038012, # lui v1, 0x8012
            0x14410004, # bne v0, at, 0xd8
            0x2463A5D0, # addiu v1, v1, -0x5a30
            0x94790EF0])# lhu t9, 0xef0(v1)
        rom.write_int32(0xDF7CB0,
            0xA44F0EF0)  # sh t7, 0xef0(v0)

    # Update grotto id data
    set_grotto_id_data(rom)

    if world.shuffle_smallkeys == 'remove' or world.shuffle_bosskeys == 'remove':
        locked_doors = get_locked_doors(rom, world)
        for _,[door_byte, door_bits] in locked_doors.items():
            write_bits_to_save(door_byte, door_bits)

    #Fix item chest animations
    chestAnimations = {
        0x3D: 0xED, #0x13 #Heart Container 
        0x3E: 0xEC, #0x14 #Piece of Heart  
        0x42: 0x02, #0xFE #Small Key   
        0x48: 0xF7, #0x09 #Recovery Heart  
        0x4F: 0xED, #0x13 #Heart Container 
        0x76: 0xEC, #0x14 #WINNER! Piece of Heart
    }
    if world.bombchus_in_logic:
        #Fix bombchu chest animations
        chestAnimations[0x6A] = 0x28 #0xD8 #Bombchu (5) 
        chestAnimations[0x03] = 0x28 #0xD8 #Bombchu (10) 
        chestAnimations[0x6B] = 0x28 #0xD8 #Bombchu (20) 
    for item_id, gfx_id in chestAnimations.items():
        rom.write_byte(0xBEEE8E + (item_id * 6) + 2, gfx_id)

    # Update chest type sizes
    if world.correct_chest_sizes:
        update_chest_sizes(rom, override_table)
        # Move Ganon's Castle's Zelda's Lullaby Chest back so is reachable if large
        rom.write_int16(0x321B176, 0xFC40) # original 0xFC48

    # give dungeon items the correct messages
    message_patch_for_dungeon_items(messages, shop_items, world)
    if world.shuffle_mapcompass == 'keysanity' and world.enhance_map_compass:
        reward_list = {'Kokiri Emerald':   "\x05\x42Kokiri Emerald\x05\x40",
                       'Goron Ruby':       "\x05\x41Goron Ruby\x05\x40",
                       'Zora Sapphire':    "\x05\x43Zora Sapphire\x05\x40",
                       'Forest Medallion': "\x05\x42Forest Medallion\x05\x40",
                       'Fire Medallion':   "\x05\x41Fire Medallion\x05\x40",
                       'Water Medallion':  "\x05\x43Water Medallion\x05\x40",
                       'Spirit Medallion': "\x05\x46Spirit Medallion\x05\x40",
                       'Shadow Medallion': "\x05\x45Shadow Medallion\x05\x40",
                       'Light Medallion':  "\x05\x44Light Medallion\x05\x40"
        }
        dungeon_list = {'DT':   ("the \x05\x42Deku Tree", 'Queen Gohma', 0x62, 0x88),
                        'DC':   ("\x05\x41Dodongo\'s Cavern", 'King Dodongo', 0x63, 0x89),
                        'JB':   ("\x05\x43Jabu Jabu\'s Belly", 'Barinade', 0x64, 0x8a),
                        'FoT':  ("the \x05\x42Forest Temple", 'Phantom Ganon', 0x65, 0x8b),
                        'FiT':  ("the \x05\x41Fire Temple", 'Volvagia', 0x7c, 0x8c),
                        'WT':   ("the \x05\x43Water Temple", 'Morpha', 0x7d, 0x8e),
                        'SpT':  ("the \x05\x46Spirit Temple", 'Twinrova', 0x7e, 0x8f),
                        'IC':   ("the \x05\x44Ice Cavern", None, 0x87, 0x92),
                        'BW':   ("the \x05\x45Bottom of the Well", None, 0xa2, 0xa5),
                        'ShT':   ("the \x05\x45Shadow Temple", 'Bongo Bongo', 0x7f, 0xa3),
        }
        for dungeon in world.dungeon_mq:
            if dungeon in ['GTG', 'GC']:
                pass
            elif dungeon in ['BW', 'IC']:
                dungeon_name, boss_name, compass_id, map_id = dungeon_list[dungeon]
                if world.world_count > 1:
                    map_message = "\x13\x76\x08\x05\x42\x0F\x05\x40 found the \x05\x41Dungeon Map\x05\x40\x01for %s\x05\x40!\x09" % (dungeon_name)
                else:
                    map_message = "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for %s\x05\x40!\x01It\'s %s!\x09" % (dungeon_name, "masterful" if world.dungeon_mq[dungeon] else "ordinary")

                if world.quest == 'mixed':
                    update_message_by_id(messages, map_id, map_message)
            else:
                dungeon_name, boss_name, compass_id, map_id = dungeon_list[dungeon]
                dungeon_reward = reward_list[world.get_location(boss_name).item.name]
                if world.world_count > 1:
                    compass_message = "\x13\x75\x08\x05\x42\x0F\x05\x40 found the \x05\x41Compass\x05\x40\x01for %s\x05\x40!\x09" % (dungeon_name)
                else:
                    compass_message = "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for %s\x05\x40!\x01It holds the %s!\x09" % (dungeon_name, dungeon_reward)
                update_message_by_id(messages, compass_id, compass_message)
                if world.quest == 'mixed':
                    if world.world_count > 1:
                        map_message = "\x13\x76\x08\x05\x42\x0F\x05\x40 found the \x05\x41Dungeon Map\x05\x40\x01for %s\x05\x40!\x09" % (dungeon_name)
                    else:
                        map_message = "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for %s\x05\x40!\x01It\'s %s!\x09" % (dungeon_name, "masterful" if world.dungeon_mq[dungeon] else "ordinary")
                    update_message_by_id(messages, map_id, map_message)

    else:
        # Set hints for boss reward shuffle
        rom.write_bytes(0xE2ADB2, [0x70, 0x7A])
        rom.write_bytes(0xE2ADB6, [0x70, 0x57])
        buildBossRewardHints(world, messages)

    # update happy mask shop to use new SOLD OUT text id
    rom.write_int16(shop_item_file.start + 0x1726, shop_items[0x26].description_message)

    # add song messages
    add_song_messages(messages, world)

    # reduce item message lengths
    update_item_messages(messages, world)

    # Add 3rd Wallet Upgrade
    rom.write_int16(0xB6D57E, 0x0003)
    rom.write_int16(0xB6EC52, 999)
    tycoon_message = "\x08\x13\x57You got a \x05\x43Tycoon's Wallet\x05\x40!\x01Now you can hold\x01up to \x05\x46999\x05\x40 \x05\x46Rupees\x05\x40."
    if world.world_count > 1:
       tycoon_message = make_player_message(tycoon_message)
    update_message_by_id(messages, 0x00F8, tycoon_message, 0x23)

    repack_messages(rom, messages)
    write_shop_items(rom, shop_item_file.start + 0x1DEC, shop_items)

    # text shuffle
    if world.text_shuffle == 'except_hints':
        shuffle_messages(rom, except_hints=True)
    elif world.text_shuffle == 'complete':
        shuffle_messages(rom, except_hints=False)

    # output a text dump, for testing...
    #with open('keysanity_' + str(world.seed) + '_dump.txt', 'w', encoding='utf-16') as f:
    #     messages = read_messages(rom)
    #     f.write('item_message_strings = {\n')
    #     for m in messages:
    #        f.write("\t0x%04X: \"%s\",\n" % (m.id, m.get_python_string()))
    #     f.write('}\n')


    scarecrow_song = None
    if world.free_scarecrow:
        scarecrow_song = str_to_song(world.scarecrow_song) #verified valid string in Main.py

        write_bits_to_save(0x0EE6, 0x10)     # Played song as adult
        write_byte_to_save(0x12C5, 0x01)    # Song is remembered
        write_bytes_to_save(0x12C6, scarecrow_song.playback_data[:(16*8)], lambda v: v != 0)

    if world.ocarina_songs:
        replace_songs(rom, scarecrow_song)

    # actually write the save table to rom
    write_save_table(rom)

    # patch music 
    if world.background_music == 'random':
        randomize_music(rom)
    elif world.background_music == 'off':    
        disable_music(rom)

    # re-seed for aesthetic effects. They shouldn't be affected by the generation seed
    random.seed()
    
    # patch tunic colors
    # Custom color tunic stuff
    Tunics = []
    Tunics.append(0x00B6DA38) # Kokiri Tunic
    Tunics.append(0x00B6DA3B) # Goron Tunic
    Tunics.append(0x00B6DA3E) # Zora Tunic
    colorList = get_tunic_colors()
    randomColors = random_choices(colorList, k=3)

    for i in range(len(Tunics)):
        # get the color option
        thisColor = world.tunic_colors[i]
        # handle true random
        randColor = [random.getrandbits(8), random.getrandbits(8), random.getrandbits(8)]
        if thisColor == 'Completely Random':
            color = randColor
        else:
            # handle random
            if world.tunic_colors[i] == 'Random Choice':
                color = TunicColors[randomColors[i]]
            # grab the color from the list
            elif thisColor in TunicColors: 
                color = TunicColors[thisColor] 
            # build color from hex code  
            else: 
                color = list(int(thisColor[i:i+2], 16) for i in (0, 2 ,4)) 
        rom.write_bytes(Tunics[i], color)

    # patch navi colors
    Navi = []
    Navi.append([0x00B5E184]) # Default
    Navi.append([0x00B5E19C, 0x00B5E1BC]) # Enemy, Boss
    Navi.append([0x00B5E194]) # NPC
    Navi.append([0x00B5E174, 0x00B5E17C, 0x00B5E18C, 0x00B5E1A4, 0x00B5E1AC, 0x00B5E1B4, 0x00B5E1C4, 0x00B5E1CC, 0x00B5E1D4]) # Everything else
    naviList = get_navi_colors()
    randomColors = random_choices(naviList, k=4)

    for i in range(len(Navi)):
        # do everything in the inner loop so that "true random" changes even for subcategories
        for j in range(len(Navi[i])):
            # get the color option
            thisColor = world.navi_colors[i]
            # handle true random
            randColor = [random.getrandbits(8), random.getrandbits(8), random.getrandbits(8), 0xFF,
                         random.getrandbits(8), random.getrandbits(8), random.getrandbits(8), 0x00]
            if thisColor == 'Completely Random':
                color = randColor
            else:
                # handle random
                if world.navi_colors[i] == 'Random Choice':
                    color = NaviColors[randomColors[i]]
                # grab the color from the list
                elif thisColor in NaviColors: 
                    color = NaviColors[thisColor] 
                # build color from hex code  
                else: 
                    color = list(int(thisColor[i:i+2], 16) for i in (0, 2 ,4)) 
                    color = color + [0xFF] + color + [0x00] 
            rom.write_bytes(Navi[i][j], color)

    #Navi hints
    NaviHint = []
    NaviHint.append([0xAE7EF2, 0xC26C7E]) #Overworld Hint
    NaviHint.append([0xAE7EC6]) #Enemy Target Hint
    naviHintSFXList = ['Default', 'Notification', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Navi - Random', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'None']
    randomNaviHintSFX = random_choices(naviHintSFXList, k=2)
    
    for i in range(len(NaviHint)):
        for j in range(len(NaviHint[i])):
            thisNaviHintSFX = world.navi_hint_sounds[i]
            if thisNaviHintSFX == 'Random Choice':
                thisNaviHintSFX = randomNaviHintSFX[i]
            if thisNaviHintSFX == 'Notification':
                naviHintSFX = [0x48, 0x20]
            elif thisNaviHintSFX == 'Rupee':
                naviHintSFX = [0x48, 0x03]
            elif thisNaviHintSFX == 'Timer':
                naviHintSFX = [0x48, 0x1A]
            elif thisNaviHintSFX == 'Tamborine':
                naviHintSFX = [0x48, 0x42]
            elif thisNaviHintSFX == 'Recovery Heart':
                naviHintSFX = [0x48, 0x0B]
            elif thisNaviHintSFX == 'Carrot Refill':
                naviHintSFX = [0x48, 0x45]
            elif thisNaviHintSFX == 'Navi - Hey!':
                naviHintSFX = [0x68, 0x5F]
            elif thisNaviHintSFX == 'Navi - Random':
                naviHintSFX = [0x68, 0x43]
            elif thisNaviHintSFX == 'Zelda - Gasp':
                naviHintSFX = [0x68, 0x79]
            elif thisNaviHintSFX == 'Cluck':
                naviHintSFX = [0x28, 0x12]
            elif thisNaviHintSFX == 'Mweep!':
                naviHintSFX = [0x68, 0x7A]
            elif thisNaviHintSFX == 'None':
                naviHintSFX = [0x00, 0x00]
            if thisNaviHintSFX != 'Default':
                rom.write_bytes(NaviHint[i][j], naviHintSFX)

    #Low health beep
    healthSFXList = ['Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'None']
    randomSFX = random.choice(healthSFXList)
    address = 0xADBA1A
    
    if world.healthSFX == 'Random Choice':
        thisHealthSFX = randomSFX
    else:
        thisHealthSFX = world.healthSFX
    if thisHealthSFX == 'Default':
        healthSFX = [0x48, 0x1B]
    elif thisHealthSFX == 'Softer Beep':
        healthSFX = [0x48, 0x04]
    elif thisHealthSFX == 'Rupee':
        healthSFX = [0x48, 0x03]
    elif thisHealthSFX == 'Timer':
        healthSFX = [0x48, 0x1A]
    elif thisHealthSFX == 'Tamborine':
        healthSFX = [0x48, 0x42]
    elif thisHealthSFX == 'Recovery Heart':
        healthSFX = [0x48, 0x0B]
    elif thisHealthSFX == 'Carrot Refill':
        healthSFX = [0x48, 0x45]
    elif thisHealthSFX == 'Navi - Hey!':
        healthSFX = [0x68, 0x5F]
    elif thisHealthSFX == 'Zelda - Gasp':
        healthSFX = [0x68, 0x79]
    elif thisHealthSFX == 'Cluck':
        healthSFX = [0x28, 0x12]
    elif thisHealthSFX == 'Mweep!':
        healthSFX = [0x68, 0x7A]
    elif thisHealthSFX == 'None':
        healthSFX = [0x00, 0x00, 0x00, 0x00]
        address = 0xADBA14
    rom.write_bytes(address, healthSFX)
        
    return rom

def get_override_table(world):
    override_entries = []
    for location in world.get_locations():
        override_entries.append(get_override_entry(location))
    override_entries.sort()
    return override_entries

def get_override_entry(location):
    scene = location.scene
    default = location.default
    item_id = location.item.index
    if None in [scene, default, item_id]:
        return []

    player_id = (location.item.world.id + 1) << 3

    if location.type in ['NPC', 'BossHeart', 'Song']:
        return [scene, player_id | 0x00, default, item_id]
    elif location.type == 'Chest':
        flag = default & 0x1F
        return [scene, player_id | 0x01, flag, item_id]
    elif location.type == 'Collectable':
        return [scene, player_id | 0x02, default, item_id]
    elif location.type == 'GS Token':
        return [scene, player_id | 0x03, default, item_id]
    elif location.type == 'Shop' and location.item.type != 'Shop':
        return [scene, player_id | 0x00, default, item_id]
    elif location.type == 'GrottoNPC' and location.item.type != 'Shop':
        return [scene, player_id | 0x04, default, item_id]    
    else:
        return []


chestTypeMap = {
        #    small   big     boss
    0x0000: [0x5000, 0x0000, 0x2000], #Large
    0x1000: [0x7000, 0x1000, 0x1000], #Large, Appears, Clear Flag
    0x2000: [0x5000, 0x0000, 0x2000], #Boss Key’s Chest
    0x3000: [0x8000, 0x3000, 0x3000], #Large, Falling, Switch Flag
    0x4000: [0x6000, 0x4000, 0x4000], #Large, Invisible
    0x5000: [0x5000, 0x0000, 0x2000], #Small
    0x6000: [0x6000, 0x4000, 0x4000], #Small, Invisible
    0x7000: [0x7000, 0x1000, 0x1000], #Small, Appears, Clear Flag
    0x8000: [0x8000, 0x3000, 0x3000], #Small, Falling, Switch Flag
    0x9000: [0x9000, 0x9000, 0x9000], #Large, Appears, Zelda's Lullaby
    0xA000: [0xA000, 0xA000, 0xA000], #Large, Appears, Sun's Song Triggered
    0xB000: [0xB000, 0xB000, 0xB000], #Large, Appears, Switch Flag
    0xC000: [0x5000, 0x0000, 0x2000], #Large
    0xD000: [0x5000, 0x0000, 0x2000], #Large
    0xE000: [0x5000, 0x0000, 0x2000], #Large
    0xF000: [0x5000, 0x0000, 0x2000], #Large
}

chestAnimationExtendedFast = [
    0x87, # Progressive Nut Capacity
    0x88, # Progressive Stick Capacity
    0x98, # Deku Tree Compass
    0x99, # Dodongo's Cavern Compass
    0x9A, # Jabu Jabu Compass
    0x9B, # Forest Temple Compass
    0x9C, # Fire Temple Compass
    0x9D, # Water Temple Compass
    0x9E, # Spirit Temple Compass
    0x9F, # Shadow Temple Compass
    0xA0, # Bottom of the Well Compass
    0xA1, # Ice Cavern Compass
    0xA2, # Deku Tree Map
    0xA3, # Dodongo's Cavern Map
    0xA4, # Jabu Jabu Map
    0xA5, # Forest Temple Map
    0xA6, # Fire Temple Map
    0xA7, # Water Temple Map
    0xA8, # Spirit Temple Map
    0xA9, # Shadow Temple Map
    0xAA, # Bottom of the Well Map
    0xAB, # Ice Cavern Map
    0xB6, # Recovery Heart
    0xB7, # Arrows (5)
    0xB8, # Arrows (10)
    0xB9, # Arrows (30)
    0xBA, # Bombs (5)
    0xBB, # Bombs (10)
    0xBC, # Bombs (20)
    0xBD, # Deku Nuts (5)
    0xBE, # Deku Nuts (10)
    0xD0, # Deku Stick (1)
    0xD1, # Deky Seeds (30)
]


def room_get_actors(rom, actor_func, room_data, scene, alternate=None):
    actors = {}
    room_start = alternate if alternate else room_data
    command = 0
    while command != 0x14: # 0x14 = end header
        command = rom.read_byte(room_data)
        if command == 0x01: # actor list
            actor_count = rom.read_byte(room_data + 1)
            actor_list = room_start + (rom.read_int32(room_data + 4) & 0x00FFFFFF)
            for _ in range(0, actor_count):
                actor_id = rom.read_int16(actor_list)
                entry = actor_func(rom, actor_id, actor_list, scene)
                if entry:
                    actors[actor_list] = entry
                actor_list = actor_list + 16
        if command == 0x18: # Alternate header list
            header_list = room_start + (rom.read_int32(room_data + 4) & 0x00FFFFFF)
            for alt_id in range(0,3):
                header_data = room_start + (rom.read_int32(header_list) & 0x00FFFFFF)
                if header_data != 0 and not alternate:
                    actors.update(room_get_actors(rom, actor_func, header_data, scene, room_start))
                header_list = header_list + 4
        room_data = room_data + 8
    return actors


def scene_get_actors(rom, actor_func, scene_data, scene, alternate=None, processed_rooms=None):
    if processed_rooms == None:
        processed_rooms = []
    actors = {}
    scene_start = alternate if alternate else scene_data
    command = 0
    while command != 0x14: # 0x14 = end header
        command = rom.read_byte(scene_data)
        if command == 0x04: #room list
            room_count = rom.read_byte(scene_data + 1)
            room_list = scene_start + (rom.read_int32(scene_data + 4) & 0x00FFFFFF)
            for _ in range(0, room_count):
                room_data = rom.read_int32(room_list);

                if not room_data in processed_rooms:
                    actors.update(room_get_actors(rom, actor_func, room_data, scene))
                    processed_rooms.append(room_data)
                room_list = room_list + 8
        if command == 0x0E: #transition actor list
            actor_count = rom.read_byte(scene_data + 1)
            actor_list = scene_start + (rom.read_int32(scene_data + 4) & 0x00FFFFFF)
            for _ in range(0, actor_count):
                actor_id = rom.read_int16(actor_list + 4)
                entry = actor_func(rom, actor_id, actor_list, scene)
                if entry:
                    actors[actor_list] = entry
                actor_list = actor_list + 16                
        if command == 0x18: # Alternate header list
            header_list = scene_start + (rom.read_int32(scene_data + 4) & 0x00FFFFFF)
            for alt_id in range(0,3):
                header_data = scene_start + (rom.read_int32(header_list) & 0x00FFFFFF)
                if header_data != 0 and not alternate:
                    actors.update(scene_get_actors(rom, actor_func, header_data, scene, scene_start, processed_rooms))
                header_list = header_list + 4

        scene_data = scene_data + 8
    return actors

def get_actor_list(rom, actor_func):
    actors = {}
    scene_table = 0x00B71440
    for scene in range(0x00, 0x65):
        scene_data = rom.read_int32(scene_table + (scene * 0x14));
        actors.update(scene_get_actors(rom, actor_func, scene_data, scene))
    return actors

def get_override_itemid(override_table, scene, type, flags):
    for entry in override_table:
        if len(entry) == 4 and entry[0] == scene and (entry[1] & 0x07) == type and entry[2] == flags:
            return entry[3]
    return None

def update_chest_sizes(rom, override_table):
    def get_chest(rom, actor_id, actor, scene):
        if actor_id == 0x000A: #Chest Actor
            actor_var = rom.read_int16(actor + 14)
            return [scene, actor_var & 0x001F]

    chest_list = get_actor_list(rom, get_chest)
    for actor, [scene, flags] in chest_list.items():
        item_id = get_override_itemid(override_table, scene, 1, flags)

        if None in [actor, scene, flags, item_id]:
            continue
        # Do not change the size of the chest under the grave in Dodongo's Cavern MQ.
        if scene == 1 and flags == 1:
            continue

        itemType = 0  # Item animation

        if item_id >= 0x80: # if extended item, always big except from exception list
            itemType = 0 if item_id in chestAnimationExtendedFast else 1
        elif rom.read_byte(0xBEEE8E + (item_id * 6) + 2) & 0x80: # get animation from rom, ice trap is big
            itemType = 0 # No animation, small chest
        else:
            itemType = 1 # Long animation, big chest
        # Don't use boss chests

        default = rom.read_int16(actor + 14)
        chestType = default & 0xF000
        newChestType = chestTypeMap[chestType][itemType]
        default = (default & 0x0FFF) | newChestType
        rom.write_int16(actor + 14, default)

def set_grotto_id_data(rom):
    def set_grotto_id(rom, actor_id, actor, scene):
        if actor_id == 0x009B: #Grotto
            actor_zrot = rom.read_int16(actor + 12)
            actor_var = rom.read_int16(actor + 14);
            grotto_scene = actor_var >> 12
            grotto_entrance = actor_zrot & 0x000F
            grotto_id = actor_var & 0x00FF

            if grotto_scene == 0 and grotto_entrance in [2, 4, 7, 10]:
                grotto_scenes.add(scene)
                rom.write_byte(actor + 15, len(grotto_scenes))

    grotto_scenes = set()

    get_actor_list(rom, set_grotto_id)

def set_deku_salesman_data(rom):
    def set_deku_salesman(rom, actor_id, actor, scene):
        if actor_id == 0x0195: #Salesman
            actor_var = rom.read_int16(actor + 14)
            if actor_var == 6:
                rom.write_int16(actor + 14, 0x0003)

    get_actor_list(rom, set_deku_salesman)

def get_locked_doors(rom, world):
    def locked_door(rom, actor_id, actor, scene):
        actor_var = rom.read_int16(actor + 14)
        actor_type = actor_var >> 6
        actor_flag = actor_var & 0x003F

        flag_id = (1 << actor_flag)
        flag_byte = 3 - (actor_flag >> 3)
        flag_bits = 1 << (actor_flag & 0x07)

        # If locked door, set the door's unlock flag
        if world.shuffle_smallkeys == 'remove':
            if actor_id == 0x0009 and actor_type == 0x02:
                return [0x00D4 + scene * 0x1C + 0x04 + flag_byte, flag_bits]
            if actor_id == 0x002E and actor_type == 0x0B:
                return [0x00D4 + scene * 0x1C + 0x04 + flag_byte, flag_bits]

        # If boss door, set the door's unlock flag
        if world.shuffle_bosskeys == 'remove':
            if actor_id == 0x002E and actor_type == 0x05:
                return [0x00D4 + scene * 0x1C + 0x04 + flag_byte, flag_bits]

    return get_actor_list(rom, locked_door)

def place_shop_items(rom, world, shop_items, messages, locations, init_shop_id=False): 
    if init_shop_id: 
        place_shop_items.shop_id = 0x32 

    shop_objs = { 0x0148 } # Sold Out 
    messages 
    for location in locations: 
        shop_objs.add(location.item.object) 
        if location.item.type == 'Shop': 
            rom.write_int16(location.address, location.item.index) 
        else: 
            shop_id = place_shop_items.shop_id 
            rom.write_int16(location.address, shop_id) 
            shop_item = shop_items[shop_id] 
 
            shop_item.object = location.item.object 
            shop_item.model = location.item.model - 1 
            shop_item.price = location.price 
            shop_item.pieces = 1 
            shop_item.get_item_id = location.default 
            shop_item.func1 = 0x808648CC 
            shop_item.func2 = 0x808636B8 
            shop_item.func3 = 0x00000000 
            shop_item.func4 = 0x80863FB4 
 
            message_id = (shop_id - 0x32) * 2 
            shop_item.description_message = 0x8100 + message_id 
            shop_item.purchase_message = 0x8100 + message_id + 1 

            shuffle_messages.shop_item_messages.extend(
                [shop_item.description_message, shop_item.purchase_message])

            if location.item.dungeonitem:
                split_item_name = location.item.name.split('(')
                split_item_name[1] = '(' + split_item_name[1]
                if world.world_count > 1:
                    description_text = '\x08\x05\x41%s  %d Rupees\x01%s\x01\x05\x42Player %d\x05\x40\x01Special deal! ONE LEFT!\x09\x0A\x02' % (split_item_name[0], location.price, split_item_name[1], location.item.world.id + 1)
                else:
                    description_text = '\x08\x05\x41%s  %d Rupees\x01%s\x01\x05\x40Special deal! ONE LEFT!\x01Get it while it lasts!\x09\x0A\x02' % (split_item_name[0], location.price, split_item_name[1])
                purchase_text = '\x08%s  %d Rupees\x09\x01%s\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x02' % (split_item_name[0], location.price, split_item_name[1])
            else:
                shop_item_name = getSimpleHintNoPrefix(location.item)

                if world.world_count > 1:
                    description_text = '\x08\x05\x41%s  %d Rupees\x01\x05\x42Player %d\x05\x40\x01Special deal! ONE LEFT!\x09\x0A\x02' % (shop_item_name, location.price, location.item.world.id + 1)
                else:
                    description_text = '\x08\x05\x41%s  %d Rupees\x01\x05\x40Special deal! ONE LEFT!\x01Get it while it lasts!\x09\x0A\x02' % (shop_item_name, location.price)
                purchase_text = '\x08%s  %d Rupees\x09\x01\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x02' % (shop_item_name, location.price)

            update_message_by_id(messages, shop_item.description_message, description_text, 0x03) 
            update_message_by_id(messages, shop_item.purchase_message, purchase_text, 0x03)  

            place_shop_items.shop_id += 1 
 
    return shop_objs 

# Format: (Title, Sequence ID)
bgm_sequence_ids = [
    ('Hyrule Field', 0x02),
    ('Dodongos Cavern', 0x18),
    ('Kakariko Adult', 0x19),
    ('Battle', 0x1A),
    ('Boss Battle', 0x1B),
    ('Inside Deku Tree', 0x1C),
    ('Market', 0x1D),
    ('Title Theme', 0x1E),
    ('House', 0x1F),
    ('Jabu Jabu', 0x26),
    ('Kakariko Child', 0x27),
    ('Fairy Fountain', 0x28),
    ('Zelda Theme', 0x29),
    ('Fire Temple', 0x2A),
    ('Forest Temple', 0x2C),
    ('Castle Courtyard', 0x2D),
    ('Ganondorf Theme', 0x2E),
    ('Lon Lon Ranch', 0x2F),
    ('Goron City', 0x30),
    ('Miniboss Battle', 0x38),
    ('Temple of Time', 0x3A),
    ('Kokiri Forest', 0x3C),
    ('Lost Woods', 0x3E),
    ('Spirit Temple', 0x3F),
    ('Horse Race', 0x40),
    ('Ingo Theme', 0x42),
    ('Fairy Flying', 0x4A),
    ('Deku Tree', 0x4B),
    ('Windmill Hut', 0x4C),
    ('Shooting Gallery', 0x4E),
    ('Sheik Theme', 0x4F),
    ('Zoras Domain', 0x50),
    ('Shop', 0x55),
    ('Chamber of the Sages', 0x56),
    ('Ice Cavern', 0x58),
    ('Kaepora Gaebora', 0x5A),
    ('Shadow Temple', 0x5B),
    ('Water Temple', 0x5C),
    ('Gerudo Valley', 0x5F),
    ('Potion Shop', 0x60),
    ('Kotake and Koume', 0x61),
    ('Castle Escape', 0x62),
    ('Castle Underground', 0x63),
    ('Ganondorf Battle', 0x64),
    ('Ganon Battle', 0x65),
    ('Fire Boss', 0x6B),
    ('Mini-game', 0x6C)
]

def randomize_music(rom):
    # Read in all the Music data
    bgm_data = []
    for bgm in bgm_sequence_ids:
        bgm_sequence = rom.read_bytes(0xB89AE0 + (bgm[1] * 0x10), 0x10)
        bgm_instrument = rom.read_int16(0xB89910 + 0xDD + (bgm[1] * 2))
        bgm_data.append((bgm_sequence, bgm_instrument))

    # shuffle data
    random.shuffle(bgm_data)

    # Write Music data back in random ordering
    for bgm in bgm_sequence_ids:
        bgm_sequence, bgm_instrument = bgm_data.pop()
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), bgm_sequence)
        rom.write_int16(0xB89910 + 0xDD + (bgm[1] * 2), bgm_instrument)

   # Write Fairy Fountain instrument to File Select (uses same track but different instrument set pointer for some reason) 
    rom.write_int16(0xB89910 + 0xDD + (0x57 * 2), rom.read_int16(0xB89910 + 0xDD + (0x28 * 2))) 
         
def disable_music(rom):
    # First track is no music
    blank_track = rom.read_bytes(0xB89AE0 + (0 * 0x10), 0x10)
    for bgm in bgm_sequence_ids:
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), blank_track)

def boss_reward_index(world, boss_name):
    code = world.get_location(boss_name).item.code
    if code >= 0x6C:
        return code - 0x6C
    else:
        return 3 + code - 0x66

def configure_dungeon_info(rom, world):
    mq_enable = world.quest == 'mixed'
    mapcompass_keysanity = world.settings.shuffle_mapcompass == 'keysanity' and world.settings.enhance_map_compass

    bosses = ['Queen Gohma', 'King Dodongo', 'Barinade', 'Phantom Ganon',
            'Volvagia', 'Morpha', 'Twinrova', 'Bongo Bongo']
    dungeon_rewards = [boss_reward_index(world, boss) for boss in bosses]

    codes = ['DT', 'DC', 'JB', 'FoT', 'FiT', 'WT', 'SpT', 'ShT',
            'BW', 'IC', 'Tower (N/A)', 'GTG', 'Hideout (N/A)', 'GC']
    dungeon_is_mq = [1 if world.dungeon_mq.get(c) else 0 for c in codes]

    rom.write_int32(rom.sym('cfg_dungeon_info_enable'), 1)
    rom.write_int32(rom.sym('cfg_dungeon_info_mq_enable'), int(mq_enable))
    rom.write_int32(rom.sym('cfg_dungeon_info_mq_need_map'), int(mapcompass_keysanity))
    rom.write_int32(rom.sym('cfg_dungeon_info_reward_need_compass'), int(mapcompass_keysanity))
    rom.write_int32(rom.sym('cfg_dungeon_info_reward_need_altar'), int(not mapcompass_keysanity))
    rom.write_bytes(rom.sym('cfg_dungeon_rewards'), dungeon_rewards)
    rom.write_bytes(rom.sym('cfg_dungeon_is_mq'), dungeon_is_mq)
