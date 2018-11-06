#include "extended_items.h"

#include "z64.h"

//=================================================================================================
// Upgrade Functions
//=================================================================================================

uint8_t no_upgrade(z64_file_t *save, uint8_t item_id) {
    return item_id;
}

uint8_t hookshot_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->items[Z64_SLOT_HOOKSHOT]) {
        case -1: return 0x08; // Hookshot
        default: return 0x09; // Longshot
    }
}

uint8_t strength_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->strength_upgrade) {
        case 0: return 0x54; // Goron Bracelet
        case 1: return 0x35; // Silver Gauntlets
        default: return 0x36; // Gold Gauntlets
    }
}

uint8_t bomb_bag_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->bomb_bag) {
        case 0: return 0x32; // Bomb Bag
        case 1: return 0x33; // Bigger Bomb Bag
        default: return 0x34; // Biggest Bomb Bag
    }
}

uint8_t bow_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->quiver) {
        case 0: return 0x04; // Bow
        case 1: return 0x30; // Big Quiver
        default: return 0x31; // Biggest Quiver
    }
}

uint8_t slingshot_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->bullet_bag) {
        case 0: return 0x05; // Slingshot
        case 1: return 0x60; // Bullet Bag (40)
        default: return 0x7B; // Bullet Bag (50)
    }
}

uint8_t wallet_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->wallet) {
        case 0: return 0x45; // Adult's Wallet
        case 1: return 0x46; // Giant's Wallet
        default: return item_id; // Tycoon's Wallet (unchanged)
    }
}

uint8_t scale_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->diving_upgrade) {
        case 0: return 0x37; // Silver Scale
        default: return 0x38; // Gold Scale
    }
}

uint8_t nut_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->nut_upgrade) {
        case 0: return 0x79; // 30 Nuts
        default: return 0x7A; // 40 Nuts
    }
}

uint8_t stick_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->stick_upgrade) {
        case 0: return 0x77; // 20 Sticks
        default: return 0x78; // 30 Sticks
    }
}

uint8_t magic_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->magic_capacity_set) {
        case 0: return 0xC0; // Single Magic
        default: return 0xC1; // Double Magic
    }
}

uint8_t bombchu_upgrade(z64_file_t *save, uint8_t item_id) {
    if (save->items[Z64_SLOT_BOMBCHU] == -1) {
        return 0x6B; // Bombchu 20 pack
    }
    if (save->ammo[8] <= 5) {
        return 0x03; // Bombchu 10 pack
    }
    return 0x6A; // Bombchu 5 pack
}

uint8_t ocarina_upgrade(z64_file_t *save, uint8_t item_id) {
    switch (save->items[Z64_SLOT_OCARINA]) {
        case -1: return item_id; // Fairy Ocarina (unchanged)
        default: return 0x0C; // Ocarina of Time
    }
}

uint8_t arrows_to_rupee(z64_file_t *save, uint8_t item_id) {
    return save->quiver ? item_id : 0x4D; // Blue Rupee
}

uint8_t bombs_to_rupee(z64_file_t *save, uint8_t item_id) {
    return save->bomb_bag ? item_id : 0x4D; // Blue Rupee
}

uint8_t seeds_to_rupee(z64_file_t *save, uint8_t item_id) {
    return save->bullet_bag ? item_id : 0x4D; // Blue Rupee
}

//=================================================================================================
// Effect Functions
//=================================================================================================

void no_effect(z64_file_t *save, int8_t arg1, int8_t arg2) {
}

void give_tycoon_wallet(z64_file_t *save, int8_t arg1, int8_t arg2) {
    save->wallet = 3;
}

void give_biggoron_sword(z64_file_t *save, int8_t arg1, int8_t arg2) {
    save->bgs_flag = 1; // Set flag to make the sword durable
}

void give_bottle(z64_file_t *save, int8_t bottle_item_id, int8_t arg2) {
    for (int i = Z64_SLOT_BOTTLE_1; i <= Z64_SLOT_BOTTLE_4; i++) {
        if (save->items[i] == -1) {
            save->items[i] = bottle_item_id;
            return;
        }
    }
}

void give_dungeon_item(z64_file_t *save, int8_t mask, int8_t dungeon_id) {
    save->dungeon_items[dungeon_id].items |= mask;
}

