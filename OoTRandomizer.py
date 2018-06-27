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
from Rom import get_tunic_color_options, get_navi_color_options
from Settings import get_settings_from_command_line_args


class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)


def start():

    settings, gui, args_loglevel = get_settings_from_command_line_args()

    if is_bundled() and len(sys.argv) == 1:
        # for the bundled builds, if we have no arguments, the user
        # probably wants the gui. Users of the bundled build who want the command line
        # interface shouuld specify at least one option, possibly setting a value to a
        # default if they like all the defaults
        close_console()
        guiMain()
        sys.exit(0)

    # ToDo: Validate files further than mere existance
    if not os.path.isfile(settings.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        sys.exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args_loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if gui:
        guiMain(settings)
    elif settings.count is not None:
        orig_seed = settings.seed
        for i in range(settings.count):
            settings.update_seed(orig_seed + '-' + str(i))
            main(settings)
    else:
        main(settings)

if __name__ == '__main__':
    start()
