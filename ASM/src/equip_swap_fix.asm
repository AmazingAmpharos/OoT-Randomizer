equip_swap_stick:
    la    t2, SAVE_CONTEXT
    lw    t2, 0x04(t2)       ; Link age
    beqz  t2, @@adult        ; Load empty display list if adult
    nop
    lui   t2, hi(0x06006CC0) ; Load child stick display list
    b     @@return
    addiu t2, t2, lo(0x06006CC0)
@@adult:
    la    t2, empty_dlist
@@return:
    jr    ra
    nop

equip_swap_mask:
    la    t7, SAVE_CONTEXT
    lw    t7, 0x04(t7)       ; Link age
    bnez  t7, @@return       ; Return if child
    nop
    la    t6, empty_dlist    ; Load empty display list if adult
@@return:
    sw    t6, 0x0004(v0)
    jr    ra
    lb    t7, 0x013F(s0)
