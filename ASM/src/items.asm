;==================================================================================================
; Item code
;==================================================================================================

Override_Object_NPC:
LW a2, 0x0030 (sp)
LH a1, 0x0004 (a2)
J Override_Object
NOP

Override_Object_Chest:
LW t9, 0x002C (sp)
LH a1, 0x0004 (t9)
J Override_Object
NOP

Override_Object:

; Load extended Object ID
LI t2, CURRENT_ITEM_DATA
LHU t3, 0x04 (t2)

BEQ t3, 0xFFFF, @@return
NOP

; Override Object ID
ORI a1, t3, 0

@@return:
JR ra
NOP

;==================================================================================================

Override_Graphic:

; Load extended Graphic ID
LI t0, CURRENT_ITEM_DATA
LB t1, 0x02 (t0)

BEQ t1, -1, @@return
NOP

; Override Graphic ID
ORI v1, t1, 0

@@return:
; Displaced code
ABS t0, v1
SB t0, 0x0852 (a0)
JR ra
NOP

;==================================================================================================

Override_Text:

LBU a1, 0x03 (v0) ; Displaced code

; Load extended Text ID
LI t0, CURRENT_ITEM_DATA
LBU t1, 0x03 (t0)

BEQ t1, 0xFF, @@return
NOP

; Override Text ID
ORI a1, t1, 0

@@return:
JR ra
NOP

;==================================================================================================

Override_Action:

; Displaced code
LW v0, 0x24 (sp)
LBU a1, 0x0000 (v0)

; Load extended Action ID
LI t0, CURRENT_ITEM_DATA
LHU t1, 0x00 (t0)

BEQ t1, 0xFFFF, @@return
NOP

; Override Action ID
ORI a1, t1, 0

SW ra, -0x04 (sp)
SW a0, 0x00 (sp)
SW a1, 0x04 (sp)
SW a2, 0x08 (sp)
ADDIU sp, sp, -0x14

; Run effect function
; Conventions for effect functions:
; - They receive a pointer to the save context in a0
; - They receive their arguments in a1 and a2
LW t1, 0x08 (t0) ; t1 = effect function
LI a0, SAVE_CONTEXT
LBU a1, 0x06 (t0)
LBU a2, 0x07 (t0)
JALR t1
NOP

ADDIU sp, sp, 0x14
LW ra, -0x04 (sp)
LW a0, 0x00 (sp)
LW a1, 0x04 (sp)
LW a2, 0x08 (sp)

@@return:
JR ra
NOP

;==================================================================================================

Inventory_Fix:

LI t0, SAVE_CONTEXT
; v0 = item ID

; Take away tunics/shields that are about to be received, to avoid breaking NPCs who give them

BNE v0, 0x2C, @@not_goron_tunic
LB t1, 0x9C (t0)
ANDI t1, t1, 0xFD
SB t1, 0x9C (t0)
@@not_goron_tunic:

BNE v0, 0x2D, @@not_zora_tunic
LB t1, 0x9C (t0)
ANDI t1, t1, 0xFB
SB t1, 0x9C (t0)
@@not_zora_tunic:

BNE v0, 0x29, @@not_deku_shield
LB t1, 0x9D (t0)
ANDI t1, t1, 0xEF
SB t1, 0x9D (t0)
@@not_deku_shield:

BNE v0, 0x2A, @@not_hylian_shield
LB t1, 0x9D (t0)
ANDI t1, t1, 0xDF
SB t1, 0x9D (t0)
@@not_hylian_shield:

JR ra
ADDU a2, t7, t8 ; Displaced code

;==================================================================================================

Store_Item_Data:

SW ra, -0x04 (sp)
SW v0, -0x08 (sp)
SW s0, -0x0C (sp)
ADDIU sp, sp, -0x1C

SB a2, 0x0424 (a3) ; Displaced code
BEQZ a2, @@return
NOP

ABS s0, a2 ; s0 = item ID being received

; Clear current item data
LI t0, -1
LI t1, CURRENT_ITEM_DATA
SW t0, 0x00 (t1)
SW t0, 0x04 (t1)
SW t0, 0x08 (t1)

