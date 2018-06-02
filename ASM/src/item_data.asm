;==================================================================================================
; Item data
;==================================================================================================

; Dungeon indexes, used with the dungeon item / small key tables in the save context
DEKU_ID    equ 0
DODONGO_ID equ 1
JABU_ID    equ 2
FOREST_ID  equ 3
FIRE_ID    equ 4
WATER_ID   equ 5
SPIRIT_ID  equ 6
SHADOW_ID  equ 7
BOTW_ID    equ 8
ICE_ID     equ 9
TOWER_ID   equ 10
GTG_ID     equ 11
FORT_ID    equ 12
CASTLE_ID  equ 13

.definelabel ITEM_TABLE_ROW_SIZE, 0x10

.macro Item_Row, base_item, action_id, graphic_id, text_id, object_id, upgrade_fn, effect_fn, effect_arg1, effect_arg2
  .byte     base_item   ; 0x00
  .byte     action_id   ; 0x01
  .byte     graphic_id  ; 0x02
  .byte     text_id     ; 0x03
  .halfword object_id   ; 0x04
  .byte     effect_arg1 ; 0x06
  .byte     effect_arg2 ; 0x07
  .word     effect_fn   ; 0x08
  .word     upgrade_fn  ; 0x0C
.endmacro

ITEM_ROW_BASE_ITEM   equ 0x00
ITEM_ROW_ACTION_ID   equ 0x01
ITEM_ROW_GRAPHIC_ID  equ 0x02
ITEM_ROW_TEXT_ID     equ 0x03
ITEM_ROW_OBJECT_ID   equ 0x04
ITEM_ROW_EFFECT_ARG1 equ 0x06
ITEM_ROW_EFFECT_ARG2 equ 0x07
ITEM_ROW_EFFECT_FN   equ 0x08
ITEM_ROW_UPGRADE_FN  equ 0x0C
ITEM_ROW_IS_EXTENDED equ 0x0C ; This offset is repurposed after the upgrades are resolved

; The "base item" mostly controls the sound effect made when you receive the item. It should be
; set to something that doesn't break NPCs.

ITEM_TABLE:
Item_Row -1, -1, -1, -1, -1, hookshot_upgrade,  no_effect, -1, -1 ; 0x80 = Progressive Hookshot
Item_Row -1, -1, -1, -1, -1, strength_upgrade,  no_effect, -1, -1 ; 0x81 = Progressive Strength
Item_Row -1, -1, -1, -1, -1, bomb_bag_upgrade,  no_effect, -1, -1 ; 0x82 = Progressive Bomb Bag
Item_Row -1, -1, -1, -1, -1, bow_upgrade,       no_effect, -1, -1 ; 0x83 = Progressive Bow
Item_Row -1, -1, -1, -1, -1, slingshot_upgrade, no_effect, -1, -1 ; 0x84 = Progressive Slingshot
Item_Row -1, -1, -1, -1, -1, wallet_upgrade,    no_effect, -1, -1 ; 0x85 = Progressive Wallet
Item_Row -1, -1, -1, -1, -1, scale_upgrade,     no_effect, -1, -1 ; 0x86 = Progressive Scale
Item_Row -1, -1, -1, -1, -1, nut_upgrade,       no_effect, -1, -1 ; 0x87 = Progressive Nut Capacity
Item_Row -1, -1, -1, -1, -1, stick_upgrade,     no_effect, -1, -1 ; 0x88 = Progressive Stick Capacity

Item_Row 0x53, 0xFF, 0x01, 0x43, 0x00C6, no_upgrade, give_bottle, 0x15, -1 ; 0x89 = Bottle with Red Potion
Item_Row 0x53, 0xFF, 0x01, 0x44, 0x00C6, no_upgrade, give_bottle, 0x16, -1 ; 0x8A = Bottle with Green Potion
Item_Row 0x53, 0xFF, 0x01, 0x45, 0x00C6, no_upgrade, give_bottle, 0x17, -1 ; 0x8B = Bottle with Blue Potion
Item_Row 0x53, 0xFF, 0x01, 0x46, 0x00C6, no_upgrade, give_bottle, 0x18, -1 ; 0x8C = Bottle with Fairy
Item_Row 0x53, 0xFF, 0x01, 0x47, 0x00C6, no_upgrade, give_bottle, 0x19, -1 ; 0x8D = Bottle with Fish
Item_Row 0x53, 0xFF, 0x01, 0x5D, 0x00C6, no_upgrade, give_bottle, 0x1C, -1 ; 0x8E = Bottle with Blue Fire
Item_Row 0x53, 0xFF, 0x01, 0x7A, 0x00C6, no_upgrade, give_bottle, 0x1D, -1 ; 0x8F = Bottle with Bugs
Item_Row 0x53, 0xFF, 0x01, 0xF9, 0x00C6, no_upgrade, give_bottle, 0x1E, -1 ; 0x90 = Bottle with Big Poe
Item_Row 0x53, 0xFF, 0x01, 0x97, 0x00C6, no_upgrade, give_bottle, 0x20, -1 ; 0x91 = Bottle with Poe

