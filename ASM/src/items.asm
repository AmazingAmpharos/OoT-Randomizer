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
    lh      a1, 0x0004 (a2)
    j       override_object
    nop

override_object_chest:
    lw      t9, 0x002C (sp)
    lh      a1, 0x0004 (t9)
    j       override_object
    nop

override_object:
    ; Load extended Object ID
    li      t2, CURRENT_ITEM_DATA
    lhu     t3, 0x04 (t2)
    beq     t3, 0xFFFF, @@return
    nop

    ; Override object ID
    ori     a1, t3, 0

@@return:
    ; Clear any pending special item, now that it's being received
    li      t3, PENDING_SPECIAL_ITEM
    sb      r0, 0x00 (t3)

    jr ra
    nop

;==================================================================================================

override_graphic:
    ; Load extended Graphic ID
    li      t0, CURRENT_ITEM_DATA
    lb      t1, 0x02 (t0)
    beq     t1, -1, @@return
    nop

    ; Override Graphic ID
    ori     v1, t1, 0

@@return:
    ; Displaced code
    abs     t0, v1
    sb      t0, 0x0852 (a0)
    jr      ra
    nop

;==================================================================================================

override_text:
    lbu     a1, 0x03 (v0) ; Displaced code

    ; Load extended Text ID
    li      t0, CURRENT_ITEM_DATA
    lbu     t1, 0x03 (t0)
    beq     t1, 0xFF, @@return
    nop

    ; Override Text ID
    ori     a1, t1, 0

@@return:
    jr      ra
    nop

;==================================================================================================

override_action:
    ; Displaced code
    lw      v0, 0x24 (sp)
    lbu     a1, 0x0000 (v0)

    ; Load extended Action ID
    li      t0, CURRENT_ITEM_DATA
    lhu     t1, 0x00 (t0)
    beq     t1, 0xFFFF, @@return
    nop

    ; Override Action ID
    ori     a1, t1, 0

    sw      a0, 0x00 (sp)
    sw      a1, 0x04 (sp)
    sw      a2, 0x08 (sp)
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    ; Run effect function
    ; Conventions for effect functions:
    ; - They receive a pointer to the save context in a0
    ; - They receive their arguments in a1 and a2
    lw      t1, 0x08 (t0) ; t1 = effect function
    li      a0, SAVE_CONTEXT
    lbu     a1, 0x06 (t0)
    lbu     a2, 0x07 (t0)
    jalr    t1
    nop

    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x18
    lw      a0, 0x00 (sp)
    lw      a1, 0x04 (sp)
    lw      a2, 0x08 (sp)

@@return:
    jr      ra
    nop

;==================================================================================================

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

;==================================================================================================

override_item_fairy_cutscene:
    ; a0 = global context
    ; a2 = fairy actor
    lw      t0, 0x1D2C (a0) ; Load switch flags
    li      t1, 1
    sll     t1, t1, 0x18
    and     v0, t0, t1 ; Isolate ZL switch
    beqz    v0, @@return
    nop

    lhu     t2, 0xA4 (a0) ; Load scene number
    bne     t2, 0x3D, @@return ; Use default behavior unless this is an item fairy
    nop

    lhu     t2, 0x02DC (a2) ; Load item fairy index
    li      t3, 1
    sllv    t3, t3, t2 ; t3 = fairy item mask
    li      t4, SAVE_CONTEXT
    lbu     t5, 0x0EF2 (t4) ; Load fairy item flags
    and     t6, t5, t3
    bnez    t6, @@return ; Use default behavior if the item is already obtained
    nop
    or      t5, t5, t3
    sb      t5, 0x0EF2 (t4) ; Mark fairy item as obtained

    nor     t1, t1, t1
    and     t0, t0, t1 ; Unset ZL switch
    sw      t0, 0x1D2C (a0)

    ; Load fairy item and mark it as pending
    li      t0, FAIRY_ITEMS
    addu    t0, t0, t2
    lb      t0, 0x00 (t0)
    li      t1, PENDING_SPECIAL_ITEM
    sb      t0, 0x00 (t1)

    li      v0, 0 ; Prevent fairy animation

@@return:
    jr      ra
    nop

;==================================================================================================

override_light_arrow_cutscene:
    li      t0, LIGHT_ARROW_ITEM
    lb      t0, 0x00 (t0)
    li      t1, PENDING_SPECIAL_ITEM
    sb      t0, 0x00 (t1)
    jr      ra
    nop

;==================================================================================================

store_item_data_hook:
    sb      a2, 0x0424 (a3) ; Displaced code

    addiu   sp, sp, -0x18
    sw      v0, 0x10 (sp)
    sw      ra, 0x14 (sp)

    jal     store_item_data
    nop

    lw      v0, 0x10 (sp)
    lw      ra, 0x14 (sp)
    addiu   sp, sp, 0x18
    jr      ra
    nop

