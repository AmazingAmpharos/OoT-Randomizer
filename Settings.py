import argparse
import textwrap
import string
import re
import random
import hashlib

from Rom import get_tunic_color_options, get_navi_color_options

class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)


# 64 characters
letters = "abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ-0123456789"
index_to_letter = { i: letters[i] for i in range(64) }
letter_to_index = { v: k for k, v in index_to_letter.items() }

def bit_string_to_text(bits):
    # pad the bits array to be multiple of 6
    if len(bits) % 6 > 0:
        bits += [0] * (6 - len(bits) % 6)
    # convert to characters
    result = ""
    for i in range(0, len(bits), 6):
        chunk = bits[i:i + 6]
        value = 0
        for b in range(6):
            value |= chunk[b] << b
        result += index_to_letter[value]
    return result

def text_to_bit_string(text):
    bits = []
    for c in text:
        index = letter_to_index[c]
        for b in range(6):
            bits += [ (index >> b) & 1 ]
    return bits

# holds the info for a single setting
class Setting_Info():

    def __init__(self, name, type, bitwidth=0, shared=False, args_params={}):
        self.name = name # name of the setting, used as a key to retrieve the setting's value everywhere
        self.type = type # type of the setting's value, used to properly convert types in GUI code
        self.bitwidth = bitwidth # number of bits needed to store the setting, used in converting settings to a string
        self.shared = shared # whether or not the setting is one that should be shared, used in converting settings to a string
        self.args_params = args_params # parameters that should be pased to the command line argument parser's add_argument() function

