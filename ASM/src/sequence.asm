.align 0x10
@secondary_audioseq_ram:
.area 0x3200, 0
.endarea

.align 0x10
@secondary_audiobank_ram:
.area 0x1720, 0
.endarea

set_primary_sequence_ram:
    addiu   t7, t6, 0x8124      
    li      at, 0x801C6C50      ; 0x801C6C50 = new primary AudioSeq end
    bne     t7, a3, @@bank      ; ensure setting primary AudioSeq pointer, otherwise set primary AudioBank
    addiu   t9, at, -0x3200     ; 3200 = maximum bgm sequence size
    beq     r0, r0, @@return
    nop
@@bank:
    addiu   t9, t9, -0x1720     ; 1720 = Ending Orchestra 2 AudioBank size
@@return:
    sw      t9, 0x0014(a3)
    jr      ra
    lw      t6, 0x005C(sp)

set_fanfare_sequence_ram:
    li      at, 0x80128054
    li      v0, 0x801C2330
    bne     at, a0, @@bank
    addiu   v0, v0, -0x1640         ; 1640 = maximum fanfare sequence size
    beq     r0, r0, @@return
    nop
@@bank:
    addiu   v0, v0, -0x1720
@@return:
    jr      ra
    or      v1, v0, r0

set_secondary_sequence_ram:
    addiu   t7, t6, 0x8124      
    bne     t7, a3, @@bank                  ; ensure setting secondary AudioSeq pointer
    nop
    beq     r0, r0, @@return
    la      at, @secondary_audioseq_ram
@@bank:
    la      at, @secondary_audiobank_ram    ; otherwise set secondary AudioBank
@@return:
    sw      at, 0x0020(a3)
    jr      ra
    lw      t6, 0x005C(sp)

force_sequence_type:
    li      at, 0x80128CC0
    bne     at, s4, @@check_if_primary
    nop
    beq     r0, r0, @@return
    addiu   a2, r0, 0x0001      ; force large fanfares to load as fanfares
@@check_if_primary:
    li      at, 0x80128B60
    bne     at, s4, @@return
    nop
    addu    a2, r0, r0          ; force small primary sequences to load as primary
@@return:
    jr      ra
    sw      a3, 0x005C(sp)