; Load the current scene number
LI t0, GLOBAL_CONTEXT
LHU t0, 0xA4 (t0)

; If this is a generic grotto, construct a virtual scene number
BNE t0, 0x3E, @@not_grotto
NOP
LI t0, SAVE_CONTEXT
LW t0, 0x1394 (t0) ; Grotto chest contents + flags 
ANDI t0, t0, 0x1F ; Isolate chest flags
ADDIU t0, t0, 0x70 ; Grotto virtual scene numbers will range from 0x70 to 0x8F
@@not_grotto:

; Construct ID used to search the override table
SLL t0, t0, 8
OR t0, t0, s0

; Look up override
LI t1, (ITEM_OVERRIDES - 0x04)
@@lookup_loop:
ADDIU t1, t1, 0x04
LHU t2, 0x00 (t1) ; t2 = ID column in table
BEQZ t2, @@not_extended ; Reached end of override table
NOP
BNE t2, t0, @@lookup_loop
NOP

LHU s0, 0x02 (t1) ; s0 = item ID found in ITEM_OVERRIDES
ORI v0, s0, 0

@@resolve_item:

ORI s0, v0, 0
ADDIU t0, s0, -0x80 ; t0 = index into extended ITEM_TABLE
BLTZ t0, @@not_extended ; Item IDs in range 0x00 - 0x7F are not extended
NOP

; Load ITEM_TABLE row
LI t1, ITEM_TABLE
SLL t0, t0, 4 ; t0 = offset into table = index * 16
ADDU t1, t1, t0 ; t1 = pointer to ITEM_TABLE row
; Check whether this item will upgrade into another item
; Conventions for upgrade functions:
; - They receive a pointer to the save context in a0
; - They receive their item ID in s0
; - They store their result in v0
LW t2, 0x0C (t1) ; t2 = upgrade function
LI a0, SAVE_CONTEXT
JALR t2
NOP
; If the upgrade function returned a new item ID, start resolution over again
BNE v0, s0, @@resolve_item 
NOP

; Store extended item data
LI t2, CURRENT_ITEM_DATA
LW t3, 0x00 (t1)
SW t3, 0x00 (t2)
LW t3, 0x04 (t1)
SW t3, 0x04 (t2)
LW t3, 0x08 (t1)
SW t3, 0x08 (t2)
B @@return
NOP

@@not_extended:
; For non-extended item IDs, put it back in the player instance and let the game handle it
BGEZ a2, @@not_negative
NOP
; The input was negative (item is coming from a chest), so make the result negative
SUBU s0, r0, s0
@@not_negative:
SB s0, 0x0424 (a3)

@@return:
ADDIU sp, sp, 0x1C
LW ra, -0x04 (sp)
LW v0, -0x08 (sp)
LW s0, -0x0C (sp)
JR ra
NOP

;==================================================================================================
; Item upgrade functions
;==================================================================================================

No_Upgrade:
JR ra
ORI v0, s0, 0

;==================================================================================================

Hookshot_Upgrade:

LBU t0, 0x7D (a0) ; Load hookshot from inventory

BEQ t0, 0xFF, @@return
LI v0, 0x08 ; Hookshot

LI v0, 0x09 ; Longshot

@@return:
JR ra
NOP

;==================================================================================================

Strength_Upgrade:

LBU t0, 0xA3 (a0) ; Load strength from inventory
ANDI t0, t0, 0xC0 ; Mask bits to isolate strength

BEQZ t0, @@return
LI v0, 0x54 ; Goron Bracelet

BEQ t0, 0x40, @@return
LI v0, 0x35 ; Silver Gauntlets

LI v0, 0x36 ; Gold Gauntlets

@@return:
JR ra
NOP

;==================================================================================================

Bomb_Bag_Upgrade:

LBU t0, 0xA3 (a0) ; Load bomb bag from inventory
ANDI t0, t0, 0x18 ; Mask bits to isolate bomb bag

BEQZ t0, @@return
LI v0, 0x32 ; Bomb Bag

BEQ t0, 0x08, @@return
LI v0, 0x33 ; Bigger Bomb Bag

LI v0, 0x34 ; Biggest Bomb Bag

