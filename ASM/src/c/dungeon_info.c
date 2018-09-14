#include "dungeon_info.h"

#include "gfx.h"
#include "text.h"
#include "util.h"
#include "z64.h"

typedef struct {
    uint8_t index;
    char name[9];
} dungeon_entry_t;

dungeon_entry_t dungeons[] = {
    {  0, "Deku"    },
    {  1, "Dodongo" },
    {  2, "Jabu"    },

    {  3, "Forest"  },
    {  4, "Fire"    },
    {  5, "Water"   },
    {  7, "Shadow"  },
    {  6, "Spirit"  },

    {  8, "BotW"    },
    {  9, "Ice"     },
    { 11, "GTG"     },
    { 12, "Hideout" },
    { 13, "Ganon"   },
};

int dungeon_count = array_size(dungeons);

int8_t has_keys[]    = { 0, 0, 0,    1, 1, 1, 1, 1,    1, 0, -1, 1, 1, 1 };
int8_t has_bosskey[] = { 0, 0, 0,    1, 1, 1, 1, 1,    0, 0, -1, 0, 0, 1 };
int8_t has_card[]    = { 0, 0, 0,    0, 0, 0, 0, 0,    0, 0, -1, 0, 1, 0 };
int8_t has_map[]     = { 1, 1, 1,    1, 1, 1, 1, 1,    1, 1, -1, 0, 0, 0 };

typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} medal_color_t;

medal_color_t medal_colors[] = {
    { 0x11, 0xC2, 0x2D }, // Forest
    { 0xD4, 0x43, 0x22 }, // Fire
    { 0x08, 0x54, 0xCE }, // Water
    { 0xD1, 0x75, 0x1A }, // Spirit
    { 0xA9, 0x3A, 0xEA }, // Shadow
    { 0xA4, 0xAB, 0x21 }, // Light
};

// FIXME: Make dynamic
int8_t rewards[] = { 4, 1, 7, 5, 0, 8, 6, 2, -1, -1, -1, -1, -1, -1 };
uint8_t dungeon_is_mq[] = { 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0 };

void draw_dungeon_info(z64_disp_buf_t *db) {
    // Call setup display list
    gSPDisplayList(db->p++, setup_db.buf);

    // Set up dimensions

    int icon_size = 16;
    int padding = 2;
    int rows = 13;
    int bg_width = (5 * icon_size) + ((8 + 6) * font_sprite.tile_w) +
        (8 * padding);
    int bg_height = (rows * icon_size) + ((rows + 1) * padding);
    int bg_left = (Z64_SCREEN_WIDTH - bg_width) / 2;
    int bg_top = (Z64_SCREEN_HEIGHT - bg_height) / 2;

    int left = bg_left + padding;
    int start_top = bg_top + padding;

    // Draw background

    gDPSetCombineMode(db->p++, G_CC_PRIMITIVE, G_CC_PRIMITIVE);
    gDPSetPrimColor(db->p++, 0, 0, 0x00, 0x00, 0x00, 0xD0);
    gSPTextureRectangle(db->p++,
            bg_left<<2, bg_top<<2,
            (bg_left + bg_width)<<2, (bg_top + bg_height)<<2,
            0,
            0, 0,
            1<<10, 1<<10);

    // Draw medals

    gDPPipeSync(db->p++);
    gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);

    sprite_load(db, &medals_sprite, 0, medals_sprite.tile_count);

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        int reward = rewards[d->index];
        if (reward < 3) continue;
        reward -= 3;

        medal_color_t *c = &(medal_colors[reward]);
        gDPSetPrimColor(db->p++, 0, 0, c->r, c->g, c->b, 0xFF);

        int top = start_top + ((icon_size + padding) * i);
        sprite_draw(db, &medals_sprite, reward,
                left, top, icon_size, icon_size);
    }

    // Draw stones

    gDPSetPrimColor(db->p++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
    sprite_load(db, &stones_sprite, 0, stones_sprite.tile_count);

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        int reward = rewards[d->index];
        if (reward < 0 || reward >= 3) continue;

        int top = start_top + ((icon_size + padding) * i);
        sprite_draw(db, &stones_sprite, reward,
                left, top, icon_size, icon_size);

    }

    left += icon_size + padding;

    // Draw dungeon names

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        int top = start_top + ((icon_size + padding) * i) + 1;
        text_print(d->name, left, top);
    }

    left += (8 * font_sprite.tile_w) + padding;

    // Draw key counts

    sprite_load(db, &quest_items_sprite, 3, 1);

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        if (!has_keys[d->index]) continue;

        int8_t keys = z64_file.dungeon_keys[d->index];
        if (keys < 0) keys = 0;
        if (keys > 9) keys = 9;

        char count[2] = "0";
        count[0] += keys;
        int top = start_top + ((icon_size + padding) * i) + 1;
        text_print(count, left, top);
    }

    left += icon_size + padding;

    // Draw boss keys

    sprite_load(db, &quest_items_sprite, 0, 1);

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        if (has_bosskey[d->index] && z64_file.dungeon_items[d->index].boss_key) {
            int top = start_top + ((icon_size + padding) * i);
            sprite_draw(db, &quest_items_sprite, 0,
                    left, top, icon_size, icon_size);
        }
    }

    left += icon_size + padding;

    // Draw maps and compasses

    int draw_maps_and_compasses = 1;
    if (draw_maps_and_compasses) {
        // Draw maps

        sprite_load(db, &quest_items_sprite, 2, 1);

        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            if (has_map[d->index] && z64_file.dungeon_items[d->index].map) {
                int top = start_top + ((icon_size + padding) * i);
                sprite_draw(db, &quest_items_sprite, 0,
                        left, top, icon_size, icon_size);
            }
        }

        left += icon_size + padding;

        // Draw compasses

        sprite_load(db, &quest_items_sprite, 1, 1);

        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            if (has_map[d->index] && z64_file.dungeon_items[d->index].compass) {
                int top = start_top + ((icon_size + padding) * i);
                sprite_draw(db, &quest_items_sprite, 0,
                        left, top, icon_size, icon_size);
            }
        }

        left += icon_size + padding;
    }

    // Draw master quest dungeons

    int show_mq = 1;
    if (show_mq) {
        //text_print("MQ", left, top);
        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            char *str = dungeon_is_mq[d->index] ? "MQ" : "Normal";
            int top = start_top + ((icon_size + padding) * i) + 1;
            text_print(str, left, top);
        }

        left += icon_size + padding;
    }

    // Finish

    text_flush(db);

    gDPFullSync(db->p++);
    gSPEndDisplayList(db->p++);
}
