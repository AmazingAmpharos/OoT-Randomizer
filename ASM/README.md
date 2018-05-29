- Download the armips assembler: <https://github.com/Kingcom/armips>
- Put the ROM you want to patch at `roms/base.z64`
- Run `armips src/build.asm`, which will create `roms/patched.z64`
- To update the front-end patch file, run:
  ```python3 scripts/rom_diff.py roms/base.z64 roms/patched.z64 ../data/base2current.json```