@@return:
JR ra
NOP

;==================================================================================================

Bow_Upgrade:

LBU t0, 0xA3 (a0) ; Load quiver from inventory
ANDI t0, t0, 0x03 ; Mask bits to isolate quiver

BEQZ t0, @@return
LI v0, 0x04 ; Bow

BEQ t0, 0x01, @@return
LI v0, 0x30 ; Big Quiver

LI v0, 0x31 ; Biggest Quiver

@@return:
JR ra
NOP

;==================================================================================================

Slingshot_Upgrade:

LBU t0, 0xA2 (a0) ; Load bullet bag from inventory
ANDI t0, t0, 0xC0 ; Mask bits to isolate bullet bag

BEQZ t0, @@return
LI v0, 0x05 ; Slingshot

BEQ t0, 0x40, @@return
LI v0, 0x60 ; Bullet Bag (40)

LI v0, 0x7B ; Bullet Bag (50)

@@return:
JR ra
NOP

;==================================================================================================

Wallet_Upgrade:

LBU t0, 0xA2 (a0) ; Load wallet from inventory
ANDI t0, t0, 0x30 ; Mask bits to isolate wallet

BEQZ t0, @@return
LI v0, 0x45 ; Adult's Wallet

LI v0, 0x46 ; Giant's Wallet

@@return:
JR ra
NOP

;==================================================================================================

Scale_Upgrade:

LBU t0, 0xA2 (a0) ; Load scale from inventory
ANDI t0, t0, 0x06 ; # Mask bits to isolate scale

BEQZ t0, @@return
LI v0, 0x37 ; Silver Scale

LI v0, 0x38 ; Gold Scale

@@return:
JR ra
NOP

;==================================================================================================

Nut_Upgrade:

LBU t0, 0xA1 (a0) ; Load nut limit from inventory
ANDI t0, t0, 0x30 ; Mask bits to isolate nut limit

BEQZ t0, @@return
LI v0, 0x79 ; 30 Nuts

LI v0, 0x7A ; 40 Nuts

@@return:
JR ra
NOP

;==================================================================================================

Stick_Upgrade:

LBU t0, 0xA1 (a0) ; Load stick limit from inventory
ANDI t0, t0, 0x06 ; Mask bits to isolate stick limit

BEQZ t0, @@return
LI v0, 0x77 ; 20 Sticks

LI v0, 0x78 ; 30 Sticks

@@return:
JR ra
NOP

;==================================================================================================
; Item effect functions
;==================================================================================================

No_Effect:
JR ra
NOP

;==================================================================================================

Give_Biggoron_Sword:
LI t0, 0x01
SB t0, 0x3E (a0) ; Set flag to make the sword durable
JR ra
NOP

;==================================================================================================

Give_Bottle:
; a0 = save context
; a1 = item code to store
ADDIU t0, a0, 0x86 ; t0 = First bottle slot
LI t1, -1 ; t1 = Bottle slot offset

@@loop:
ADDIU t1, t1, 1
BGT t1, 3, @@return ; No free bottle slots
NOP

; Check whether slot is full
ADDU t2, t0, t1
LBU t3, 0x00 (t2)
BNE t3, 0xFF, @@loop
NOP

; Found an open slot
SB a1, 0x00 (t2)

@@return:
JR ra
NOP

;==================================================================================================

Give_Dungeon_Item:
; a0 = save context
; a1 = mask (0x01 = boss key, 0x02 = compass, 0x04 = map)
; a2 = dungeon index
ADDIU t0, a0, 0xA8
ADDU t0, t0, a2 ; t0 = address of this dungeon's items
LBU t1, 0x00 (t0)
OR t1, t1, a1
SB t1, 0x00 (t0)
JR ra
NOP

;==================================================================================================

Give_Small_Key:
; a0 = save context
; a1 = dungeon index
ADDIU t0, a0, 0xBC
ADDU t0, t0, a1 ; t0 = address of this dungeon's key count
LB t1, 0x00 (t0)
BGEZ t1, @not_negative
NOP
LI t1, 0x00
@not_negative:
ADDIU t1, t1, 1
SB t1, 0x00 (t0)
JR ra
NOP
