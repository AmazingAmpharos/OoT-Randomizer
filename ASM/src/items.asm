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
    lh      a1, 0x0004 (a2)
    j       override_object
    nop

override_object_chest:
    lw      t9, 0x002C (sp)
    lh      a1, 0x0004 (t9)
    j       override_object
    nop

override_object:
    li      t2, EXTENDED_ITEM_DATA
    lw      t3, ITEM_ROW_IS_EXTENDED (t2)
    beqz    t3, @@return
    nop

    ; Override Object ID
    lhu     a1, ITEM_ROW_OBJECT_ID (t2)

@@return:
    ; Clear any pending special item, now that it's being received
    li      t2, PENDING_SPECIAL_ITEM
    sb      r0, 0x00 (t2)

    jr ra
    nop

;==================================================================================================

override_graphic:
    li      t0, EXTENDED_ITEM_DATA
    lw      t1, ITEM_ROW_IS_EXTENDED (t0)
    beqz    t1, @@return
    nop

    ; Override Graphic ID
    lb      v1, ITEM_ROW_GRAPHIC_ID (t0)

@@return:
    ; Displaced code
    abs     t0, v1
    sb      t0, 0x0852 (a0)
    jr      ra
    nop

;==================================================================================================

override_text:
    lbu     a1, 0x03 (v0) ; Displaced code

    li      t0, EXTENDED_ITEM_DATA
    lw      t1, ITEM_ROW_IS_EXTENDED (t0)
    beqz    t1, @@return
    nop

    ; Override Text ID
    lbu     a1, ITEM_ROW_TEXT_ID (t0)

@@return:
    jr      ra
    nop

;==================================================================================================

override_action:
    ; Displaced code
    lw      v0, 0x24 (sp)
    lbu     a1, 0x0000 (v0)

    li      t0, EXTENDED_ITEM_DATA
    lw      t1, ITEM_ROW_IS_EXTENDED (t0)
    beqz    t1, @@return
    nop

    ; Override Action ID
    lbu     a1, ITEM_ROW_ACTION_ID (t0)

    sw      a0, 0x00 (sp)
    sw      a1, 0x04 (sp)
    sw      a2, 0x08 (sp)
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    ; Run effect function
    li      a0, SAVE_CONTEXT
    lbu     a1, ITEM_ROW_EFFECT_ARG1 (t0)
    lbu     a2, ITEM_ROW_EFFECT_ARG2 (t0)
    lw      t1, ITEM_ROW_EFFECT_FN (t0)
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

    addiu   sp, sp, -0x20
    sw      v0, 0x10 (sp)
    sw      v1, 0x14 (sp)
    sw      ra, 0x18 (sp)

    jal     store_item_data
    nop

    lw      v0, 0x10 (sp)
    lw      v1, 0x14 (sp)
    lw      ra, 0x18 (sp)
    addiu   sp, sp, 0x20
    jr      ra
    nop

;==================================================================================================

store_item_data:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    ; Clear current item data
    li      t0, EXTENDED_ITEM_DATA
    sw      r0, 0x00 (t0)
    sw      r0, 0x04 (t0)
    sw      r0, 0x08 (t0)
    sw      r0, 0x0C (t0)

    li      t0, PLAYER_ACTOR
    lb      t1, 0x0424 (t0) ; t1 = item ID being received
    beqz    t1, @@return
    nop

    abs     a0, t1
    lw      a1, 0x0428 (t0) ; a1 = actor giving the item
    jal     lookup_override ; v0 = new item ID from override
    nop
    bltz    v0, @@return
    nop

    ori     a0, v0, 0
    jal     resolve_extended_item ; v0 = resolved item ID, v1 = ITEM_TABLE entry
    nop
    beqz    v1, @@update_player_actor
    nop

    ; Store extended item data
    li      t0, EXTENDED_ITEM_DATA
    lw      t1, 0x00 (v1)
    sw      t1, 0x00 (t0)
    lw      t1, 0x04 (v1)
    sw      t1, 0x04 (t0)
    lw      t1, 0x08 (v1)
    sw      t1, 0x08 (t0)
    ; Mark the extended item data as active
    li      t1, 1
    sw      t1, ITEM_ROW_IS_EXTENDED (t0)
    ; Load the base item to be stored back in the player actor
    lbu     v0, ITEM_ROW_BASE_ITEM (v1)

@@update_player_actor:
    li      t0, PLAYER_ACTOR
    lb      t1, 0x0424 (t0)
    bgez    t1, @@not_negative
    nop
    ; The input was negative (item is coming from a chest), so make the result negative
    subu    v0, r0, v0
@@not_negative:
    sb      v0, 0x0424 (t0)

@@return:
    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x18
    jr      ra
    nop

;==================================================================================================

