#include "file_icons.h"

#include "color.h"
#include "hud_colors.h"
#include "triforce.h"

#define ICON_SIZE 0x0C

#define NUM_ICON_SPRITES 3
sprite_t* const icon_sprites[NUM_ICON_SPRITES] = {
    &items_sprite,
    &quest_items_sprite,
    &linkhead_skull_sprite
};


#define LEFT_OFFSET (int)0x38
#define TOP_OFFSET  (int)0x5C
typedef struct {
    uint8_t left;
    int8_t  top;
} tile_position;


static int get_left( tile_position pos ) {
    return LEFT_OFFSET + (int)pos.left;
}


static int get_top( tile_position pos ) {
    return TOP_OFFSET + (int)pos.top;
}


#define DIM_LEVEL 0x2C
#define DIM_TO( c_in, n ) (uint8_t)((c_in * (uint16_t)n) >> 8)
static void dim_color(colorRGB8_t* color) {
    color->r = DIM_TO(color->r, DIM_LEVEL);
    color->g = DIM_TO(color->g, DIM_LEVEL);
    color->b = DIM_TO(color->b, DIM_LEVEL);
}

static const colorRGB8_t WHITE = {0xFF, 0xFF, 0xFF};
static const colorRGB8_t DIM = {DIM_TO(0xFF, DIM_LEVEL), DIM_TO(0xFF, DIM_LEVEL), DIM_TO(0xFF, DIM_LEVEL)};


/*=============================================================================
  Fixed Tiles: tiles with a fixed image that can be either bright or dim.
  One bit of storage is used for each.
=============================================================================*/

typedef struct {
    int8_t sprite;
    uint8_t tile_index;
    tile_position pos;
} fixed_tile_data_t;


