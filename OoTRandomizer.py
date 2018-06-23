#!/usr/bin/env python3
import argparse
import os
import logging
import random
import textwrap
import sys

from Gui import guiMain
from Main import main
from Utils import is_bundled, close_console
from Rom import get_tunic_color_options


class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)


def start():
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--create_spoiler', help='Output a Spoiler File', action='store_true')
    parser.add_argument('--bridge', default='medallions', const='medallions', nargs='?', choices=['medallions', 'vanilla', 'dungeons', 'open'],
                        help='''\
                             Select requirement to spawn the Rainbow Bridge to reach Ganon's Castle. (default: %(default)s)
                             Medallions:    Collect all six medallions to create the bridge.
                             Vanilla:       Collect only the Shadow and Spirit Medallions and then view the Light Arrow cutscene.
                             All Dungeons:  Collect all spiritual stones and all medallions to create the bridge.
                             Open:          The bridge will spawn without an item requirement.
                             ''')
    parser.add_argument('--rom', default='ZOOTDEC.z64', help='Path to an OoT 1.0 rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--count', help='''\
                             Use to batch generate multiple seeds with same settings.
                             If --seed is provided, it will be used for the first seed, then
                             used to derive the next seed (i.e. generating 10 seeds with
                             --seed given will produce the same 10 (different) roms each
                             time).
                             ''', type=int)
    parser.add_argument('--open_forest', help='''\
                             Mido no longer blocks the path to the Deku Tree and
                             the Kokiri boy no longer blocks the path out of the forest.
                             ''', action='store_true')
    parser.add_argument('--open_door_of_time', help='''\
                             The Door of Time is open from the beginning of the game.
                             ''', action='store_true')
    parser.add_argument('--fast_ganon', help='''\
                             The barrier within Ganon's Castle leading to Ganon's Tower is dispelled from the
                             beginning of the game, the Boss Key is not required in Ganon's Tower, Ganondorf
                             gives a hint for the location of Light Arrows, and the tower collapse sequence
                             is removed.
                             ''', action='store_true')
    parser.add_argument('--nodungeonitems', help='''\
                             Remove Maps and Compasses from Itempool, replacing them by
                             empty slots.
                             ''', action='store_true')
    parser.add_argument('--beatableonly', help='''\
                             Only check if the game is beatable with placement. Do not
                             ensure all locations are reachable. This only has an effect
                             on the restrictive algorithm currently.
                             ''', action='store_true')
    parser.add_argument('--hints', default='none', const='always', nargs='?', choices=['none', 'mask', 'agony', 'always'],
                        help='''\
                             Choose how Gossip Stones behave
                             none:   Default behavior
                             mask:   Have useful hints that are read with the Mask of Truth (untested)
                             agony:  Have useful hints that are read with Stone of Agony
                             always: Have useful hints which can always be read
                             ''')
    parser.add_argument('--kokiricolor', default='Kokiri Green', const='Kokiri Green', nargs='?', choices=get_tunic_color_options(),
                        help='''\
                             Choose the color for Link's Kokiri Tunic. (default: %(default)s)
                             Color:        Make the Kokiri Tunic this color.
                             Random:       Choose a random color from this list of colors.
                             True Random:  Choose a random color from any color the N64 can draw.
                             ''')
    parser.add_argument('--goroncolor', default='Goron Red', const='Goron Red', nargs='?', choices=get_tunic_color_options(),
                        help='''\
                             Choose the color for Link's Goron Tunic. (default: %(default)s)
                             Color:        Make the Goron Tunic this color.
                             Random:       Choose a random color from this list of colors.
                             True Random:  Choose a random color from any color the N64 can draw.
                             ''')
    parser.add_argument('--zoracolor', default='Zora Blue', const='Zora Blue', nargs='?', choices=get_tunic_color_options(),
                        help='''\
                             Choose the color for Link's Zora Tunic. (default: %(default)s)
                             Color:        Make the Zora Tunic this color.
                             Random:       Choose a random color from this list of colors.
                             True Random:  Choose a random color from any color the N64 can draw.
                             ''')
    parser.add_argument('--healthSFX', default='Default', const='Default', nargs='?', choices=['Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'Random', 'None'],
                        help='''\
                             Select the sound effect that loops at low health. (default: %(default)s)
                             Sound:        Replace the sound effect with the chosen sound.
                             Random:       Replace the sound effect with a random sound from this list.
                             None:         Eliminate heart beeps.
                             ''')
    parser.add_argument('--navicolordefault', default='White', const='White', nargs='?', choices=get_navi_color_options(),
                        help='''\
                             Choose the color for Navi when she is idle. (default: %(default)s)
                             Color:        Make the Navi this color.
                             Random:       Choose a random color from this list of colors.
                             True Random:  Choose a random color from any color the N64 can draw.
                             ''')
    parser.add_argument('--navicolorenemy', default='Yellow', const='Yellow', nargs='?', choices=get_navi_color_options(),
                        help='''\
                             Choose the color for Navi when she is targeting an enemy. (default: %(default)s)
                             Color:        Make the Navi this color.
                             Random:       Choose a random color from this list of colors.
                             True Random:  Choose a random color from any color the N64 can draw.
                             ''')
    parser.add_argument('--navicolornpc', default='Light Blue', const='Light Blue', nargs='?', choices=get_navi_color_options(),
                        help='''\
                             Choose the color for Navi when she is targeting an NPC. (default: %(default)s)
                             Color:        Make the Navi this color.
                             Random:       Choose a random color from this list of colors.
                             True Random:  Choose a random color from any color the N64 can draw.
                             ''')
    parser.add_argument('--navicolorprop', default='Green', const='Green', nargs='?', choices=get_navi_color_options(),
                        help='''\
                             Choose the color for Navi when she is targeting a prop. (default: %(default)s)
                             Color:        Make the Navi this color.
                             Random:       Choose a random color from this list of colors.
                             True Random:  Choose a random color from any color the N64 can draw.
                             ''')
    parser.add_argument('--custom_logic', help='''\
                             Removes a number of bad locations from logic,
                             and adds a number allowed tricks
                             ''', action='store_true')
    parser.add_argument('--text_shuffle', default='none', const='none', nargs='?', choices=['none', 'except_hints', 'complete'],
                        help='''\
                             Choose how to shuffle the game's messages.
                             none:          Default behavior
                             except_hints:  All text except Gossip Stone hints and Dungeon reward hints is shuffled.
                             complete:      All text is shuffled
                             ''')
    parser.add_argument('--ocarina_songs', help='''\
                             Randomizes the notes need to play for each ocarina song.
                             ''', action='store_true')
    parser.add_argument('--suppress_rom', help='Do not create an output rom file.', action='store_true')
    parser.add_argument('--compress_rom', help='Create a compressed version of the output rom file.', action='store_true')
    parser.add_argument('--gui', help='Launch the GUI', action='store_true')
    args = parser.parse_args()

    if is_bundled() and len(sys.argv) == 1:
        # for the bundled builds, if we have no arguments, the user
        # probably wants the gui. Users of the bundled build who want the command line
        # interface shouuld specify at least one option, possibly setting a value to a
        # default if they like all the defaults
        close_console()
        guiMain()
        sys.exit(0)

    # ToDo: Validate files further than mere existance
    if not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        sys.exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if args.gui:
        guiMain(args)
    elif args.count is not None:
        seed = args.seed
        for _ in range(args.count):
            main(seed=seed, args=args)
            seed = random.randint(0, 999999999)
    else:
        main(seed=args.seed, args=args)

if __name__ == '__main__':
    start()
