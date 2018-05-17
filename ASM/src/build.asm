.n64
.relativeinclude on

.create "../roms/patched.z64", 0
.incbin "../roms/base.z64"

;==================================================================================================
; Base game editing region
;==================================================================================================

.include "hacks.asm"

;==================================================================================================
; New code region
;==================================================================================================

; 0x80400000 in memory -> 0x03480000 in ROM
.headersize 0x7CF80000
.org 0x80400000

; 0x000 - 0x5FF: Settings and tables which the front-end may write
.area 0x600, 0
.include "config.asm"
.include "item_data.asm" ; Placed here temporarily, won't fit in the code area
.endarea

; 0x600 - 0x9FF: Currently reserved for code blocks written by Rom.py
.skip 0x400

; 0xA00 - 0xFFF: New code blocks
.area 0x600, 0
.include "constants.asm"
.include "state.asm"
.include "items.asm"
.include "fixes.asm"
.include "menu.asm"
.endarea

.close
