lacs_condition_check:
    lw      t1, LACS_CONDITION
    li      t2, 1
    beq     t1, t2, @@medallions
    li      t2, 2
    beq     t1, t2, @@dungeons
    li      t2, 3
    beq     t1, t2, @@stones
    nop

@@vanilla:
    li      t3, 0x0018
    and     t4, v0, t3
    bne     t3, t4, @@return
    li      v1, 0
    b       @@return
    li      v1, 1

@@medallions:
    li      t3, 0x003F
    and     t4, v0, t3
    bne     t3, t4, @@return
    li      v1, 0
    b       @@return
    li      v1, 1

@@dungeons:
    lui     t3, 0x001C
    addiu   t3, t3, 0x003F
    and     t4, v0, t3
    bne     t3, t4, @@return
    li      v1, 0
    b       @@return
    li      v1, 1

@@stones:
    lui     t3, 0x001C
    and     t4, v0, t3
    bne     t3, t4, @@return
    li      v1, 0
    li      v1, 1

@@return:
    jr      ra
    nop
