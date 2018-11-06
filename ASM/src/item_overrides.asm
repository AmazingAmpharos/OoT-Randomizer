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

; Set t7 to nonzero if warping should be prevented
can_warp:
    ; Prevent warp if an actor is trying to give an item
    li      v0, PLAYER_ACTOR
    lw      v0, 0x428 (v0)
    bnez    v0, @@return
    li      t7, 1

    lh      t7, 0x640C (s2) ; Load warp restriction flag from global context

@@return:
    ; Displaced code
    lhu     v0, 0x63F0 (s2)
    jr      ra
    slti    at, v0, 0x000F

;==================================================================================================

; a1 = pointer to the skulltula token actor

override_skulltula_token:
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
    addiu   sp, sp, -0x18
    sw      ra, 0x14 (sp)

    li      t2, item_is_extended
    lw      t2, 0x00 (t2)
    beqz    t2, @@return
    nop

    ; Override Object ID
    li      a1, ext_object_id
    lw      a1, 0x00 (a1)
    lhu     a1, 0x00 (a1)

@@return:
    sw      a1, 0x10 (sp)
    jal     item_received
    nop

    lw      a1, 0x10 (sp)
    lw      ra, 0x14 (sp)
    jr      ra
    addiu   sp, sp, 0x18

;==================================================================================================

override_graphic:
    li      t0, item_is_extended
    lw      t0, 0x00 (t0)
    beqz    t0, @@return
    nop

    ; Override Graphic ID
    li      v1, ext_graphic_id
    lw      v1, 0x00 (v1)
    lb      v1, 0x00 (v1)

@@return:
    ; Displaced code
    abs     t0, v1
    sb      t0, 0x0852 (a0)
    jr      ra
    nop

;==================================================================================================

override_text:
    lbu     a1, 0x03 (v0) ; Displaced code

    li      t0, item_is_extended
    lw      t0, 0x00 (t0)
    beqz    t0, @@return
    nop

    ; Override Text ID
    li      a1, ext_text_id
    lw      a1, 0x00 (a1)
    lbu     a1, 0x00 (a1)

@@return:
    jr      ra
    nop

;==================================================================================================

override_action:
    ; Displaced code
    lw      v0, 0x24 (sp)
    lbu     a1, 0x0000 (v0)

    li      t0, item_is_extended
    lw      t0, 0x00 (t0)
    beqz    t0, @@return

    ; Override Action ID
    li      a1, ext_action_id
    lw      a1, 0x00 (a1)
    lbu     a1, 0x00 (a1)

    addiu   sp, sp, -0x20
    sw      a0, 0x10 (sp)
    sw      a1, 0x14 (sp)
    sw      ra, 0x18 (sp)

    ; Run effect function
    li      a0, SAVE_CONTEXT
    li      a1, ext_effect_arg1
    lw      a1, 0x00 (a1)
    lbu     a1, 0x00 (a1)
    li      a2, ext_effect_arg2
    lw      a2, 0x00 (a2)
    lbu     a2, 0x00 (a2)
    li      t0, ext_effect
    lw      t0, 0x00 (t0)
    lw      t0, 0x00 (t0)
    jalr    t0
    nop

    lw      a0, 0x10 (sp)
    lw      a1, 0x14 (sp)
    lw      ra, 0x18 (sp)
    addiu   sp, sp, 0x20

@@return:
    jr      ra
    nop

;==================================================================================================

store_item_data_hook:
    sb      a2, 0x0424 (a3) ; Displaced code

    addiu   sp, sp, -0x20
    sw      a3, 0x10 (sp)
    sw      v0, 0x14 (sp)
    sw      v1, 0x18 (sp)
    sw      ra, 0x1C (sp)

    jal     store_item_data
    nop

    lw      a3, 0x10 (sp)
    lw      v0, 0x14 (sp)
    lw      v1, 0x18 (sp)
    lw      ra, 0x1C (sp)
    jr      ra
    addiu   sp, sp, 0x20
