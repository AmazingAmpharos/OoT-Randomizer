#!/usr/bin/env python3
import os
import sys
import subprocess
from SettingsToJson import CreateJSON
from Utils import local_path
 
def guiMain():
    web_version = '--web' in sys.argv
    if '--skip-settingslist' not in sys.argv:
        CreateJSON(local_path('setting_list.json'), web_version)

    args = ["node", "run.js", "release", "python", sys.executable]
    subprocess.Popen(args,shell=False,cwd="GUI")


if __name__ == '__main__':
    guiMain()
