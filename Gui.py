#!/usr/bin/env python3
import os
import sys
import subprocess
from SettingsToJson import CreateJSON
from Utils import data_path, check_python_version, compare_version, VersionError
import shutil

def guiMain():
    try:
        check_python_version()
        version_check("Node", "8.0.0")
        version_check("NPM", "0.0.0")
    except VersionError as ex:
        print(ex)
        return

    web_version = '--web' in sys.argv
    if '--skip-settingslist' not in sys.argv:
        CreateJSON(data_path('generated/settings_list.json'), web_version)

    args = ["node", "run.js", "release", "python", sys.executable]
    subprocess.Popen(args,shell=False,cwd="GUI")


def version_check(name, version):
    try:
        process = subprocess.Popen([shutil.which(name.lower()), "--version"], stdout=subprocess.PIPE)
    except Exception as ex:
        raise VersionError(f'{name} is not installed. Please install {name} {version} or later')

    while True:
        line = str(process.stdout.readline().strip(), 'UTF-8')
        if line == '':
            break
        if compare_version(line, version) < 0:
            raise VersionError(f'{name} {version} or later is requires but you are using {line}')
        print(f'Using {name} {line}')


if __name__ == '__main__':
    guiMain()
