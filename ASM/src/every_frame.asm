before_game_state_update:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    ; Don't give pending item during cutscene. This can lead to a crash when giving an item
    ; during another item cutscene.
    li      t2, PLAYER_ACTOR
    lb      t0, 0x066C (t2)    ;link's state
    andi    t0, 0x20           ;cutscene
    bnez    t0, @@no_pending_item
    nop

    ; Don't give an item if link's camera is not being used
    ; If an item is given in this state then it will cause the
    ; Walking-While-Talking glitch.
    li      t2, GLOBAL_CONTEXT
    lw      t0, 0x0794 (t2)        ; Camera 2
    bnez    t0, @@no_pending_item  

    ; clear pending item index
    li      t1, PENDING_SPECIAL_ITEM_END
    li      t2, 0xFF
    sb      t2, 0x00 (t1)

    ; If there is a pending item, try to make the player instance receive it. If the player has
    ; control on this frame, they will receive the item. Otherwise nothing will happen, and
    ; we try again next frame.
    li      t1, PENDING_SPECIAL_ITEM 
    li      t2, -1
    li      t4, (PENDING_SPECIAL_ITEM_END - PENDING_SPECIAL_ITEM) ; max number of entries
@@loop:
    addi    t2, t2, 0x01
    beq     t2, t4, @@no_pending_item ; stop if end of list
    add     t3, t1, t2

    lb      t0, 0x00 (t3)
    beqz    t0, @@loop ; loop if index is empty
    nop

    ; Store index of pending item to be given
    li      t1, PENDING_SPECIAL_ITEM_END
    sb      t2, 0x00 (t1)

    ; Disable warping when there is a pending item. Currently this code is only used in places
    ; where warping is allowed, so warping can always be re-enabled after the item is received.
    li      t1, GLOBAL_CONTEXT + 0x104E4
    li      t2, 1
    sh      t2, 0x00 (t1)
    ; PLAYER_ACTOR+0x0424 holds the item to be received. +0x0428 holds a pointer to the actor
    ; giving the item. The game is not picky about this actor, it just needs to read a non-zero
    ; value at actor+0x0130, and it overwrites actor+0x0118. Construct a dummy actor in an usused
    ; memory area to satisfy these requirements.
    li      t1, DUMMY_ACTOR
    li      t2, 1
    sw      t2, 0x130 (t1)
    li      t2, PLAYER_ACTOR
    sb      t0, 0x0424 (t2)
    sw      t1, 0x0428 (t2)
    jal     store_item_data
    nop
@@no_pending_item:

    ; Displaced code
    lw      t9, 0x04 (s0)
    or      a0, s0, r0

    lw      ra, 0x10 (sp)
    jr      ra
    addiu   sp, sp, 0x18

after_game_state_update:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    jal     c_after_game_state_update
    nop

    ; Displaced code
    lui     t6, 0x8012
    lbu     t6, 0x1212 (t6)

    lw      ra, 0x10 (sp)
    jr      ra
    addiu   sp, sp, 0x18
