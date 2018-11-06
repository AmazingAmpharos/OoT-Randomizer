override_great_fairy_cutscene:
    ; a0 = global context
    ; a2 = fairy actor
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    lw      t0, 0x1D2C (a0) ; t0 = switch flags
    li      t1, 1
    sll     t1, t1, 0x18 ; t1 = ZL switch flag
    and     v0, t0, t1
    beqz    v0, @@return ; Do nothing until ZL is played
    nop

    lhu     t2, 0x02DC (a2) ; Load fairy index
    li      t3, SAVE_CONTEXT

    lhu     t4, 0xA4 (a0) ; Load scene number
    beq     t4, 0x3D, @@item_fairy
    nop

    ; Handle upgrade fairies
    addu    t4, a0, t2
    lbu     t5, 0x1D28 (t4) ; t5 = chest flag for this fairy
    bnez    t5, @@return ; Use default behavior if the item is already obtained
    nop
    li      t5, 1
    sb      t5, 0x1D28 (t4) ; Mark item as obtained
    addiu   t2, t2, 3 ; t2 = index of the item in FAIRY_ITEMS
    b       @@give_item
    nop

@@item_fairy:
    li      t4, 1
    sllv    t4, t4, t2 ; t4 = fairy item mask
    lbu     t5, 0x0EF2 (t3) ; t5 = fairy item flags
    and     t6, t5, t4
    bnez    t6, @@return ; Use default behavior if the item is already obtained
    nop
    or      t6, t5, t4
    sb      t6, 0x0EF2 (t3) ; Mark item as obtained

@@give_item:
    ; Unset ZL switch
    nor     t1, t1, t1
    and     t0, t0, t1
    sw      t0, 0x1D2C (a0)

    ; Load fairy item and add it to the pending item queue
    li      t0, FAIRY_ITEMS
    addu    t0, t0, t2
    lb      a0, 0x00 (t0)
    jal     push_pending_item
    li      a1, 2

    li      v0, 0 ; Prevent fairy animation

@@return:
    lw      ra, 0x10 (sp)
    jr      ra
    addiu   sp, sp, 0x18

;==================================================================================================

override_light_arrow_cutscene:
    li      t0, LIGHT_ARROW_ITEM
    lb      a0, 0x00 (t0)
    j       push_pending_item
    li      a1, 3

;==================================================================================================

override_fairy_ocarina_cutscene:
    li      t0, FAIRY_OCARINA_ITEM
    lb      a0, 0x00 (t0)
    j       push_pending_item
    li      a1, 4

;==================================================================================================

; a3 = item ID
override_ocarina_songs:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    addi    a0, a3, -0x5A + 0x61
    jal     push_pending_item
    li      a1, 5

    li      v0, 0xFF

    lw      ra, 0x10 (sp)
    jr      ra
    addiu   sp, sp, 0x18

;==================================================================================================

override_requiem_song:
    addiu   sp, sp, -0x20
    sw      at, 0x10 (sp)
    sw      v1, 0x14 (sp)
    sw      ra, 0x18 (sp)

    li      a0, 0x64
    jal     push_pending_item
    li      a1, 5

    lw      at, 0x10 (sp)
    lw      v1, 0x14 (sp)
    lw      ra, 0x18 (sp)
    jr      ra
    addiu   sp, sp, 0x20

;==================================================================================================

override_epona_song:
    addiu   sp, sp, -0x20
    sw      a2, 0x10 (sp)
    sw      a3, 0x14 (sp)
    sw      ra, 0x18 (sp)

    lui     at, 0x8012
    addiu   at, at, 0xA5D0 ; v1 = 0x8012A5D0 # save context (sav)
    lb      t0, 0x0EDE (at) ; check learned song from malon flag
    ori     t0, t0, 0x01 ; t9 = "Invited to Sing With Child Malon"
    sb      t0, 0x0EDE (at)

    li      a0, 0x68
    jal     push_pending_item
    li      a1, 5

    lw      a2, 0x10 (sp)
    lw      a3, 0x14 (sp)
    lw      ra, 0x18 (sp)
    jr      ra
    addiu   sp, sp, 0x20

;==================================================================================================

override_suns_song:
    addiu   sp, sp, -0x18
    sw      v1, 0x10 (sp)
    sw      ra, 0x14 (sp)

    lui     at, 0x8012
    addiu   at, at, 0xA5D0 ; v1 = 0x8012A5D0 # save context (sav)
    lb      t0, 0x0EDE (at) ; learned song from sun's song
    ori     t0, t0, 0x04
    sb      t0, 0x0EDE (at)

    li      a0, 0x6A
    jal     push_pending_item
    li      a1, 5

    lw      v1, 0x10 (sp)
    lw      ra, 0x14 (sp)
    jr      ra
    addiu   sp, sp, 0x18

;==================================================================================================

override_song_of_time:
    addiu   sp, sp, -0x28
    sw      a0, 0x10 (sp)
    sw      v0, 0x14 (sp)
    sw      t7, 0x18 (sp)
    sw      ra, 0x20 (sp)

    li      a0, 0x6B
    jal     push_pending_item
    li      a1, 5

    li      a1, 3 ; Displaced code

    lw      a0, 0x10 (sp)
    lw      v0, 0x14 (sp)
    lw      t7, 0x18 (sp)
    lw      ra, 0x20 (sp)
    jr      ra
    addiu   sp, sp, 0x28

;==================================================================================================

override_saria_song_check:
    move    t7, v1
    lb      t4, 0x0EDF(t7)
    andi    t6, t4, 0x80
    beqz    t6, @@get_item
    li      v1, 5

    jr      ra
    li      v0, 2

@@get_item:
    jr      ra
    move    v0, v1

;==================================================================================================

set_saria_song_flag:
    lh      v0, 0xa4(t6)       ; v0 = scene
    li      t0, SAVE_CONTEXT
    lb      t1, 0x0EDF(t0)
    ori     t1, t1, 0x80
    sb      t1, 0x0EDF(t0)
    jr      ra
    nop

;==================================================================================================

; Injection for talking to the Altar in the Temple of Time
; Should set flag in save that it has been spoken to.
set_dungeon_knowledge:
    addiu   sp, sp, -0x10
    sw      ra, 0x04(sp)

    ; displaced instruction
    jal     0xD6218
    nop

    li      t4, SAVE_CONTEXT
    lh      t5, 0x0F2E(t4) ; flags
    lw      t8, 0x0004(t4) ; age

    beqz    t8, @@set_flag
    li      t6, 0x0001 ; adult bit
    li      t6, 0x0002 ; child bit

@@set_flag:
    or      t5, t5, t6
    sh      t5, 0x0F2E(t4) ; set the flag

    lw      ra, 0x04(sp)
    addiu   sp, sp, 0x10

    jr      ra
    nop
