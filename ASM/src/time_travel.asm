before_time_travel:
    ; s0 = save context
    li      t0, TIME_TRAVEL_SAVED_EQUIPS

    ; B and C buttons
    lw      t1, 0x68 (s0)
    sw      t1, 0x00 (t0)
    ; C button indexes
    lw      t1, 0x6C (s0)
    sw      t1, 0x04 (t0)
    ; Equipment
    lhu     t1, 0x70 (s0)
    sh      t1, 0x08 (t0)
    ; Owned equipment
    lhu     t1, 0x9C (s0)
    sh      t1, 0x0A (t0)

    jr      ra
    lw      t6, 0x04 (s0) ; Displaced code

;==================================================================================================

after_time_travel:
    li      a0, TIME_TRAVEL_SAVED_EQUIPS
    li      a1, SAVE_CONTEXT
    lw      t0, 0x04 (a1) ; t2 = 1 if going forward in time, 0 if going back
    beqz    t0, @@going_back
    nop
    j       after_going_forward
    nop
@@going_back:
    j       after_going_back
    nop

;==================================================================================================

after_going_forward:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    ; Save child buttons
    lw      t0, 0x00 (a0)
    sw      t0, 0x40 (a1)
    lw      t0, 0x04 (a0)
    sw      t0, 0x44 (a1)
    ; Save child equipment
    lhu     t0, 0x08 (a0)
    sh      t0, 0x48 (a1)

    ; Unset swordless flag
    sb      r0, 0x0F33 (a1)

    ; Initialize adult equips, if going forward for the first time
    lbu     t0, 0x4A (a1) ; t0 = saved adult B
    bne     t0, 0xFF, @@no_init
    nop
    jal     initialize_adult
    nop
@@no_init:

    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x18
    jr      ra
    nop

;==================================================================================================

after_going_back:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    ; Restore child buttons
    lw      t0, 0x40 (a1)
    sw      t0, 0x68 (a1)
    lw      t0, 0x44 (a1)
    sw      t0, 0x6C (a1)
    ; Restore child equipment
    lhu     t0, 0x48 (a1)
    sh      t0, 0x70 (a1)
    ; Set swordless flag if needed
    lbu     t0, 0x68 (a1)
    bne     t0, 0xFF, @@not_swordless
    nop
    li      t0, 1
    sb      t0, 0x0F33 (a1)
@@not_swordless:

    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x18
    jr      ra
    nop

;==================================================================================================

initialize_adult:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    ; a0 = TIME_TRAVEL_SAVED_EQUIPS
    ; a1 = save context

    ; If we have mirror shield, equip it
    lhu     t0, 0x9C (a1)
    andi    t0, t0, 0x0040
    beqz    t0, @@no_mirror_shield
    nop
    lhu     t0, 0x70 (a1)
    andi    t0, t0, 0xFF0F
    ori     t0, t0, 0x0030
    sh      t0, 0x70 (a1)
@@no_mirror_shield:

    ; Try to preserve child C-button equips
    lbu     t0, 0x01 (a0)
    sb      t0, 0x69 (a1)
    lhu     t0, 0x02 (a0)
    sh      t0, 0x6A (a1)
    lw      t0, 0x04 (a0)
    sw      t0, 0x6C (a1)

    jal     init_adult_button
    li      a0, 0

    jal     init_adult_button
    li      a0, 1

    jal     init_adult_button
    li      a0, 2

    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x18
    jr      ra
    nop

;==================================================================================================

init_adult_button:
    ; a0 = C-button index
    ; a1 = save context
    addu    t0, a0, a1 ; t0 = save context (offset by button index)

    li      t1, ADULT_VALID_ITEMS
    lbu     t2, 0x6C (t0) ; t2 = inventory index of item on this button
    beq     t2, 0xFF, @@empty ; If the button is empty, try to initialize it
    nop
    addu    t1, t1, t2
    lbu     t1, 0x00 (t1)
    bnez    t1, @@return ; If the existing item is valid for adult, do nothing
    nop
@@empty:

    li      t1, (ADULT_INIT_ITEMS - 1)
@@loop:
    addiu   t1, t1, 1
    lbu     t2, 0x00 (t1) ; t2 = inventory index
    beqz    t2, @@set_empty ; Ran out out of eligible items
    nop
    addu    t3, a1, t2
    lbu     t3, 0x74 (t3) ; t3 = inventory contents
    beq     t3, 0xFF, @@loop ; Item not in inventory
    nop
    lbu     t4, 0x6C (a1)
    beq     t4, t2, @@loop ; Item already on C-left
    nop
    lbu     t4, 0x6D (a1)
    beq     t4, t2, @@loop ; Item already on C-down
    nop
    lbu     t4, 0x6E (a1)
    beq     t4, t2, @@loop ; Item already on C-right
    nop
    ; Valid item found, update the button
    sb      t3, 0x69 (t0)
    sb      t2, 0x6C (t0)
    b       @@return
    nop

@@set_empty:
    ; Ran out out of eligible items, leave the button empty
    li      t1, 0xFF
    sb      t1, 0x69 (t0)
    sb      t1, 0x6C (t0)

@@return:
    jr      ra
    nop

; Items that can populate empty adult C-buttons, by inventory index
ADULT_INIT_ITEMS:
.byte 0x07 ; Ocarina
.byte 0x09 ; Hookshot
.byte 0x0F ; Hammer
.byte 0x02 ; Bombs
.byte 0x03 ; Bow
.byte 0x01 ; Deku Nuts
.byte 0x0D ; Lens of Truth
.byte 0x0B ; Farore's Wind
.byte 0x00 ; null terminate
.align 4

ADULT_VALID_ITEMS:
.byte 0 ; Deku Sticks
.byte 1 ; Deku Nuts
.byte 1 ; Deku Bombs
.byte 1 ; Bow
.byte 1 ; Fire Arrows
.byte 1 ; Din's Fire

.byte 0 ; Slingshot
.byte 1 ; Ocarina
.byte 1 ; Bombchus
.byte 1 ; Hookshot
.byte 1 ; Ice Arrows
.byte 1 ; Farore's Wind

.byte 0 ; Boomerang
.byte 1 ; Lens of Truth
.byte 0 ; Magic Beans
.byte 1 ; Hammer
.byte 1 ; Light Arrows
.byte 1 ; Nayru's Love

.byte 1 ; Bottle 1
.byte 1 ; Bottle 2
.byte 1 ; Bottle 3
.byte 1 ; Bottle 4
.byte 1 ; Adult Trade Item
.byte 0 ; Child Trade Item
.align 4
