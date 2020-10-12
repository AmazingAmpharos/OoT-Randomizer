from version import __version__
from Utils import data_path
from Colors import *
import random
import logging
import Music as music
import Sounds as sfx
import IconManip as icon
from JSONDump import dump_obj, CollapseList, CollapseDict, AlignedDict, SortedDict
from SettingsList import setting_infos
from Plandomizer import InvalidFileException
import json


def patch_targeting(rom, settings, log, symbols):
    # Set default targeting option to Hold
    if settings.default_targeting == 'hold':
        rom.write_byte(0xB71E6D, 0x01)
    else:
        rom.write_byte(0xB71E6D, 0x00)


def patch_dpad(rom, settings, log, symbols):
    # Display D-Pad HUD
    if settings.display_dpad:
        rom.write_byte(symbols['CFG_DISPLAY_DPAD'], 0x01)
    else:
        rom.write_byte(symbols['CFG_DISPLAY_DPAD'], 0x00)
    log.display_dpad = settings.display_dpad



def patch_music(rom, settings, log, symbols):
    # patch music
    if settings.background_music != 'normal' or settings.fanfares != 'normal' or log.src_dict.get('bgm', {}):
        music.restore_music(rom)
        log.bgm, errors = music.randomize_music(rom, settings, log.src_dict.get('bgm', {}))
        log.errors.extend(errors)
    else:
        music.restore_music(rom)


def patch_model_colors(rom, color, model_addresses):
    main_addresses, dark_addresses = model_addresses

    for address in main_addresses:
        rom.write_bytes(address, color)

    darkened_color = list(map(lambda light: int(max((light - 0x32) * 0.6, 0)), color))
    for address in dark_addresses:
        rom.write_bytes(address, darkened_color)


def patch_tunic_icon(rom, tunic, color):
    # patch tunic icon colors
    icon_locations = {
        'Kokiri Tunic': 0x007FE000,
        'Goron Tunic': 0x007FF000,
        'Zora Tunic': 0x00800000,
    }

    tunic_icon = icon.generate_tunic_icon(color)

    rom.write_bytes(icon_locations[tunic], tunic_icon)


def patch_tunic_colors(rom, settings, log, symbols):
    # patch tunic colors
    tunics = [
        ('Kokiri Tunic', 'kokiri_color', 0x00B6DA38),
        ('Goron Tunic',  'goron_color',  0x00B6DA3B),
        ('Zora Tunic',   'zora_color',   0x00B6DA3E),
    ]
    tunic_color_list = get_tunic_colors()

    for tunic, tunic_setting, address in tunics:
        tunic_option = settings.__dict__[tunic_setting]

        # Handle Plando
        if log.src_dict.get('equipment_colors', {}).get(tunic, {}).get('color', ''):
            tunic_option = log.src_dict['equipment_colors'][tunic]['color']

        # handle random
        if tunic_option == 'Random Choice':
            tunic_option = random.choice(tunic_color_list)
        # handle completely random
        if tunic_option == 'Completely Random':
            color = generate_random_color()
        # grab the color from the list
        elif tunic_option in tunic_colors:
            color = list(tunic_colors[tunic_option])
        # build color from hex code
        else:
            color = hex_to_color(tunic_option)
            tunic_option = 'Custom'

        # "Weird" weirdshots will crash if the Kokiri Tunic Green value is > 0x90. Brickwall it.
        if settings.logic_rules != 'glitchless' and tunic == 'Kokiri Tunic':
            color[1] = min(color[1],0x90)
        rom.write_bytes(address, color)

        # patch the tunic icon
        if [tunic, tunic_option] not in [['Kokiri Tunic', 'Kokiri Green'], ['Goron Tunic', 'Goron Red'], ['Zora Tunic', 'Zora Blue']]:
            patch_tunic_icon(rom, tunic, color)

        log.equipment_colors[tunic] = CollapseDict({
            ':option': tunic_option,
            'color': color_to_hex(color),
        })