# holds the particular choices for a run's settings
class Settings():

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
            print(setting.name + ': ' + str(value))
            self.__dict__[setting.name] = value

        self.settings_string = self.get_settings_string()
        self.numeric_seed = self.get_numeric_seed()

    def get_numeric_seed(self):
        # salt seed with the settings, and hash to get a numeric seed
        full_string = self.settings_string + self.seed
        return int(hashlib.sha256(full_string.encode('utf-8')).hexdigest(), 16)

    def sanatize_seed(self):
        # leave only alphanumeric and some punctuation
        self.seed = re.sub(r'[^a-zA-Z0-9_]', '', self.seed, re.UNICODE)

    def update_seed(self, seed):
        self.seed = seed
        self.sanatize_seed()
        self.numeric_seed = self.get_numeric_seed()

    # add the settings as fields, and calculate information based on them
    def __init__(self, settings_dict):
        self.__dict__.update(settings_dict)
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
    Setting_Info('create_spoiler', bool, 1, True, {
            'help': 'Output a Spoiler File',
            'action': 'store_true'}),
    Setting_Info('suppress_rom', bool, 0, False, {
            'help': 'Do not create an output rom file.',
            'action': 'store_true'}),
    Setting_Info('compress_rom', bool, 0, False, {
            'help': 'Create a compressed version of the output rom file.',
            'action': 'store_true'}),
    Setting_Info('bridge', str, 2, True, {
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
                    '''}),
    Setting_Info('open_forest', bool, 1, True, {
            'help': '''\
                    Mido no longer blocks the path to the Deku Tree and
                    the Kokiri boy no longer blocks the path out of the forest.
                    ''',
            'action': 'store_true'}),
    Setting_Info('open_door_of_time', bool, 1, True, {
            'help': '''\
                    The Door of Time is open from the beginning of the game.
                    ''',
            'action': 'store_true'}),
    Setting_Info('fast_ganon', bool, 1, True, {
            'help': '''\
                    The barrier within Ganon's Castle leading to Ganon's Tower is dispelled from the
                    beginning of the game, the Boss Key is not required in Ganon's Tower, Ganondorf
                    gives a hint for the location of Light Arrows, and the tower collapse sequence
                    is removed.
                    ''',
            'action': 'store_true'}),
    Setting_Info('nodungeonitems', bool, 1, True, {
            'help': '''\
                    Remove Maps and Compasses from Itempool, replacing them by
                    empty slots.
                    ''',
            'action': 'store_true'}),
    Setting_Info('beatableonly', bool, 1, True, {
            'help': '''\
                    Only check if the game is beatable with placement. Do not
                    ensure all locations are reachable. This only has an effect
                    on the restrictive algorithm currently.
                    ''',
            'action': 'store_true'}),
    Setting_Info('hints', str, 2, True, {
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
                    '''}),
    Setting_Info('custom_logic', bool, 1, True, {
            'help': '''\
                    Removes a number of bad locations from logic,
                    and adds a number allowed tricks
                    ''',
            'action': 'store_true'}),
    Setting_Info('text_shuffle', str, 2, True, {
            'default': 'none',
            'const': 'none',
            'nargs': '?',
            'choices': ['none', 'except_hints', 'complete'],
            'help': '''\
                    Choose how to shuffle the game's messages.
                    none:          Default behavior
                    except_hints:  All text except Gossip Stone hints and Dungeon reward hints is shuffled.
                    complete:      All text is shuffled
                    '''}),
    Setting_Info('ocarina_songs', bool, 1, True, {
            'help': '''\
                    Randomizes the notes need to play for each ocarina song.
                    ''',
            'action': 'store_true'}),
    Setting_Info('kokiricolor', str, 0, False, {
            'default': 'Kokiri Green',
            'const': 'Kokiri Green',
            'nargs': '?',
            'choices': get_tunic_color_options(),
            'help': '''\
                    Choose the color for Link's Kokiri Tunic. (default: %(default)s)
                    Color:        Make the Kokiri Tunic this color.
                    Random:       Choose a random color from this list of colors.
                    True Random:  Choose a random color from any color the N64 can draw.
                    '''}),
    Setting_Info('goroncolor', str, 0, False, {
            'default': 'Goron Red',
            'const': 'Goron Red',
            'nargs': '?',
            'choices': get_tunic_color_options(),
            'help': '''\
                    Choose the color for Link's Goron Tunic. (default: %(default)s)
                    Color:        Make the Goron Tunic this color.
                    Random:       Choose a random color from this list of colors.
                    True Random:  Choose a random color from any color the N64 can draw.
                    '''}),
    Setting_Info('zoracolor', str, 0, False, {
            'default': 'Zora Blue',
            'const': 'Zora Blue',
            'nargs': '?',
            'choices': get_tunic_color_options(),
            'help': '''\
                    Choose the color for Link's Zora Tunic. (default: %(default)s)
                    Color:        Make the Zora Tunic this color.
                    Random:       Choose a random color from this list of colors.
                    True Random:  Choose a random color from any color the N64 can draw.
                    '''}),
    Setting_Info('navicolordefault', str, 0, False, {
            'default': 'White',
            'const': 'White',
            'nargs': '?',
            'choices': get_navi_color_options(),
            'help': '''\
                    Choose the color for Navi when she is idle. (default: %(default)s)
                    Color:        Make the Navi this color.
                    Random:       Choose a random color from this list of colors.
                    True Random:  Choose a random color from any color the N64 can draw.
                    '''}),
    Setting_Info('navicolorenemy', str, 0, False, {
            'default': 'Yellow',
            'const': 'Yellow',
            'nargs': '?',
            'choices': get_navi_color_options(),
            'help': '''\
                    Choose the color for Navi when she is targeting an enemy. (default: %(default)s)
                    Color:        Make the Navi this color.
                    Random:       Choose a random color from this list of colors.
                    True Random:  Choose a random color from any color the N64 can draw.
                    '''}),
    Setting_Info('navicolornpc', str, 0, False, {
            'default': 'Light Blue',
            'const': 'Light Blue',
            'nargs': '?',
            'choices': get_navi_color_options(),
            'help': '''\
                    Choose the color for Navi when she is targeting an NPC. (default: %(default)s)
                    Color:        Make the Navi this color.
                    Random:       Choose a random color from this list of colors.
                    True Random:  Choose a random color from any color the N64 can draw.
                    '''}),
    Setting_Info('navicolorprop', str, 0, False, {
            'default': 'Green',
            'const': 'Green',
            'nargs': '?',
            'choices': get_navi_color_options(),
            'help': '''\
                    Choose the color for Navi when she is targeting a prop. (default: %(default)s)
                    Color:        Make the Navi this color.
                    Random:       Choose a random color from this list of colors.
                    True Random:  Choose a random color from any color the N64 can draw.
                    '''}),
    Setting_Info('healthSFX', str, 0, False, {
            'default': 'Default',
            'const': 'Default',
            'nargs': '?',
            'choices': ['Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'Random', 'None'],
            'help': '''\
                    Select the sound effect that loops at low health. (default: %(default)s)
                    Sound:        Replace the sound effect with the chosen sound.
                    Random:       Replace the sound effect with a random sound from this list.
                    None:         Eliminate heart beeps.
                    '''}),
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