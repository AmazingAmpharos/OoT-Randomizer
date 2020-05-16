malon_goto_item:
    lb      t2, SONGS_AS_ITEMS
    beqz    t2, @@return   ;if songs as items is not on then return normally
    lw      t3, 0x138(a2)  ;overlay table entry
    lw      t3, 0x10(t3)   ;overlay address
    addiu   t1, t3, 0x0ADC ;item actionFunc offset
@@return:
    jr      ra
    sw      t1, 0x0180(a2)

;============================================

;if songs as items is not on, show song staff
malon_handle_staff:
    addiu   sp, sp, -0x18
    sw      ra, 0x14(sp)
    lb      t2, SONGS_AS_ITEMS
    bnez    t2, @@return
    nop
    jal     0x800DD400 ;show staff
@@return:
    lw      ra, 0x14(sp)
    jr      ra
    addiu   sp, sp, 0x18

;============================================

;displaced stuff to make room for saving ra
malon_ra_displaced:
    lui   at, 0x80
    lui   t8, 0x0001
    jr    ra
    lw    t6, 0x0670(v0)

;if song as items is on, dont wait for dialog state
malon_songs_as_items:
    lb      t2, SONGS_AS_ITEMS
    beqz    t2, @@return
    nop
    li      t8, 0x03 ;if songs as items is on, make t8 3 so it doesnt wait on dialog state
@@return:
    la      a3, SAVE_CONTEXT
    jr      ra
    addiu   at, r0, 0x0003 ;displaced

;if songs as items is on, give item and change dialog state. return
malon_check_give_item:
    lb      t2, SONGS_AS_ITEMS
    beqz    t2, @@return ;if songs as items is not on, reutrn
    nop
    jal     override_epona_song ;give item for songs as items
    nop
    la      t0, 0x801D8966 ;globalCtx->msgCtx.unk_E3EE 
    li      t1, 0x0004
    sh      t1, 0x00(t0)
    nop
@@return:
    lw      ra, 0x14(sp)
    jr      ra
    addiu   sp, sp, 0x18

;============================================

;for songs as items not on, handle resetting dialog state and flag
;after item is given, restore malon so she can talk again
malon_set_wait:
    addiu   sp, sp, -0x20
    sw      ra, 0x14(sp)
    sw      a0, 0x18(sp)
    la      t3, SAVE_CONTEXT
    lb      t4, 0xEDE(t3)
    andi    t4, t4, 0x01
    bnez    t4, @@item_done ;skip item stuff if flag is set
    lb      t2, SONGS_AS_ITEMS
    bnez    t2, @@return
    addiu   a0, a1, 0x20D8 ;msgCtx
    jal     0x800DD464     ;returns dialog state
    nop
    addiu   at, r0, 0x0008
    bne     v0, at, @@return
    la      t0, 0x801D8966 ;globalCtx->msgCtx.unk_E3EE 
    li      t1, 0x0004
    sh      t1, 0x00(t0)
    lb      t4, 0xEDE(t3)
    ori    t4, t4, 0x01
    sb      t4, 0xEDE(t3) ;set flag for learned song
    b       @@return
    nop
@@item_done:
    lw      a0, 0x18(sp)
    lw      t0, 0x138(a0)  ;overlay table entry
    lw      t0, 0x10(t0)   ;overlay address
    addiu   t1, t0, 0x0708 ;wait actionFunc offset
    sw      t1, 0x0180(a0) ;store to actionFunc
    sh      r0, 0x01D8(a0) ;reset malon so she can talk again

@@return:
    lw      ra, 0x14(sp)
    jr      ra
    addiu   sp, sp, 0x20