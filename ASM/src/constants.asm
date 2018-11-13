; Pointers to game state
.definelabel SAVE_CONTEXT,      0x8011A5D0
.definelabel GLOBAL_CONTEXT,    0x801C84A0
.definelabel SUBSCREEN_CONTEXT, 0x801D8C00
.definelabel PLAYER_ACTOR,      0x801DAA30
.definelabel GET_ITEMTABLE,     0x803A9E7E

; Extended memory map:
; Loaded code files   0x80400000
; ASM working memory  0x80480000
; C working memory    0x80500000

.definelabel C_HEAP,      0x80500000

; Delayed item flags
DELAYED_LIGHT_ARROWS     equ 0x01
DELAYED_FAIRY_OCARINA    equ 0x02
DELAYED_ITEM_FAIRIES     equ 0x10 ; 0x10 to 0x12
DELAYED_UPGRADE_FAIRIES  equ 0x13 ; 0x13 to 0x15
DELAYED_OCARINA_SONGS    equ 0x20 ; 0x20 to 0x2B
DELAYED_REQUIEM          equ 0x23
DELAYED_EPONAS_SONG      equ 0x27
DELAYED_SUNS_SONG        equ 0x29
DELAYED_SONG_OF_TIME     equ 0x2A
