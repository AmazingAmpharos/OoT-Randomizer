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
    li      t7, PLAYER_ACTOR
    lw      v0, 0x428 (t7)
    beqz    v0, @@check_flag
    nop
    lb      v0, 0x424 (t7)
    bgez    v0, @@return
    li      t7, 1

@@check_flag:
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
    li      t2, extended_item_row
    lw      t2, 0x00 (t2)
    beqz    t2, @@return
    nop

    ; Override Object ID
    li      a1, ext_object_id
    lw      a1, 0x00 (a1)

@@return:
    jr      ra
    nop

;==================================================================================================

override_graphic:
    li      t0, extended_item_row
    lw      t0, 0x00 (t0)
    beqz    t0, @@return
    nop

    ; Override Graphic ID
    li      v1, ext_graphic_id
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

    li      t0, extended_item_row
    lw      t0, 0x00 (t0)
    beqz    t0, @@return
    nop

    ; Override Text ID
    li      a1, ext_text_id
    lw      a1, 0x00 (a1)

@@return:
    jr      ra
    nop

;==================================================================================================

override_action:
    lbu     a1, 0x0000 (v0) ; Displaced code

    addiu   sp, sp, -0x18
    sw      a1, 0x10 (sp)
    sw      ra, 0x14 (sp)

    li      t0, extended_item_row
    lw      t0, 0x00 (t0)
    beqz    t0, @@return
    nop

    ; Override Action ID
    li      a1, ext_action_id
    lw      a1, 0x00 (a1)
    sw      a1, 0x10 (sp)

    jal     call_effect_function
    move    a0, t0

@@return:
    jal     item_received
    nop

    lw      a1, 0x10 (sp)
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