def patch_navi_colors(rom, settings, log, symbols):
    # patch navi colors
    navi = [
        # colors for Navi
        ('Navi Idle',            'navi_color_default',
            [0x00B5E184]), # Default
        ('Navi Targeting Enemy', 'navi_color_enemy',
            [0x00B5E19C, 0x00B5E1BC]), # Enemy, Boss
        ('Navi Targeting NPC',   'navi_color_npc',
            [0x00B5E194]), # NPC
        ('Navi Targeting Prop',  'navi_color_prop',
            [0x00B5E174, 0x00B5E17C, 0x00B5E18C,
            0x00B5E1A4, 0x00B5E1AC, 0x00B5E1B4,
            0x00B5E1C4, 0x00B5E1CC, 0x00B5E1D4]), # Everything else
    ]
    navi_color_list = get_navi_colors()
    for navi_action, navi_setting, navi_addresses in navi:
        navi_option_inner = settings.__dict__[navi_setting+'_inner']
        navi_option_outer = settings.__dict__[navi_setting+'_outer']
        plando_colors = log.src_dict.get('navi_colors', {}).get(navi_action, {}).get('colors', [])

        # choose a random choice for the whole group
        if navi_option_inner == 'Random Choice':
            navi_option_inner = random.choice(navi_color_list)
        if navi_option_outer == 'Random Choice':
            navi_option_outer = random.choice(navi_color_list)

        if navi_option_outer == '[Same as Inner]':
            navi_option_outer = navi_option_inner

        colors = []
        for address_index, address in enumerate(navi_addresses):
            address_colors = {}
            colors.append(address_colors)
            for index, (navi_part, option) in enumerate([('inner', navi_option_inner), ('outer', navi_option_outer)]):
                color = None

                # Plando
                if len(plando_colors) > address_index and plando_colors[address_index].get(navi_part, ''):
                    color = hex_to_color(plando_colors[address_index][navi_part])

                # completely random is random for every subgroup
                if color is None and option == 'Completely Random':
                    color = generate_random_color()

                # grab the color from the list
                if color is None and option in NaviColors:
                    color = list(NaviColors[option][index])

                # build color from hex code
                if color is None:
                    color = hex_to_color(option)
                    option = 'Custom'

                # Check color validity
                if color is None:
                    raise Exception(f'Invalid {navi_part} color {option} for {navi_action}')

                address_colors[navi_part] = color

            # write color
            color = address_colors['inner'] + [0xFF] + address_colors['outer'] + [0xFF]
            rom.write_bytes(address, color)

        # Get the colors into the log.
        log.navi_colors[navi_action] = CollapseDict({
            ':option_inner': navi_option_inner,
            ':option_outer': navi_option_outer,
            'colors': [],
        })
        for address_colors in colors:
            address_colors_str = CollapseDict()
            log.navi_colors[navi_action]['colors'].append(address_colors_str)
            for i, color in address_colors.items():
                address_colors_str[i] = color_to_hex(color)


def patch_sword_trails(rom, settings, log, symbols):
    # patch sword trail colors
    sword_trails = [
        ('Inner Initial Sword Trail', 'inner',
            [(0x00BEFF80, 0xB0, 0x40), (0x00BEFF88, 0x20, 0x00)], symbols['CFG_RAINBOW_SWORD_INNER_ENABLED']),
        ('Outer Initial Sword Trail', 'outer',
            [(0x00BEFF7C, 0xB0, 0xFF), (0x00BEFF84, 0x10, 0x00)], symbols['CFG_RAINBOW_SWORD_OUTER_ENABLED']),
    ]

    sword_color_list = get_sword_colors()

    log.equipment_colors['sword_trail_color'] = {}
    for index, item in enumerate(sword_trails):
        sword_trail_name, sword_trail_setting_ending, sword_trail_addresses, sword_trail_rainbow_symbol = item
        sword_trail_setting = 'sword_trail_color_' + sword_trail_setting_ending
        sword_trail_option = settings.__dict__[sword_trail_setting]

        # Setup Plando
        plando_colors = log.src_dict.get('equipment_colors', {}).get('sword_trail_color', {}).get(sword_trail_setting_ending, {}).get('colors', [])

        # handle random
        if sword_trail_option == 'Random Choice':
            sword_trail_option = random.choice(sword_color_list)

        colors = []
        custom_color = False
        for index, (address, transparency, white_transparency) in enumerate(sword_trail_addresses):
            # set rainbow option
            if sword_trail_option == 'Rainbow':
                rom.write_byte(sword_trail_rainbow_symbol, 0x01)
                color = [0x00, 0x00, 0x00]
                continue
            else:
                rom.write_byte(sword_trail_rainbow_symbol, 0x00)

            # handle plando
            if len(plando_colors) > index and plando_colors[index]:
                color = hex_to_color(plando_colors[index])
                custom_color = True

            # handle completely random
            elif sword_trail_option == 'Completely Random':
                color = generate_random_color()

            elif sword_trail_option in sword_colors:
                color = list(sword_colors[sword_trail_option][index])
            # build color from hex code
            else:
                color = hex_to_color(sword_trail_option)
                custom_color = True

            colors.append(color)
            if sword_trail_option == 'White':
                color = color + [white_transparency]
            else:
                color = color + [transparency]

            rom.write_bytes(address, color)

        if custom_color:
            sword_trail_option = 'Custom'
        log.equipment_colors['sword_trail_color'][sword_trail_setting_ending] = CollapseDict({':option': sword_trail_option})
        if sword_trail_option != "Rainbow":
            log.equipment_colors['sword_trail_color'][sword_trail_setting_ending]['colors'] = CollapseList([color_to_hex(color) for color in colors])
    rom.write_byte(0x00BEFF8C, settings.sword_trail_duration)


