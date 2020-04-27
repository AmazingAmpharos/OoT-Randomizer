;Set Links next action to falling off a ladder if a cutscene is playing and he is not climbing

prevent_ladder_softlock:
la      t0, PLAYER_ACTOR
lb      t1, 0x069D(t0)
li      t2, 0x03
bne     t1, t2, @@return
lw      t3, 0x0670(t0)
andi    t3, t3, 0x1000
sra     t3, t3, 0x0C
beqz    t3, @@return
li      t4, 0x8039AB68
sw      t4, 0x664(t0)

@@return:
jr      ra
nop