restore_swordless_flag:
    ; Displaced code
    lbu     t6, 0x0040 (a1)
    lbu     v0, 0x0070 (a1)

    li      v1, 0xFF
    bne     t6, v1, @@return
    nop
    li      v1, 1
    sb      v1, 0x0F33 (a1) ; If restoring 0xFF to B equip, set the swordless flag
@@return:
    jr      ra
    nop

;==================================================================================================

save_child_b_equip:
    ; t0 = save context
    lw      t1, 0x04 (t0)
    beqz    t1, @@return ; Only do this as child
    nop

    lbu     t1, 0x68 (t0) ; Load current B equip
    beq     t1, 0x3B, @@save
    nop

    li      t1, 0xFF

@@save:
    sb      t1, 0x40 (t0) ; Save B equip, will be loaded on next adult -> child transition

@@return:
    jr      ra
    sb      t6, 0x68 (t0) ; Displaced code