#define FIXED_BITS_PER_WORD 32
#define NUM_FIXED_WORDS 2
const fixed_tile_data_t fixed_tile_positions[NUM_FIXED_WORDS*FIXED_BITS_PER_WORD] = {
    { 0, Z64_ITEM_STICK,          {0x54, 0x00}}, // 0:0
    { 0, Z64_ITEM_NUT,            {0x60, 0x00}}, // 0:1
    { 0, Z64_ITEM_BOMB,           {0x6C, 0x00}}, // 0:2
    { 0, Z64_ITEM_BOW,            {0x78, 0x00}}, // 0:3
    { 0, Z64_ITEM_FIRE_ARROW,     {0x84, 0x00}}, // 0:4
    { 0, Z64_ITEM_DINS_FIRE,      {0x90, 0x00}}, // 0:5
    { 0, Z64_ITEM_SLINGSHOT,      {0x54, 0x0C}}, // 0:6
    {-1, Z64_ITEM_FAIRY_OCARINA,  {0x60, 0x0C}}, // 0:7
    { 0, Z64_ITEM_BOMBCHU,        {0x6C, 0x0C}}, // 1:0
    {-1, Z64_ITEM_HOOKSHOT,       {0x78, 0x0C}}, // 1:1
    { 0, Z64_ITEM_ICE_ARROW,      {0x84, 0x0C}}, // 1:2
    { 0, Z64_ITEM_FARORES_WIND,   {0x90, 0x0C}}, // 1:3
    { 0, Z64_ITEM_BOOMERANG,      {0x54, 0x18}}, // 1:4
    { 0, Z64_ITEM_LENS,           {0x60, 0x18}}, // 1:5
    { 0, Z64_ITEM_BEANS,          {0x6C, 0x18}}, // 1:6
    { 0, Z64_ITEM_HAMMER,         {0x78, 0x18}}, // 1:7
    { 0, Z64_ITEM_LIGHT_ARROW,    {0x84, 0x18}}, // 2:0
    { 0, Z64_ITEM_NAYRUS_LOVE,    {0x90, 0x18}}, // 2:1
    {-1, 0,                       {0xFF, 0xFF}}, // 2:2
    {-1, 0,                       {0xFF, 0xFF}}, // 2:3
    {-1, 0,                       {0xFF, 0xFF}}, // 2:4
    {-1, 0,                       {0xFF, 0xFF}}, // 2:5
    {-1, 0,                       {0xFF, 0xFF}}, // 2:6
    {-1, 0,                       {0xFF, 0xFF}}, // 2:7
    {-1, 0,                       {0xFF, 0xFF}}, // 3:0
    {-1, 0,                       {0xFF, 0xFF}}, // 3:1
    {-1, 0,                       {0xFF, 0xFF}}, // 3:2
    {-1, 0,                       {0xFF, 0xFF}}, // 3:3
    {-1, 0,                       {0xFF, 0xFF}}, // 3:4
    {-1, 0,                       {0xFF, 0xFF}}, // 3:5
    {-1, 0,                       {0xFF, 0xFF}}, // 3:6
    {-1, 0,                       {0xFF, 0xFF}}, // 3:7
    
    { 0, Z64_ITEM_KOKIRI_SWORD,   {0x84, 0x2A}}, // 4:0
    { 0, Z64_ITEM_MASTER_SWORD,   {0x90, 0x2A}}, // 4:1
    { 0, Z64_ITEM_BIGGORON_SWORD, {0x9C, 0x2A}}, // 4:2
    {-1, 0,                       {0xFF, 0xFF}}, // 4:3
    { 0, Z64_ITEM_DEKU_SHIELD,    {0x84, 0x36}}, // 4:4
    { 0, Z64_ITEM_HYLIAN_SHIELD,  {0x90, 0x36}}, // 4:5
    { 0, Z64_ITEM_MIRROR_SHIELD,  {0x9C, 0x36}}, // 4:6
    {-1, 0,                       {0xFF, 0xFF}}, // 4:7
    { 0, Z64_ITEM_KOKIRI_TUNIC,   {0x84, 0x42}}, // 5:0
    { 0, Z64_ITEM_GORON_TUNIC,    {0x90, 0x42}}, // 5:1
    { 0, Z64_ITEM_ZORA_TUNIC,     {0x9C, 0x42}}, // 5:2
    {-1, 0,                       {0xFF, 0xFF}}, // 5:3
    { 0, Z64_ITEM_KOKIRI_BOOTS,   {0x84, 0x4E}}, // 5:4
    { 0, Z64_ITEM_IRON_BOOTS,     {0x90, 0x4E}}, // 5:5
    { 0, Z64_ITEM_HOVER_BOOTS,    {0x9C, 0x4E}}, // 5:6
    {-1, 0,                       {0xFF, 0xFF}}, // 5:7
    { 0, Z64_ITEM_BOTTLE,         {0x9C, 0x00}}, // 6:0
    { 0, Z64_ITEM_LETTER,         {0x54, 0x36}}, // 6:1
    { 1, 6 /* Emerald */,         {0x12, 0x24}}, // 6:2
    { 1, 7 /* Ruby */,            {0x1E, 0x24}}, // 6:3
    { 1, 8 /* Sapphire */,        {0x2A, 0x24}}, // 6:4
    { 1, 9 /* Stone of Agony */,  {0x6C, 0x36}}, // 6:5
    { 1, 10 /* Gerudo's Card */,  {0x60, 0x36}}, // 6:6
    {-1, 0,                       {0xFF, 0xFF}}, // 6:7
    { 1, 0 /* Forest Med. */,     {0x00, 0x30}}, // 7:0
    { 1, 1 /* Fire Med. */,       {0x0C, 0x30}}, // 7:1
    { 1, 2 /* Water Med. */,      {0x18, 0x30}}, // 7:2
    { 1, 3 /* Spirit Med. */,     {0x24, 0x30}}, // 7:3
    { 1, 4 /* Shadow Med. */,     {0x30, 0x30}}, // 7:4
    { 1, 5 /* Light Med. */,      {0x3C, 0x30}}, // 7:5
    {-1, 0,                       {0xFF, 0xFF}}, // 7:6
    {-1, 0,                       {0xFF, 0xFF}}, // 7:7
};

typedef union {
    uint32_t bits[NUM_FIXED_WORDS];
    struct {
        uint32_t inventory_bits; // word 0
        uint8_t  medallion_bits; // word 1 HI-3
        uint8_t  other_bits;     // word 1 HI-2
        uint16_t equipment_bits; // word 1 LO
    };
} fixed_tile_info_t;


