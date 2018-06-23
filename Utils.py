import os
import subprocess
import sys
import logging

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

def output_path(path, arg_path = None):
    logger = logging.getLogger('')

    if (output_path.cached_path is not None and arg_path is None) or output_path.invalid_output_arg or (output_path.cached_path is not None and output_path.cached_path == arg_path):
        return os.path.join(output_path.cached_path, path)

    if not is_bundled():
        if arg_path is not None:
            output_path.cached_path = arg_path

        else:
            output_path.cached_path = '.'

        if output_path.cached_path != '.' and not os.path.exists(output_path.cached_path):
            try:
                os.mkdir(output_path.cached_path)
            except:
                logger.info('Unable to create --output path. Defaulting to local path.')
                logger.info(output_path.cached_path)
                output_path.invalid_output_arg = True
                output_path.cached_path = '.'

        return os.path.join(output_path.cached_path, path)
    else:
        # has been packaged, so cannot use CWD for output.
        if sys.platform == 'win32':
            #windows
            import ctypes.wintypes
            CSIDL_PERSONAL = 5       # My Documents
            SHGFP_TYPE_CURRENT = 0   # Get current, not default value

            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

            documents = buf.value

        elif sys.platform == 'darwin':
            from AppKit import NSSearchPathForDirectoriesInDomains # pylint: disable=import-error
            # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
            NSDocumentDirectory = 9
            NSUserDomainMask = 1
            # True for expanding the tilde into a fully qualified path
            documents = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, True)[0]
        else:
            raise NotImplementedError('Not supported yet')

        output_path.cached_path = os.path.join(documents, 'OoTRandomizer')
        if not os.path.exists(output_path.cached_path):
            os.mkdir(output_path.cached_path)
        return os.path.join(output_path.cached_path, path)

output_path.cached_path = None
output_path.invalid_output_arg = False

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