Item_Row 0x53, 0xFF, 0x0A, 0xC7, 0x00B9, no_upgrade, give_dungeon_item, 0x01, FOREST_ID  ; 0x92 = Forest Temple Boss Key
Item_Row 0x53, 0xFF, 0x0A, 0xC7, 0x00B9, no_upgrade, give_dungeon_item, 0x01, FIRE_ID    ; 0x93 = Fire Temple Boss Key
Item_Row 0x53, 0xFF, 0x0A, 0xC7, 0x00B9, no_upgrade, give_dungeon_item, 0x01, WATER_ID   ; 0x94 = Water Temple Boss Key
Item_Row 0x53, 0xFF, 0x0A, 0xC7, 0x00B9, no_upgrade, give_dungeon_item, 0x01, SPIRIT_ID  ; 0x95 = Spirit Temple Boss Key
Item_Row 0x53, 0xFF, 0x0A, 0xC7, 0x00B9, no_upgrade, give_dungeon_item, 0x01, SHADOW_ID  ; 0x96 = Shadow Temple Boss Key
Item_Row 0x53, 0xFF, 0x0A, 0xC7, 0x00B9, no_upgrade, give_dungeon_item, 0x01, CASTLE_ID  ; 0x97 = Ganon's Castle Boss Key

Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, DEKU_ID    ; 0x98 = Deku Tree Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, DODONGO_ID ; 0x99 = Dodongo's Cavern Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, JABU_ID    ; 0x9A = Jabu Jabu Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, FOREST_ID  ; 0x9B = Forest Temple Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, FIRE_ID    ; 0x9C = Fire Temple Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, WATER_ID   ; 0x9D = Water Temple Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, SPIRIT_ID  ; 0x9E = Spirit Temple Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, SHADOW_ID  ; 0x9F = Shadow Temple Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, BOTW_ID    ; 0xA0 = Bottom of the Well Compass
Item_Row 0x53, 0xFF, 0x0B, 0x67, 0x00B8, no_upgrade, give_dungeon_item, 0x02, ICE_ID     ; 0xA1 = Ice Cavern Compass

Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, DEKU_ID    ; 0xA2 = Deku Tree Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, DODONGO_ID ; 0xA3 = Dodongo's Cavern Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, JABU_ID    ; 0xA4 = Jabu Jabu Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, FOREST_ID  ; 0xA5 = Forest Temple Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, FIRE_ID    ; 0xA6 = Fire Temple Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, WATER_ID   ; 0xA7 = Water Temple Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, SPIRIT_ID  ; 0xA8 = Spirit Temple Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, SHADOW_ID  ; 0xA9 = Shadow Temple Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, BOTW_ID    ; 0xAA = Bottom of the Well Map
Item_Row 0x53, 0xFF, 0x1C, 0x66, 0x00C8, no_upgrade, give_dungeon_item, 0x04, ICE_ID     ; 0xAB = Ice Cavern Map

Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, FOREST_ID, -1 ; 0xAC = Forest Temple Small Key
Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, FIRE_ID,   -1 ; 0xAD = Fire Temple Small Key
Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, WATER_ID,  -1 ; 0xAE = Water Temple Small Key
Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, SPIRIT_ID, -1 ; 0xAF = Spirit Temple Small Key
Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, SHADOW_ID, -1 ; 0xB0 = Shadow Temple Small Key
Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, BOTW_ID,   -1 ; 0xB1 = Bottom of the Well Small Key
Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, GTG_ID,    -1 ; 0xB2 = Gerudo Training Small Key
Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, FORT_ID,   -1 ; 0xB3 = Gerudo Fortress Small Key
Item_Row 0x53, 0xFF, 0xFE, 0x60, 0x00AA, no_upgrade, give_small_key, CASTLE_ID, -1 ; 0xB4 = Ganon's Castle Small Key

Item_Row 0x53, 0x3D, 0x43, 0x0C, 0x00F8, no_upgrade, give_biggoron_sword, -1, -1 ; 0xB5 = Biggoron Sword

Item_Row 0x4D, 0x83, 0x09, 0x55, 0x00B7, no_upgrade,      no_effect, -1, -1 ; 0xB6 = Recovery Heart
Item_Row 0x53, 0x92, 0xDB, 0xE6, 0x00D8, arrows_to_rupee, no_effect, -1, -1 ; 0xB7 = Arrows (5)
Item_Row 0x53, 0x93, 0xDA, 0xE6, 0x00D8, arrows_to_rupee, no_effect, -1, -1 ; 0xB8 = Arrows (10)
Item_Row 0x53, 0x94, 0xD9, 0xE6, 0x00D8, arrows_to_rupee, no_effect, -1, -1 ; 0xB9 = Arrows (30)
Item_Row 0x53, 0x8E, 0xE0, 0x32, 0x00CE, bombs_to_rupee,  no_effect, -1, -1 ; 0xBA = Bombs (5)
Item_Row 0x53, 0x8F, 0xE0, 0x32, 0x00CE, bombs_to_rupee,  no_effect, -1, -1 ; 0xBB = Bombs (10)
Item_Row 0x53, 0x90, 0xE0, 0x32, 0x00CE, bombs_to_rupee,  no_effect, -1, -1 ; 0xBC = Bombs (20)
Item_Row 0x53, 0x8C, 0xEE, 0x34, 0x00BB, no_upgrade,      no_effect, -1, -1 ; 0xBD = Deku Nuts (5)
Item_Row 0x53, 0x8D, 0xEE, 0x34, 0x00BB, no_upgrade,      no_effect, -1, -1 ; 0xBE = Deku Nuts (10)

Item_Row 0x4F, 0xFF, 0x13, 0xE9, 0x00BD, no_upgrade, give_defense, -1, -1 ; 0xBF = Double Defense
