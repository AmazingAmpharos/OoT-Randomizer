save_child_b_equip:
    ; t0 = save context
    lw      at, 0x04 (t0)
    beqz    at, @@return ; Only do this as child
    nop
    lbu     at, 0x68 (t0) ; Load current B equip
    sb      at, 0x40 (t0) ; Save B equip, will be loaded on next adult -> child transition
@@return:
    jr      ra
    sb      t6, 0x68 (t0) ; Displaced code
