;==================================================================================================
; Remove free Kokiri Sword
;==================================================================================================

; Child -> Adult: Don't save hard-coded 0x3B (Kokiri Sword) as child's B equip
; Replaces:
;   sb      a0, 0x0040 (v1)
.org 0xAE57A8 ; In memory: 0x8006F848
    nop

; Adult -> Child: Don't skip restoring child's B equip if 0xFF is the saved value
; Replaces:
;   addiu   v1, r0, 0x00FF
.org 0xAE58F4 ; In memory: 0x8006F994
    nop

; Child -> Adult: Save the child's B equip before it gets overwritten
; Replaces:
;   sb      t6, 0x0068 (t0)
;   lw      a0, 0x0030 (sp)
.org 0xAE5F74 ; In memory: 0x80070014
    jal     save_child_b_equip
    lw      a0, 0x0030 (sp)

; Prevent Kokiri Sword from being added to inventory on game load
; Replaces:
;   sh      t9, 0x009C (v0)
.org 0xBAED6C ; In memory: 0x803B2B6C
    nop

;==================================================================================================
; Extended items
;==================================================================================================

; Runs when storing the pending item to the player instance
; Replaces:
;   sb      a2, 0x0424 (a3)
;   sw      a0, 0x0428 (a3)
.org 0xA98C30 ; In memory: 0x80022CD0
    jal     store_item_data_hook
    sw      a0, 0x0428 (a3)

; Override object ID (NPCs)
; Replaces:
;   lw      a2, 0x0030 (sp)
;   or      a0, s0, r0
;   jal     ...
;   lh      a1, 0x0004 (a2)
.org 0xBDA0D8 ; In memory: 0x803950C8
    jal     override_object_npc
    or      a0, s0, r0
.skip 4
    nop

; Override object ID (Chests)
; Replaces:
;   lw      t9, 0x002C (sp)
;   or      a0, s0, r0
;   jal     ...
;   lh      a1, 0x0004 (t9)
.org 0xBDA264 ; In memory: 0x80395254
    jal     override_object_chest
    or      a0, s0, r0
.skip 4
    nop

; Override graphic ID
; Replaces:
;   bltz    v1, A
;   subu    t0, r0, v1
;   jr      ra
;   sb      v1, 0x0852 (a0)
; A:
;   sb      t0, 0x0852 (a0)
;   jr      ra
.org 0xBCECBC ; In memory: 0x80389CAC
    j       override_graphic
    nop
    nop
    nop
    nop
    nop

; Override text ID
; Replaces:
;   lbu     a1, 0x03 (v0)
;   sw      a3, 0x0028 (sp)
.org 0xBE9AC0 ; In memory: 0x803A4AB0
    jal     override_text
    sw      a3, 0x0028 (sp)

; Override action ID
; Replaces:
;   lw      v0, 0x0024 (sp)
;   lw      a0, 0x0028 (sp)
;   jal     0x8006FDCC
;   lbu     a1, 0x0000 (v0)
.org 0xBE9AD8 ; In memory: 0x803A4AC8
    jal     override_action
    lw      a0, 0x0028 (sp)
.skip 4
    nop

; Inventory fix
; Replaces:
;   addu    a2, t7, t8
;   sw      s0, 0x0118 (t9)
.org 0xBDA094 ; In memory: 0x80395084
    jal     inventory_fix
    sw      s0, 0x0118 (t9)

; Prevent Silver Gauntlets warp
; Replaces:
;   addiu   at, r0, 0x0035
.org 0xBE9BDC ; In memory: 0x803A4BCC
    addiu   at, r0, 0x8383 ; Make branch impossible

; Replace all generic grotto prizes with 20 bombs
.org 0xE9A550
.fill 8, 0x67

;==================================================================================================
; Special item sources
;==================================================================================================

; Replaces:
;   sw      r0, 0x0428 (s0)
;   sw      r0, 0x0118 (v1)
.org 0xBCDD6C ; In memory: 0x80388D5C
    jal     item_source_clear
    sw      r0, 0x0118 (v1)

; Replaces:
;   sw      r0, 0x0428 (s0)
;   sh      t0, 0x0426 (s0)
.org 0xBE5730 ; In memory: 0x803A0720
    jal     item_source_clear
    sh      t0, 0x0426 (s0)

;==================================================================================================
; Menu hacks
;==================================================================================================

; Make the "SOLD OUT" menu text blank
.org 0x8A9C00
.fill 0x400, 0

; Item Menu hooks:
;
; There are 4 removed checks for whether the cursor is allowed to move to an adjacent space,
; one for each cardinal direction.
;
; There are 4 hooks that override the item ID used to display the item description.
; One runs periodically (because the description flips between the item name and "< v > to Equip").
; The other three run immediately when the cursor moves.

; Left movement check
; Replaces:
;   beq     s4, t5, 0x8038F2B4
;   nop
.org 0xBB77B4 ; In memory: 0x8038F134
    nop
    nop

; Right movement check AND an immediate description update
; Replaces:
;   lbu     t4, 0x0074 (t9)
;   beq     s4, t4, 0x8038F2B4
;   nop
.org 0xBB7890 ; In memory: 0x8038F210
    jal     item_menu_description_id_immediate_1
    nop
    nop

; Immediate description update
; Replaces:
;   lbu     t6, 0x0074 (t5)
;   sh      t6, 0x009A (sp)
.org 0xBB7950 ; In memory: 0x8038F2D0
    jal     item_menu_description_id_immediate_2
    nop

; Upward movement check
; Replaces:
;   beq     s4, t4, 0x8038F598
;   nop
.org 0xBB7BA0 ; In memory: 0x8038F520
    nop
    nop

; Downward movement check
; Replaces:
;   beq     s4, t4, 0x8038F598
;   nop
.org 0xBB7BFC ; In memory: 0x8038F57C
    nop
    nop

; Immediate description update
; Replaces:
;   lbu     t7, 0x0074 (t6)
;   sh      t7, 0x009A (sp)
.org 0xBB7C3C ; In memory: 0x8038F5BC
    jal     item_menu_description_id_immediate_3
    nop

; Periodic description update
; Replaces:
;   lbu     t9, 0x0074 (t8)
;   sh      t9, 0x009A (sp)
.org 0xBB7C58 ; In memory: 0x8038F5D8
    jal     item_menu_description_id_periodic
    nop