lookup_override:
    ; a0 = item ID being received
    ; a1 = actor giving the item

    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    jal     get_override_search_key
    nop
    ori     a0, v0, 0
    jal     scan_override_table
    nop

    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x18
    jr      ra
    nop

;==================================================================================================

get_override_search_key:
    ; a0 = item ID being received
    ; a1 = actor giving the item

    ; Load the current scene number
    li      v0, GLOBAL_CONTEXT
    lhu     v0, 0xA4 (v0)

    li      t0, 0x00 ; t0 = override type
    ori     t1, a0, 0 ; t1 = override ID
    lhu     t2, 0x00 (a1) ; t2 = actor ID

    bne     t2, 0x000A, @@not_chest
    nop
    beq     v0, 0x10, @@not_chest ; Scene 0x10 = treasure chest game, use item-based override here
    nop
    li      t0, 0x01
    lhu     t1, 0x1C (a1)
    andi    t1, t1, 0x1F ; t1 = chest flag
@@not_chest:

    bne     t2, 0x0015, @@not_collectible
    nop
    li      t0, 0x02
    lbu     t1, 0x0141 (a1) ; t1 = collectible flag
@@not_collectible:

    ; Construct ID used to search the override table
    ; v0 = (scene << 16) | (override_type << 8) | override_id
    sll     v0, v0, 8
    or      v0, v0, t0
    sll     v0, v0, 8
    or      v0, v0, t1

    jr      ra
    nop

;==================================================================================================

scan_override_table:
    ; a0 = override search key

    li      v0, -1

    ; Look up override
    li      t0, (ITEM_OVERRIDES - 0x04)
@@lookup_loop:
    addiu   t0, t0, 0x04
    lw      t1, 0x00 (t0) ; t1 = override entry
    beqz    t1, @@return ; Reached end of override table
    nop
    srl     t2, t1, 8 ; t2 = override key
    bne     t2, a0, @@lookup_loop
    nop

    andi    v0, t1, 0xFF ; v0 = found item ID

@@return:
    jr      ra
    nop

;==================================================================================================

resolve_extended_item:
    ; a0 = input item ID

    addiu   sp, sp, -0x20
    sw      s0, 0x10 (sp)
    sw      s1, 0x14 (sp)
    sw      ra, 0x18 (sp)

    ori     v0, a0, 0 ; Return resolved item ID in v0

@@loop:
    ori     s0, v0, 0
    addiu   t0, s0, -0x80 ; t0 = index into extended ITEM_TABLE
    bltz    t0, @@not_extended ; Item IDs in range 0x00 - 0x7F are not extended
    nop
    ; Load table entry
    li      s1, ITEM_TABLE
    li      t1, ITEM_TABLE_ROW_SIZE
    mult    t0, t1
    mflo    t0
    addu    s1, s1, t0 ; s1 = pointer to table entry
    ; Check whether this item will upgrade into another item
    ; Conventions for upgrade functions:
    ; - They receive a pointer to the save context in a0
    ; - They receive their item ID in a1
    ; - They store their result in v0
    li      a0, SAVE_CONTEXT
    ori     a1, s0, 0
    lw      t0, ITEM_ROW_UPGRADE_FN (s1)
    jalr    t0 ; v0 = upgraded item ID
    nop
    ; If the upgrade function returned a new item ID, start resolution over again
    bne     v0, s0, @@loop
    nop

    ori     v1, s1, 0 ; Return pointer to ITEM_TABLE entry in v1
    b       @@return
    nop

@@not_extended:
    li      v1, 0

@@return:
    lw      s0, 0x10 (sp)
    lw      s1, 0x14 (sp)
    lw      ra, 0x18 (sp)
    addiu   sp, sp, 0x20
    jr      ra
    nop

;==================================================================================================
; Item upgrade functions
;==================================================================================================

no_upgrade:
    jr      ra
    ori     v0, a1, 0

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

arrows_to_rupee:
    lbu     t0, 0xA3 (a0) ; Load quiver from inventory
    andi    t0, t0, 0x03 ; Mask bits to isolate quiver

    beqz    t0, @@return
    li      v0, 0x4D ; Blue Rupee

    ori     v0, a1, 0

@@return:
    jr      ra
    nop

;==================================================================================================

bombs_to_rupee:
    lbu     t0, 0xA3 (a0) ; Load bomb bag from inventory
    andi    t0, t0, 0x18 ; Mask bits to isolate bomb bag

    beqz    t0, @@return
    li      v0, 0x4D ; Blue Rupee

    ori     v0, a1, 0

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
    ; a0 = save context
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

;==================================================================================================

give_defense:
    ; a0 = save context
    li      t0, 0x01
    sb      t0, 0x3D (a0) ; Set double defense flag
    lhu     t0, 0x2E (a0) ; Load health capacity (0x10 per heart container)
    srl     t0, t0, 4
    sb      t0, 0xCF (a0) ; Set number of hearts to display as double defense
    jr      ra
    nop
