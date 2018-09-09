; Update CRC
.org 0x10
    .word 0x9345AE5B, 0x97DB4131

; Add dmatable entries for new code
.org 0xD260
    .word 0x03480000, 0x03485000, 0x03480000, 0
    .word 0x034B3000, 0x034BE000, 0x034B3000, 0

; Load new code from ROM
; Replaces:
;   lui     v0, 0x8012
;   addiu   v0, v0, 0xD2A0
;   sw      ra, 0x001C (sp)
;   sw      a0, 0x0140 (sp)
;   addiu   t6, r0, 0x0140
;   lui     at, 0x8010
;   sw      t6, 0xE500 (at)
;   lui     at, 0x8010
.org 0xB17BB4 ; In memory: 0x800A1C54
    sw      ra, 0x001C (sp)
    sw      a0, 0x0140 (sp)

    ; Load first code file from ROM
    lui     a0, 0x8040
    lui     a1, 0x0348
    jal     0x80000DF0
    ori     a2, r0, 0x5000

    jal     init
    nop
