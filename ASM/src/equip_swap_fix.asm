equip_swap_stick:
    la    t2, SAVE_CONTEXT
    lw    t2, 0x04(t2) ; Link age
    beqz  t2, @@adult  ; Load empty display list if adult
    nop
    lui   t2, 0x0600   ; Load child stick display list
    b     @@return
    addiu t2, t2, 0x6CC0
@@adult:
    la    t2, empty_dlist
@@return:
    jr    ra
    nop

equip_swap_mask:
    la    t7, SAVE_CONTEXT
    lw    t7, 0x04(t7) ; Link age
    beqz  t7, @@adult  ; Load empty display list if adult
    nop
    addu  t6, t6, t4   ; Load child mask display list
    b     @@return
    lw    t6, 0xB098(t6)
@@adult:
    la    t6, empty_dlist
@@return:
    jr    ra
    nop
