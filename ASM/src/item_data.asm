;==================================================================================================
; Item data
;==================================================================================================

; Dungeon indexes, used with the dungeon item / small key tables in the save context
.definelabel DEKU,    0
.definelabel DODONGO, 1
.definelabel JABU,    2
.definelabel FOREST,  3
.definelabel FIRE,    4
.definelabel WATER,   5
.definelabel SPIRIT,  6
.definelabel SHADOW,  7
.definelabel BOTW,    8
.definelabel TOWER,   10 
.definelabel GTG,     11
.definelabel FORT,    12
.definelabel CASTLE,  13

; Item rows are 12 bytes long
.macro Item_Row, action_id, graphic_id, text_id, object_id, upgrade_fn, effect_fn, effect_arg1, effect_arg2
  .dh action_id   ; 0x00
  .db graphic_id  ; 0x02
  .db text_id     ; 0x03
  .dh object_id   ; 0x04
  .dh upgrade_fn  ; 0x06 (lower 16 bits only)
  .dh effect_fn   ; 0x08 (lower 16 bits only)
  .db effect_arg1 ; 0x0A
  .db effect_arg2 ; 0x0B
.endmacro

ITEM_TABLE:
;          AAAA    GG    TT    OOOO
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Hookshot_Upgrade,  No_Effect, 0xFF, 0xFF ; 0x80 = Progressive Hookshot
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Strength_Upgrade,  No_Effect, 0xFF, 0xFF ; 0x81 = Progressive Strength
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Bomb_Bag_Upgrade,  No_Effect, 0xFF, 0xFF ; 0x82 = Progressive Bomb Bag
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Bow_Upgrade,       No_Effect, 0xFF, 0xFF ; 0x83 = Progressive Bow
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Slingshot_Upgrade, No_Effect, 0xFF, 0xFF ; 0x84 = Progressive Slingshot
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Wallet_Upgrade,    No_Effect, 0xFF, 0xFF ; 0x85 = Progressive Wallet
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Scale_Upgrade,     No_Effect, 0xFF, 0xFF ; 0x86 = Progressive Scale
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Nut_Upgrade,       No_Effect, 0xFF, 0xFF ; 0x87 = Progressive Nut Capacity
Item_Row 0xFFFF, 0xFF, 0xFF, 0xFFFF, Stick_Upgrade,     No_Effect, 0xFF, 0xFF ; 0x88 = Progressive Stick Capacity

Item_Row 0x00FF, 0x01, 0x43, 0x00C6, No_Upgrade, Give_Bottle, 0x15, 0xFF ; 0x89 = Bottle with Red Potion
Item_Row 0x00FF, 0x01, 0x44, 0x00C6, No_Upgrade, Give_Bottle, 0x16, 0xFF ; 0x8A = Bottle with Green Potion
Item_Row 0x00FF, 0x01, 0x45, 0x00C6, No_Upgrade, Give_Bottle, 0x17, 0xFF ; 0x8B = Bottle with Blue Potion
Item_Row 0x00FF, 0x01, 0x46, 0x00C6, No_Upgrade, Give_Bottle, 0x18, 0xFF ; 0x8C = Bottle with Fairy
Item_Row 0x00FF, 0x01, 0x47, 0x00C6, No_Upgrade, Give_Bottle, 0x19, 0xFF ; 0x8D = Bottle with Fish
Item_Row 0x00FF, 0x01, 0x5D, 0x00C6, No_Upgrade, Give_Bottle, 0x1C, 0xFF ; 0x8E = Bottle with Blue Fire
Item_Row 0x00FF, 0x01, 0x7A, 0x00C6, No_Upgrade, Give_Bottle, 0x1D, 0xFF ; 0x8F = Bottle with Bugs
Item_Row 0x00FF, 0x01, 0xF9, 0x00C6, No_Upgrade, Give_Bottle, 0x1E, 0xFF ; 0x90 = Bottle with Big Poe
Item_Row 0x00FF, 0x01, 0x97, 0x00C6, No_Upgrade, Give_Bottle, 0x20, 0xFF ; 0x91 = Bottle with Poe

