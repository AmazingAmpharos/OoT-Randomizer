set_primary_sequence_ram:
    addiu   t7, t6, 0x8124      
    lui     t8, 0x801C      
    addiu   t6, t8, 0x6E60      ; 0x801C6E60 = new primary AudioSeq end
    bne     t7, a3, @@pbank     ; ensure setting primary AudioSeq pointer, otherwise set primary AudioBank
    addiu   t9, t6, -0x3200     ; 2800 = maximum bgm sequence size
    beq     r0, r0, @@preturn
    nop
@@pbank:
    addiu   t9, t9, -0x1720     
@@preturn:
    sw      t9, 0x0014(a3)
    jr      ra
    lw      t6, 0x005C(sp)

set_fanfare_sequence_ram:
    lui     t6, 0x8013
    addiu   t7, t6, 0x8054      ; 0x80128054 = fanfare AudioSeq pointer
    lui     t8, 0x801C
    addiu   v0, t8, 0x0CF0      ; 0x801C0CF0 = new fanfare AudioSeq start
    bne     t7, a0, @@fbank
    nop
    beq     r0, r0, @@freturn
    nop
@@fbank:
    lui     t6, 0x8013
    addiu   t7, t6, 0x8164      ; 0x80128164 = fanfare AudioBank pointer
    bne     t7, a0, @@freturn   ; for some reasons some rando seeds call this function when the opening starts
    nop
    addiu   v0, v0, -0x1720
@@freturn:
    jr      ra
    or      v1, v0, r0

set_secondary_sequence_ram:
    addiu   t7, t6, 0x8124      
    lui     t8, 0x8080      
    addiu   t6, t8, 0xFFF0       ; currently using very end of ram
    bne     t7, a3, @@sbank      ; ensure setting secondary AudioSeq pointer, otherwise set secondary AudioBank
    addiu   t9, t6, -0x3200      ; 3200 = maximum bgm sequence size
    beq     r0, r0, @@sreturn
    nop
@@sbank:
    addiu   t9, t9, -0x1720     
@@sreturn:
    sw      t9, 0x0020(a3)
    jr      ra
    lw      t6, 0x005C(sp)

force_sequence_type:
    lui     t9, 0x8013
    addiu   t8, t9, 0x8CC0
    bne     t8, s4, @@check_if_primary
    nop
    addiu   a2, r0, 0x0001      ; force large fanfares to load as fanfares
    beq     r0, r0, @@return
    nop
@@check_if_primary:             
    lui     t9, 0x8013
    addiu   t8, t9, 0x8B60
    bne     t8, s4, @@return
    nop
    addu   a2, r0, r0           ; force small primary sequences to load as primary
    nop
@@return:
    jr      ra
    sw      a3, 0x005C(sp)
