override_great_fairy_cutscene:
    ; a0 = global context
    ; a2 = fairy actor
    lw      t0, 0x1D2C (a0) ; t0 = switch flags
    li      t1, 1
    sll     t1, t1, 0x18 ; t1 = ZL switch flag
    and     v0, t0, t1
    beqz    v0, @@return ; Do nothing until ZL is played
    nop

    lhu     t2, 0x02DC (a2) ; Load fairy index
    li      t3, SAVE_CONTEXT

    lhu     t4, 0xA4 (a0) ; Load scene number
    beq     t4, 0x3D, @@item_fairy
    nop

    ; Handle upgrade fairies
    addu    t4, a0, t2
    lbu     t5, 0x1D28 (t4) ; t5 = chest flag for this fairy
    bnez    t5, @@return ; Use default behavior if the item is already obtained
    nop
    li      t5, 1
    sb      t5, 0x1D28 (t4) ; Mark item as obtained
    addiu   t2, t2, 3 ; t2 = index of the item in FAIRY_ITEMS
    b       @@give_item
    nop

@@item_fairy:
    li      t4, 1
    sllv    t4, t4, t2 ; t4 = fairy item mask
    lbu     t5, 0x0EF2 (t3) ; t5 = fairy item flags
    and     t6, t5, t4
    bnez    t6, @@return ; Use default behavior if the item is already obtained
    nop
    or      t6, t5, t4
    sb      t6, 0x0EF2 (t3) ; Mark item as obtained

@@give_item:
    ; Unset ZL switch
    nor     t1, t1, t1
    and     t0, t0, t1
    sw      t0, 0x1D2C (a0)

    ; Load fairy item and mark it as pending
    li      t0, FAIRY_ITEMS
    addu    t0, t0, t2
    lb      t0, 0x00 (t0)
    li      t1, PENDING_SPECIAL_ITEM
    sb      t0, 0x00 (t1)

    li      v0, 0 ; Prevent fairy animation

@@return:
    jr      ra
    nop

;==================================================================================================

override_light_arrow_cutscene:
    li      t0, LIGHT_ARROW_ITEM
    lb      t0, 0x00 (t0)
    li      t1, PENDING_SPECIAL_ITEM
    sb      t0, 0x00 (t1)
    jr      ra
    nop

override_fairy_ocarina_cutscene:
    li      t0, FAIRY_OCARINA_ITEM
    lb      t0, 0x00 (t0)
    li      t1, PENDING_SPECIAL_ITEM
    sb      t0, 0x00 (t1)
    jr      ra
    nop