#define NUM_NORMAL_INVENTORY_SLOTS 18
static void populate_fixed(const z64_file_t* file, fixed_tile_info_t* info) {
    // inventory (excluding bottles and trade items)
    uint32_t inv = 0;
    uint32_t mask = 0x1;
    const fixed_tile_data_t* inv_data = fixed_tile_positions;
    for (int i = 0; i < NUM_NORMAL_INVENTORY_SLOTS; ++i) {
        uint8_t item = file->items[i];
        if (inv_data->sprite == 0 && item == inv_data->tile_index) {
            inv |= mask;
        }
        ++inv_data;
        mask <<= 1;
    }
    info->inventory_bits = inv;
    
    // medallions
    info->medallion_bits = (uint8_t)(file->quest_items & 0x0000003F);

    // equipment
    uint16_t equipment = file->equipment;
    
    // special handling of Biggoron Sword (need to check flag)
    equipment &= 0xFFFB;
    if (file->bgs_flag) {
        equipment |= 0x0004;
    }
    info->equipment_bits = equipment;
    
    // other
    uint8_t other = (uint8_t)((file->quest_items & 0x007C0000) >> 16);

    for (uint8_t slot = Z64_SLOT_BOTTLE_1; slot <= Z64_SLOT_BOTTLE_4; ++slot) {
        uint8_t item = file->items[slot];
        if (Z64_ITEM_BOTTLE <= item && item <= Z64_ITEM_POE && item != Z64_ITEM_LETTER) {
            // bottle
            other |= (0x01 << 0);
        }
        else if (item == Z64_ITEM_LETTER) {
            // letter
            other |= (0x01 << 1);
        }
    }
    if (file->event_chk_inf[3] & 0x0008) {
        // letter (king zora moved)
        other |= (0x01 << 1);
    }
    info->other_bits = other;
}


static void draw_fixed(z64_disp_buf_t* db, const fixed_tile_info_t* info, uint8_t alpha) {
    colorRGB8_t color = DIM;
    for (uint8_t enabled = 0; enabled <= 1; ++enabled) {
        gDPSetPrimColor(db->p++, 0, 0, color.r, color.g, color.b, alpha);

        const fixed_tile_data_t* data = fixed_tile_positions;
        for (int i = 0; i < NUM_FIXED_WORDS; ++i) {
            uint32_t word = info->bits[i];
            for (int j = 0; j < FIXED_BITS_PER_WORD; ++j) {
                if (data->sprite >= 0 && (word & 0x1) == enabled) {
                    sprite_t* sprite = icon_sprites[data->sprite];
                    sprite_load(db, sprite, data->tile_index, 1);
                    sprite_draw(db, sprite, 0, get_left(data->pos), get_top(data->pos), ICON_SIZE, ICON_SIZE);                
                }
                word >>= 1;
                ++data;
            }
        }
        
        color = WHITE;
    }
}


/*=============================================================================
  Variable Tiles: tiles with a variable image that can be either bright or dim.
  They have a fixed sprite but can change their tile index. Two bytes of 
  storage are used for each: 1 for bright/dim, and 1 for tile index.
=============================================================================*/

typedef struct {
    uint8_t sprite;
    tile_position pos;
} variable_tile_data_t;

#define NUM_VARIABLE 7
const variable_tile_data_t variable_tile_positions[NUM_VARIABLE] = {
    {0, {0x60, 0x0C}}, // Fairy Ocarina
    {0, {0x78, 0x0C}}, // Hookshot
    {0, {0x9C, 0x0C}}, // Child Trade
    {0, {0x9C, 0x18}}, // Adult Trade
    {1, {0x54, 0x2A}}, // Magic
    {0, {0x60, 0x2A}}, // Strength
    {0, {0x6C, 0x2A}}, // Scale
};

typedef struct {
    uint8_t enabled;
    uint8_t tile_index;
} variable_tile_t;

typedef struct {
    variable_tile_t tiles[NUM_VARIABLE];
} variable_tile_info_t;


static void populate_upgrade_item(const z64_file_t* file, variable_tile_t* tile, uint8_t slot, uint8_t base_item) {
    uint8_t item = file->items[slot];
    if (item == base_item || item == base_item + 1) {
        tile->enabled = 1;
        tile->tile_index = item;
    }
    else {
        tile->enabled = 0;
        tile->tile_index = base_item;
    }
}