def patch_gauntlet_colors(rom, settings, log, symbols):
    # patch gauntlet colors
    gauntlets = [
        ('Silver Gauntlets', 'silver_gauntlets_color', 0x00B6DA44,
            ([0x173B4CC], [0x173B4D4, 0x173B50C, 0x173B514])), # GI Model DList colors
        ('Gold Gauntlets', 'golden_gauntlets_color',  0x00B6DA47,
            ([0x173B4EC], [0x173B4F4, 0x173B52C, 0x173B534])), # GI Model DList colors
    ]
    gauntlet_color_list = get_gauntlet_colors()

    for gauntlet, gauntlet_setting, address, model_addresses in gauntlets:
        gauntlet_option = settings.__dict__[gauntlet_setting]

        # Handle Plando
        if log.src_dict.get('equipment_colors', {}).get(gauntlet, {}).get('color', ''):
            gauntlet_option = log.src_dict['equipment_colors'][gauntlet]['color']

        # handle random
        if gauntlet_option == 'Random Choice':
            gauntlet_option = random.choice(gauntlet_color_list)
        # handle completely random
        if gauntlet_option == 'Completely Random':
            color = generate_random_color()
        # grab the color from the list
        elif gauntlet_option in gauntlet_colors:
            color = list(gauntlet_colors[gauntlet_option])
        # build color from hex code
        else:
            color = hex_to_color(gauntlet_option)
            gauntlet_option = 'Custom'
        rom.write_bytes(address, color)
        if settings.correct_model_colors:
            patch_model_colors(rom, color, model_addresses)
        log.equipment_colors[gauntlet] = CollapseDict({
            ':option': gauntlet_option,
            'color': color_to_hex(color),
        })

def patch_heart_colors(rom, settings, log, symbols):
    # patch heart colors
    hearts = [
        ('Heart Color', 'heart_color', symbols['CFG_HEART_COLOR'], 0xBB0994,
            ([0x14DA474, 0x14DA594, 0x14B701C, 0x14B70DC], 
             [0x14B70FC, 0x14DA494, 0x14DA5B4, 0x14B700C, 0x14B702C, 0x14B703C, 0x14B704C, 0x14B705C, 
              0x14B706C, 0x14B707C, 0x14B708C, 0x14B709C, 0x14B70AC, 0x14B70BC, 0x14B70CC])), # GI Model DList colors
    ]
    heart_color_list = get_heart_colors()

    for heart, heart_setting, symbol, file_select_address, model_addresses in hearts:
        heart_option = settings.__dict__[heart_setting]

        # Handle Plando
        if log.src_dict.get('ui_colors', {}).get(heart, {}).get('color', ''):
            heart_option = log.src_dict['ui_colors'][heart]['color']

        # handle random
        if heart_option == 'Random Choice':
            heart_option = random.choice(heart_color_list)
        # handle completely random
        if heart_option == 'Completely Random':
            color = generate_random_color()
        # grab the color from the list
        elif heart_option in heart_colors:
            color = list(heart_colors[heart_option])
        # build color from hex code
        else:
            color = hex_to_color(heart_option)
            heart_option = 'Custom'
        rom.write_int16s(symbol, color) # symbol for ingame HUD
        rom.write_int16s(file_select_address, color) # file select normal hearts
        if heart_option != 'Red':
            rom.write_int16s(file_select_address + 6, color) # file select DD hearts
            if settings.correct_model_colors:
                patch_model_colors(rom, color, model_addresses) # heart model colors
                icon.patch_overworld_icon(rom, color, 0xF43D80) # Overworld Heart Icon
        log.ui_colors[heart] = CollapseDict({
            ':option': heart_option,
            'color': color_to_hex(color),
        })

