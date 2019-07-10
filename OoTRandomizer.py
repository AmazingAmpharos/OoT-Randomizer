#!/usr/bin/env python3
import argparse
import os
import logging
import random
import textwrap
import sys
import hashlib

from Gui import guiMain
from Main import main, from_patch_file, cosmetic_patch
from Utils import is_bundled, close_console, check_version, VersionError, check_python_version, default_output_path
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
    if settings.compress_rom != 'None' and not os.path.isfile(settings.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % settings.rom)
        sys.exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args_loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    logger = logging.getLogger('')

    settings_string_hash = hashlib.sha1(settings.settings_string.encode('utf-8')).hexdigest().upper()[:5]
    if settings.output_file:
        outfilebase = settings.output_file
    elif settings.world_count > 1:
        outfilebase = 'OoT_%s_%s_W%d' % (settings_string_hash, settings.seed, settings.world_count)
    else:
        outfilebase = 'OoT_%s_%s' % (settings_string_hash, settings.seed)
    output_dir = default_output_path(settings.output_dir)
    log_path = os.path.join(output_dir, '%s.log' % outfilebase)
    log_file = logging.FileHandler(log_path)
    logger.addHandler(log_file)

    if not settings.check_version:
        try:
            version_error = check_version(settings.checked_version)
        except VersionError as e:
            logger.warning(str(e))

    try:
        if gui:
            guiMain(settings)
        elif settings.cosmetics_only:
            cosmetic_patch(settings)
        elif settings.patch_file != '':
            from_patch_file(settings)
        elif settings.count > 1:
            orig_seed = settings.seed
            for i in range(settings.count):
                settings.update_seed(orig_seed + '-' + str(i))
                main(settings)
        else:
            main(settings)
    except Exception as ex:
        logger.exception(ex)


if __name__ == '__main__':
    check_python_version()
    start()
