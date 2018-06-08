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
    parser.add_argument('--nodungeonitems', help='''\
                             Remove Maps and Compasses from Itempool, replacing them by
                             empty slots.
                             ''', action='store_true')
    parser.add_argument('--beatableonly', help='''\
                             Only check if the game is beatable with placement. Do not
                             ensure all locations are reachable. This only has an effect
                             on the restrictive algorithm currently.
                             ''', action='store_true')
    parser.add_argument('--hints', help='''\
                             Gossip Stones provide helpful hints about which items are
                             in inconvenient locations if the Stone of Agony is in
                             the player's inventory.
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
