init:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    ; Load second code file from ROM
    li      a0, 0x80405000
    li      a1, 0x034B3000
    li      a2, 0xB000
    jal     0x80000DF0
    nop

    jal     c_init
    nop

    ; Displaced code
    lui     v0, 0x8012
    addiu   v0, v0, 0xD2A0
    addiu   t6, r0, 0x0140
    lui     at, 0x8010
    sw      t6, 0xE500 (at)

    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x18
    jr      ra
    nop
