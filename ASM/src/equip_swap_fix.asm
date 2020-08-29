equip_swap_stick:
    la    t2, SAVE_CONTEXT
    lw    t2, 0x04(t2) ; Link age
    beqz  t2, @@adult  ; Load empty display list if adult
    nop
    lui   t2, 0x0600
    b @@return
    addiu t2, t2, 0x6CC0
@@adult:
    la    t2, empty_dlist
@@return:
    jr    ra
    nop
