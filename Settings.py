import argparse
import textwrap
import string
import re
import hashlib
import math
import sys
import base64
import json

from version import __version__
from Utils import random_choices
from SettingsList import setting_infos

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

def get_settings_preset_choices():
    return {
        '---': '',
        'Accessible Weekly 2018 Oct': 'eyJ3b3JsZF9jb3VudCI6IDEsICJjcmVhdGVfc3BvaWxlciI6IHRydWUsICJjb21wcmVzc19yb20iOiAiUGF0Y2giLCAib3Blbl9mb3Jlc3QiOiB0cnVlLCAib3Blbl9rYWthcmlrbyI6IHRydWUsICJvcGVuX2Rvb3Jfb2ZfdGltZSI6IHRydWUsICJnZXJ1ZG9fZm9ydHJlc3MiOiAibm9ybWFsIiwgImJyaWRnZSI6ICJtZWRhbGxpb25zIiwgImxvZ2ljX3J1bGVzIjogImdsaXRjaGxlc3MiLCAiYWxsX3JlYWNoYWJsZSI6IHRydWUsICJib21iY2h1c19pbl9sb2dpYyI6IGZhbHNlLCAib25lX2l0ZW1fcGVyX2R1bmdlb24iOiBmYWxzZSwgInRyaWFsc19yYW5kb20iOiBmYWxzZSwgInRyaWFscyI6IDAsICJub19lc2NhcGVfc2VxdWVuY2UiOiB0cnVlLCAibm9fZ3VhcmRfc3RlYWx0aCI6IGZhbHNlLCAibm9fZXBvbmFfcmFjZSI6IHRydWUsICJmYXN0X2NoZXN0cyI6IHRydWUsICJiaWdfcG9lX2NvdW50X3JhbmRvbSI6IGZhbHNlLCAiYmlnX3BvZV9jb3VudCI6IDEsICJmcmVlX3NjYXJlY3JvdyI6IGZhbHNlLCAic2h1ZmZsZV9rb2tpcmlfc3dvcmQiOiB0cnVlLCAic2h1ZmZsZV93ZWlyZF9lZ2ciOiBmYWxzZSwgInNodWZmbGVfb2NhcmluYXMiOiBmYWxzZSwgInNodWZmbGVfc29uZ19pdGVtcyI6IGZhbHNlLCAic2h1ZmZsZV9nZXJ1ZG9fY2FyZCI6IGZhbHNlLCAic2h1ZmZsZV9zY3J1YnMiOiAib2ZmIiwgInNob3BzYW5pdHkiOiAib2ZmIiwgInNodWZmbGVfbWFwY29tcGFzcyI6ICJzdGFydHdpdGgiLCAic2h1ZmZsZV9ib3Nza2V5cyI6ICJkdW5nZW9uIiwgImVuaGFuY2VfbWFwX2NvbXBhc3MiOiBmYWxzZSwgInVubG9ja2VkX2dhbm9uZG9yZiI6IHRydWUsICJ0b2tlbnNhbml0eSI6ICJvZmYiLCAibXFfZHVuZ2VvbnNfcmFuZG9tIjogZmFsc2UsICJtcV9kdW5nZW9ucyI6IDAsICJsb2dpY19za3VsbHR1bGFzIjogNTAsICJsb2dpY19ub19uaWdodF90b2tlbnNfd2l0aG91dF9zdW5zX3NvbmciOiBmYWxzZSwgImxvZ2ljX25vX2JpZ19wb2VzIjogZmFsc2UsICJsb2dpY19ub19jaGlsZF9maXNoaW5nIjogZmFsc2UsICJsb2dpY19ub19hZHVsdF9maXNoaW5nIjogZmFsc2UsICJsb2dpY19ub190cmFkZV9za3VsbF9tYXNrIjogZmFsc2UsICJsb2dpY19ub190cmFkZV9tYXNrX29mX3RydXRoIjogdHJ1ZSwgImxvZ2ljX25vXzE1MDBfYXJjaGVyeSI6IGZhbHNlLCAibG9naWNfbm9fbWVtb3J5X2dhbWUiOiBmYWxzZSwgImxvZ2ljX25vX3NlY29uZF9kYW1wZV9yYWNlIjogZmFsc2UsICJsb2dpY19ub190cmFkZV9iaWdnb3JvbiI6IGZhbHNlLCAibG9naWNfZWFybGllc3RfYWR1bHRfdHJhZGUiOiAicHJlc2NyaXB0aW9uIiwgImxvZ2ljX2xhdGVzdF9hZHVsdF90cmFkZSI6ICJjbGFpbV9jaGVjayIsICJsb2dpY190cmlja3MiOiBmYWxzZSwgImxvZ2ljX21hbl9vbl9yb29mIjogZmFsc2UsICJsb2dpY19jaGlsZF9kZWFkaGFuZCI6IGZhbHNlLCAibG9naWNfZGNfanVtcCI6IGZhbHNlLCAibG9naWNfd2luZG1pbGxfcG9oIjogZmFsc2UsICJsb2dpY19jcmF0ZXJfYmVhbl9wb2hfd2l0aF9ob3ZlcnMiOiBmYWxzZSwgImxvZ2ljX3pvcmFfd2l0aF9jdWNjbyI6IGZhbHNlLCAibG9naWNfem9yYV93aXRoX2hvdmVycyI6IGZhbHNlLCAibG9naWNfZmV3ZXJfdHVuaWNfcmVxdWlyZW1lbnRzIjogdHJ1ZSwgImxvZ2ljX21vcnBoYV93aXRoX3NjYWxlIjogZmFsc2UsICJsb2dpY19sZW5zIjogImFsbCIsICJvY2FyaW5hX3NvbmdzIjogZmFsc2UsICJjb3JyZWN0X2NoZXN0X3NpemVzIjogZmFsc2UsICJjbGVhcmVyX2hpbnRzIjogZmFsc2UsICJoaW50cyI6ICJhZ29ueSIsICJoaW50X2Rpc3QiOiAiYmFsYW5jZWQiLCAidGV4dF9zaHVmZmxlIjogIm5vbmUiLCAiaXRlbV9wb29sX3ZhbHVlIjogImJhbGFuY2VkIiwgImRhbWFnZV9tdWx0aXBsaWVyIjogIm5vcm1hbCJ9'
    }

