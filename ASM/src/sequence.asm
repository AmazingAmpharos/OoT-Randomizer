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
    li      t9, 0x801C0C10      ; 0x801BF5D0 = new primary AudioSeq start
    bne     t7, a3, @@bank      ; ensure setting primary AudioSeq pointer, otherwise set primary AudioBank
    nop
    beq     r0, r0, @@return
    nop
@@bank:
    li      t9, 0x801C5530
@@return:
    sw      t9, 0x0014(a3)
    jr      ra
    lw      t6, 0x005C(sp)

set_fanfare_sequence_ram:
    li      at, 0x80128054
    li      v0, 0x801BF5D0
    bne     at, a0, @@bank
    nop
    beq     r0, r0, @@return
    nop
@@bank:
    li      v0, 0x801C3E10
@@return:
    jr      ra
    or      v1, v0, r0

set_secondary_sequence_ram:
    addiu   t7, t6, 0x8124
    bne     t7, a3, @@bank                  ; ensure setting secondary AudioSeq pointer
    nop
    la      at, @secondary_audioseq_ram
    beq     r0, r0, @@return
    nop
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
