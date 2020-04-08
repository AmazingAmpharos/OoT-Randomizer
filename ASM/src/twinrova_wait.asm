START_TWINROVA_FIGHT:
.byte 0x00
.align 4

rova_check_pos:
    sw      s0, 0x3C(sp) ;displaced

    addiu   sp, sp, -0x10
    la      t1, START_TWINROVA_FIGHT
    lb      t2, 0x00(t1)
    bnez    t2, @@return
    nop     
    li      t3, 0x44610000 ;900.0f
    sw      t3, 0x28(a0)   ;rova y, put them in the ceiling
    lw      t3, 0x28(s2)   ;links height
    li      t4, 0x43700000 ;240.0f
    blt     t3, t4, @@return
    li      t5, 0x01
    sb      t5, 0x00(t1)
    li      a0, 0x1B
    sw      ra, 0x00(sp)
    jal     0x800CAA70     ;set background music
    nop
    lw      ra, 0x00(sp)

    @@return:
    jr      ra
    addiu   sp, sp, 0x10
    

twinrova_displaced:
    lw      s2, 0x1C44(s3)
    addiu   t6, r0, 0x03
    sb      t6, 0x05B0(s1)
    lbu     t7, 0x07AF(s3)
    mfc1    a2, f22
    mfc1    a3, f20
    jr      ra
    nop