def patch_magic_colors(rom, settings, log, symbols):
    # patch magic colors
    magic = [
        ('Magic Meter Color', 'magic_color', symbols["CFG_MAGIC_COLOR"],
            ([0x154C654, 0x154CFB4], [0x154C65C, 0x154CFBC])), # GI Model DList colors
    ]
    magic_color_list = get_magic_colors()

    for magic_color, magic_setting, symbol, model_addresses in magic:
        magic_option = settings.__dict__[magic_setting]

        # Handle Plando
        if log.src_dict.get('ui_colors', {}).get(magic_color, {}).get('color', ''):
            magic_option = log.src_dict['ui_colors'][magic_color]['color']

        if magic_option == 'Random Choice':
           magic_option = random.choice(magic_color_list)

        if magic_option == 'Completely Random':
            color = generate_random_color()
        elif magic_option in magic_colors:
            color = list(magic_colors[magic_option])
        else:
            color = hex_to_color(magic_option)
            magic_option = 'Custom'
        rom.write_int16s(symbol, color)
        if magic_option != 'Green' and settings.correct_model_colors:
            patch_model_colors(rom, color, model_addresses)
            icon.patch_overworld_icon(rom, color, 0xF45650, data_path('icons/magicSmallExtras.raw')) # Overworld Small Pot
            icon.patch_overworld_icon(rom, color, 0xF47650, data_path('icons/magicLargeExtras.raw')) # Overworld Big Pot
        log.ui_colors[magic_color] = CollapseDict({
            ':option': magic_option,
            'color': color_to_hex(color),
        })

