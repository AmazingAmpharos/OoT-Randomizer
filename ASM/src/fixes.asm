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
