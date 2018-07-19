import argparse
import textwrap
import string
import re
import random
import hashlib

from Rom import get_tunic_color_options, get_navi_color_options
from version import __version__

class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)


# 32 characters
letters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
index_to_letter = { i: letters[i] for i in range(32) }
letter_to_index = { v: k for k, v in index_to_letter.items() }

def bit_string_to_text(bits):
    # pad the bits array to be multiple of 5
    if len(bits) % 5 > 0:
        bits += [0] * (5 - len(bits) % 5)
    # convert to characters
    result = ""
    for i in range(0, len(bits), 5):
        chunk = bits[i:i + 5]
        value = 0
        for b in range(5):
            value |= chunk[b] << b
        result += index_to_letter[value]
    return result

def text_to_bit_string(text):
    bits = []
    for c in text:
        index = letter_to_index[c]
        for b in range(5):
            bits += [ (index >> b) & 1 ]
    return bits

# holds the info for a single setting
class Setting_Info():

    def __init__(self, name, type, bitwidth=0, shared=False, args_params={}, gui_params=None):
        self.name = name # name of the setting, used as a key to retrieve the setting's value everywhere
        self.type = type # type of the setting's value, used to properly convert types in GUI code
        self.bitwidth = bitwidth # number of bits needed to store the setting, used in converting settings to a string
        self.shared = shared # whether or not the setting is one that should be shared, used in converting settings to a string
        self.args_params = args_params # parameters that should be pased to the command line argument parser's add_argument() function
        self.gui_params = gui_params # parameters that the gui uses to build the widget components

# holds the particular choices for a run's settings
class Settings():

    def get_settings_display(self):
        padding = 0
        for setting in filter(lambda s: s.shared, setting_infos):
            padding = max( len(setting.name), padding )
        padding += 2
        output = ''
        for setting in filter(lambda s: s.shared, setting_infos):
            name = setting.name + ': ' + ' ' * (padding - len(setting.name))
            val = str(self.__dict__[setting.name])
            output += name + val + '\n'
        return output

    def get_settings_string(self):
        bits = []
        for setting in filter(lambda s: s.shared and s.bitwidth > 0, setting_infos):
            value = self.__dict__[setting.name]
            i_bits = []
            if setting.type == bool:
                i_bits = [ 1 if value else 0 ]
            if setting.type == str:
                index = setting.args_params['choices'].index(value)
                # https://stackoverflow.com/questions/10321978/integer-to-bitfield-as-a-list
                i_bits = [1 if digit=='1' else 0 for digit in bin(index)[2:]]
                i_bits.reverse()
            if setting.type == int:
                value = value - ('min' in setting.gui_params and setting.gui_params['min'] or 0)
                value = int(value / ('step' in setting.gui_params and setting.gui_params['step'] or 1))
                value = min(value, ('max' in setting.gui_params and setting.gui_params['max'] or value))
                # https://stackoverflow.com/questions/10321978/integer-to-bitfield-as-a-list
                i_bits = [1 if digit=='1' else 0 for digit in bin(value)[2:]]
                i_bits.reverse()
            # pad it
            i_bits += [0] * ( setting.bitwidth - len(i_bits) )
            bits += i_bits
        return bit_string_to_text(bits)

    def update_with_settings_string(self, text):
        bits = text_to_bit_string(text)

        for setting in filter(lambda s: s.shared and s.bitwidth > 0, setting_infos):
            cur_bits = bits[:setting.bitwidth]
            bits = bits[setting.bitwidth:]
            value = None
            if setting.type == bool:
                value = True if cur_bits[0] == 1 else False
            if setting.type == str:
                index = 0
                for b in range(setting.bitwidth):
                    index |= cur_bits[b] << b
                value = setting.args_params['choices'][index]
            if setting.type == int:
                value = 0
                for b in range(setting.bitwidth):
                    value |= cur_bits[b] << b
                value = value * ('step' in setting.gui_params and setting.gui_params['step'] or 1)
                value = value + ('min' in setting.gui_params and setting.gui_params['min'] or 0)
            self.__dict__[setting.name] = value

        self.settings_string = self.get_settings_string()
        self.numeric_seed = self.get_numeric_seed()

    def get_numeric_seed(self):
        # salt seed with the settings, and hash to get a numeric seed
        full_string = self.settings_string + __version__ + self.seed
        return int(hashlib.sha256(full_string.encode('utf-8')).hexdigest(), 16)

    def sanatize_seed(self):
        # leave only alphanumeric and some punctuation
        self.seed = re.sub(r'[^a-zA-Z0-9_-]', '', self.seed, re.UNICODE)

    def update_seed(self, seed):
        self.seed = seed
        self.sanatize_seed()
        self.numeric_seed = self.get_numeric_seed()

    # add the settings as fields, and calculate information based on them
    def __init__(self, settings_dict):
        self.__dict__.update(settings_dict)
        for info in setting_infos:
            if info.name not in self.__dict__:
                if info.type == bool:
                    self.__dict__[info.name] = True if info.gui_params['default'] == 'checked' else False
                if info.type == str:
                    if 'default' in info.args_params:
                        self.__dict__[info.name] = info.gui_params['default'] or info.args_params['default']
                    else:
                        self.__dict__[info.name] = ""
                if info.type == int:
                    self.__dict__[info.name] = info.gui_params['default'] or 1
        self.settings_string = self.get_settings_string()
        if(self.seed is None):
            # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
            self.seed = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.sanatize_seed()
        self.numeric_seed = self.get_numeric_seed()