static const uint8_t MASK_LOOKUP[16] = {
    Z64_ITEM_MASK_OF_TRUTH, // 0x00
    Z64_ITEM_KEATON_MASK,   // 0x01
    Z64_ITEM_SKULL_MASK,    // 0x02
    Z64_ITEM_SKULL_MASK,
    Z64_ITEM_SPOOKY_MASK,   // 0x04
    Z64_ITEM_SPOOKY_MASK,
    Z64_ITEM_SPOOKY_MASK,
    Z64_ITEM_SPOOKY_MASK,
    Z64_ITEM_BUNNY_HOOD,    // 0x08
    Z64_ITEM_BUNNY_HOOD,
    Z64_ITEM_BUNNY_HOOD,
    Z64_ITEM_BUNNY_HOOD,
    Z64_ITEM_BUNNY_HOOD,
    Z64_ITEM_BUNNY_HOOD,
    Z64_ITEM_BUNNY_HOOD,
    Z64_ITEM_BUNNY_HOOD   
};


static void populate_child_trade(const z64_file_t* file, variable_tile_t* tile) {
    uint8_t item_child = file->items[Z64_SLOT_CHILD_TRADE];
    uint16_t mask_bits = (file->item_get_inf[2] >> 3) & 0x8F;
    uint16_t itemdata3 = file->item_get_inf[3];
    uint16_t infdata7 = file->inf_table[7];
    if (itemdata3 & 0x8000 || mask_bits > 0x0F) {
        tile->tile_index = Z64_ITEM_MASK_OF_TRUTH;
        tile->enabled = 1;
    }
    else if (mask_bits > 0) {
        tile->tile_index = MASK_LOOKUP[mask_bits];
        tile->enabled = 1;
    }
    else if (Z64_ITEM_WEIRD_EGG <= item_child && item_child <= Z64_ITEM_ZELDAS_LETTER) {
        tile->tile_index = item_child;
        tile->enabled = 1;
    }
    else {
        tile->tile_index = Z64_ITEM_MASK_OF_TRUTH;
        tile->enabled = 0;
    }
}

static void populate_adult_trade(const z64_file_t* file, variable_tile_t* tile) {
    uint8_t item_adult = file->items[Z64_SLOT_ADULT_TRADE];
    if (Z64_ITEM_POCKET_EGG <= item_adult && item_adult <= Z64_ITEM_CLAIM_CHECK) {
        tile->tile_index = item_adult;
        tile->enabled = 1;
    }
    else {
        tile->tile_index = Z64_ITEM_CLAIM_CHECK;
        tile->enabled = 0;
    }
}

static void populate_magic(const z64_file_t* file, variable_tile_t* tile) {
    if (file->magic_capacity) {
        tile->tile_index = 19;
        tile->enabled = 1;
    }
    else {
        tile->tile_index = 18;
        tile->enabled = file->magic_acquired;
    }
}

static void populate_upgrade_equip(const z64_file_t* file, variable_tile_t* tile, uint8_t value, uint8_t max, uint8_t base_tile) {
    if (value > max) value = max;
    if (!value) {
        tile->enabled = 0;
        tile->tile_index = base_tile;
    }
    else {
        tile->enabled = 1;
        tile->tile_index = base_tile + (value - 1);
    }
}

static void populate_variable(const z64_file_t* file, variable_tile_info_t* info) {
    variable_tile_t* tile = info->tiles;
    
    populate_upgrade_item( file, tile++, Z64_SLOT_OCARINA, Z64_ITEM_FAIRY_OCARINA);
    populate_upgrade_item( file, tile++, Z64_SLOT_HOOKSHOT, Z64_ITEM_HOOKSHOT);
    populate_child_trade(  file, tile++);
    populate_adult_trade(  file, tile++);
    populate_magic(        file, tile++);
    populate_upgrade_equip(file, tile++, file->strength_upgrade, 3, Z64_ITEM_GORONS_BRACELET);
    populate_upgrade_equip(file, tile++, file->diving_upgrade,   2, Z64_ITEM_SILVER_SCALE);
}


