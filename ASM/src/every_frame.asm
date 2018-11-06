before_game_state_update:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    jal     give_pending_item
    nop

    ; Displaced code
    lw      t9, 0x04 (s0)
    or      a0, s0, r0

    lw      ra, 0x10 (sp)
    jr      ra
    addiu   sp, sp, 0x18

after_game_state_update:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    jal     c_after_game_state_update
    nop

    ; Displaced code
    lui     t6, 0x8012
    lbu     t6, 0x1212 (t6)

    lw      ra, 0x10 (sp)
    jr      ra
    addiu   sp, sp, 0x18