def get_settings_base64_string(settings):
    settings_to_save = {setting.name: settings.__dict__[setting.name] for setting in
                        filter(lambda s: s.shared and s.bitwidth > 0, setting_infos)}
    settings_to_save_json = json.dumps(settings_to_save)
    settings_to_save_base64 = base64.b64encode(str.encode(settings_to_save_json, "utf-8"))
    return settings_to_save_base64

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
                if 'choices' in setting.args_params:
                    try:
                        index = setting.args_params['choices'].index(value)
                    except ValueError:
                        index = setting.args_params['choices'].index(setting.args_params['default'])
                    # https://stackoverflow.com/questions/10321978/integer-to-bitfield-as-a-list
                    i_bits = [1 if digit=='1' else 0 for digit in bin(index)[2:]]
                    i_bits.reverse()
                elif 'char_options' in setting.gui_params:
                    char_bitwidth = math.ceil(math.log(len(setting.gui_params['char_options']), 2))
                    for c in value.upper():
                        index = setting.gui_params['char_options'].index(c)
                        # https://stackoverflow.com/questions/10321978/integer-to-bitfield-as-a-list
                        c_bits = [1 if digit=='1' else 0 for digit in bin(index)[2:]]
                        c_bits.reverse()
                        c_bits += [0] * ( char_bitwidth - len(c_bits) )
                        i_bits.extend(c_bits)
                else:
                    raise ValueError('Setting is string type, but missing parse parameters.')
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
                if 'choices' in setting.args_params:
                    index = 0
                    for b in range(setting.bitwidth):
                        index |= cur_bits[b] << b
                    value = setting.args_params['choices'][index]
                elif 'char_options' in setting.gui_params:
                    char_bitwidth = math.ceil(math.log(len(setting.gui_params['char_options']), 2))
                    value = ''
                    for i in range(0, setting.bitwidth, char_bitwidth):
                        char_bits = cur_bits[i:i+char_bitwidth]
                        index = 0
                        for b in range(char_bitwidth):
                            index |= char_bits[b] << b
                        value += setting.gui_params['char_options'][index]  
                else:
                    raise ValueError('Setting is string type, but missing parse parameters.')
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

    def sanitize_seed(self):
        # leave only alphanumeric and some punctuation
        self.seed = re.sub(r'[^a-zA-Z0-9_-]', '', self.seed, re.UNICODE)

    def update_seed(self, seed):
        self.seed = seed
        self.sanitize_seed()
        self.numeric_seed = self.get_numeric_seed()

    def update(self):
        self.settings_string = self.get_settings_string()
        self.numeric_seed = self.get_numeric_seed()

    # add the settings as fields, and calculate information based on them
    def __init__(self, settings_dict):
        self.__dict__.update(settings_dict)
        for info in setting_infos:
            if info.name not in self.__dict__:
                if info.type == bool:
                    if info.gui_params is not None and 'default' in info.gui_params:
                        self.__dict__[info.name] = True if info.gui_params['default'] == 'checked' else False
                    else:
                        self.__dict__[info.name] = False
                if info.type == str:
                    if 'default' in info.args_params:
                        self.__dict__[info.name] = info.args_params['default']
                    elif info.gui_params is not None and 'default' in info.gui_params:
                        if 'options' in info.gui_params and isinstance(info.gui_params['options'], dict):
                            self.__dict__[info.name] = info.gui_params['options'][info.gui_params['default']]
                        else:
                            self.__dict__[info.name] = info.gui_params['default']
                    else:
                        self.__dict__[info.name] = ""
                if info.type == int:
                    if 'default' in info.args_params:
                        self.__dict__[info.name] = info.args_params['default']
                    elif info.gui_params is not None and 'default' in info.gui_params:                      
                        self.__dict__[info.name] = info.gui_params['default']
                    else:
                        self.__dict__[info.name] = 1
        self.settings_string = self.get_settings_string()
        if(self.seed is None):
            # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
            self.seed = ''.join(random_choices(string.ascii_uppercase + string.digits, k=10))
        self.sanitize_seed()
        self.numeric_seed = self.get_numeric_seed()


# gets the randomizer settings, whether to open the gui, and the logger level from command line arguments
def get_settings_from_command_line_args():
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    for info in setting_infos:
        parser.add_argument("--" + info.name, **info.args_params)

    parser.add_argument('--gui', help='Launch the GUI', action='store_true')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--settings_string', help='Provide sharable settings using a settings string. This will override all flags that it specifies.')
    parser.add_argument('--convert_settings', help='Only convert the specified settings to a settings string. If a settings string is specified output the used settings instead.', action='store_true')

    args = parser.parse_args()

    result = {}
    for info in setting_infos:
        result[info.name] = vars(args)[info.name]
    settings = Settings(result)

    if args.settings_string is not None:
        settings.update_with_settings_string(args.settings_string)

    if args.convert_settings:
        if args.settings_string is not None:
            print(settings.get_settings_display())
        else:
            print(settings.get_settings_string())
        sys.exit(0)
        
    return settings, args.gui, args.loglevel