static void draw_variable(z64_disp_buf_t* db, const variable_tile_info_t* info, uint8_t alpha) {
    colorRGB8_t color = DIM;
    for (uint8_t enabled = 0; enabled <= 1; ++enabled) {
        gDPSetPrimColor(db->p++, 0, 0, color.r, color.g, color.b, alpha);

        const variable_tile_t* tile = info->tiles;
        const variable_tile_data_t* data = variable_tile_positions;
        while (data != variable_tile_positions + NUM_VARIABLE) {
            if (tile->enabled == enabled) {
                sprite_t* sprite = icon_sprites[data->sprite];
                sprite_load(db, sprite, tile->tile_index, 1);
                sprite_draw(db, sprite, 0, get_left(data->pos), get_top(data->pos), ICON_SIZE, ICON_SIZE);                
            }
            ++tile;
            ++data;
        }
        
        color = WHITE;
    }
}


/*=============================================================================
  Music Tiles: tiles that use the music note sprite with different colors
  that can be either bright or dim. One bit of storage is used for each.
=============================================================================*/

typedef struct {
    colorRGB8_t color;
    tile_position pos;
} music_tile_data_t;

#define NUM_SONGS 12
#define SONG_SHIFT 6
music_tile_data_t song_note_data[NUM_SONGS] = {
    {{0x97, 0xFF, 0x63}, {0x4E, 0x54}}, // Minuet of forest
    {{0xFF, 0x50, 0x28}, {0x56, 0x54}}, // Bolero of fire
    {{0x63, 0x97, 0xFF}, {0x5E, 0x54}}, // Serenade of water
    {{0xFF, 0x9F, 0x00}, {0x66, 0x54}}, // Requiem of spirit
    {{0xFF, 0x63, 0xFF}, {0x6E, 0x54}}, // Nocturne of shadow
    {{0xFF, 0xF0, 0x63}, {0x76, 0x54}}, // Prelude of light
    {{0xFF, 0xFF, 0xFF}, {0x4E, 0x48}}, // Zelda's lullaby
    {{0xFF, 0xFF, 0xFF}, {0x56, 0x48}}, // Epona's song
    {{0xFF, 0xFF, 0xFF}, {0x5E, 0x48}}, // Saria's song
    {{0xFF, 0xFF, 0xFF}, {0x66, 0x48}}, // Sun's song
    {{0xFF, 0xFF, 0xFF}, {0x6E, 0x48}}, // Song of time
    {{0xFF, 0xFF, 0xFF}, {0x76, 0x48}}  // Song of storms
};

typedef struct {
    uint16_t bits;
} music_tile_info_t;


static void populate_songs(const z64_file_t* file, music_tile_info_t* songs) {
    songs->bits = (uint16_t)((file->quest_items >> SONG_SHIFT) & 0x0FFF);
}


static void draw_songs(z64_disp_buf_t* db, music_tile_info_t* songs, uint8_t alpha) {
    uint16_t bits = songs->bits;
    const music_tile_data_t* data = song_note_data;
    sprite_load(db, &song_note_sprite, 0, 1);

    colorRGB8_t last_color = {0x00, 0x00, 0x00};
    while (data != song_note_data + NUM_SONGS) {
        colorRGB8_t color = data->color;
        if ((bits & 0x1) == 0) {
            dim_color(&color);
        }

        if (last_color.r != color.r || last_color.g != color.g || last_color.b != color.b) {
            gDPSetPrimColor(db->p++, 0, 0, color.r, color.g, color.b, alpha);
        }
        sprite_draw(db, &song_note_sprite, 0, get_left(data->pos), get_top(data->pos), (ICON_SIZE * 2 / 3), ICON_SIZE);
        
        bits >>= 1;
        ++data;
        last_color = color;
    }
}


/*=============================================================================
  Counter Tiles: special tiles display a numerical count. These are handled
  on an individual basis.
=============================================================================*/

#define NUM_COUNTER 5
#define COUNTER_ICON_SIZE 0x10
tile_position counter_positions[NUM_COUNTER] = {
    {0x00, 0x00}, // Hearts
    {0x14, 0x00}, // Rupees
    {0x28, 0x00}, // Skulltulas
    {0x3C, 0x00}, // Triforce/Boss Key
    {0xAE, 0xEE}, // Deaths
};

