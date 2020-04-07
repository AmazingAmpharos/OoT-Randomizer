;move the call to 8038C110 to the beginning of the function guarded by a null check for the grabbed actor
;this is the exact fix they did in 1.1 to patch empty bomb

empty_bomb:
   ;displaced
   or      s1, a1, r0

   addiu   sp, sp, -0x10
   sw      ra, 0x04(sp)
   lw      t6, 0x039C(a0) ;link grabbed actor
   bnez    t6, @@return     ;return if null
   nop
   or      a0, a1, r0
   jal     0x8038B040     ;clear action parameter related things
   or      a1, s0, r0

@@return:
   lw     ra, 0x04(sp)
   jr     ra
   addiu  sp, sp, 0x10