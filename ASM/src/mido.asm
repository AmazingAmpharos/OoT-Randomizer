; ==================================================================================================
; Change flags used to spawn Mido outside Deku and inside his house as child.
; Now requires the flags for showing Mido a sword/shield as well as
; either Obtained Zelda's Letter or beating Deku Tree to move Mido to his house.
; As a result, the short scene when leaving Deku after beating Gohma is skipped.
; ==================================================================================================
.orga 0xE62948
    sw      a0, 0(sp)               ; sw      a0, 0(sp)
    lh      v0, 0x00A4(a1)          ; lh      v0, 0x00A4(a1)
    lui     v1, 0x8012              ; li      at, 0x0055
    li      at, 0x0055              ; lui     v1, 0x8012
    addiu   v1, v1, 0xA5D0          ; bne     v0, at, 0x00E62988
    lhu     t0, 0X0ED4(v1)          ; addiu   v1, v1, 0xA5D0
    andi    t1, t0, 0x0080          ; lhu     t6, 0x0ED6(v1)
    andi    t2, t0, 0x0010          ; andi    t7, t6, 0x1000
    lhu     t0, 0X0EDC(v1)          ; bnez    t7, 0x00E62988
    andi    t3, t0, 0x0001          ; nop
    or      t5, t1, t3              ; lhu     t8, 0X0EDC(v1)
    bne     v0, at, @@branch_2988   ; andi    t9, t8, 0x0001
    li      t6, 0x0010              ; bnez    t9, 0x00E62988
    beqz    t5, @@return            ; nop
    nop                             ; jr      ra
    beq     t2, t6, @@branch_2988   ; li      v0, 1
    nop                             ; lui     v1, 0x8012
@@return:
    jr      ra                      ; li      at, 0x0028
    li      v0, 1                   ; bne     v0, at, 0x00E629CC
@@branch_2988:
    li      at, 0x0028              ; addiu   v1, v1, 0xA5D0
    bne     v0, at, @@branch_29D0   ; lhu     t0, 0x0ED6(v1)
    li      at, 0x005B              ; andi    t1, t0, 0x1000
    beqz    t5, @@branch_29D0       ; bnezl   t1, 0x00E629BC
    nop                             ; lw      t4, 0x0004(v1)
    bne     t2, t6, @@branch_29D0   ; lhu     t2, 0x0EDC(v1)
    nop                             ; andi    t3, t2, 0x0001
    lw      t4, 0x0004(v1)          ; beqzl   t3, 0x00E629D0
    beqz    t4, @@branch_29D0       ; li      at, 0x005B
    nop                             ; lw      t4, 0x0004(v1)
    jr      ra                      ; beqzl   t4, 0x00E629D0
    li      v0, 1                   ; li      at, 0x005B
@@branch_29D0:
    bnel    v0, at, @@branch_29E4   ; jr      ra
    move    v0, zero                ; li      v0, 1
    jr      ra                      ; li      at, 0x005B
    li      v0, 1                   ; bnel    v0, at, 0x00E629E4
@@branch_29E4:
    jr      ra                      ; move    v0, zero
    nop                             ; jr      ra
    nop                             ; li      v0, 1
    nop                             ; move    v0, zero
    nop                             ; jr      ra
    nop                             ; nop