typedef struct {
    uint8_t draw_triforce;
    uint8_t enable_bosskey;
    uint8_t enable_skulltula;
    uint8_t wallet;
    uint8_t double_defense;
    uint8_t show_deaths;
    uint8_t heart_digits[3];
    uint8_t rupee_digits[3];
    uint8_t triforce_digits[3];
    uint8_t skulltula_digits[3];
    uint8_t death_digits[3];
} counter_tile_info_t;


void make_digits(uint8_t* digits, int16_t value) {
    digits[0] = digits[1] = digits[2] = 0xFF;
    if (value < 0) {
        return;
    }
    else if (value > 999) {
        value = 999;
    }

    for (int idx = 2; idx >= 0; --idx) {
        digits[idx] = value % 10;
        value /= 10;
        if (value == 0) break;
    }
}


static void populate_counts(const z64_file_t* file, counter_tile_info_t* counts) {

    // Rupees
    counts->wallet = file->wallet;    
    make_digits(counts->rupee_digits, (int16_t)file->rupees);
    
    // Skulltulas
    counts->enable_skulltula = file->gold_skulltula;
    make_digits(counts->skulltula_digits, counts->enable_skulltula ? file->gs_tokens : -1);
    
    // Triforce or Boss Key
    counts->enable_bosskey = file->dungeon_items[10].boss_key;
    counts->draw_triforce = triforce_hunt_enabled;
    if (!counts->enable_bosskey && counts->draw_triforce) {
        make_digits(counts->triforce_digits, (int16_t)file->scene_flags[0x48].unk_00_);
    }
    else {
        make_digits(counts->triforce_digits, -1);
    }
    
    // Hearts
    counts->double_defense = (uint8_t)file->double_defense;
    make_digits(counts->heart_digits, file->energy_capacity / 0x10);
    
    // Deaths
    counts->show_deaths = (file->deaths > 0);
    if (counts->show_deaths) {
        make_digits(counts->death_digits, file->deaths);
    }
    else {
        make_digits(counts->death_digits, -1);
    }
}


// note: must load item_digit_sprite before calling this function
static void draw_digits(z64_disp_buf_t* db, const uint8_t* digits, const tile_position* pos, int voffset) {
    int left = get_left(*pos) - 1;
    int top = get_top(*pos) + voffset;
    
    for (int i = 0; i < 3; ++i) {
        if (digits[i] <= 9) {
            if (digits[i] == 1 && i > 0) --left; // adjust for narrow "1" sprite
            sprite_draw(db, &item_digit_sprite, digits[i], left, top, 8, 8);
            if (digits[i] == 1) --left; // adjust for narrow "1" sprite
            left += 6;
        }
        else {
            left += 3;
        }
    }
}


