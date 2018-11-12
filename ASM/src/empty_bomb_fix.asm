;when a bomb instance is unloading, write the correct value for "Held Item" to denote the bomb is no longer in hand
empty_bomb_fix:
   ;displaced
   lw a0, 0x001C($sp)
   
   addiu    sp, sp, -0x10
   sw       t0, 0x04(sp)
   sw       t1, 0x08(sp)
   li       t0, 0x0100FE00
   lui      t1, 0x801E
   sw       t0, 0xAB70(t1) ;save 0x0100FE00 to 801DAB70
   li       t0, 0x00
   sb       t0, 0xAB74(t1) ;store 0x00 to 801DAB74
   lw       t1, 0x08(sp)
   lw       t0, 0x04(sp)
   jr       ra
   addiu    sp, sp, 0x10
