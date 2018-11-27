easier_fishing:
    lw      t2, (SAVE_CONTEXT+4)
    bne     t2, r0, @@L_C24
    andi    t8, t3, 0x0001
    bne     t8, r0, @@return
    lui     t8, 0x4230
    lui     t8, 0x4250
    jr      ra
    nop

@@L_C24:
    bne     t8, r0, @@return
    lui     t8, 0x4210
    lui     t8, 0x4238
@@return:
    jr      ra
    nop