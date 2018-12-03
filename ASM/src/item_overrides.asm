inventory_check:
    andi    a0, a0, 0xFF
    li      t0, SAVE_CONTEXT

    beq     a0, 0x8C, @@return ; Deku Nuts (5)
    lbu     v0, 0x75 (t0)

    beq     a0, 0x8D, @@return ; Deku Nuts (10)
    lbu     v0, 0x75 (t0)

    beq     a0, 0x00, @@return ; Deku Stick
    lbu     v0, 0x74 (t0)

    beq     a0, 0x8A, @@return ; Deku Sticks (5)
    lbu     v0, 0x74 (t0)

    beq     a0, 0x8B, @@return ; Deku Sticks (10)
    lbu     v0, 0x74 (t0)

    beq     a0, 0x58, @@return ; Deku Seeds (5)
    li      v0, 0x00

    beq     a0, 0x78, @@return ; Small Magic Jar
    li      v0, 0x00

    beq     a0, 0x79, @@return ; Large Magic Jar
    li      v0, 0x00

    li      v0, 0xFF

@@return:
    jr      ra
    nop

;==================================================================================================

override_object_npc:
    lw      a2, 0x0030 (sp)
    j       override_object
    lh      a1, 0x0004 (a2)

override_object_chest:
    lw      t9, 0x002C (sp)
    j       override_object
    lh      a1, 0x0004 (t9)

override_object:
    li      t2, active_item_row
    lw      t2, 0x00 (t2)
    beqz    t2, @@return
    nop

    ; Override Object ID
    li      a1, active_item_object_id
    lw      a1, 0x00 (a1)

@@return:
    jr      ra
    nop

;==================================================================================================

override_graphic:
    li      t0, active_item_row
    lw      t0, 0x00 (t0)
    beqz    t0, @@return
    nop

    ; Override Graphic ID
    li      v1, active_item_graphic_id
    lw      v1, 0x00 (v1)

@@return:
    ; Displaced code
    abs     t0, v1
    sb      t0, 0x0852 (a0)
    jr      ra
    nop

;==================================================================================================

override_text:
    lbu     a1, 0x03 (v0) ; Displaced code

    li      t0, active_item_row
    lw      t0, 0x00 (t0)
    beqz    t0, @@return
    nop

    ; Override Text ID
    li      a1, active_item_text_id
    lw      a1, 0x00 (a1)

@@return:
    jr      ra
    nop

;==================================================================================================

override_action:
    addiu   sp, sp, -0x18
    sw      s0, 0x10 (sp)
    sw      ra, 0x14 (sp)

    li      t0, OUTGOING_OVERRIDE
    lw      t0, 0x00 (t0)
    bnez    t0, @@return
    li      s0, 0x41 ; Outgoing co-op item, do nothing for this player

    li      t0, active_item_row
    lw      t0, 0x00 (t0)
    beqz    t0, @@return
    lbu     s0, 0x00 (v0) ; No active override, load non-override action ID

    ; Override Action ID
    li      t0, active_item_action_id
    lw      s0, 0x00 (t0)

    jal     call_effect_function
    move    a0, s0

@@return:
    jal     after_item_received
    nop

    move    a1, s0 ; Base game expects this value in a1

    lw      s0, 0x10 (sp)
    lw      ra, 0x14 (sp)
    jr      ra
    addiu   sp, sp, 0x18

;==================================================================================================

get_item_hook:
    addiu   sp, sp, -0x20
    sw      a3, 0x10 (sp)
    sw      v0, 0x14 (sp)
    sw      v1, 0x18 (sp)
    sw      ra, 0x1C (sp)

    ; a0 = actor giving item
    ; a2 = incoming item id
    jal     get_item
    move    a1, a3 ; a1 = player instance

    lw      a3, 0x10 (sp)
    lw      v0, 0x14 (sp)
    lw      v1, 0x18 (sp)
    lw      ra, 0x1C (sp)
    jr      ra
    addiu   sp, sp, 0x20