def patch_button_colors(rom, settings, log, symbols):
    buttons = [
        ('A Button Color', 'a_button_color', a_button_colors,
            [('A Button Color', symbols['CFG_A_BUTTON_COLOR'],
                None),
             ('Text Cursor Color', symbols['CFG_TEXT_CURSOR_COLOR'],
                [(0xB88E81, 0xB88E85, 0xB88E9)]), # Initial Inner Color
             ('Shop Cursor Color', symbols['CFG_SHOP_CURSOR_COLOR'],
                None),
             ('Save/Death Cursor Color', None,
                [(0xBBEBC2, 0xBBEBC3, 0xBBEBD6), (0xBBEDDA, 0xBBEDDB, 0xBBEDDE)]), # Save Cursor / Death Cursor
             ('Pause Menu A Cursor Color', None,
                [(0xBC7849, 0xBC784B, 0xBC784D), (0xBC78A9, 0xBC78AB, 0xBC78AD), (0xBC78BB, 0xBC78BD, 0xBC78BF)]), # Inner / Pulse 1 / Pulse 2
             ('Pause Menu A Icon Color', None,
                [(0x845754, 0x845755, 0x845756)]),
             ('A Note Color', symbols['CFG_A_NOTE_COLOR'], # For Textbox Song Display
                [(0xBB299A, 0xBB299B, 0xBB299E), (0xBB2C8E, 0xBB2C8F, 0xBB2C92), (0xBB2F8A, 0xBB2F8B, 0xBB2F96)]), # Pause Menu Song Display
            ]),
        ('B Button Color', 'b_button_color', b_button_colors,
            [('B Button Color', symbols['CFG_B_BUTTON_COLOR'],
                None),
            ]),
        ('C Button Color', 'c_button_color', c_button_colors,
            [('C Button Color', symbols['CFG_C_BUTTON_COLOR'],
                None),
             ('Pause Menu C Cursor Color', None,
                [(0xBC7843, 0xBC7845, 0xBC7847), (0xBC7891, 0xBC7893, 0xBC7895), (0xBC78A3, 0xBC78A5, 0xBC78A7)]), # Inner / Pulse 1 / Pulse 2
             ('Pause Menu C Icon Color', None,
                [(0x8456FC, 0x8456FD, 0x8456FE)]),
             ('C Note Color', symbols['CFG_C_NOTE_COLOR'], # For Textbox Song Display
                [(0xBB2996, 0xBB2997, 0xBB29A2), (0xBB2C8A, 0xBB2C8B, 0xBB2C96), (0xBB2F86, 0xBB2F87, 0xBB2F9A)]), # Pause Menu Song Display
            ]),
        ('Start Button Color', 'start_button_color', start_button_colors,
            [('Start Button Color', None,
                [(0xAE9EC6, 0xAE9EC7, 0xAE9EDA)]),
            ]),
    ]

    for button, button_setting, button_colors, patches in buttons:
        button_option = settings.__dict__[button_setting]
        color_set = None
        colors = {}
        log_dict = CollapseDict({':option': button_option, 'colors': {}})
        log.ui_colors[button] = log_dict

        # Setup Plando
        plando_colors = log.src_dict.get('ui_colors', {}).get(button, {}).get('colors', {})

        # handle random
        if button_option == 'Random Choice':
            button_option = random.choice(list(button_colors.keys()))
        # handle completely random
        if button_option == 'Completely Random':
            fixed_font_color = [10, 10, 10]
            color = [0, 0, 0]
            # Avoid colors which have a low contrast with the font inside buttons (eg. the A letter)
            while contrast_ratio(color, fixed_font_color) <= 3:
                color = generate_random_color()
        # grab the color from the list
        elif button_option in button_colors:
            color_set = [button_colors[button_option]] if isinstance(button_colors[button_option][0], int) else list(button_colors[button_option])
            color = color_set[0]
        # build color from hex code
        else:
            color = hex_to_color(button_option)
            button_option = 'Custom'
        log_dict[':option'] = button_option

        # apply all button color patches
        for i, (patch, symbol, byte_addresses) in enumerate(patches):
            if plando_colors.get(patch, ''):
                colors[patch] = hex_to_color(plando_colors[patch])
            elif color_set is not None and len(color_set) > i and color_set[i]:
                colors[patch] = color_set[i]
            else:
                colors[patch] = color

            if symbol:
                rom.write_int16s(symbol, colors[patch])

            if byte_addresses:
                for r_addr, g_addr, b_addr in byte_addresses:
                    rom.write_byte(r_addr, colors[patch][0])
                    rom.write_byte(g_addr, colors[patch][1])
                    rom.write_byte(b_addr, colors[patch][2])

            log_dict['colors'][patch] = color_to_hex(colors[patch])


def patch_sfx(rom, settings, log, symbols):
    # Configurable Sound Effects
    sfx_config = [
          ('sfx_navi_overworld', sfx.SoundHooks.NAVI_OVERWORLD),
          ('sfx_navi_enemy',     sfx.SoundHooks.NAVI_ENEMY),
          ('sfx_low_hp',         sfx.SoundHooks.HP_LOW),
          ('sfx_menu_cursor',    sfx.SoundHooks.MENU_CURSOR),
          ('sfx_menu_select',    sfx.SoundHooks.MENU_SELECT),
          ('sfx_nightfall',      sfx.SoundHooks.NIGHTFALL),
          ('sfx_horse_neigh',    sfx.SoundHooks.HORSE_NEIGH),
          ('sfx_hover_boots',    sfx.SoundHooks.BOOTS_HOVER),
    ]
    sound_dict = sfx.get_patch_dict()

    for setting, hook in sfx_config:
        selection = settings.__dict__[setting]

        # Handle Plando
        if log.src_dict.get('sfx', {}).get(hook.value.name, ''):
            selection = log.src_dict['sfx'][hook.value.name]

        if selection == 'default':
            for loc in hook.value.locations:
                sound_id = rom.original.read_int16(loc)
                rom.write_int16(loc, sound_id)
        else:
            if selection == 'random-choice':
                selection = random.choice(sfx.get_hook_pool(hook)).value.keyword
            elif selection == 'random-ear-safe':
                selection = random.choice(sfx.get_hook_pool(hook, "TRUE")).value.keyword
            elif selection == 'completely-random':
                selection = random.choice(sfx.standard).value.keyword
            sound_id  = sound_dict[selection]
            for loc in hook.value.locations:
                rom.write_int16(loc, sound_id)
        log.sfx[hook.value.name] = selection


