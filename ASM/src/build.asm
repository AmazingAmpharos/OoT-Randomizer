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
.skip 0x110

.area 0xE0, 0
.include "menu.asm" ; Placed here temporarily, won't fit in the code area
.include "fixes.asm" ; Placed here temporarily, won't fit in the code area
.endarea

.skip 0x70

.area 0xC0, 0
.include "every_frame.asm" ; Placed here temporarily, won't fit in the code area
.endarea

.skip 0xE0

; 0xA00 - 0xFFF: New code blocks
.area 0x600, 0
.include "constants.asm"
.include "state.asm"
.include "items.asm"
.endarea

.close