;==================================================================================================

store_item_data:
    addiu   sp, sp, -0x28
    sw      s0, 0x10 (sp)
    sw      s1, 0x14 (sp)
    sw      s2, 0x18 (sp)
    sw      ra, 0x20 (sp)

    li      s1, PLAYER_ACTOR
    lb      t0, 0x0424 (s1)
    beqz    t0, @@return

    abs     s0, t0 ; s0 = item ID being received

    ; Clear current item data
    li      t0, -1
    li      t1, CURRENT_ITEM_DATA
    sw      t0, 0x00 (t1)
    sw      t0, 0x04 (t1)
    sw      t0, 0x08 (t1)

    ; Load the current scene number
    li      t0, GLOBAL_CONTEXT
    lhu     t0, 0xA4 (t0)

    ; If this is a generic grotto, construct a virtual scene number
    bne     t0, 0x3E, @@not_grotto
    nop
    li      t0, SAVE_CONTEXT
    lw      t0, 0x1394 (t0) ; Grotto chest contents + flags 
    andi    t0, t0, 0x1F ; Isolate chest flags
    addiu   t0, t0, 0x70 ; Grotto virtual scene numbers will range from 0x70 to 0x8F
@@not_grotto:

    ; Construct ID used to search the override table
    sll     t0, t0, 8
    or      t0, t0, s0

    ; Look up override
    li      t1, (ITEM_OVERRIDES - 0x04)
@@lookup_loop:
    addiu   t1, t1, 0x04
    lhu     t2, 0x00 (t1) ; t2 = ID column in table
    beqz    t2, @@not_extended ; Reached end of override table
    nop
    bne     t2, t0, @@lookup_loop
    nop

    lhu     s0, 0x02 (t1) ; s0 = item ID found in ITEM_OVERRIDES

    ori     v0, s0, 0
@@resolve_item:
    ori     s0, v0, 0
    addiu   t0, s0, -0x80 ; t0 = index into extended ITEM_TABLE
    bltz    t0, @@not_extended ; Item IDs in range 0x00 - 0x7F are not extended
    nop
    ; Load ITEM_TABLE row
    li      s2, ITEM_TABLE
    sll     t0, t0, 4 ; t0 = offset into table = index * 16
    addu    s2, s2, t0 ; s2 = pointer to ITEM_TABLE row
    ; Check whether this item will upgrade into another item
    ; Conventions for upgrade functions:
    ; - They receive a pointer to the save context in a0
    ; - They receive their item ID in s0
    ; - They store their result in v0
    lw      t0, 0x0C (s2) ; t0 = upgrade function
    li      a0, SAVE_CONTEXT
    jalr    t0
    nop
    ; If the upgrade function returned a new item ID, start resolution over again
    bne     v0, s0, @@resolve_item
    nop

    ; Store extended item data
    li      t2, CURRENT_ITEM_DATA
    lw      t3, 0x00 (s2)
    sw      t3, 0x00 (t2)
    lw      t3, 0x04 (s2)
    sw      t3, 0x04 (t2)
    lw      t3, 0x08 (s2)
    sw      t3, 0x08 (t2)
    b       @@return
    nop

@@not_extended:
    ; For non-extended item IDs, put it back in the player instance and let the game handle it
    lb      t0, 0x0424 (s1)
    bgez    t0, @@not_negative
    nop
    ; The input was negative (item is coming from a chest), so make the result negative
    subu    s0, r0, s0
@@not_negative:
    sb      s0, 0x0424 (s1)

@@return:
    lw      s0, 0x10 (sp)
    lw      s1, 0x14 (sp)
    lw      s2, 0x18 (sp)
    lw      ra, 0x20 (sp)
    addiu   sp, sp, 0x28
    jr      ra
    nop

;==================================================================================================
; Item upgrade functions
;==================================================================================================

no_upgrade:
    jr      ra
    ori     v0, s0, 0

;==================================================================================================

hookshot_upgrade:
    lbu     t0, 0x7D (a0) ; Load hookshot from inventory

    beq     t0, 0xFF, @@return
    li      v0, 0x08 ; Hookshot

    li      v0, 0x09 ; Longshot

@@return:
    jr      ra
    nop

;==================================================================================================

strength_upgrade:
    lbu     t0, 0xA3 (a0) ; Load strength from inventory
    andi    t0, t0, 0xC0 ; Mask bits to isolate strength

    beqz    t0, @@return
    li      v0, 0x54 ; Goron Bracelet

    beq     t0, 0x40, @@return
    li      v0, 0x35 ; Silver Gauntlets

    li      v0, 0x36 ; Gold Gauntlets

@@return:
    jr      ra
    nop