def patch_instrument(rom, settings, log, symbols):
    # Player Instrument
    instruments = {
           #'none':            0x00,
            'ocarina':         0x01,
            'malon':           0x02,
            'whistle':         0x03,
            'harp':            0x04,
            'grind-organ':     0x05,
            'flute':           0x06,
           #'another_ocarina': 0x07,
            }

    choice = settings.sfx_ocarina
    if log.src_dict.get('sfx', {}).get('Ocarina', ''):
        choice = log.src_dict['sfx']['Ocarina']
    if choice != 'random-choice':
        choice = settings.sfx_ocarina
    else:
        choice = random.choice(list(instruments.keys()))

    rom.write_byte(0x00B53C7B, instruments[choice])
    rom.write_byte(0x00B4BF6F, instruments[choice]) # For Lost Woods Skull Kids' minigame in Lost Woods
    log.sfx['Ocarina'] = choice


legacy_cosmetic_data_headers = [
    0x03481000,
    0x03480810,
]

global_patch_sets = [
    patch_targeting,
    patch_music,
    patch_tunic_colors,
    patch_navi_colors,
    patch_gauntlet_colors,
    patch_sfx,
    patch_instrument,    
]

patch_sets = {
    0x1F04FA62: {
        "patches": [
            patch_dpad,
            patch_sword_trails,
        ],
        "symbols": {    
            "CFG_DISPLAY_DPAD": 0x0004,
            "CFG_RAINBOW_SWORD_INNER_ENABLED": 0x0005,
            "CFG_RAINBOW_SWORD_OUTER_ENABLED": 0x0006,
        },
    },
    0x1F05D3F9: {
        "patches": [
            patch_dpad,
            patch_sword_trails,
        ],
        "symbols": {    
            "CFG_DISPLAY_DPAD": 0x0004,
            "CFG_RAINBOW_SWORD_INNER_ENABLED": 0x0005,
            "CFG_RAINBOW_SWORD_OUTER_ENABLED": 0x0006,
        },
    },
    0x1F0693FB: {
        "patches": [
            patch_dpad,
            patch_sword_trails,
            patch_heart_colors,
            patch_magic_colors,
        ],
        "symbols": {
            "CFG_MAGIC_COLOR": 0x0004,
            "CFG_HEART_COLOR": 0x000A,
            "CFG_DISPLAY_DPAD": 0x0010,
            "CFG_RAINBOW_SWORD_INNER_ENABLED": 0x0011,
            "CFG_RAINBOW_SWORD_OUTER_ENABLED": 0x0012,
        }
    },
    0x1F073FC9: {
        "patches": [
            patch_dpad,
            patch_sword_trails,
            patch_heart_colors,
            patch_magic_colors,
            patch_button_colors,
        ],
        "symbols": {
            "CFG_MAGIC_COLOR": 0x0004,
            "CFG_HEART_COLOR": 0x000A,
            "CFG_A_BUTTON_COLOR": 0x0010,
            "CFG_B_BUTTON_COLOR": 0x0016,
            "CFG_C_BUTTON_COLOR": 0x001C,
            "CFG_TEXT_CURSOR_COLOR": 0x0022,
            "CFG_SHOP_CURSOR_COLOR": 0x0028,
            "CFG_A_NOTE_COLOR": 0x002E,
            "CFG_C_NOTE_COLOR": 0x0034,
            "CFG_DISPLAY_DPAD": 0x003A,
            "CFG_RAINBOW_SWORD_INNER_ENABLED": 0x003B,
            "CFG_RAINBOW_SWORD_OUTER_ENABLED": 0x003C,
        }
    },
}


