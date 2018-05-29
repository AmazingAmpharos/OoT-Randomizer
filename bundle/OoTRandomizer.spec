# -*- mode: python -*-
from PyInstaller.compat import is_win
block_cipher = None

# Todo: the runtime hooks should only be installed on windows
a = Analysis(['../OoTRandomizer.py'],
             pathex=['bundle'],
             binaries=[],
             datas=[('../data/', 'data/'), ('../Compress/', 'Compress/'), ('../Decompress/', 'Decompress/'), ('../README.html', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=['bundle/_rt_hook.py'],
             excludes=['lzma', 'bz2'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='OoTRandomizer',
          debug=False,
          strip=False,
          upx=False,
          icon='data/ER.ico',
          console=is_win )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='OoTRandomizer')
app = BUNDLE(coll,
             name ='OoTRandomizer.app',
             icon = 'data/ER.icns',
             bundle_identifier = None)