void give_small_key(z64_file_t *save, int8_t dungeon_id, int8_t arg2) {
    int8_t keys = save->dungeon_keys[dungeon_id];
    if (keys < 0) {
        keys = 0;
    }
    save->dungeon_keys[dungeon_id] = keys + 1;
}

void give_defense(z64_file_t *save, int8_t arg1, int8_t arg2) {
    save->double_defense = 1;
    save->defense_hearts = 20;
    save->refill_hearts = 20 * 16;
}

void give_magic(z64_file_t *save, int8_t arg1, int8_t arg2) {
    save->magic_capacity_set = 1; // Set meter level
    save->magic_acquired = 1; // Required for meter to persist on save load
    save->magic_meter_size = 0x30; // Set meter size
    save->magic = 0x30; // Fill meter
}

void double_magic(z64_file_t *save, int8_t arg1, int8_t arg2) {
    save->magic_capacity_set = 2; // Set meter level
    save->magic_acquired = 1; // Required for meter to persist on save load
    save->magic_capacity = 1; // Required for meter to persist on save load
    save->magic_meter_size = 0x60; // Set meter size
    save->magic = 0x60; // Fill meter
}

void give_fairy_ocarina(z64_file_t *save, int8_t arg1, int8_t arg2) {
    save->items[Z64_SLOT_OCARINA] = 0x07;
}

void give_song(z64_file_t *save, int8_t quest_bit, int8_t arg2) {
    save->quest_items |= 1 << quest_bit;
}

//=================================================================================================
// Item Table
//=================================================================================================

enum dungeon {
    DEKU_ID = 0,
    DODONGO_ID = 1,
    JABU_ID = 2,
    FOREST_ID = 3,
    FIRE_ID = 4,
    WATER_ID = 5,
    SPIRIT_ID = 6,
    SHADOW_ID = 7,
    BOTW_ID = 8,
    ICE_ID = 9,
    TOWER_ID = 10,
    GTG_ID = 11,
    FORT_ID = 12,
    CASTLE_ID = 13,
};

#define ITEM_ROW( \
        base_item_id_, action_id_, graphic_id_, text_id_, object_id_, \
        upgrade_, effect_, effect_arg1_, effect_arg2_) \
    { base_item_id_, action_id_, graphic_id_, text_id_, object_id_, \
      effect_arg1_, effect_arg2_, effect_, upgrade_ }

// The "base item" mostly controls the sound effect made when you receive the item. It should be
// set to something that doesn't break NPCs.

// Action ID 0x41 (give kokiri tunic) is used to indicate no action.

