MINIGAME_SWORDLESS:
.byte 0x00
.align 4

;if the b button is blank, set a flag so that it can be restored when the game is finished
minigames_check_b:
    addiu   sp, sp, -0x20
    sw      t0, 0x14(sp)
    sw      t1, 0x18(sp)
    bne     t5, v1, @@return
    li      t0, 0x01
    la      t1, MINIGAME_SWORDLESS
    sb      t0, 0x00(t1) ;set flag

@@return:
    lw      t1, 0x18(sp)
    lw      t0, 0x14(sp)
    jr      ra
    addiu   sp, sp, 0x20

;if MINIGAME_SWORDLESS is set, set B to ITEM_NONE and unset flag
minigames_restore_b:
    addiu   sp, sp, -0x18
    sw      ra, 0x14(sp)
    la      t3, MINIGAME_SWORDLESS
    lb      t0, 0x00(t3)
    beqz    t0, @@skip   ;if flag is 0 dont change anything
    nop
    la      t2, SAVE_CONTEXT
    li      t1, 0xFF
    sb      t1, 0x68(t2) ;b button item
    sb      r0, 0x00(t3) ;clear flag
    b       @@return
    nop
@@skip:
    jal     0x8006FB50   ;Interface_LoadItemIcon1
    nop
@@return:
    lw      ra, 0x14(sp)
    jr      ra
    addiu   sp, sp, 0x18