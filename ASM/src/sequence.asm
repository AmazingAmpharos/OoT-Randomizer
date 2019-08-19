set_secondary_sequence_ram:
    addiu   t6, t6, 0x8124      ; 0x80128124 = secondary sequence pointer
    bnel    t6, a3, @@return    ; ensure setting secondary sequence address, otherwise return
    nop
    lui     t7, 0x8080          ; currently using very end of ram
    addiu   t9, t7, 0xC780      ; 3800 = maximum sequence size, C780 = two's complement negative
@@return:
    sw      t9, 0x0020(a3)
    jr      ra
    lw      t6, 0x005C(sp)

set_opening_sequence_ram:
    lui     t6, 0x801C
    addiu   t7, t6, 0x1BD0      ; 0x801C1BD0 = opening sequence pointer
    bnel    t7, v0, @@continue  ; ensure opening sequence, otherwise continue
    nop
    addiu   a1, a1, 0xFC18      ; subtract 0x1000 to point v0 to normal primary sequence
    addiu   a2, a2, 0x1000      ; increase an assumed length value by the 0x1000 now available
@@continue:
    j       0x800B39F4          ; jump to function that sets an audio pointer to a specified address
    nop
