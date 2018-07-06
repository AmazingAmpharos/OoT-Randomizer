import os
import subprocess
import sys

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
        path = os.path.join('.', 'Output')

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