# a list of the possible settings
setting_infos = [
    Setting_Info('rom', str, 0, False, {
            'default': 'ZOOTDEC.z64',
            'help': 'Path to an OoT 1.0 rom to use as a base.'}),
    Setting_Info('output_dir', str, 0, False, {
            'default': '',
            'help': 'Path to output directory for rom generation.'}),
    Setting_Info('seed', str, 0, False, {
            'help': 'Define seed number to generate.'}),
    Setting_Info('count', int, 0, False, {
            'help': '''\
                    Use to batch generate multiple seeds with same settings.
                    If --seed is provided, it will be used for the first seed, then
                    used to derive the next seed (i.e. generating 10 seeds with
                    --seed given will produce the same 10 (different) roms each
                    time).
                    ''',
            'type': int}),
    Setting_Info('world_count', int, 0, False, {
            'help': '''\
                    Use to create a multi-world generation for co-op seeds.
                    World count is the number of players. Warning: Increasing
                    the world count will drastically increase generation time.
                    ''',
            'type': int}),
    Setting_Info('player_num', int, 0, False, {
            'help': '''\
                    Use to select world to generate when there are multiple worlds.
                    ''',
            'type': int}),
    Setting_Info('create_spoiler', bool, 1, True, 
        {
            'help': 'Output a Spoiler File',
            'action': 'store_true'
        }, 
        {
            'text': 'Create Spoiler Log',
            'group': 'rom_tab',
            'widget': 'Checkbutton',
            'default': 'checked'
        }),
    Setting_Info('suppress_rom', bool, 0, False, 
        {
            'help': 'Do not create an output rom file.',
            'action': 'store_true'
        }, 
        {
            'text': 'Do not create Rom',
            'group': 'rom_tab',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('compress_rom', bool, 0, False, 
        {
            'help': 'Create a compressed version of the output rom file.',
            'action': 'store_true'
        },
        {
            'text': 'Compress Rom. Improves stability but will take longer to generate',
            'group': 'rom_tab',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('open_forest', bool, 1, True, 
        {
            'help': '''\
                    Mido no longer blocks the path to the Deku Tree and
                    the Kokiri boy no longer blocks the path out of the forest.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Open Forest',
            'group': 'open',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('open_door_of_time', bool, 1, True, 
        {
            'help': '''\
                    The Door of Time is open from the beginning of the game.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Open Door of Time',
            'group': 'open',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('gerudo_fortress', str, 2, True, 
        {
            'default': 'normal',
            'const': 'normal',
            'nargs': '?',
            'choices': ['normal', 'fast', 'open'],
            'help': '''\
                    Select how much of Gerudo Fortress is required. (default: %(default)s)
                    Normal: Free all four carpenters to get the Gerudo Card.
                    Fast:   Free only the carpenter closest to Link's prison to get the Gerudo Card.
                    Open:   Start with the Gerudo Card and all it's benefits.
                    '''
        },
        {
            'text': 'Gerudo Fortress',
            'group': 'open',
            'widget': 'Combobox',
            'default': 'Default Behavior',
            'options': {
                'Default Behavior': 'normal',
                'Rescue one carpenter': 'fast',
                'Start with Gerudo Card': 'open',
            },
        }),
    Setting_Info('bridge', str, 2, True, 
        {
            'default': 'medallions',
            'const': 'medallions',
            'nargs': '?',
            'choices': ['medallions', 'vanilla', 'dungeons', 'open'],
            'help': '''\
                    Select requirement to spawn the Rainbow Bridge to reach Ganon's Castle. (default: %(default)s)
                    Medallions:    Collect all six medallions to create the bridge.
                    Vanilla:       Collect only the Shadow and Spirit Medallions and then view the Light Arrow cutscene.
                    All Dungeons:  Collect all spiritual stones and all medallions to create the bridge.
                    Open:          The bridge will spawn without an item requirement.
                    '''
        },
        {
            'text': 'Rainbow Bridge Requirement',
            'group': 'open',
            'widget': 'Combobox',
            'default': 'All medallions',
            'options': {
                'All dungeons': 'dungeons',
                'All medallions': 'medallions',
                'Vanilla requirements': 'vanilla',
                'Always open': 'open',
            },
        }),
    Setting_Info('bombchus_in_logic', bool, 1, True, 
        {
            'help': '''\
                    Bombchus will be considered in logic. This has a few effects:
                    -Back alley shop will open once you've found Bombchus
                    -It will sell an affordable pack (5 for 60), and never sell out
                    -Bombchu Bowling will open once you've found Bombchus
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Bombchus are considered in logic',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'checked'
        }),
    Setting_Info('trials', int, 3, True, 
        {
            'default': 6,
            'const': 6,
            'nargs': '?',
            'choices': [0, 1, 2, 3, 4, 5, 6],
            'help': '''\
                    Select how many trials must be cleared to enter Ganon's Tower.
                    The trials you must complete will be selected randomly.
                    ''',
            'type': int                    
        },
        {
            'text': 'Number of Ganon\'s Trials',
            'group': 'open',
            'widget': 'Scale',
            'default': 6,
            'min': 0,
            'max': 6,
        }),
    Setting_Info('no_escape_sequence', bool, 1, True, 
        {
            'help': '''\
                    The tower collapse escape sequence between Ganondorf and Ganon will be skipped.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Skip Tower Collapse Escape Sequence',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('no_guard_stealth', bool, 1, True, 
        {
            'help': '''\
                    The crawlspace into Hyrule Castle will take you straight to Zelda.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Skip Interior Castle Guard Stealth Sequence',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('no_epona_race', bool, 1, True, 
        {
            'help': '''\
                    Having Epona's song will allow you to summon epona without racing Ingo.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Skip Epona Race',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('only_one_big_poe', bool, 1, True, 
        {
            'help': '''\
                    The Poe buyer will give a reward for turning in a single Big Poe.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Big Poe Reward only requires one Big Poe',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('fast_chests', bool, 1, True, 
        {
            'help': '''\
                    Makes all chests open without the large chest opening cutscene
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Fast Chest Cutscenes',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'checked'
        }),
    Setting_Info('free_scarecrow', bool, 1, True, 
        {
            'help': '''\
                    Start with the scarecrow song. You do not need
                    to play it as child or adult at the scarecrow
                    patch to be able to summon Pierre.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Start with Scarecrow Song',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('scarecrow_song', str, 0, False, 
        {
            'help': '''\
                    The song started with if 'free_scarecrow' is True
                    ''',
            'action': 'store_true'
        },
        {
            'group': 'convenience',
            'widget': 'Entry',
            'default': 'DAAAAAAA',
            'dependency': { 'free_scarecrow':True }
        }),
    Setting_Info('unlocked_ganondorf', bool, 1, True, 
        {
            'help': '''\
                    The Boss Key door in Ganon's Tower will start unlocked.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Remove Ganon\'s Boss Door Lock',
            'group': 'open',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('all_reachable', bool, 1, True, 
        {
            'help': '''\
                    When disabled, only check if the game is beatable with 
                    placement. Do not ensure all locations are reachable. 
                    This only has an effect on the restrictive algorithm 
                    currently.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'All Locations Reachable',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'checked'
        }),
    Setting_Info('shuffle_weird_egg', bool, 1, True, 
        {
            'help': '''\
                    Shuffles the Weird Egg item from Malon into the pool.
                    This means that you need to find the egg before going Zelda.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Shuffle Weird Egg',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('shuffle_fairy_ocarina', bool, 1, True, 
        {
            'help': '''\
                    Shuffles the Fairy Ocarina item from Saria into the pool.
                    This means that you need to find the ocarina before playing songs. 
                    You can still always recieve it from Ocarina of Time location
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Shuffle Fairy Ocarina',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('shuffle_song_items', bool, 1, True, 
        {
            'help': '''\
                    Shuffles the songs with with rest of the item pool so that
                    song can appear at other locations, and items can appear at
                    the song locations.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Shuffle Songs with Items',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('keysanity', bool, 1, True, 
        {
            'help': '''\
                    Small Keys, Boss Keys, Maps, and Compasses will be shuffled into the pool at
                    large, instead of just being restricted to their own dungeons.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Keysanity',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('tokensanity', str, 2, True, 
        {
            'default': 'off',
            'const': 'off',
            'nargs': '?',
            'choices': ['off', 'dungeons', 'all'],
            'help': '''\
                    Gold Skulltula Tokens will be shuffled into the pool,
                    and Gold Skulltula locations can have any item.
                    off:        Don't use this feature
                    dungeons:   Only dungeon skulltulas will be shuffled
                    all:        All skulltulas will be shuffled
                    '''
        },
        {
            'text': 'Tokensanity',
            'group': 'logic',
            'widget': 'Combobox',
            'default': 'Off',
            'options': {
                'Off': 'off',
                'Dungeons Only': 'dungeons',
                'All Tokens': 'all',
            },
        }),
    Setting_Info('nodungeonitems', bool, 1, True, 
        {
            'help': '''\
                    Remove Maps and Compasses from Itempool, replacing them by
                    empty slots.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Remove Maps and Compasses',
            'group': 'other',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('progressive_bombchus', bool, 1, True, 
        {
            'help': '''\
                    Bombchus amounts are progressive. 20 pack first time.
                    Other bombchus will give 10 when low on bombchus, otherwise 5.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Progressive Bombchus',
            'group': 'other',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_skulltulas', int, 3, True, 
        {
            'default': 50,
            'const': 50,
            'nargs': '?',
            'choices': [0, 10, 20, 30, 40, 50],
            'help': '''\
                    Choose the maximum number of gold skulltula tokens you will be expected to collect.
                    ''',
            'type': int
        },
        {
            'text': 'Maximum expected skulltula tokens',
            'group': 'rewards',
            'widget': 'Scale',
            'default': 50,
            'min': 0,
            'max': 50,
            'step': 10,

        }),
    Setting_Info('logic_no_night_tokens_without_suns_song', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to collect nighttime-only skulltulas
                    unless you have Sun's Song
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Nighttime Skulltulas without Sun\'s Song',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_big_poes', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to collect 10 big poes.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Big Poes',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_child_fishing', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to obtain the child fishing reward.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Child Fishing',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_adult_fishing', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to obtain the adult fishing reward.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Adult Fishing',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_trade_skull_mask', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to show the skull mask at the forest stage.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Skull Mask reward',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_trade_mask_of_truth', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to show the mask of truth at the forest stage.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Mask of Truth reward',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_trade_biggoron', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to trade for biggoron's reward.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Biggoron reward',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_1500_archery', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to win the 1500 point horseback archery reward.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No 1500 Horseback Archery',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_memory_game', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to play the memory game in lost woods with the skull kids.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Lost Woods Memory Game',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_no_second_dampe_race', bool, 1, True, 
        {
            'help': '''\
                    You will not be expected to race Dampe a second time.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Racing Dampe a second time',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_man_on_roof', bool, 1, True, 
        {
            'help': '''\
                    The man on the roof will not require the hookshot in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Man on Roof without Hookshot',
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_child_deadhand', bool, 1, True, 
        {
            'help': '''\
                    Deadhand in the Bottom of the Well will not require the Kokiri sword in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Child Deadhand without Kokiri Sword',
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_dc_jump', bool, 1, True, 
        {
            'help': '''\
                    Jumping towards the bomb bag chest in Dodongo's Cavern as an adult
                    will not require hover boots in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Dodongo\'s Cavern spike trap room jump without Hover Boots',
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_windmill_hp', bool, 1, True, 
        {
            'help': '''\
                    Getting the heart piece in the windmill as an adult will require nothing in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Windmill HP as adult with nothing',
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('logic_lens', str, 2, True, 
        {
            'default': 'all',
            'const': 'always',
            'nargs': '?',
            'choices': ['chest', 'chest-wasteland', 'all'],
            'help': '''\
                    Choose what expects the Lens of Truth:
                    all:              All lens spots expect the lens (except those that did not in the original game)
                    chest-wasteland:  Only wasteland and chest minigame expect the lens
                    chest:            Only the chest minigame expects the lens
                    '''
        },
        {
            'text': 'Lens of Truth',
            'group': 'tricks',
            'widget': 'Combobox',
            'default': 'Required everywhere',
            'options': {
                'Required everywhere': 'all',
                'Wasteland and Chest Minigame': 'chest-wasteland',
                'Only Chest Minigame': 'chest',
            },
        }),
    Setting_Info('ocarina_songs', bool, 1, True, 
        {
            'help': '''\
                    Randomizes the notes need to play for each ocarina song.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Randomize ocarina song notes',
            'group': 'other',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('correct_chest_sizes', bool, 1, True, 
        {
            'help': '''\
                    Updates the chest sizes to match their contents.
                    Small Chest = Useless Item
                    Big Chest = Progression Item
                    Boss Chest = Dungeon Item
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Chests size matches contents',
            'group': 'other',
            'widget': 'Checkbutton',
            'default': 'unchecked'
        }),
    Setting_Info('hints', str, 2, True, 
        {
            'default': 'none',
            'const': 'always',
            'nargs': '?',
            'choices': ['none', 'mask', 'agony', 'always'],
            'help': '''\
                    Choose how Gossip Stones behave
                    none:   Default behavior
                    mask:   Have useful hints that are read with the Mask of Truth (untested)
                    agony:  Have useful hints that are read with Stone of Agony
                    always: Have useful hints which can always be read
                    '''
        },
        {
            'text': 'Gossip Stones',
            'group': 'other',
            'widget': 'Combobox',
            'default': 'Hints; Need Stone of Agony',
            'options': {
                'No Hints': 'none',
                'Hints; Need Mask of Truth': 'mask',
                'Hints; Need Stone of Agony': 'agony',
                'Hints; Need Nothing': 'always',
            },
        }),
    Setting_Info('text_shuffle', str, 2, True, 
        {
            'default': 'none',
            'const': 'none',
            'nargs': '?',
            'choices': ['none', 'except_hints', 'complete'],
            'help': '''\
                    Choose how to shuffle the game's messages.
                    none:          Default behavior
                    except_hints:  All text except Gossip Stone hints and Dungeon reward hints is shuffled.
                    complete:      All text is shuffled
                    '''
        },
        {
            'text': 'Text Shuffle',
            'group': 'other',
            'widget': 'Combobox',
            'default': 'No text shuffled',
            'options': {
                'No text shuffled': 'none',
                'Shuffled except Hints': 'except_hints',
                'All text shuffled': 'complete',
            },
        }),
    Setting_Info('default_targeting', str, 1, False, 
        {
            'default': 'hold',
            'const': 'always',
            'nargs': '?',
            'choices': ['hold', 'switch'],
            'help': '''\
                    Choose what the default targeting is.
                    '''
        },
        {
            'text': 'Default Targeting Option',
            'group': 'rom_tab',
            'widget': 'Combobox',
            'default': 'Hold',
            'options': {
                'Hold': 'hold',
                'Switch': 'switch',
            },
        }),



    Setting_Info('kokiricolor', str, 0, False, 
        {
            'default': 'Kokiri Green',
            'const': 'Kokiri Green',
            'nargs': '?',
            'choices': get_tunic_color_options(),
            'help': '''\
                    Choose the color for Link's Kokiri Tunic. (default: %(default)s)
                    Color:              Make the Kokiri Tunic this color.
                    Random Choice:      Choose a random color from this list of colors.
                    Comepletely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Kokiri Tunic Color',
            'group': 'tuniccolor',
            'widget': 'Combobox',
            'default': 'Kokiri Green',
            'options': get_tunic_color_options(),
        }),
    Setting_Info('goroncolor', str, 0, False, 
        {
            'default': 'Goron Red',
            'const': 'Goron Red',
            'nargs': '?',
            'choices': get_tunic_color_options(),
            'help': '''\
                    Choose the color for Link's Goron Tunic. (default: %(default)s)
                    Color:              Make the Goron Tunic this color.
                    Random Choice:      Choose a random color from this list of colors.
                    Comepletely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Goron Tunic Color',
            'group': 'tuniccolor',
            'widget': 'Combobox',
            'default': 'Goron Red',
            'options': get_tunic_color_options(),
        }),
    Setting_Info('zoracolor', str, 0, False, 
        {
            'default': 'Zora Blue',
            'const': 'Zora Blue',
            'nargs': '?',
            'choices': get_tunic_color_options(),
            'help': '''\
                    Choose the color for Link's Zora Tunic. (default: %(default)s)
                    Color:              Make the Zora Tunic this color.
                    Random Choice:      Choose a random color from this list of colors.
                    Comepletely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Zora Tunic Color',
            'group': 'tuniccolor',
            'widget': 'Combobox',
            'default': 'Zora Blue',
            'options': get_tunic_color_options(),
        }),
    Setting_Info('navicolordefault', str, 0, False, 
        {
            'default': 'White',
            'const': 'White',
            'nargs': '?',
            'choices': get_navi_color_options(),
            'help': '''\
                    Choose the color for Navi when she is idle. (default: %(default)s)
                    Color:             Make the Navi this color.
                    Random Chocie:     Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Navi Idle',
            'group': 'navicolor',
            'widget': 'Combobox',
            'default': 'White',
            'options': get_navi_color_options(),
        }),
    Setting_Info('navicolorenemy', str, 0, False, 
        {
            'default': 'Yellow',
            'const': 'Yellow',
            'nargs': '?',
            'choices': get_navi_color_options(),
            'help': '''\
                    Choose the color for Navi when she is targeting an enemy. (default: %(default)s)
                    Color:             Make the Navi this color.
                    Random Chocie:     Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Navi Targeting Enemy',
            'group': 'navicolor',
            'widget': 'Combobox',
            'default': 'Yellow',
            'options': get_navi_color_options(),
        }),
    Setting_Info('navicolornpc', str, 0, False, 
        {
            'default': 'Light Blue',
            'const': 'Light Blue',
            'nargs': '?',
            'choices': get_navi_color_options(),
            'help': '''\
                    Choose the color for Navi when she is targeting an NPC. (default: %(default)s)
                    Color:             Make the Navi this color.
                    Random Chocie:     Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Navi Targeting NPC',
            'group': 'navicolor',
            'widget': 'Combobox',
            'default': 'Light Blue',
            'options': get_navi_color_options(),
        }),
    Setting_Info('navicolorprop', str, 0, False, 
        {
            'default': 'Green',
            'const': 'Green',
            'nargs': '?',
            'choices': get_navi_color_options(),
            'help': '''\
                    Choose the color for Navi when she is targeting a prop. (default: %(default)s)
                    Color:             Make the Navi this color.
                    Random Choice:     Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Navi Targeting Prop',
            'group': 'navicolor',
            'widget': 'Combobox',
            'default': 'Green',
            'options': get_navi_color_options(),
        }),
    Setting_Info('healthSFX', str, 0, False, 
        {
            'default': 'Default',
            'const': 'Default',
            'nargs': '?',
            'choices': ['Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'Random', 'None'],
            'help': '''\
                    Select the sound effect that loops at low health. (default: %(default)s)
                    Sound:         Replace the sound effect with the chosen sound.
                    Random Chocie: Replace the sound effect with a random sound from this list.
                    None:          Eliminate heart beeps.
                    '''
        },
        {
            'text': 'Low Health SFX',
            'group': 'lowhp',
            'widget': 'Combobox',
            'default': 'Default',
            'options': [
                'Random Choice', 
                'Default', 
                'Softer Beep', 
                'Rupee', 
                'Timer', 
                'Tamborine', 
                'Recovery Heart', 
                'Carrot Refill', 
                'Navi - Hey!', 
                'Zelda - Gasp', 
                'Cluck', 
                'Mweep!', 
                'None',
            ]
        }),
]

# gets the randomizer settings, whether to open the gui, and the logger level from command line arguments
def get_settings_from_command_line_args():
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    for info in setting_infos:
        parser.add_argument("--" + info.name, **info.args_params)

    parser.add_argument('--gui', help='Launch the GUI', action='store_true')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--settings_string', help='Provide sharable settings using a settings string. This will override all flags that it specifies.')

    args = parser.parse_args()

    result = {}
    for info in setting_infos:
        result[info.name] = vars(args)[info.name]
    settings = Settings(result)

    if args.settings_string is not None:
        settings.update_with_settings_string(args.settings_string)

    return settings, args.gui, args.loglevel