item_row_t item_table[] = {

ITEM_ROW(-1, -1, -1, -1, -1, hookshot_upgrade,  no_effect, -1, -1), // 0x80 = Progressive Hookshot
ITEM_ROW(-1, -1, -1, -1, -1, strength_upgrade,  no_effect, -1, -1), // 0x81 = Progressive Strength
ITEM_ROW(-1, -1, -1, -1, -1, bomb_bag_upgrade,  no_effect, -1, -1), // 0x82 = Progressive Bomb Bag
ITEM_ROW(-1, -1, -1, -1, -1, bow_upgrade,       no_effect, -1, -1), // 0x83 = Progressive Bow
ITEM_ROW(-1, -1, -1, -1, -1, slingshot_upgrade, no_effect, -1, -1), // 0x84 = Progressive Slingshot
ITEM_ROW(0x53, 0x41, 0x23, 0xF8, 0x00D1, wallet_upgrade, give_tycoon_wallet, -1, -1), // 0x85 = Progressive Wallet
ITEM_ROW(-1, -1, -1, -1, -1, scale_upgrade,     no_effect, -1, -1), // 0x86 = Progressive Scale
ITEM_ROW(-1, -1, -1, -1, -1, nut_upgrade,       no_effect, -1, -1), // 0x87 = Progressive Nut Capacity
ITEM_ROW(-1, -1, -1, -1, -1, stick_upgrade,     no_effect, -1, -1), // 0x88 = Progressive Stick Capacity

ITEM_ROW(0x53, 0x41, 0x38, 0x43, 0x00EB, no_upgrade, give_bottle, 0x15, -1), // 0x89 = Bottle with Red Potion
ITEM_ROW(0x53, 0x41, 0x37, 0x44, 0x00EB, no_upgrade, give_bottle, 0x16, -1), // 0x8A = Bottle with Green Potion
ITEM_ROW(0x53, 0x41, 0x39, 0x45, 0x00EB, no_upgrade, give_bottle, 0x17, -1), // 0x8B = Bottle with Blue Potion
ITEM_ROW(0x53, 0x41, 0x6B, 0x46, 0x0177, no_upgrade, give_bottle, 0x18, -1), // 0x8C = Bottle with Fairy
ITEM_ROW(0x53, 0x41, 0x3F, 0x47, 0x00F4, no_upgrade, give_bottle, 0x19, -1), // 0x8D = Bottle with Fish
ITEM_ROW(0x53, 0x41, 0x67, 0x5D, 0x0173, no_upgrade, give_bottle, 0x1C, -1), // 0x8E = Bottle with Blue Fire
ITEM_ROW(0x53, 0x41, 0x68, 0x7A, 0x0174, no_upgrade, give_bottle, 0x1D, -1), // 0x8F = Bottle with Bugs
ITEM_ROW(0x53, 0x41, 0x70, 0xF9, 0x0176, no_upgrade, give_bottle, 0x1E, -1), // 0x90 = Bottle with Big Poe
ITEM_ROW(0x53, 0x41, 0x6A, 0x97, 0x0176, no_upgrade, give_bottle, 0x20, -1), // 0x91 = Bottle with Poe

ITEM_ROW(0x53, 0x41, 0x0A, 0x06, 0x00B9, no_upgrade, give_dungeon_item, 0x01, FOREST_ID ), // 0x92 = Forest Temple Boss Key
ITEM_ROW(0x53, 0x41, 0x0A, 0x1C, 0x00B9, no_upgrade, give_dungeon_item, 0x01, FIRE_ID   ), // 0x93 = Fire Temple Boss Key
ITEM_ROW(0x53, 0x41, 0x0A, 0x1D, 0x00B9, no_upgrade, give_dungeon_item, 0x01, WATER_ID  ), // 0x94 = Water Temple Boss Key
ITEM_ROW(0x53, 0x41, 0x0A, 0x1E, 0x00B9, no_upgrade, give_dungeon_item, 0x01, SPIRIT_ID ), // 0x95 = Spirit Temple Boss Key
ITEM_ROW(0x53, 0x41, 0x0A, 0x2A, 0x00B9, no_upgrade, give_dungeon_item, 0x01, SHADOW_ID ), // 0x96 = Shadow Temple Boss Key
ITEM_ROW(0x53, 0x41, 0x0A, 0x61, 0x00B9, no_upgrade, give_dungeon_item, 0x01, TOWER_ID  ), // 0x97 = Ganon's Castle Boss Key

ITEM_ROW(0x4D, 0x41, 0xF5, 0x62, 0x00B8, no_upgrade, give_dungeon_item, 0x02, DEKU_ID   ), // 0x98 = Deku Tree Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0x63, 0x00B8, no_upgrade, give_dungeon_item, 0x02, DODONGO_ID), // 0x99 = Dodongo's Cavern Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0x64, 0x00B8, no_upgrade, give_dungeon_item, 0x02, JABU_ID   ), // 0x9A = Jabu Jabu Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0x65, 0x00B8, no_upgrade, give_dungeon_item, 0x02, FOREST_ID ), // 0x9B = Forest Temple Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0x7C, 0x00B8, no_upgrade, give_dungeon_item, 0x02, FIRE_ID   ), // 0x9C = Fire Temple Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0x7D, 0x00B8, no_upgrade, give_dungeon_item, 0x02, WATER_ID  ), // 0x9D = Water Temple Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0x7E, 0x00B8, no_upgrade, give_dungeon_item, 0x02, SPIRIT_ID ), // 0x9E = Spirit Temple Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0x7F, 0x00B8, no_upgrade, give_dungeon_item, 0x02, SHADOW_ID ), // 0x9F = Shadow Temple Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0xA2, 0x00B8, no_upgrade, give_dungeon_item, 0x02, BOTW_ID   ), // 0xA0 = Bottom of the Well Compass
ITEM_ROW(0x4D, 0x41, 0xF5, 0x87, 0x00B8, no_upgrade, give_dungeon_item, 0x02, ICE_ID    ), // 0xA1 = Ice Cavern Compass

ITEM_ROW(0x4D, 0x41, 0xE4, 0x88, 0x00C8, no_upgrade, give_dungeon_item, 0x04, DEKU_ID   ), // 0xA2 = Deku Tree Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0x89, 0x00C8, no_upgrade, give_dungeon_item, 0x04, DODONGO_ID), // 0xA3 = Dodongo's Cavern Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0x8A, 0x00C8, no_upgrade, give_dungeon_item, 0x04, JABU_ID   ), // 0xA4 = Jabu Jabu Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0x8B, 0x00C8, no_upgrade, give_dungeon_item, 0x04, FOREST_ID ), // 0xA5 = Forest Temple Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0x8C, 0x00C8, no_upgrade, give_dungeon_item, 0x04, FIRE_ID   ), // 0xA6 = Fire Temple Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0x8E, 0x00C8, no_upgrade, give_dungeon_item, 0x04, WATER_ID  ), // 0xA7 = Water Temple Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0x8F, 0x00C8, no_upgrade, give_dungeon_item, 0x04, SPIRIT_ID ), // 0xA8 = Spirit Temple Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0xA3, 0x00C8, no_upgrade, give_dungeon_item, 0x04, SHADOW_ID ), // 0xA9 = Shadow Temple Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0xA5, 0x00C8, no_upgrade, give_dungeon_item, 0x04, BOTW_ID   ), // 0xAA = Bottom of the Well Map
ITEM_ROW(0x4D, 0x41, 0xE4, 0x92, 0x00C8, no_upgrade, give_dungeon_item, 0x04, ICE_ID    ), // 0xAB = Ice Cavern Map

ITEM_ROW(0x53, 0x41, 0x02, 0x93, 0x00AA, no_upgrade, give_small_key, FOREST_ID, -1), // 0xAC = Forest Temple Small Key
ITEM_ROW(0x53, 0x41, 0x02, 0x94, 0x00AA, no_upgrade, give_small_key, FIRE_ID,   -1), // 0xAD = Fire Temple Small Key
ITEM_ROW(0x53, 0x41, 0x02, 0x95, 0x00AA, no_upgrade, give_small_key, WATER_ID,  -1), // 0xAE = Water Temple Small Key
ITEM_ROW(0x53, 0x41, 0x02, 0xA6, 0x00AA, no_upgrade, give_small_key, SPIRIT_ID, -1), // 0xAF = Spirit Temple Small Key
ITEM_ROW(0x53, 0x41, 0x02, 0xA9, 0x00AA, no_upgrade, give_small_key, SHADOW_ID, -1), // 0xB0 = Shadow Temple Small Key
ITEM_ROW(0x53, 0x41, 0x02, 0x9B, 0x00AA, no_upgrade, give_small_key, BOTW_ID,   -1), // 0xB1 = Bottom of the Well Small Key
ITEM_ROW(0x53, 0x41, 0x02, 0x9F, 0x00AA, no_upgrade, give_small_key, GTG_ID,    -1), // 0xB2 = Gerudo Training Small Key
ITEM_ROW(0x53, 0x41, 0x02, 0xA0, 0x00AA, no_upgrade, give_small_key, FORT_ID,   -1), // 0xB3 = Gerudo Fortress Small Key
ITEM_ROW(0x53, 0x41, 0x02, 0xA1, 0x00AA, no_upgrade, give_small_key, CASTLE_ID, -1), // 0xB4 = Ganon's Castle Small Key

ITEM_ROW(0x53, 0x3D, 0x43, 0x0C, 0x00F8, no_upgrade, give_biggoron_sword, -1, -1), // 0xB5 = Biggoron Sword

ITEM_ROW(0x4D, 0x83, 0xF7, 0x55, 0x00B7, no_upgrade,      no_effect, -1, -1), // 0xB6 = Recovery Heart
ITEM_ROW(0x4D, 0x92, 0xDB, 0xE6, 0x00D8, arrows_to_rupee, no_effect, -1, -1), // 0xB7 = Arrows (5),
ITEM_ROW(0x4D, 0x93, 0xDA, 0xE6, 0x00D8, arrows_to_rupee, no_effect, -1, -1), // 0xB8 = Arrows (10),
ITEM_ROW(0x4D, 0x94, 0xD9, 0xE6, 0x00D8, arrows_to_rupee, no_effect, -1, -1), // 0xB9 = Arrows (30),
ITEM_ROW(0x4D, 0x8E, 0xE0, 0x32, 0x00CE, bombs_to_rupee,  no_effect, -1, -1), // 0xBA = Bombs (5),
ITEM_ROW(0x4D, 0x8F, 0xE0, 0x32, 0x00CE, bombs_to_rupee,  no_effect, -1, -1), // 0xBB = Bombs (10),
ITEM_ROW(0x4D, 0x90, 0xE0, 0x32, 0x00CE, bombs_to_rupee,  no_effect, -1, -1), // 0xBC = Bombs (20),
ITEM_ROW(0x4D, 0x8C, 0xEE, 0x34, 0x00BB, no_upgrade,      no_effect, -1, -1), // 0xBD = Deku Nuts (5),
ITEM_ROW(0x4D, 0x8D, 0xEE, 0x34, 0x00BB, no_upgrade,      no_effect, -1, -1), // 0xBE = Deku Nuts (10),

ITEM_ROW(0x53, 0x41, 0x13, 0xE9, 0x00BD, no_upgrade,    give_defense, -1, -1), // 0xBF = Double Defense
ITEM_ROW(0x53, 0x41, 0x1E, 0xE4, 0x00CD, magic_upgrade, give_magic,   -1, -1), // 0xC0 = Progressive Magic Meter
ITEM_ROW(0x53, 0x41, 0x1F, 0xE8, 0x00CD, no_upgrade,    double_magic, -1, -1), // 0xC1 = Double Magic

ITEM_ROW(-1, -1, -1, -1, -1, bombchu_upgrade,  no_effect, -1, -1), // 0xC2 = Progressive Bombchus
ITEM_ROW(0x53, 0x41, 0x46, 0x4A, 0x010E, ocarina_upgrade,  give_fairy_ocarina, -1, -1), // 0xC3 = Progressive Ocarina

ITEM_ROW(0x53, 0x41, 0x03, 0xB0, 0x00B6, no_upgrade, give_song, 6, -1 ), // 0xC4 = Minuet of Forest
ITEM_ROW(0x53, 0x41, 0x04, 0xB1, 0x00B6, no_upgrade, give_song, 7, -1 ), // 0xC5 = Bolero of Fire
ITEM_ROW(0x53, 0x41, 0x05, 0xB2, 0x00B6, no_upgrade, give_song, 8, -1 ), // 0xC6 = Serenade of Water
ITEM_ROW(0x53, 0x41, 0x06, 0xB3, 0x00B6, no_upgrade, give_song, 9, -1 ), // 0xC7 = Requiem of Spirit
ITEM_ROW(0x53, 0x41, 0x07, 0xB6, 0x00B6, no_upgrade, give_song, 10, -1), // 0xC8 = Nocturn of Shadow
ITEM_ROW(0x53, 0x41, 0x08, 0xB7, 0x00B6, no_upgrade, give_song, 11, -1), // 0xC9 = Prelude of Light

ITEM_ROW(0x53, 0x41, 0x04, 0xB8, 0x00B6, no_upgrade, give_song, 12, -1), // 0xCA = Zelda's Lullaby
ITEM_ROW(0x53, 0x41, 0x06, 0xB9, 0x00B6, no_upgrade, give_song, 13, -1), // 0xCB = Epona's Song
ITEM_ROW(0x53, 0x41, 0x03, 0xBA, 0x00B6, no_upgrade, give_song, 14, -1), // 0xCC = Saria's Song
ITEM_ROW(0x53, 0x41, 0x08, 0xBB, 0x00B6, no_upgrade, give_song, 15, -1), // 0xCD = Sun's Song
ITEM_ROW(0x53, 0x41, 0x05, 0xBC, 0x00B6, no_upgrade, give_song, 16, -1), // 0xCE = Song of Time
ITEM_ROW(0x53, 0x41, 0x07, 0xBD, 0x00B6, no_upgrade, give_song, 17, -1), // 0xCF = Song of Storms

ITEM_ROW(0x4D, 0x00, 0xE5, 0x37, 0x00C7, no_upgrade,     no_effect, -1, -1), // 0xD0 = Deku Sticks (1),
ITEM_ROW(0x4D, 0x95, 0xB8, 0xDC, 0x0119, seeds_to_rupee, no_effect, -1, -1), // 0xD1 = Deku Seeds (30),

ITEM_ROW(0x77, 0x3E, 0xE3, 0x4C, 0x00CB, no_upgrade, no_effect, -1, -1), // 0xD2 = Deku Shield
ITEM_ROW(0x77, 0x3F, 0xD4, 0x4D, 0x00DC, no_upgrade, no_effect, -1, -1), // 0xD3 = Hylian Shield

};

item_row_t *get_extended_item_row(uint8_t index) {
    return &(item_table[index - 0x80]);
}