def patch_cosmetics(settings, rom):
    # re-seed for aesthetic effects. They shouldn't be affected by the generation seed
    random.seed()
    settings.resolve_random_settings(cosmetic=True)

    # Initialize log and load cosmetic plando.
    log = CosmeticsLog(settings)

    # patch cosmetics that use vanilla oot data, and always compatible
    for patch_func in global_patch_sets:
        patch_func(rom, settings, log, {})

    # try to detect the cosmetic patch data format
    versioned_patch_set = None
    cosmetic_context = rom.read_int32(rom.sym('RANDO_CONTEXT') + 4)
    if cosmetic_context >= 0x80000000:
        cosmetic_context = (cosmetic_context - 0x80400000) + 0x3480000 # convert from RAM to ROM address
        cosmetic_version = rom.read_int32(cosmetic_context)
        versioned_patch_set = patch_sets.get(cosmetic_version)
    else:
        # If cosmetic_context is not a valid pointer, then try to
        # search over all possible legacy header locations.
        for header in legacy_cosmetic_data_headers:
            cosmetic_context = header
            cosmetic_version = rom.read_int32(cosmetic_context)
            if cosmetic_version in patch_sets:
                versioned_patch_set = patch_sets[cosmetic_version]
                break

    # patch version specific patches
    if versioned_patch_set:
        # offset the cosmetic_context struct for absolute addressing
        cosmetic_context_symbols = {
            sym: address + cosmetic_context
            for sym, address in versioned_patch_set['symbols'].items()
        }

        # warn if patching a legacy format
        if cosmetic_version != rom.read_int32(rom.sym('COSMETIC_FORMAT_VERSION')):
            log.errors.append("ROM uses old cosmetic patch format.")

        for patch_func in versioned_patch_set['patches']:
            patch_func(rom, settings, log, cosmetic_context_symbols)
    else:
        # Unknown patch format
        log.errors.append("Unable to patch some cosmetics. ROM uses unknown cosmetic patch format.")

    return log


class CosmeticsLog(object):

    def __init__(self, settings):
        self.settings = settings

        self.equipment_colors = {}
        self.ui_colors = {}
        self.navi_colors = {}
        self.sfx = {}
        self.bgm = {}

        self.src_dict = {}
        self.errors = []

        if self.settings.enable_cosmetic_file:
            if self.settings.cosmetic_file:
                try:
                    if any(map(self.settings.cosmetic_file.endswith, ['.z64', '.n64', '.v64'])):
                        raise InvalidFileException("Your Ocarina of Time ROM doesn't belong in the cosmetics plandomizer setting. If you don't know what this is for, or don't plan to use it, disable cosmetic plandomizer and try again.")
                    with open(self.settings.cosmetic_file) as infile:
                        self.src_dict = json.load(infile)
                except json.decoder.JSONDecodeError as e:
                    raise InvalidFileException(f"Invalid Cosmetic Plandomizer File. Make sure the file is a valid JSON file. Failure reason: {str(e)}") from None
                except FileNotFoundError:
                    message = "Cosmetic Plandomizer file not found at %s" % (self.settings.cosmetic_file)
                    logging.getLogger('').warning(message)
                    self.errors.append(message)
                    self.settings.enable_cosmetic_file = False
                except InvalidFileException as e:
                    logging.getLogger('').warning(str(e))
                    self.errors.append(str(e))
                    self.settings.enable_cosmetic_file = False
            else:
                logging.getLogger('').warning("Cosmetic Plandomizer enabled, but no file provided.")
                self.settings.enable_cosmetic_file = False

        if self.src_dict.get('settings', {}):
            valid_settings = []
            for setting in setting_infos:
                if setting.name not in self.src_dict['settings'] or not setting.cosmetic:
                    continue
                self.settings.__dict__[setting.name] = self.src_dict['settings'][setting.name]
                valid_settings.append(setting.name)
            for setting in list(self.src_dict['settings'].keys()):
                if setting not in valid_settings:
                    del self.src_dict['settings'][setting]
            if self.src_dict['settings'].get('randomize_all_cosmetics', False):
                settings.resolve_random_settings(cosmetic=True, randomize_key='randomize_all_cosmetics')
            if self.src_dict['settings'].get('randomize_all_sfx', False):
                settings.resolve_random_settings(cosmetic=True, randomize_key='randomize_all_sfx')


    def to_json(self):
        self_dict = {
            ':version': __version__,
            ':enable_cosmetic_file': True,
            ':errors': self.errors,
            'settings': self.settings.to_json_cosmetics(),
            'equipment_colors': self.equipment_colors,
            'ui_colors': self.ui_colors,
            'navi_colors': self.navi_colors,
            'sfx': self.sfx,
            'bgm': self.bgm,
        }

        if (not self.settings.enable_cosmetic_file):
            del self_dict[':enable_cosmetic_file'] # Done this way for ordering purposes.
        if (not self.errors):
            del self_dict[':errors']

        return self_dict


    def to_str(self):
        return dump_obj(self.to_json(), ensure_ascii=False)


    def to_file(self, filename):
        json = self.to_str()
        with open(filename, 'w') as outfile:
            outfile.write(json)
