every_frame:
    sw      a0, 0x68 (sp)
    sw      a1, 0x6C (sp)
    sw      a2, 0x70 (sp)
    sw      a3, 0x74 (sp)
    addiu   sp, sp, -0x18
    sw      v1, 0x10 (sp)
    sw      ra, 0x14 (sp)

    ; If there is a pending item, try to make the player instance receive it. If the player has
    ; control on this frame, they will receive the item. Otherwise nothing will happen, and
    ; we try again next frame.
    li      t0, PENDING_SPECIAL_ITEM
    lb      t0, 0x00 (t0)
    beqz    t0, @@no_pending_item
    nop
    ; PLAYER_ACTOR+0x0424 holds the item to be received. +0x0428 holds a pointer to the actor
    ; giving the item. The game is not picky about this actor, it just needs to read a non-zero
    ; value at actor+0x0130, and it overwrites actor+0x0118. Construct a dummy actor in an usused
    ; memory area to satisfy these requirements.
    li      t1, 0x80410000
    li      t2, 1
    sw      t2, 0x130 (t1)
    li      t2, PLAYER_ACTOR
    sb      t0, 0x0424 (t2)
    sw      t1, 0x0428 (t2)
    jal     store_item_data
    nop
@@no_pending_item:

    lw      v1, 0x10 (sp)
    lw      ra, 0x14 (sp)
    addiu   sp, sp, 0x18
    lw      a0, 0x68 (sp)
    lw      a1, 0x6C (sp)
    lw      a2, 0x70 (sp)
    lw      a3, 0x74 (sp)

    lh      t6, 0x13C4 (v1) ; Displaced code

    jr      ra
    nop
