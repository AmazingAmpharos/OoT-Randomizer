;==================================================================================================
; Remove free Kokiri Sword
;==================================================================================================

; Child -> Adult: Don't save hard-coded 0x3B (Kokiri Sword) as child's B equip
; Replaces:
;     SB a0, 0x0040 (v1)
.org 0xAE57A8 ; In memory: 0x8006F848
NOP

; Adult -> Child: Don't skip restoring child's B equip if 0xFF is the saved value
; Replaces:
;     ADDIU V1, R0, 0x00FF
.org 0xAE58F4 ; In memory: 0x8006F994
NOP

; Child -> Adult: Save the child's B equip before it gets overwritten
; Replaces:
;     SB t6, 0x0068 (t0)
;     LW a0, 0x0030 (sp)
.org 0xAE5F74 ; In memory: 0x80070014
JAL Save_Child_B_Equip
LW a0, 0x0030 (sp)

; Prevent Kokiri Sword from being added to inventory on game load
; Replaces:
;     SH t9, 0x009C (v0)
.org 0xBAED6C ; In memory: 0x803B2B6C
NOP

;==================================================================================================
; Item hacks
;==================================================================================================

; Runs when storing the pending item to the player instance
; Replaces:
;     SB a2, 0x0424 (a3)
;     SW a0, 0x0428 (a3)
.org 0xA98C30 ; In memory: 0x80022CD0
JAL Store_Item_Data
SW a0, 0x0428 (a3)

; Override object ID (NPCs)
; Replaces:
;     LW a2, 0x0030 (sp)
;     OR a0, s0, r0
;     JAL ...
;     LH a1, 0x0004 (a2)
.org 0xBDA0D8 ; In memory: 0x803950C8
JAL Override_Object_NPC
OR a0, s0, r0
.skip 4
NOP

; Override object ID (Chests)
; Replaces:
;     LW t9, 0x002C (sp)
;     OR a0, s0, r0
;     JAL ...
;     LH a1, 0x0004 (t9)
.org 0xBDA264 ; In memory: 0x80395254
JAL Override_Object_Chest
OR a0, s0, r0
.skip 4
NOP

; Override graphic ID
; Replaces:
;     BLTZ v1, A
;     SUBU t0, r0, v1
;     JR ra
;     SB v1, 0x0852 (a0)
;  A: SB t0, 0x0852 (a0)
;     JR ra
.org 0xBCECBC ; In memory: 0x80389CAC
J Override_Graphic
NOP
NOP
NOP
NOP
NOP

; Override text ID
; Replaces:
;     LBU a1, 0x03 (v0)
;     SW a3, 0x0028 (sp)
.org 0xBE9AC0 ; In memory: 0x803A4AB0
JAL Override_Text
SW a3, 0x0028 (sp)

; Override action ID
; Replaces:
;     LW v0, 0x0024 (sp)
;     LW a0, 0x0028 (sp)
;     JAL 0x8006FDCC
;     LBU a1, 0x0000 (v0)
.org 0xBE9AD8 ; In memory: 0x803A4AC8
JAL Override_Action
LW a0, 0x0028 (sp)
.skip 4
NOP

; Inventory fix
; Replaces:
;     ADDU A2, T7, T8
;     SW s0, 0x0118 (t9)
.org 0xBDA094 ; In memory: 0x80395084
JAL Inventory_Fix
SW s0, 0x0118 (t9)

; Prevent Silver Gauntlets warp
; Replaces:
;     ADDIU at, r0, 0x0035
.org 0xBE9BDC ; In memory: 0x803A4BCC
ADDIU at, r0, 0x8383 ; Make branch impossible

; Replace all generic grotto prizes with 20 bombs
.org 0xE9A550
.fill 8, 0x67

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
;   BEQ    S4, T5, 0x8038F2B4
;   NOP
.org 0xBB77B4 ; In memory: 0x8038F134
NOP
NOP

; Right movement check AND an immediate description update
; Replaces:
;   LBU    T4, 0x0074 (T9)
;   BEQ    S4, T4, 0x8038F2B4
;   NOP
.org 0xBB7890 ; In memory: 0x8038F210
JAL    ItemMenu_Description_ID_Immediate1
NOP
NOP

; Immediate description update
; Replaces:
;   LBU    T6, 0x0074 (T5)
;   SH     T6, 0x009A (SP)
.org 0xBB7950 ; In memory: 0x8038F2D0
JAL    ItemMenu_Description_ID_Immediate2
NOP

; Upward movement check
; Replaces:
;   BEQ    S4, T4, 0x8038F598
;   NOP
.org 0xBB7BA0 ; In memory: 0x8038F520
NOP
NOP

; Downward movement check
; Replaces:
;   BEQ    S4, T4, 0x8038F598
;   NOP
.org 0xBB7BFC ; In memory: 0x8038F57C
NOP
NOP

; Immediate description update
; Replaces:
;   LBU    T7, 0x0074 (T6)
;   SH     T7, 0x009A (SP)
.org 0xBB7C3C ; In memory: 0x8038F5BC
JAL    ItemMenu_Description_ID_Immediate3
NOP

; Periodic description update
; Replaces:
;   LBU    T9, 0x0074 (T8)
;   SH     T9, 0x009A (SP)
.org 0xBB7C58 ; In memory: 0x8038F5D8
JAL    ItemMenu_Description_ID_Periodic
NOP