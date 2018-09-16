#include "dungeon_info.h"

#include "gfx.h"
#include "text.h"
#include "util.h"
#include "z64.h"

typedef struct {
    uint8_t index;
    struct {
        uint8_t has_keys : 1;
        uint8_t has_boss_key : 1;
        uint8_t has_card : 1;
        uint8_t has_map : 1;
    };
    char name[10];
} dungeon_entry_t;

dungeon_entry_t dungeons[] = {
    {  0, 0, 0, 0, 1, "Deku"    },
    {  1, 0, 0, 0, 1, "Dodongo" },
    {  2, 0, 0, 0, 1, "Jabu"    },

    {  3, 1, 1, 0, 1, "Forest"  },
    {  4, 1, 1, 0, 1, "Fire"    },
    {  5, 1, 1, 0, 1, "Water"   },
    {  7, 1, 1, 0, 1, "Shadow"  },
    {  6, 1, 1, 0, 1, "Spirit"  },

    {  8, 1, 0, 0, 1, "BotW"    },
    {  9, 0, 0, 0, 1, "Ice"     },
    { 11, 1, 0, 0, 0, "GTG"     },
    { 12, 1, 0, 1, 0, "Hideout" },
    { 13, 1, 1, 0, 0, "Ganon"   },
};

int dungeon_count = array_size(dungeons);

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

uint32_t cfg_dungeon_info_enable = 1;
uint32_t cfg_dungeon_info_mq_enable = 0;
uint32_t cfg_dungeon_info_mq_need_compass = 0;
uint32_t cfg_dungeon_info_reward_need_map = 0;

int8_t cfg_dungeon_rewards[] = { 0, 1, 2, 3, 4, 5, 6, 7, -1, -1, -1, -1, -1, -1 };
uint8_t cfg_dungeon_is_mq[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

void draw_dungeon_info(z64_disp_buf_t *db) {
    if (!cfg_dungeon_info_enable) return;

    db->p = db->buf;

    // Call setup display list
    gSPDisplayList(db->p++, setup_db.buf);

    // Set up dimensions

    int icon_size = 16;
    int padding = 2;
    int rows = 13;
    int mq_width = cfg_dungeon_info_mq_enable ?
        ((6 * font_sprite.tile_w) + padding) :
        0;
    int bg_width =
        (5 * icon_size) +
        (8 * font_sprite.tile_w) +
        (7 * padding) +
        mq_width;
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
        if (cfg_dungeon_info_reward_need_map &&
                !z64_file.dungeon_items[d->index].map) {
            continue;
        }
        int reward = cfg_dungeon_rewards[d->index];
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
        if (cfg_dungeon_info_reward_need_map &&
                !z64_file.dungeon_items[d->index].map) {
            continue;
        }
        int reward = cfg_dungeon_rewards[d->index];
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
        if (!d->has_keys) continue;

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
        if (d->has_boss_key && z64_file.dungeon_items[d->index].boss_key) {
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
            if (d->has_map && z64_file.dungeon_items[d->index].map) {
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
            if (d->has_map && z64_file.dungeon_items[d->index].compass) {
                int top = start_top + ((icon_size + padding) * i);
                sprite_draw(db, &quest_items_sprite, 0,
                        left, top, icon_size, icon_size);
            }
        }

        left += icon_size + padding;
    }

    // Draw master quest dungeons

    if (cfg_dungeon_info_mq_enable) {
        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            if (cfg_dungeon_info_mq_need_compass && d->has_map &&
                    !z64_file.dungeon_items[d->index].compass) {
                continue;
            }
            char *str = cfg_dungeon_is_mq[d->index] ? "MQ" : "Normal";
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