static void draw_counts(z64_disp_buf_t* db, const counter_tile_info_t* info, uint8_t alpha) {
    const tile_position* pos = counter_positions;

    // Heart
    gDPSetPrimColor(db->p++, 0, 0, WHITE.r, WHITE.g, WHITE.b, alpha);        
    sprite_load(db, &quest_items_sprite, 12, 1);
    if (!info->double_defense) {
        sprite_draw(db, &quest_items_sprite, 0, get_left(*pos), get_top(*pos), COUNTER_ICON_SIZE, COUNTER_ICON_SIZE);
    }
    else {
        sprite_draw(db, &quest_items_sprite, 0, get_left(*pos)-2, get_top(*pos), COUNTER_ICON_SIZE, COUNTER_ICON_SIZE);
        sprite_draw(db, &quest_items_sprite, 0, get_left(*pos)+2, get_top(*pos), COUNTER_ICON_SIZE, COUNTER_ICON_SIZE);
    }
    ++pos;

    // Rupee
    colorRGB8_t rupee_color = rupee_colors[info->wallet];
    gDPSetPrimColor(db->p++, 0, 0, rupee_color.r, rupee_color.g, rupee_color.b, alpha);        
    sprite_load(db, &key_rupee_clock_sprite, 1, 1);
    sprite_draw(db, &key_rupee_clock_sprite, 0, get_left(*pos), get_top(*pos), COUNTER_ICON_SIZE, COUNTER_ICON_SIZE);
    ++pos;
    
    // Skulltula
    colorRGB8_t token_color = info->enable_skulltula ? WHITE : DIM;
    gDPSetPrimColor(db->p++, 0, 0, token_color.r, token_color.g, token_color.b, alpha);        
    sprite_load(db, &quest_items_sprite, 11, 1);
    sprite_draw(db, &quest_items_sprite, 0, get_left(*pos), get_top(*pos), COUNTER_ICON_SIZE, COUNTER_ICON_SIZE);
    ++pos;
    
    // Triforce/Boss Key
    if (info->draw_triforce) {
        static uint8_t frame_counter = 0;
        gDPSetPrimColor(db->p++, 0, 0, 0xF4, 0xEC, 0x30, alpha);        
        sprite_load(db, &triforce_sprite, (frame_counter++ >> 2) % 16, 1);
        sprite_draw(db, &triforce_sprite, 0, get_left(*pos), get_top(*pos) + 2, COUNTER_ICON_SIZE, COUNTER_ICON_SIZE);
    }
    else {
        colorRGB8_t key_color = info->enable_bosskey ? WHITE : DIM;
        gDPSetPrimColor(db->p++, 0, 0, key_color.r, key_color.g, key_color.b, alpha);
        sprite_load(db, &quest_items_sprite, 14, 1);
        sprite_draw(db, &quest_items_sprite, 0, get_left(*pos), get_top(*pos), COUNTER_ICON_SIZE, COUNTER_ICON_SIZE);
    }
    ++pos;
    
    // Deaths
    if (info->show_deaths) {
        gDPSetPrimColor(db->p++, 0, 0, WHITE.r, WHITE.g, WHITE.b, alpha);        
        sprite_load(db, &linkhead_skull_sprite, 1, 1);
        sprite_draw(db, &linkhead_skull_sprite, 0, get_left(*pos), get_top(*pos), COUNTER_ICON_SIZE, COUNTER_ICON_SIZE);
    }
    
    pos = counter_positions;
    gDPSetPrimColor(db->p++, 0, 0, 0xFF, 0xFF, 0xFF, alpha);        
    sprite_load(db, &item_digit_sprite, 0, 10);
    draw_digits(db, info->heart_digits,     pos++,  16);
    draw_digits(db, info->rupee_digits,     pos++,  16);
    draw_digits(db, info->skulltula_digits, pos++,  16);
    draw_digits(db, info->triforce_digits,  pos++,  16);
    draw_digits(db, info->death_digits,     pos++,  16);
}


/*=============================================================================
  Stored data for selected file
=============================================================================*/

typedef struct {
    fixed_tile_info_t fixed;
    variable_tile_info_t variable;
    counter_tile_info_t counters;
    music_tile_info_t songs;
} file_info_t;

static file_info_t draw_data;


void read_file_data(const z64_file_t* file) {
    populate_fixed(file, &draw_data.fixed);
    populate_variable(file, &draw_data.variable);
    populate_counts(file, &draw_data.counters);
    populate_songs(file, &draw_data.songs);
}


static uint8_t get_alpha(uint32_t transition, uint32_t transition_frame) {
    switch (transition) {
        case 0x03:
        case 0x06:
            return 0xC8;
            break;
        case 0x02:
            return (uint8_t)(((8 - transition_frame) * 0xC8) / 8);
            break;
        case 0x04:
            return (uint8_t)((transition_frame * 0xC8) / 8);
            break;
        default:
            return 0x00;
    }
}


void draw_file_icons(z64_disp_buf_t* db, z64_menudata_t* menu_data) {
    if (menu_data->menu_depth == 0x02) {
        if (menu_data->menu_transition == 0x00 && menu_data->transition_frame == 8) {
            read_file_data(&menu_data->sram_buffer->primary_saves[menu_data->selected_file]);
            return;
        }
        uint8_t icon_alpha = get_alpha(menu_data->menu_transition, menu_data->transition_frame);

        if (icon_alpha) {
            
            gDPPipeSync(db->p++);
            gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);

            draw_fixed(db, &draw_data.fixed, icon_alpha);
            draw_variable(db, &draw_data.variable, icon_alpha);
            draw_songs(db, &draw_data.songs, icon_alpha);
            draw_counts(db, &draw_data.counters, icon_alpha);
        }
    }

}