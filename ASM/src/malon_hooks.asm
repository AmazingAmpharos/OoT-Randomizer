malon_give_item:
    addiu   sp, sp, -0x18
    sw      ra, 0x14(sp)
    addiu   a0, a1, 0x20D8 ;msgCtx
    jal     0x800DD464     ;returns dialog state
    nop
    addiu   at, r0, 0x0008
    bne     v0, at, @@return
    la      t0, 0x801D8966 ;globalCtx->msgCtx.unk_E3EE 
    li      t1, 0x0004
    sh      t1, 0x00(t0)

@@return:
    lw      ra, 0x14(sp)
    jr      ra
    addiu   sp, sp, 0x18

    
;    Item_Give(globalCtx, ITEM_SONG_STORMS); or override_eponas_song?
;    globalCtx->msgCtx.unk_E3EE = 4;
   