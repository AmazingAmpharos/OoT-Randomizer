import argparse
import re
from Patches import get_tunic_color_options, get_navi_color_options, get_NaviSFX_options, get_HealthSFX_options

# holds the info for a single setting
class Setting_Info():

    def __init__(self, name, type, bitwidth=0, shared=False, args_params={}, gui_params=None):
        self.name = name # name of the setting, used as a key to retrieve the setting's value everywhere
        self.type = type # type of the setting's value, used to properly convert types in GUI code
        self.bitwidth = bitwidth # number of bits needed to store the setting, used in converting settings to a string
        self.shared = shared # whether or not the setting is one that should be shared, used in converting settings to a string
        self.args_params = args_params # parameters that should be pased to the command line argument parser's add_argument() function
        self.gui_params = gui_params # parameters that the gui uses to build the widget components

        # create the choices parameters from the gui options if applicable
        if gui_params and 'options' in gui_params and 'choices' not in args_params \
                and not ('type' in args_params and callable(args_params['type'])):
            if isinstance(gui_params['options'], list):
                self.args_params['choices'] = list(gui_params['options'])
            elif isinstance(gui_params['options'], dict):
                self.args_params['choices'] = list(gui_params['options'].values())


def parse_custom_tunic_color(s):
    if s == 'Custom Color':
        raise argparse.ArgumentTypeError('Specify custom color by using \'Custom (#xxxxxx)\'')
    elif re.match(r'^Custom \(#[A-Fa-f0-9]{6}\)$', s):
        return re.findall(r'[A-Fa-f0-9]{6}', s)[0]
    elif s in get_tunic_color_options():
        return s
    else:
        raise argparse.ArgumentTypeError('Invalid color specified')


def parse_custom_navi_color(s):
    if s == 'Custom Color':
        raise argparse.ArgumentTypeError('Specify custom color by using \'Custom (#xxxxxx)\'')
    elif re.match(r'^Custom \(#[A-Fa-f0-9]{6}\)$', s):
        return re.findall(r'[A-Fa-f0-9]{6}', s)[0]
    elif s in get_navi_color_options():
        return s
    else:
        raise argparse.ArgumentTypeError('Invalid color specified')


def validate_scarecrow_string(value):
    if len(value) > 8:
        return None
    for c in value.upper():
        if c not in ['A', 'D', 'R', 'L', 'U']:
            return None
    return value


