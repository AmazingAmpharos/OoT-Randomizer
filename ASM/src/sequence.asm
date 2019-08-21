set_secondary_sequence_ram:
    addiu   t7, t6, 0x8124      ; 0x80128124 = secondary sequence pointer
    lui     t8, 0x8080          ; currently using very end of ram
    bne     t7, a3, @@bank      ; ensure setting secondary sequence address, otherwise check if setting seecondary sequence bank
    addiu   t9, t8, -0x3800     ; 3800 = maximum sequence size
    beq     r0, r0, @@return
    nop
@@bank:                         ; set secondary sequence audiobank ram
    addiu   t9, t9, -0x1720     ; 1720 = size of Ending Orchestra 2
@@return:
    sw      t9, 0x0020(a3)
    jr      ra
    lw      t6, 0x005C(sp)

set_opening_sequence_ram:
    lui     t6, 0x801C
    addiu   t7, t6, 0x1BD0      ; 0x801C1BD0 = opening sequence pointer
    bnel    t7, v0, @@continue  ; ensure opening sequence, otherwise continue
    nop
    addiu   a1, a1, -0x1000     ; subtract 0x1000 to point v0 to normal primary sequence
    addiu   a2, a2, 0x1000      ; increase an assumed length value by the 0x1000 now available
@@continue:
    j       0x800B39F4          ; jump to function that sets an audio pointer to a specified address
    nop
