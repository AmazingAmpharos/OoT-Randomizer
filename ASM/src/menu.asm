item_menu_prevent_empty_equip_display:
    addu    s1, t6, t7 ; s1 = entry in usability table
    ; Fall through to item_menu_prevent_empty_equip
    ; (the required checks and register usage happen to be identical)
item_menu_prevent_empty_equip:
    ; t1 = item under cursor
    bne     t1, 0xFF, @@return
    lbu     v0, 0x00 (s1) ; Load from item usability table

    li      v0, 0xFF ; Prevent equip

@@return:
    jr      ra
    li      at, 9 ; Restore value expected by caller

item_menu_use_blank_description:
    ; 0x17A is an invalid texture index, used if item ID = 0xFF
    bne     v1, 0x17A, @@not_blank
    nop
    li      v1, 0x7A ; 0x7A = index of texture that we made blank
@@not_blank:

    ; Displaced code
    sll     t4, v1, 10
    jr      ra
    addu    a1, t4, t5