# a list of the possible settings
setting_infos = [
    Setting_Info('check_version', bool, 0, False,
    {
        'help': '''\
                Checks if you are on the latest version
                ''',
        'action': 'store_true'
    }),
    Setting_Info('checked_version', str, 0, False, {
            'default': '',
            'help': 'Supress version warnings if checked_version is less than __version__.'}),
    Setting_Info('rom', str, 0, False, {
            'default': '',
            'help': 'Path to an OoT 1.0 rom to use as a base.'}),
    Setting_Info('output_dir', str, 0, False, {
            'default': '',
            'help': 'Path to output directory for rom generation.'}),
    Setting_Info('seed', str, 0, False, {
            'help': 'Define seed number to generate.'}),
    Setting_Info('patch_file', str, 0, False, {
            'default': '',
            'help': 'Path to a patch file.'}),
    Setting_Info('count', int, 0, False, {
            'help': '''\
                    Use to batch generate multiple seeds with same settings.
                    If --seed is provided, it will be used for the first seed, then
                    used to derive the next seed (i.e. generating 10 seeds with
                    --seed given will produce the same 10 (different) roms each
                    time).
                    ''',
            'type': int}),
    Setting_Info('world_count', int, 5, True, {
            'default': 1,
            'help': '''\
                    Use to create a multi-world generation for co-op seeds.
                    World count is the number of players. Warning: Increasing
                    the world count will drastically increase generation time.
                    ''',
            'type': int}, {}),
    Setting_Info('player_num', int, 0, False, 
        {
            'default': 1,
            'help': '''\
                    Use to select world to generate when there are multiple worlds.
                    ''',
            'type': int
        }),
    Setting_Info('create_spoiler', bool, 1, True,
        {
            'help': 'Output a Spoiler File',
            'action': 'store_true'
        },
        {
            'text': 'Create Spoiler Log',
            'group': 'rom_tab',
            'widget': 'Checkbutton',
            'default': 'checked',
            'dependency': lambda guivar: guivar['compress_rom'].get() != 'No ROM Output',
            'tooltip':'''\
                      Enabling this will change the seed.
                      '''
        }),
    Setting_Info('compress_rom', str, 2, False,
        {
            'default': 'True',
            'const': 'True',
            'nargs': '?',
            'help': '''\
                    Create a compressed version of the output ROM file.
                    True: Compresses. Improves stability. Will take longer to generate
                    False: Uncompressed. Unstable. Faster generation
                    Patch: Patch file. No ROM, but used to send the patch data
                    None: No ROM Output. Creates spoiler log only
                    ''',
        },
        {
            'text': 'Output Type',
            'group': 'rom_tab',
            'widget': 'Radiobutton',
            'default': 'Compressed [Stable]',
            'horizontal': True,
            'options': {
                'Compressed [Stable]': 'True',
                'Uncompressed [Crashes]': 'False',
                'Patch File': 'Patch',
                'No Output': 'None',
            },
            'tooltip':'''\
                      The first time compressed generation will take a while,
                      but subsequent generations will be quick. It is highly
                      recommended to compress or the game will crash
                      frequently except on real N64 hardware.

                      Patch files are used to send the patched data to other
                      people without sending the ROM file.
                      '''
        }),
    Setting_Info('open_forest', bool, 1, True,
        {
            'help': '''\
                    Mido no longer blocks the path to the Deku Tree, and
                    the Kokiri boy no longer blocks the path out of the forest.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Open Forest',
            'group': 'open',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                      Mido no longer blocks the path to the Deku Tree,
                      and the Kokiri boy no longer blocks the path out
                      of the forest.

                      When this option is off, the Kokiri Sword and
                      Slingshot are always available somewhere
                      in the forest.
                      '''
        }),
    Setting_Info('open_kakariko', bool, 1, True,
        {
            'help': '''\
                    The gate in Kakariko Village to Death Mountain Trail
                    is always open instead of needing Zelda's Letter.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Open Kakariko Gate',
            'group': 'open',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      The gate in Kakariko Village to Death Mountain Trail
                      is always open instead of needing Zelda's Letter.

                      Either way, the gate is always open as an adult.
                      '''
        }),
    Setting_Info('open_door_of_time', bool, 1, True,
        {
            'help': '''
                    The Door of Time is open from the beginning of the game.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Open Door of Time',
            'group': 'open',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      The Door of Time starts opened instead of needing to
                      play the Song of Time. If this is not set, only
                      an Ocarina and Song of Time must be found to open
                      the Door of Time.
                      '''
        }),
    Setting_Info('gerudo_fortress', str, 2, True,
        {
            'default': 'normal',
            'const': 'normal',
            'nargs': '?',
            'help': '''Select how much of Gerudo Fortress is required. (default: %(default)s)
                       Normal: Free all four carpenters to get the Gerudo Card.
                       Fast:   Free only the carpenter closest to Link's prison to get the Gerudo Card.
                       Open:   Start with the Gerudo Card and all its benefits.
                    '''
        },
        {
            'text': 'Gerudo Fortress',
            'group': 'open',
            'widget': 'Combobox',
            'default': 'Default Behavior',
            'options': {
                'Default Behavior': 'normal',
                'Rescue One Carpenter': 'fast',
                'Start with Gerudo Card': 'open',
            },
            'tooltip':'''\
                      'Rescue One Carpenter': Only the bottom left
                      carpenter must be rescued.

                      'Start with Gerudo Card': The carpenters are rescued from
                      the start of the game, and the player starts with the Gerudo
                      Card in the inventory allowing access to Gerudo Training Grounds.
                      '''
        }),
    Setting_Info('bridge', str, 2, True,
        {
            'default': 'medallions',
            'const': 'medallions',
            'nargs': '?',
            'help': '''\
                    Select requirement to spawn the Rainbow Bridge to reach Ganon's Castle. (default: %(default)s)
                    Medallions:    Collect all six medallions to create the bridge.
                    Vanilla:       Collect only the Shadow and Spirit Medallions and possess the Light Arrows.
                    All Dungeons:  Collect all spiritual stones and all medallions to create the bridge.
                    Open:          The bridge will spawn without an item requirement.
                    '''
        },
        {
            'text': 'Rainbow Bridge Requirement',
            'group': 'open',
            'widget': 'Combobox',
            'default': 'All Medallions',
            'options': {
                'All Dungeons': 'dungeons',
                'All Medallions': 'medallions',
                'Vanilla Requirements': 'vanilla',
                'Always Open': 'open',
            },
            'tooltip':'''\
                      'All Dungeons': All Medallions and Stones

                      'All Medallions': All 6 Medallions only

                      'Vanilla Requirements': Spirit and Shadow
                      Medallions and the Light Arrows

                      'Always Open': Rainbow Bridge is always present
                      '''
        }),
    Setting_Info('logic_rules', str, 1, True,
        {
            'default': 'glitchless',
            'const': 'glitchless',
            'nargs': '?',
            'help': '''\
                    Sets the rules the logic uses to determine accessibility:
                    glitchless:  No glitches are required, but may require some minor tricks
                    none:        All locations are considered available. May not be beatable.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Logic Rules',
            'group': 'world',
            'widget': 'Combobox',
            'default': 'Glitchless',
            'options': {
                'Glitchless': 'glitchless',
                'No Logic': 'none',
            },
            'tooltip':'''\
                      Sets the rules the logic uses
                      to determine accessibility.

                      'Glitchless': No glitches are
                      required, but may require some
                      minor tricks

                      'No Logic': All locations are
                      considered available. May not
                      be beatable.
                      '''
        }),    
    Setting_Info('all_reachable', bool, 1, True,
        {
            'help': '''\
                    When disabled, only check if the game is beatable with
                    placement. Do not ensure all locations are reachable.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'All Locations Reachable',
            'group': 'world',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                      When this option is enabled, the randomizer will
                      guarantee that every item is obtainable and every
                      location is reachable.

                      When disabled, only required items and locations
                      to beat the game will be guaranteed reachable.

                      Even when enabled, some locations may still be able
                      to hold the keys needed to reach them.
                      ''',
            'dependency': lambda guivar: guivar['logic_rules'].get() == 'Glitchless',
        }),
    Setting_Info('bombchus_in_logic', bool, 1, True,
        {
            'help': '''\
                    Bombchus will be considered in logic. This has a few effects:
                    -Back Alley shop will open once you've found Bombchus.
                    -It will sell an affordable pack (5 for 60) and never sell out.
                    -Bombchus refills cannot be bought until Bombchus have been obtained.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Bombchus Are Considered in Logic',
            'group': 'world',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                      Bombchus are properly considered in logic.

                      The first Bombchu pack will always be 20.
                      Subsequent packs will be 5 or 10 based on
                      how many you have.

                      Bombchus can be purchased for 60/99/180
                      rupees once they are been found.

                      Bombchu Bowling opens with Bombchus.
                      Bombchus are available at Kokiri Shop
                      and the Bazaar. Bombchu refills cannot
                      be bought until Bombchus have been
                      obtained.
                      ''',
        }),
    Setting_Info('one_item_per_dungeon', bool, 1, True,
        {
            'help': '''\
                    Each dungeon will have exactly one major item.
                    Does not include dungeon items or GS Tokens.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Dungeons Have One Major Item',
            'group': 'world',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Dungeons have exactly one major
                      item. This naturally makes each
                      dungeon similar in value instaed
                      of valued based on chest count.

                      Spirit Temple Colossus hands count
                      as part of the dungeon. Spirit
                      Temple has TWO items to match
                      vanilla distribution.

                      Dungeon items and GS Tokens do
                      not count as major items.
                      ''',
        }),
    Setting_Info('trials_random', bool, 1, True,
        {
            'help': '''\
                    Sets the number of trials must be cleared to enter
                    Ganon's Tower to a random value.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Random Number of Ganon\'s Trials',
            'group': 'open',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Sets a random number of trials to
                      enter Ganon's Tower.
                      '''
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
            'group': 'open',
            'widget': 'Scale',
            'default': 6,
            'min': 0,
            'max': 6,
            'random': True,
            'tooltip':'''\
                      Trials are randomly selected. If hints are
                      enabled, then there will be hints for which
                      trials need to be completed.
                      ''',
            'dependency': lambda guivar: not guivar['trials_random'].get(),
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
            'default': 'unchecked',
            'tooltip':'''\
                      The tower collapse escape sequence between
                      Ganondorf and Ganon will be skipped.
                      '''
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
            'default': 'unchecked',
            'tooltip':'''\
                      The crawlspace into Hyrule Castle goes
                      straight to Zelda, skipping the guards.
                      '''
        }),
    Setting_Info('no_epona_race', bool, 1, True,
        {
            'help': '''\
                    Having Epona's Song will allow you to summon Epona without racing Ingo.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Skip Epona Race',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Epona can be summoned with Epona's Song
                      without needing to race Ingo.
                      '''
        }),
    Setting_Info('fast_chests', bool, 1, True,
        {
            'help': '''\
                    Makes all chests open without the large chest opening cutscene.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Fast Chest Cutscenes',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                      All chest animations are fast. If disabled,
                      the animation time is slow for major items.
                      '''
        }),
    Setting_Info('big_poe_count_random', bool, 1, True,
        {
            'help': '''\
                    Sets a random number of Big Poes to receive an item from the buyer.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Random Big Poe Target Count',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      The Poe buyer will give a reward for turning
                      in a random number of Big Poes.
                      '''
        }),
    Setting_Info('big_poe_count', int, 4, True,
        {
            'default': 10,
            'const': 10,
            'nargs': '?',
            'choices': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'help': '''\
                    Select the number of Big Poes to receive an item from the buyer.
                    ''',
            'type': int,
        },
        {
            'group': 'convenience',
            'widget': 'Scale',
            'default': 10,
            'min': 1,
            'max': 10,
            'tooltip':'''\
                      The Poe buyer will give a reward for turning
                      in the chosen number of Big Poes.
                      ''',
            'dependency': lambda guivar: not guivar['big_poe_count_random'].get(),
        }),
    Setting_Info('free_scarecrow', bool, 1, True,
        {
            'help': '''\
                    Start with Scarecrow's Song. You do not need
                    to play it as child or adult at the scarecrow
                    patch to be able to summon Pierre.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Start with Scarecrow\'s Song',
            'group': 'convenience',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Skips needing to go to Lake Hylia as both
                      child and adult to learn Scarecrow's Song.
                      '''
        }),
    Setting_Info('scarecrow_song', str, 3*8, True,
        {
            'default': 'DAAAAAAA',
            'const': 'DAAAAAAA',
            'nargs': '?',
            'help': '''\
                    The song started with if 'free_scarecrow' is True
                    Valid notes: A, U, L, R, D
                    ''',
        },
        {
            'group': 'convenience',
            'widget': 'Entry',
            'default': 'DAAAAAAA',
            'char_options': ['A', 'D', 'U', 'L', 'R'],
            'validate': validate_scarecrow_string,
            'dependency': lambda guivar: guivar['free_scarecrow'].get(),
            'tooltip':'''\
                      The song must be 8 notes long and have
                      at least two different notes.
                      Valid notes are:
                      'A': A Button
                      'D': C-Down
                      'U': C-Up
                      'L': C-Left
                      'R': C-Right
                      '''
        }),
    Setting_Info('shuffle_kokiri_sword', bool, 1, True,
        {
            'help': '''\
                    Shuffles the Kokiri Sword into the pool.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Shuffle Kokiri Sword',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                      Disabling this will make the Kokiri Sword
                      always available at the start.
                      '''
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
            'default': 'checked',
            'tooltip':'''\
                      You need to find the egg before going Zelda.
                      This means the Weird Egg locks the rewards from
                      Impa, Saria, Malon, and Talon as well as the
                      Happy Mask sidequest.
                      '''
        }),
    Setting_Info('shuffle_ocarinas', bool, 1, True,
        {
            'help': '''\
                    Shuffles the Fairy Ocarina and the Ocarina of Time into the pool.
                    This means that you need to find an ocarina before playing songs.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Shuffle Ocarinas',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                      The Fairy Ocarina and Ocarina of Time are
                      randomized. One will be required before
                      songs can be played.
                      '''
        }),
    Setting_Info('shuffle_song_items', bool, 1, True,
        {
            'help': '''\
                    Shuffles the songs with with rest of the item pool so that
                    songs can appear at other locations and items can appear at
                    the song locations.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Shuffle Songs with Items',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                      Songs can appear anywhere as normal items.

                      If this option is not set, songs will still
                      be shuffled but will be limited to the
                      locations that has songs in the original game.
                      '''
        }),
    Setting_Info('shuffle_gerudo_card', bool, 1, True,
        {
            'help': '''\
                    Shuffles the Gerudo Card into the item pool.
                    The Gerudo Card does not stop guards from throwing you in jail.
                    It only grants access to Gerudo Training Grounds after all carpenters
                    have been rescued. This option does nothing if "gerudo_fortress" is "open".
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Shuffle Gerudo Card',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'dependency': lambda guivar: guivar['gerudo_fortress'].get() != 'Start with Gerudo Card',
            'tooltip':'''\
                      Gerudo Card is required to enter
                      Gerudo Training Grounds.
                      '''
        }),
    Setting_Info('shuffle_scrubs', str, 3, True,
        {
            'default': 'off',
            'const': 'off',
            'nargs': '?',
            'help': '''\
                    Deku Scrub Salesmen are randomized:
                    off:        Only the 3 Scrubs that give one-time items
                                in the vanilla game will have random items.
                    low:        All Scrubs will have random items and their
                                prices will be reduced to 10 rupees each.
                    regular:    All Scrubs will have random items and each
                                of them will demand their vanilla prices.
                    random:     All Scrubs will have random items and their
                                price will also be random between 10-99 rupees.
                    '''
        },
        {
            'text': 'Scrub Shuffle',
            'group': 'logic',
            'widget': 'Combobox',
            'default': 'Off',
            'options': {
                'Off': 'off',
                'On (Affordable)': 'low',
                'On (Expensive)': 'regular',
                'On (Random Prices)': 'random',
            },
            'tooltip':'''\
                      'Off': Only the 3 Scrubs that give one-time
                      items in the vanilla game (PoH, Deku Nut
                      capacity, and Deku Stick capacity) will
                      have random items.

                      'Affordable': All Scrub prices will be
                      reduced to 10 rupees each.

                      'Expensive': All Scrub prices will be
                      their vanilla prices. This will require
                      spending over 1000 rupees on Scrubs.

                      'Random Prices': All Scrub prices will be
                      between 0-99 rupees. This will on average
                      be very, very expensive overall.

                      The texts of the Scrubs are not updated.
                      '''
        }),
    Setting_Info('shopsanity', str, 3, True,
        {
            'default': 'off',
            'const': 'off',
            'nargs': '?',
            'help': '''\
                    Shop contents are randomized. Non-shop items
                    are one time purchases. This setting also
                    changes the item pool to introduce a new Wallet
                    upgrade and more money.
                    off:        Normal Shops*
                    0-4:        Shop contents are shuffled and N non-shop
                                items are added to every shop. So more
                                possible item locations.
                    random:     Shop contents are shuffles and each shop
                                will have a random number of non-shop items
                    '''
        },
        {
            'text': 'Shopsanity',
            'group': 'logic',
            'widget': 'Combobox',
            'default': 'Off',
            'options': {
                'Off': 'off',
                'Shuffled Shops (0 Items)': '0',
                'Shuffled Shops (1 Items)': '1',
                'Shuffled Shops (2 Items)': '2',
                'Shuffled Shops (3 Items)': '3',
                'Shuffled Shops (4 Items)': '4',
                'Shuffled Shops (Random)': 'random',
            },
            'tooltip':'''\
                      Shop contents are randomized.
                      (X Items): Shops have X random non-shop (Special
                      Deal!) items. They will always be on the left
                      side, and some of the lower value shop items
                      will be replaced to make room for these.

                      (Random): Each shop will have a random number
                      of non-shop items up to a maximum of 4.

                      The non-shop items have no requirements except
                      money, while the normal shop items (such as
                      200/300 rupee tunics) have normal vanilla
                      requirements. This means that, for example,
                      as a child you cannot buy 200/300 rupee
                      tunics, but you can buy non-shop tunics.

                      Non-shop Bombchus will unlock the chu slot
                      in your inventory, which, if Bombchus are in
                      logic, is needed to buy Bombchu refills.
                      Otherwise, the Bomb Bag is required.
                      '''
        }),
    Setting_Info('shuffle_mapcompass', str, 2, True,
        {
        'default': 'dungeon',
        'const': 'dungeon',
        'nargs': '?',
        'help': '''\
                    Sets the Map and Compass placement rules
                    remove:      Maps and Compasses are removed from the world.
                    startwith:   Start with all Maps and Compasses.
                    dungeon:     Maps and Compasses are put in their dungeon.
                    keysanity:   Maps and Compasses can appear anywhere.
                    '''
        },
        {
            'text': 'Shuffle Dungeon Items',
            'group': 'logic',
            'widget': 'Combobox',
            'default': 'Maps/Compasses: Dungeon Only',
            'options': {
                'Maps/Compasses: Remove': 'remove',
                'Maps/Compasses: Start With': 'startwith',
                'Maps/Compasses: Dungeon Only': 'dungeon',
                'Maps/Compasses: Anywhere': 'keysanity'
            },
            'tooltip':'''\
                      'Remove': Maps and Compasses are removed.
                      This will add a small amount of money and
                      refill items to the pool.

                      'Start With': Maps and Compasses are given to
                      you from the start. This will add a small
                      amount of money and refill items to the pool.

                      'Dungeon': Maps and Compasses can only appear
                      in their respective dungeon.

                      'Anywhere': Maps and Compasses can appear
                      anywhere in the world.

                      Setting 'Remove', 'Start With, or 'Anywhere' will
                      add 2 more possible locations to each Dungeons.
                      This makes dungeons more profitable, especially
                      Ice Cavern, Water Temple, and Jabu Jabu's Belly.
                      '''
        }),
    Setting_Info('shuffle_smallkeys', str, 2, True,
        {
        'default': 'dungeon',
        'const': 'dungeon',
        'nargs': '?',
        'help': '''\
                    Sets the Small Keys placement rules
                    remove:      Small Keys are removed from the world.
                    dungeon:     Small Keys are put in their dungeon.
                    keysanity:   Small Keys can appear anywhere.
                    '''
        },
        {
            'group': 'logic',
            'widget': 'Combobox',
            'default': 'Small Keys: Dungeon Only',
            'options': {
                'Small Keys: Remove (Keysy)': 'remove',
                'Small Keys: Dungeon Only': 'dungeon',
                'Small Keys: Anywhere (Keysanity)': 'keysanity'
            },
            'tooltip':'''\
                      'Remove': Small Keys are removed. All locked
                      doors in dungeons will be unlocked. An easier
                      mode.

                      'Dungeon': Small Keys can only appear in their
                      respective dungeon. If Fire Temple is not a
                      Master Quest dungeon, the door to the Boss Key
                      chest will be unlocked

                      'Anywhere': Small Keys can appear
                      anywhere in the world. A difficult mode since
                      it is more likely to need to enter a dungeon
                      multiple times.

                      Try different combination out, such as:
                      'Small Keys: Dungeon' + 'Boss Keys: Anywhere'
                      for a milder Keysanity experience.
                      '''
        }),
    Setting_Info('shuffle_bosskeys', str, 2, True,
        {
        'default': 'dungeon',
        'const': 'dungeon',
        'nargs': '?',
        'help': '''\
                    Sets the Boss Keys placement rules
                    remove:      Boss Keys are removed from the world.
                    dungeon:     Boss Keys are put in their dungeon.
                    keysanity:   Boss Keys can appear anywhere.
                    '''
        },
        {
            'group': 'logic',
            'widget': 'Combobox',
            'default': 'Boss Keys: Dungeon Only',
            'options': {
                'Boss Keys: Remove (Keysy)': 'remove',
                'Boss Keys: Dungeon Only': 'dungeon',
                'Boss Keys: Anywhere (Keysanity)': 'keysanity'
            },
            'tooltip':'''\
                      'Remove': Boss Keys are removed. All locked
                      doors in dungeons will be unlocked. An easier
                      mode.

                      'Dungeon': Boss Keys can only appear in their
                      respective dungeon.

                      'Anywhere': Boss Keys can appear
                      anywhere in the world. A difficult mode since
                      it is more likely to need to enter a dungeon
                      multiple times.

                      Try different combination out, such as:
                      'Small Keys: Dungeon' + 'Boss Keys: Anywhere'
                      for a milder Keysanity experience.
                      '''
        }),
    Setting_Info('enhance_map_compass', bool, 1, True,
        {
            'help': '''\
                    Gives the Map and Compass extra functionality.
                    Map will tell if a dungeon is vanilla or Master Quest.
                    Compass will tell what medallion or stone is within.
                    The Temple of Time Altar will no longer provide any
                    information. If the maps and compasses are removed then
                    the information will be unavailable.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Maps and Compasses Give Information',
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                    Gives the Map and Compass extra functionality.
                    Map will tell if a dungeon is vanilla or Master Quest.
                    Compass will tell what medallion or stone is within.
                    The Temple of Time Altar will no longer provide any
                    information.

                    'Maps/Compasses: Remove': The dungeon information is
                    not available anywhere in the game.

                    'Maps/Compasses: Start With': The dungeon information
                    is available immediately from the dungeon menu.
                    ''',
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
            'group': 'logic',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      The Boss Key door in Ganon's Tower
                      will start unlocked. This is intended
                      to be used with reduced trial
                      requirements to make it more likely
                      that skipped trials can be avoided.
                      ''',
            'dependency': lambda guivar: guivar['shuffle_bosskeys'].get() != 'Boss Keys: Remove (Keysy)',
        }),
    Setting_Info('tokensanity', str, 2, True,
        {
            'default': 'off',
            'const': 'off',
            'nargs': '?',
            'help': '''\
                    Gold Skulltula Tokens will be shuffled into the pool,
                    and Gold Skulltula locations can have any item.
                    off:        Don't use this feature
                    dungeons:   Only dungeon Skulltulas will be shuffled
                    all:        All Gold Skulltulas will be shuffled
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
            'tooltip':'''\
                      Token reward from Gold Skulltulas are
                      shuffled into the pool.

                      'Dungeons Only': This only shuffles
                      the GS locations that are within
                      dungeons, increasing the value of
                      most dungeons and making internal
                      dungeon exploration more diverse.

                      'All Tokens': Effectively adds 100
                      new locations for items to appear.
                      '''
        }),
    Setting_Info('mq_dungeons_random', bool, 1, True,
        {
            'help': '''\
                    If set, a uniformly random number of dungeons will have Master Quest designs.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Random Number of MQ Dungeons',
            'group': 'world',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      If set, a random number of dungeons
                      will have Master Quest designs.
                      '''
        }),
    Setting_Info('mq_dungeons', int, 4, True,
        {
            'default': 0,
            'const': 0,
            'nargs': '?',
            'choices': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'help': '''\
                    Select a number (0-12) of Master Quest dungeons to appear in the game.
                    0:  (default) All dungeon will have their original designs.
                    ...
                    6:  50/50 split; Half of all dungeons will be from Master Quest.
                    ...
                    12: All dungeons will have Master Quest redesigns.
                    '''
        },
        {
            'group': 'world',
            'widget': 'Scale',
            'default': 0,
            'min': 0,
            'max': 12,
            'dependency': lambda guivar: not guivar['mq_dungeons_random'].get(),
            'tooltip':'''\
                      Select a number of Master Quest
                      dungeons to appear in the game.

                      0: All dungeon will have their
                      original designs. (default)

                      6: Half of all dungeons will
                      be from Master Quest.

                      12: All dungeons will have
                      Master Quest redesigns.
                      ''',
        }),
    Setting_Info('logic_skulltulas', int, 3, True,
        {
            'default': 50,
            'const': 50,
            'nargs': '?',
            'choices': [0, 10, 20, 30, 40, 50],
            'help': '''\
                    Choose the maximum number of Gold Skulltula Tokens you will be expected to collect.
                    ''',
            'type': int
        },
        {
            'text': 'Maximum Expected Skulltula Tokens',
            'group': 'rewards',
            'widget': 'Scale',
            'default': 50,
            'min': 0,
            'max': 50,
            'step': 10,
            'tooltip':'''\
                      Choose the maximum number of Gold Skulltula
                      Tokens you will be expected to collect.
                      '''
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
            'default': 'unchecked',
            'tooltip':'''\
                      GS Tokens that can only be obtained
                      during the night expect you to have Sun's
                      Song to collect them. This prevents needing
                      to wait until night for some locations.
                      '''
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
            'default': 'unchecked',
            'tooltip':'''\
                      The Big Poe vendor will not have a
                      required item.
                      '''
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
            'default': 'unchecked',
            'tooltip':'''\
                      Fishing does not work correctly on
                      Bizhawk.
                      '''
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
            'default': 'unchecked',
            'tooltip':'''\
                      Fishing does not work correctly on
                      Bizhawk.
                      '''
        }),
    Setting_Info('logic_no_trade_skull_mask', bool, 1, True,
        {
            'help': '''\
                    You will not be expected to show the Skull Mask at the forest stage.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Skull Mask Reward',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Showing off the Skull Mask will
                      not yield a required item.
                      '''
        }),
    Setting_Info('logic_no_trade_mask_of_truth', bool, 1, True,
        {
            'help': '''\
                    You will not be expected to show the Mask of Truth at the forest stage.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Mask of Truth Reward',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Showing off the Mask of Truth
                      will not yield a required item.
                      '''
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
            'default': 'unchecked',
            'tooltip':'''\
                      Scoring 1500 points at horseback
                      archery will not yield a required item.
                      '''
        }),
    Setting_Info('logic_no_memory_game', bool, 1, True,
        {
            'help': '''\
                    You will not be expected to play the ocarina memory game in Lost Woods.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Lost Woods Memory Game',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Playing the ocarina memory game
                      will not yield a required item.
                      '''
        }),
    Setting_Info('logic_no_second_dampe_race', bool, 1, True,
        {
            'help': '''\
                    You will not be expected to race Dampe a second time.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Racing Dampe a Second Time',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      The second Dampe race will
                      not yield a required item.
                      '''
        }),
    Setting_Info('logic_no_trade_biggoron', bool, 1, True,
        {
            'help': '''\
                    You will not be expected to show the Claim Check to Biggoron.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'No Biggoron Reward',
            'group': 'rewards',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Showing the Claim Check to Biggoron
                      will not yield a required item.
                      '''
        }),
    Setting_Info('logic_earliest_adult_trade', str, 4, True,
        {
            'default': 'pocket_egg',
            'const': 'always',
            'nargs': '?',
            'help': '''\
                    Select the earliest item that can appear in the adult trade sequence:
                    'pocket_egg'
                    'pocket_cucco'
                    'cojiro'
                    'odd_mushroom'
                    'poachers_saw'
                    'broken_sword'
                    'prescription'
                    'eyeball_frog'
                    'eyedrops'
                    'claim_check'
                    '''
        },
        {
            'text': 'Adult Trade Sequence',
            'group': 'rewards',
            'widget': 'Combobox',
            'dependency': lambda guivar: not guivar['logic_no_trade_biggoron'].get(),
            'default': 'Earliest: Pocket Egg',
            'options': {
                'Earliest: Pocket Egg': 'pocket_egg',
                'Earliest: Pocket Cucco': 'pocket_cucco',
                'Earliest: Cojiro': 'cojiro',
                'Earliest: Odd Mushroom': 'odd_mushroom',
                'Earliest: Poacher\'s Saw': 'poachers_saw',
                'Earliest: Broken Sword': 'broken_sword',
                'Earliest: Prescription': 'prescription',
                'Earliest: Eyeball Frog': 'eyeball_frog',
                'Earliest: Eyedrops': 'eyedrops',
                'Earliest: Claim Check': 'claim_check'},
            'tooltip':'''\
                      Select the earliest item that can appear in the adult trade sequence.
                      '''
        }),
    Setting_Info('logic_latest_adult_trade', str, 4, True,
        {
            'default': 'claim_check',
            'const': 'always',
            'nargs': '?',
            'help': '''\
                    Select the latest item that can appear in the adult trade sequence:
                    'pocket_egg'
                    'pocket_cucco'
                    'cojiro'
                    'odd_mushroom'
                    'poachers_saw'
                    'broken_sword'
                    'prescription'
                    'eyeball_frog'
                    'eyedrops'
                    'claim_check'
                    '''
        },
        {
            'group': 'rewards',
            'widget': 'Combobox',
            'dependency': lambda guivar: not guivar['logic_no_trade_biggoron'].get(),
            'default': 'Latest: Claim Check',
            'options': {
                'Latest: Pocket Egg': 'pocket_egg',
                'Latest: Pocket Cucco': 'pocket_cucco',
                'Latest: Cojiro': 'cojiro',
                'Latest: Odd Mushroom': 'odd_mushroom',
                'Latest: Poacher\'s Saw': 'poachers_saw',
                'Latest: Broken Sword': 'broken_sword',
                'Latest: Prescription': 'prescription',
                'Latest: Eyeball Frog': 'eyeball_frog',
                'Latest: Eyedrops': 'eyedrops',
                'Latest: Claim Check': 'claim_check'},
            'tooltip':'''\
                      Select the latest item that can appear in the adult trade sequence.
                      '''
        }),
    Setting_Info('logic_tricks', bool, 1, True,
        {
            'help': '''\
                    Enable various advanced tricks that do not require glitches.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Various Advanced Tricks',
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Enables a large number of minor
                      tricks that do not require glitches.
                      '''
        }),
    Setting_Info('logic_man_on_roof', bool, 1, True,
        {
            'help': '''\
                    The man on the roof will not require the Hookshot in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Man on Roof without Hookshot',
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Can be reached by side-hopping off
                      the watchtower.
                      '''
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
            'default': 'unchecked',
            'tooltip':'''\
                      Requires 9 sticks or 5 jump slashes.
                      '''
        }),
    Setting_Info('logic_dc_jump', bool, 1, True,
        {
            'help': '''\
                    Jumping towards the Bomb Bag chest in Dodongo's Cavern as an adult
                    will not require Hover Boots in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Dodongo\'s Cavern Spike Trap Room Jump without Hover Boots',
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Jump is adult only.
                      '''
        }),
    Setting_Info('logic_windmill_poh', bool, 1, True,
        {
            'help': '''\
                    Getting the Piece of Heart in the windmill as an adult will require nothing in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Windmill PoH as Adult with Nothing',
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Can jump up to the spinning platform from
                      below as adult.
                      '''
        }),
    Setting_Info('logic_crater_bean_poh_with_hovers', bool, 1, True,
        {
            'help': '''\
                    The Piece of Heart in Death Mountain Crater that normally requires the bean to
                    reach will optionally require the Hover Boots in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': "Crater's Bean PoH with Hover Boots",
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Hover from the base of the bridge
                      near Goron City and walk up the
                      very steep slope.
                      '''
        }),
    Setting_Info('logic_zora_with_cucco', bool, 1, True,
        {
            'help': '''\
                    Zora's Domain can be entered with a Cucco as child in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': "Zora's Domain Entry with Cucco",
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Can fly behind the waterfall with
                      a cucco as child.
                      '''
        }),
    Setting_Info('logic_zora_with_hovers', bool, 1, True,
        {
            'help': '''\
                    Zora's Domain can be entered with Hover Boots as Adult in logic.
                    ''',
            'action': 'store_true'
        },
        {
            'text': "Zora's Domain Entry with Hover Boots",
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Can hover behind the waterfall as adult.
                      This is very difficult.
                      '''
        }),
    Setting_Info('logic_fewer_tunic_requirements', bool, 1, True,
        {
            'help': '''\
                    Allows the following possible without Goron or Zora Tunic:
                    Enter Water Temple
                    Enter Fire Temple
                    Zoras Fountain Bottom Freestanding PoH
                    Gerudo Training Grounds Underwater Silver Rupee Chest
                    ''',
            'action': 'store_true'
        },
        {
            'text': "Fewer Tunic Requirements",
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Allows the following possible without Tunics:
                      - Enter Water Temple. The key below the center
                      pillar still requires Zora Tunic.
                      - Enter Fire Temple. Only the first floor is
                      accessible, and not Volvagia.
                      - Zora's Fountain Bottom Freestanding PoH.
                      Might not have enough health to resurface.
                      - Gerudo Training Grounds Underwater
                      Silver Rupee Chest. May need to make multiple
                      trips.
                      '''
        }),
    Setting_Info('logic_morpha_with_scale', bool, 1, True,
        {
            'help': '''\
                    Allows entering Water Temple and beating
                    Morpha with Gold Scale instead of Iron Boots.
                    Only applicable for keysanity and keysy.
                    ''',
            'action': 'store_true'
        },
        {
            'text': "Morpha with Gold Scale",
            'group': 'tricks',
            'widget': 'Checkbutton',
            'default': 'checked',
            'tooltip':'''\
                      Allows entering Water Temple and beating
                      Morpha with Gold Scale instead of Iron Boots.
                      Only applicable for keysanity and keysy due
                      to the logic always seeing every chest in
                      Water Temple that could contain the Boss Key
                      as requiring Iron Boots.
                      ''',
            'dependency': lambda guivar: guivar['shuffle_bosskeys'].get() != 'Boss Keys: Dungeon Only'
        }),
    Setting_Info('logic_lens', str, 2, True,
        {
            'default': 'all',
            'const': 'always',
            'nargs': '?',
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
            'default': 'Required Everywhere',
            'options': {
                'Required Everywhere': 'all',
                'Wasteland and Chest Minigame': 'chest-wasteland',
                'Only Chest Minigame': 'chest',
            },
            'tooltip':'''\
                      'Required everywhere': every invisible or
                      fake object will expect you to have the
                      Lens of Truth and Magic. The exception is
                      passing through the first wall in Bottom of
                      the Well, since that is required in vanilla.

                      'Wasteland': The lens is needed to follow
                      the ghost guide across the Haunted Wasteland.
                      '''
        }),
    Setting_Info('ocarina_songs', bool, 1, True,
        {
            'help': '''\
                    Randomizes the notes needed to play each ocarina song.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Randomize Ocarina Song Notes',
            'group': 'other',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Will need to memorize a new set of songs.
                      Can be silly, but difficult. Songs are
                      generally sensible, and warp songs are
                      typically more difficult.
                      '''
        }),
    Setting_Info('correct_chest_sizes', bool, 1, True,
        {
            'help': '''\
                    Updates the chest sizes to match their contents.
                    Small Chest = Non-required Item
                    Big Chest = Progression Item
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Chest Size Matches Contents',
            'group': 'other',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      Chests will be large if they contain a major
                      item and small if they don't. This allows skipping
                      chests if they are small. However, skipping
                      small chests will mean having low health,
                      ammo, and rupees, so doing so is a risk.
                      '''
        }),
    Setting_Info('clearer_hints', bool, 1, True,
        {
            'help': '''\
                    The hints provided by Gossip Stones are
                    very direct.
                    ''',
            'action': 'store_true'
        },
        {
            'text': 'Clearer Hints',
            'group': 'other',
            'widget': 'Checkbutton',
            'default': 'unchecked',
            'tooltip':'''\
                      The hints provided by Gossip Stones will
                      be very direct if this option is enabled.
                      '''
        }),
    Setting_Info('hints', str, 2, True,
        {
            'default': 'none',
            'const': 'agony',
            'nargs': '?',
            'help': '''\
                    Choose how Gossip Stones behave
                    none:   Default behavior
                    mask:   Have useful hints that are read with the Mask of Truth.
                    agony:  Have useful hints that are read with Stone of Agony.
                    always: Have useful hints which can always be read.
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
            'tooltip':'''\
                      Gossip Stones can be made to give hints
                      about where items can be found.

                      Different settings can be chosen to
                      decide which item is needed to
                      speak to Gossip Stones. Choosing to
                      stick with the Mask of Truth will
                      make the hints very difficult to
                      obtain.

                      Hints for 'on the way of the hero' are
                      locations that contain items that are
                      required to beat the game.
                      '''
        }),
    Setting_Info('hint_dist', str, 2, True,
        {
            'default': 'balanced',
            'const': 'balanced',
            'nargs': '?',
            'help': '''\
                    Choose how Gossip Stones hints are distributed
                    balanced: Use a balanced distribution of hint types
                    strong: Use a strong distribution of hint types
                    very_strong: Use a very strong distribution of hint types
                    '''
        },
        {
            'text': 'Hint Distribution',
            'group': 'other',
            'widget': 'Combobox',
            'default': 'Balanced',
            'options': {
                'Balanced': 'balanced',
                'Strong': 'strong',
                'Very Strong': 'very_strong',
            },
            'tooltip':'''\
                      Strong distribution has some
                      duplicate hints and no junk
                      hints.
                      Very Strong distribution has
                      only very useful hints.
                      '''
        }),
    Setting_Info('text_shuffle', str, 2, True,
        {
            'default': 'none',
            'const': 'none',
            'nargs': '?',
            'help': '''\
                    Choose how to shuffle the game's messages.
                    none:          Default behavior
                    except_hints:  All non-useful text is shuffled.
                    complete:      All text is shuffled.
                    '''
        },
        {
            'text': 'Text Shuffle',
            'group': 'other',
            'widget': 'Combobox',
            'default': 'No Text Shuffled',
            'options': {
                'No Text Shuffled': 'none',
                'Shuffled except Hints and Keys': 'except_hints',
                'All Text Shuffled': 'complete',
            },
            'tooltip':'''\
                      Will make things confusing for comedic value.

                      'Shuffled except Hints and Keys': Key texts
                      are not shuffled because in keysanity it is
                      inconvenient to figure out which keys are which
                      without the correct text. Similarly, non-shop
                      items sold in shops will also retain standard
                      text for the purpose of accurate price checks.
                      '''
        }),
    Setting_Info('item_pool_value', str, 2, True,
        {
            'default': 'balanced',
            'const': 'balanced',
            'nargs': '?',
            'help': '''\
                    Change the item pool for an added challenge.
                    plentiful:      Duplicates most of the major items, making it easier to find progression.
                    balanced:       Default items
                    scarce:         Double defense, double magic, and all 8 heart containers are removed. Ammo
                                    for each type can only be expanded once and you can only find three Bombchu packs.
                    minimal:        Double defense, double magic, Nayru's Love, and all health upgrades are removed.
                                    No ammo expansions are available and you can only find one Bombchu pack.
                    '''
        },
        {
            'text': 'Item Pool Value',
            'group': 'other',
            'widget': 'Combobox',
            'default': 'Balanced',
            'options': {
                'Plentiful': 'plentiful',
                'Balanced': 'balanced',
                'Scarce': 'scarce',
                'Minimal': 'minimal'
            },
            'tooltip':'''\
                      Changes the amount of bonus items that
                      are available in the game.

                      'Plentiful': Extra major items are added.

                      'Balanced': Original item pool.

                      'Scarce': Some excess items are removed,
                      including health upgrades.

                      'Minimal': Most excess items are removed.
                      '''
        }),
    Setting_Info('damage_multiplier', str, 3, True,
        {
            'default': 'normal',
            'const': 'normal',
            'nargs': '?',
            'help': '''\
                    Change the amount of damage taken.
                    half:           Half damage taken.
                    normal:         Normal damage taken.
                    double:         Double damage taken.
                    quadruple:      Quadruple damage taken.
                    ohko:           Link will die in one hit.
                    '''
        },
        {
            'text': 'Damage Multiplier',
            'group': 'other',
            'widget': 'Combobox',
            'default': 'Normal',
            'options': {
                'Half': 'half',
                'Normal': 'normal',
                'Double': 'double',
                'Quadruple': 'quadruple',
                'OHKO': 'ohko',
            },
            'tooltip':'''\
                      Changes the amount of damage taken.

                      'OHKO': Link dies in one hit.
                      '''
        }),
    Setting_Info('default_targeting', str, 1, False,
        {
            'default': 'hold',
            'const': 'always',
            'nargs': '?',
            'help': '''\
                    Choose what the default Z-targeting is.
                    '''
        },
        {
            'text': 'Default Targeting Option',
            'group': 'cosmetics',
            'widget': 'Combobox',
            'default': 'Hold',
            'options': {
                'Hold': 'hold',
                'Switch': 'switch',
            }
        }),
    Setting_Info('background_music', str, 2, False,
        {
            'default': 'normal',
            'const': 'normal',
            'nargs': '?',
            'help': '''\
                    Sets the background music behavior
                    normal:      Areas play their normal background music
                    off:         No background music
                    random:      Areas play random background music
                    '''
        },
        {
            'text': 'Background Music',
            'group': 'cosmetics',
            'widget': 'Combobox',
            'default': 'Normal',
            'options': {
                'Normal': 'normal',
                'No Music': 'off',
                'Random': 'random',
            },
            'tooltip': '''\
                       'No Music': No background music.
                       is played.

                       'Random': Area background music is
                       randomized.
                       '''
        }),

    Setting_Info('kokiricolor', str, 0, False,
        {
            'default': 'Kokiri Green',
            'const': 'Kokiri Green',
            'nargs': '?',
            'type': parse_custom_tunic_color,
            'help': '''\
                    Choose the color for Link's Kokiri Tunic. (default: %(default)s)
                    Color:              Make the Kokiri Tunic this color.
                    Random Choice:      Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Kokiri Tunic Color',
            'group': 'tuniccolor',
            'widget': 'Combobox',
            'default': 'Kokiri Green',
            'options': get_tunic_color_options(),
            'tooltip':'''\
                      'Random Choice': Choose a random
                      color from this list of colors.
                      'Completely Random': Choose a random
                      color from any color the N64 can draw.
                      '''
        }),
    Setting_Info('goroncolor', str, 0, False,
        {
            'default': 'Goron Red',
            'const': 'Goron Red',
            'nargs': '?',
            'type': parse_custom_tunic_color,
            'help': '''\
                    Choose the color for Link's Goron Tunic. (default: %(default)s)
                    Color:              Make the Goron Tunic this color.
                    Random Choice:      Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Goron Tunic Color',
            'group': 'tuniccolor',
            'widget': 'Combobox',
            'default': 'Goron Red',
            'options': get_tunic_color_options(),
            'tooltip':'''\
                      'Random Choice': Choose a random
                      color from this list of colors.
                      'Completely Random': Choose a random
                      color from any color the N64 can draw.
                      '''
        }),
    Setting_Info('zoracolor', str, 0, False,
        {
            'default': 'Zora Blue',
            'const': 'Zora Blue',
            'nargs': '?',
            'type': parse_custom_tunic_color,
            'help': '''\
                    Choose the color for Link's Zora Tunic. (default: %(default)s)
                    Color:              Make the Zora Tunic this color.
                    Random Choice:      Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Zora Tunic Color',
            'group': 'tuniccolor',
            'widget': 'Combobox',
            'default': 'Zora Blue',
            'options': get_tunic_color_options(),
            'tooltip':'''\
                      'Random Choice': Choose a random
                      color from this list of colors.
                      'Completely Random': Choose a random
                      color from any color the N64 can draw.
                      '''
        }),
    Setting_Info('navicolordefault', str, 0, False,
        {
            'default': 'White',
            'const': 'White',
            'nargs': '?',
            'type': parse_custom_navi_color,
            'help': '''\
                    Choose the color for Navi when she is idle. (default: %(default)s)
                    Color:             Make the Navi this color.
                    Random Choice:     Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Navi Idle',
            'group': 'navicolor',
            'widget': 'Combobox',
            'default': 'White',
            'options': get_navi_color_options(),
            'tooltip':'''\
                      'Random Choice': Choose a random
                      color from this list of colors.
                      'Completely Random': Choose a random
                      color from any color the N64 can draw.
                      '''
        }),
    Setting_Info('navicolorenemy', str, 0, False,
        {
            'default': 'Yellow',
            'const': 'Yellow',
            'nargs': '?',
            'type': parse_custom_navi_color,
            'help': '''\
                    Choose the color for Navi when she is targeting an enemy. (default: %(default)s)
                    Color:             Make the Navi this color.
                    Random Choice:     Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Navi Targeting Enemy',
            'group': 'navicolor',
            'widget': 'Combobox',
            'default': 'Yellow',
            'options': get_navi_color_options(),
            'tooltip':'''\
                      'Random Choice': Choose a random
                      color from this list of colors.
                      'Completely Random': Choose a random
                      color from any color the N64 can draw.
                      '''
        }),
    Setting_Info('navicolornpc', str, 0, False,
        {
            'default': 'Light Blue',
            'const': 'Light Blue',
            'nargs': '?',
            'type': parse_custom_navi_color,
            'help': '''\
                    Choose the color for Navi when she is targeting an NPC. (default: %(default)s)
                    Color:             Make the Navi this color.
                    Random Choice:     Choose a random color from this list of colors.
                    Completely Random: Choose a random color from any color the N64 can draw.
                    '''
        },
        {
            'text': 'Navi Targeting NPC',
            'group': 'navicolor',
            'widget': 'Combobox',
            'default': 'Light Blue',
            'options': get_navi_color_options(),
            'tooltip':'''\
                      'Random Choice': Choose a random
                      color from this list of colors.
                      'Completely Random': Choose a random
                      color from any color the N64 can draw.
                      '''
        }),
    Setting_Info('navicolorprop', str, 0, False,
        {
            'default': 'Green',
            'const': 'Green',
            'nargs': '?',
            'type': parse_custom_navi_color,
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
            'tooltip':'''\
                      'Random Choice': Choose a random
                      color from this list of colors.
                      'Completely Random': Choose a random
                      color from any color the N64 can draw.
                      '''
        }),
    Setting_Info('navisfxoverworld', str, 0, False,
        {
            'default': 'Default',
            'const': 'Default',
            'nargs': '?',
            'help': '''\
                    Select the sound effect that plays when Navi has a hint. (default: %(default)s)
                    Sound:         Replace the sound effect with the chosen sound.
                    Random Choice: Replace the sound effect with a random sound from this list.
                    None:          Eliminate Navi hint sounds.
                    '''
        },
        {
            'text': 'Navi Hint',
            'group': 'navihint',
            'widget': 'Combobox',
            'default': 'Default',
            'options': get_NaviSFX_options(),
        }),
        Setting_Info('navisfxenemytarget', str, 0, False,
        {
            'default': 'Default',
            'const': 'Default',
            'nargs': '?',
            'help': '''\
                    Select the sound effect that plays when targeting an enemy. (default: %(default)s)
                    Sound:         Replace the sound effect with the chosen sound.
                    Random Choice: Replace the sound effect with a random sound from this list.
                    None:          Eliminate Navi hint sounds.
                    '''
        },
        {
            'text': 'Navi Enemy Target',
            'group': 'navihint',
            'widget': 'Combobox',
            'default': 'Default',
            'options': get_NaviSFX_options(),
        }),
    Setting_Info('healthSFX', str, 0, False,
        {
            'default': 'Default',
            'const': 'Default',
            'nargs': '?',
            'help': '''\
                    Select the sound effect that loops at low health. (default: %(default)s)
                    Sound:         Replace the sound effect with the chosen sound.
                    Random Choice: Replace the sound effect with a random sound from this list.
                    None:          Eliminate heart beeps.
                    '''
        },
        {
            'text': 'Low Health SFX',
            'group': 'lowhp',
            'widget': 'Combobox',
            'default': 'Default',
            'options': get_HealthSFX_options(),
            'tooltip':'''\
                      'Random Choice': Choose a random
                      sound from this list.
                      'Default': Beep. Beep. Beep.
                      '''
        }),
]