;==================================================================================================

bomb_bag_upgrade:
    lbu     t0, 0xA3 (a0) ; Load bomb bag from inventory
    andi    t0, t0, 0x18 ; Mask bits to isolate bomb bag

    beqz    t0, @@return
    li      v0, 0x32 ; Bomb Bag

    beq     t0, 0x08, @@return
    li      v0, 0x33 ; Bigger Bomb Bag

    li      v0, 0x34 ; Biggest Bomb Bag

@@return:
    jr      ra
    nop

;==================================================================================================

bow_upgrade:
    lbu     t0, 0xA3 (a0) ; Load quiver from inventory
    andi    t0, t0, 0x03 ; Mask bits to isolate quiver

    beqz    t0, @@return
    li      v0, 0x04 ; Bow

    beq     t0, 0x01, @@return
    li      v0, 0x30 ; Big Quiver

    li      v0, 0x31 ; Biggest Quiver

@@return:
    jr      ra
    nop

;==================================================================================================

slingshot_upgrade:
    lbu     t0, 0xA2 (a0) ; Load bullet bag from inventory
    andi    t0, t0, 0xC0 ; Mask bits to isolate bullet bag

    beqz    t0, @@return
    li      v0, 0x05 ; Slingshot

    beq     t0, 0x40, @@return
    li      v0, 0x60 ; Bullet Bag (40)

    li      v0, 0x7B ; Bullet Bag (50)

@@return:
    jr      ra
    nop

;==================================================================================================

wallet_upgrade:
    lbu     t0, 0xA2 (a0) ; Load wallet from inventory
    andi    t0, t0, 0x30 ; Mask bits to isolate wallet

    beqz    t0, @@return
    li      v0, 0x45 ; Adult's Wallet

    li      v0, 0x46 ; Giant's Wallet

@@return:
    jr      ra
    nop

;==================================================================================================

scale_upgrade:
    lbu     t0, 0xA2 (a0) ; Load scale from inventory
    andi    t0, t0, 0x06 ; # Mask bits to isolate scale

    beqz    t0, @@return
    li      v0, 0x37 ; Silver Scale

    li      v0, 0x38 ; Gold Scale

@@return:
    jr      ra
    nop

;==================================================================================================

nut_upgrade:
    lbu     t0, 0xA1 (a0) ; Load nut limit from inventory
    andi    t0, t0, 0x30 ; Mask bits to isolate nut limit

    beqz    t0, @@return
    li      v0, 0x79 ; 30 Nuts

    li      v0, 0x7A ; 40 Nuts

@@return:
    jr      ra
    nop

;==================================================================================================

stick_upgrade:
    lbu     t0, 0xA1 (a0) ; Load stick limit from inventory
    andi    t0, t0, 0x06 ; Mask bits to isolate stick limit

    beqz    t0, @@return
    li      v0, 0x77 ; 20 Sticks

    li      v0, 0x78 ; 30 Sticks

@@return:
    jr      ra
    nop

;==================================================================================================
; Item effect functions
;==================================================================================================

no_effect:
    jr      ra
    nop

;==================================================================================================

give_biggoron_sword:
    li      t0, 0x01
    sb      t0, 0x3E (a0) ; Set flag to make the sword durable
    jr      ra
    nop

;==================================================================================================

give_bottle:
    ; a0 = save context
    ; a1 = item code to store
    addiu   t0, a0, 0x86 ; t0 = First bottle slot
    li      t1, -1 ; t1 = Bottle slot offset

@@loop:
    addiu   t1, t1, 1
    bgt     t1, 3, @@return ; No free bottle slots
    nop

    ; Check whether slot is full
    addu    t2, t0, t1
    lbu     t3, 0x00 (t2)
    bne     t3, 0xFF, @@loop
    nop

    ; Found an open slot
    sb      a1, 0x00 (t2)

@@return:
    jr      ra
    nop

;==================================================================================================

give_dungeon_item:
    ; a0 = save context
    ; a1 = mask (0x01 = boss key, 0x02 = compass, 0x04 = map)
    ; a2 = dungeon index
    addiu   t0, a0, 0xA8
    addu    t0, t0, a2 ; t0 = address of this dungeon's items
    lbu     t1, 0x00 (t0)
    or      t1, t1, a1
    sb      t1, 0x00 (t0)
    jr      ra
    nop

;==================================================================================================

give_small_key:
    ; a0 = save context
    ; a1 = dungeon index
    addiu   t0, a0, 0xBC
    addu    t0, t0, a1 ; t0 = address of this dungeon's key count
    lb      t1, 0x00 (t0)
    bgez    t1, @not_negative
    nop
    li      t1, 0x00
@not_negative:
    addiu   t1, t1, 1
    sb      t1, 0x00 (t0)
    jr      ra
    nop
