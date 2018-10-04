import os
import subprocess
import sys
import urllib.request
from urllib.error import URLError, HTTPError
import re
from version import __version__
from random import choice as random_choice

def is_bundled():
    return getattr(sys, 'frozen', False)

def local_path(path):
    if local_path.cached_path is not None:
        return os.path.join(local_path.cached_path, path)

    if is_bundled():
        # we are running in a bundle
        local_path.cached_path = sys._MEIPASS # pylint: disable=protected-access,no-member
    else:
        # we are running in a normal Python environment
        local_path.cached_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(local_path.cached_path, path)

local_path.cached_path = None

def default_output_path(path):
    if path == '':
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Output')

    if not os.path.exists(path):
        os.mkdir(path)
    return path


def open_file(filename):
    if sys.platform == 'win32':
        os.startfile(filename)
    else:
        open_command = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([open_command, filename])

def close_console():
    if sys.platform == 'win32':
        #windows
        import ctypes.wintypes
        try:
            ctypes.windll.kernel32.FreeConsole()
        except Exception:
            pass

def compare_version(a, b):
    if not a and not b:
        return 0
    elif a and not b:
        return 1
    elif not a and b:
        return -1

    sa = a.replace(' ', '.').split('.')
    sb = b.replace(' ', '.').split('.')

    for i in range(0,3):
        if int(sa[i]) > int(sb[i]):
            return 1
        if int(sa[i]) < int(sb[i]):
            return -1
    return 0

class VersionError(Exception):
    pass

def check_version(checked_version):
    try:
        with urllib.request.urlopen('http://raw.githubusercontent.com/TestRunnerSRL/OoT-Randomizer/Dev/version.py') as versionurl:
            version = versionurl.read()
            version = re.search(".__version__ = '(.+)'", str(version)).group(1)

            if compare_version(version, __version__) > 0 and compare_version(checked_version, __version__) < 0:
                raise VersionError("You do not seem to be on the latest version!\nYou are on version " + __version__ + ", and the latest is version " + version + ".")
    except (URLError, HTTPError) as e:
        logger.warning("Could not fetch latest version: " + str(e))

# Shim for the sole purpose of maintaining compatibility with older versions of
# Python 3. Note: cum weights, as well as fractional weights are unimplemented,
# as neither were used elsewhere at the time of writing.
def random_choices(population, weights=None, k=1):
    pop_size = len(population)
    if (weights is None):
        weights = [1] * pop_size
    else:
        assert (pop_size == len(weights)), "population and weights mismatch"

    weighted_pop = []
    for i in range(pop_size):
        for each in range(weights[i]):
            weighted_pop.append(population[i])

    result = []
    for i in range(k):
        result.append(random_choice(weighted_pop))

    return result
