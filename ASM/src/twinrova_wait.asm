START_TWINROVA_FIGHT:
.byte 0x00
.align 4

TWINROVA_MOVE_TIMER:
.byte 0x00
.align 4

rova_check_pos:
    sw      s0, 0x3C(sp) ;displaced

    addiu   sp, sp, -0x10
    la      t1, START_TWINROVA_FIGHT
    lb      t2, 0x00(t1)
    bnez    t2, @@return
    nop     
    li      t3, 0x42c80000 ;900.0f 0x44610000 0x42c80000
    ;sw      t3, 0x28(a0)   ;rova y, put them in the ceiling
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
    lb      a0, TWINROVA_MOVE_TIMER
    li      a1, 0xFF
    beq     a0, a1, @@skip_timer
    nop
    addiu   a0, a0, 0x1
    sb      a0, TWINROVA_MOVE_TIMER
@@skip_timer:
    lw      s2, 0x1C44(s3)
    addiu   t6, r0, 0x03
    sb      t6, 0x05B0(s1)
    lbu     t7, 0x07AF(s3)
    mfc1    a2, f22
    mfc1    a3, f20
    jr      ra
    nop

rova_move_down:
    addiu   sp, sp, -0x30
    sw      ra, 0x14(sp)
    sw      a0, 0x18(sp)
    sw      a1, 0x1C(sp)
    sw      a2, 0x20(sp)
    sw      a3, 0x24(sp)
    lb      a0, TWINROVA_MOVE_TIMER
    li      a1, 0xFF
    beqz    a0, @@return
    nop
    beq     a0, a1, @@return
    nop
    or      a0, s1, r0
    lh      a1, 0x1C(a0)   ;params
    beqz    a1, @@neg
    nop
    li      a2, 0x44160000 ;600
    b       @@store
    nop
@@neg:
    li      a2, 0xC4160000 ;-600
@@store:
    sw      a2, 0x24(a0)
    sw      r0, 0x2C(a0)
    addiu   a0, a0, 0x28   ;&y pos
    li      a1, 0x43C80000
    li      a2, 0x43960000
    li      a3, 0x447A0000
    ;jal     0x80064280     ;Math_SmoothScaleMaxF
    nop

@@return:
    lw      ra, 0x14(sp)
    lw      a0, 0x18(sp)
    lw      a1, 0x1C(sp)
    lw      a2, 0x20(sp)
    lw      a3, 0x24(sp)
    lw      s0, 0x13C(s1) ;displaced
    jr      ra
    addiu   sp, sp, 0x30

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
twinrova_set_action:
    la     t0, twinrova_rise
    jr     ra
    sw     t0, 0x13C(s0)

twinrova_rise:
    jr     ra
    nop