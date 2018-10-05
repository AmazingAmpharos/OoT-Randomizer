; a0 = char index into name
get_name_char:
   li    t0, PLAYER_NAME_ID
   lbu   t0, 0x00 (t0)

   bnez  t0, @@coop_player_name
   nop

   li    t0, SAVE_CONTEXT
   add   t0, t0, a0
   lbu   v0, 0x24 (t0)
   b     @@return
   nop

@@coop_player_name:
   sll   t0, t0, 3
   li    v0, PLAYER_NAMES
   add   t0, t0, v0
   add   t0, t0, a0
   lbu   v0, 0x00 (t0)

@@return:
   jr    ra
   nop


reset_player_name_id:
   ; displaced code
   lw    s6,48(sp)
   lw    s7,52(sp)
   lw    s8,56(sp)

   li    t0, PLAYER_NAME_ID
   sb    zero, 0x00 (t0)   

   jr    ra
   nop