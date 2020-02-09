CHAIN_HBA_REWARDS:
.byte 0x00
.align 4

handle_hba_rewards_chain:
    lw      t2, 0x138(a0)       ; pointer to actor overlay table entry
    lw      t2, 0x10(t2)        ; actor loaded ram address
    addiu   t6, t2, 0x1618      ; default routine to end the dialog (80A90718)

    lb      t0, CHAIN_HBA_REWARDS
    beqz    t0, @@return        ; use the default routine if rewards shouldn't be chained
    la      t1, SAVE_CONTEXT
    lhu     t0, 0x1406(t1)      ; current score
    slti    at, t0, 1500
    bnez    at, @@return        ; use the default routine if the score is < 1500
    lhu     t0, 0x29C(a0)
    andi    t0, t0, 0x0002
    bnez    t0, @@return        ; use the default routine if we just received the 2nd reward
    nop

    addiu   t6, t2, 0x14D0      ; routine to chain rewards and give the 2nd reward instantly (80A905D0)

@@return:
    jr      ra
    nop