Item_Row 0x00FF, 0x0A, 0xC7, 0x00B9, No_Upgrade, Give_Dungeon_Item, 0x01, FOREST  ; 0x92 = Forest Temple Boss Key
Item_Row 0x00FF, 0x0A, 0xC7, 0x00B9, No_Upgrade, Give_Dungeon_Item, 0x01, FIRE    ; 0x93 = Fire Temple Boss Key
Item_Row 0x00FF, 0x0A, 0xC7, 0x00B9, No_Upgrade, Give_Dungeon_Item, 0x01, WATER   ; 0x94 = Water Temple Boss Key
Item_Row 0x00FF, 0x0A, 0xC7, 0x00B9, No_Upgrade, Give_Dungeon_Item, 0x01, SPIRIT  ; 0x95 = Spirit Temple Boss Key
Item_Row 0x00FF, 0x0A, 0xC7, 0x00B9, No_Upgrade, Give_Dungeon_Item, 0x01, SHADOW  ; 0x96 = Shadow Temple Boss Key
Item_Row 0x00FF, 0x0A, 0xC7, 0x00B9, No_Upgrade, Give_Dungeon_Item, 0x01, CASTLE  ; 0x97 = Ganon's Tower Boss Key

Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, DEKU    ; 0x98 = Deku Tree Compass
Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, DODONGO ; 0x98 = Dodongo's Cavern Compass
Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, JABU    ; 0x9A = Jabu Jabu Compass
Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, FOREST  ; 0x9B = Forest Temple Compass
Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, FIRE    ; 0x9C = Fire Temple Compass
Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, WATER   ; 0x9D = Water Temple Compass
Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, SPIRIT  ; 0x9E = Spirit Temple Compass
Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, SHADOW  ; 0x9F = Shadow Temple Compass
Item_Row 0x00FF, 0x0B, 0x67, 0x00B8, No_Upgrade, Give_Dungeon_Item, 0x02, BOTW    ; 0xA0 = Bottom of the Well Compass

Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, DEKU    ; 0xA1 = Deku Tree Map
Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, DODONGO ; 0xA2 = Dodongo's Cavern Map
Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, JABU    ; 0xA3 = Jabu Jabu Map
Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, FOREST  ; 0xA4 = Forest Temple Map
Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, FIRE    ; 0xA5 = Fire Temple Map
Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, WATER   ; 0xA6 = Water Temple Map
Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, SPIRIT  ; 0xA7 = Spirit Temple Map
Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, SHADOW  ; 0xA8 = Shadow Temple Map
Item_Row 0x00FF, 0x1C, 0x66, 0x00C8, No_Upgrade, Give_Dungeon_Item, 0x04, BOTW    ; 0xA9 = Bottom of the Well Map

Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, FOREST, 0xFF ; 0xAA = Forest Temple Small Key
Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, FIRE,   0xFF ; 0xAB = Fire Temple Small Key
Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, WATER,  0xFF ; 0xAC = Water Temple Small Key
Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, SPIRIT, 0xFF ; 0xAD = Spirit Temple Small Key
Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, SHADOW, 0xFF ; 0xAE = Shadow Temple Small Key
Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, BOTW,   0xFF ; 0xAF = Bottom of the Well Small Key
Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, GTG,    0xFF ; 0xB0 = Gerudo Training Small Key
Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, FORT,   0xFF ; 0xB1 = Gerudo Fortress Small Key
Item_Row 0x00FF, 0xFE, 0x60, 0x00AA, No_Upgrade, Give_Small_Key, CASTLE, 0xFF ; 0xB2 = Ganon's Castle Small Key

Item_Row 0x003D, 0x43, 0x0C, 0x00F8, No_Upgrade, Give_Biggoron_Sword, 0xFF, 0xFF ; 0xB3 = Biggoron Sword
