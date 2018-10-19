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
    { 12, 1, 0, 1, 0, "Gerudo"  },
    { 11, 1, 0, 0, 0, "GTG"     },
    { 13, 1, 1, 0, 0, "Ganon"   },
};

int dungeon_count = array_size(dungeons);

typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} medal_color_t;

medal_color_t medal_colors[] = {
    { 0x00, 0xFF, 0x00 }, // Forest
    { 0xFF, 0x3C, 0x00 }, // Fire
    { 0x00, 0x64, 0xFF }, // Water
    { 0xFF, 0x82, 0x00 }, // Spirit
    { 0xC8, 0x32, 0xFF }, // Shadow
    { 0xC8, 0xC8, 0x00 }, // Light
};

uint32_t cfg_dungeon_info_enable = 1;
uint32_t cfg_dungeon_info_mq_enable = 0;
uint32_t cfg_dungeon_info_mq_need_map = 0;
uint32_t cfg_dungeon_info_reward_need_compass = 0;
uint32_t cfg_dungeon_info_reward_need_altar = 0;

int8_t cfg_dungeon_rewards[] = { 0, 1, 2, 3, 4, 5, 6, 7, -1, -1, -1, -1, -1, -1 };
uint8_t cfg_dungeon_is_mq[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

void draw_dungeon_info(z64_disp_buf_t *db) {
    if (!cfg_dungeon_info_enable) return;

    db->p = db->buf;

    // Call setup display list
    gSPDisplayList(db->p++, setup_db.buf);

    uint16_t altar_flags = z64_file.inf_table[27];
    int show_medals = !cfg_dungeon_info_reward_need_altar || (altar_flags & 1);
    int show_stones = !cfg_dungeon_info_reward_need_altar || (altar_flags & 2);
    int show_keys = 1;
    int show_map_compass = 1;
    int show_mq = cfg_dungeon_info_mq_enable;

    // Set up dimensions

    int icon_size = 16;
    int padding = 1;
    int rows = 13;
    int mq_width = show_mq ?
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

    gDPPipeSync(db->p++);
    gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);

    // Draw medals

    if (show_medals) {
        sprite_load(db, &medals_sprite, 0, medals_sprite.tile_count);

        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            if (cfg_dungeon_info_reward_need_compass &&
                    !z64_file.dungeon_items[d->index].compass) {
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
    }

    gDPSetPrimColor(db->p++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);

    // Draw stones

    if (show_stones) {
        sprite_load(db, &stones_sprite, 0, stones_sprite.tile_count);

        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            if (cfg_dungeon_info_reward_need_compass &&
                    !z64_file.dungeon_items[d->index].compass) {
                continue;
            }
            int reward = cfg_dungeon_rewards[d->index];
            if (reward < 0 || reward >= 3) continue;

            int top = start_top + ((icon_size + padding) * i);
            sprite_draw(db, &stones_sprite, reward,
                    left, top, icon_size, icon_size);
        }
    }

    left += icon_size + padding;

    // Draw dungeon names

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        int top = start_top + ((icon_size + padding) * i) + 1;
        text_print(d->name, left, top);
    }

    left += (8 * font_sprite.tile_w) + padding;

    // Draw keys

    if (show_keys) {
        // Draw small key counts

        sprite_load(db, &quest_items_sprite, 17, 1);

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

        sprite_load(db, &quest_items_sprite, 14, 1);

        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            // Replace index 13 (Ganon's Castle) with 10 (Ganon's Tower)
            int index = d->index == 13 ? 10 : d->index;

            if (d->has_boss_key && z64_file.dungeon_items[index].boss_key) {
                int top = start_top + ((icon_size + padding) * i);
                sprite_draw(db, &quest_items_sprite, 0,
                        left, top, icon_size, icon_size);
            }
        }

        // Draw gerudo card

        sprite_load(db, &quest_items_sprite, 10, 1);

        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            if (d->has_card && z64_file.gerudos_card) {
                int top = start_top + ((icon_size + padding) * i);
                sprite_draw(db, &quest_items_sprite, 0,
                        left, top, icon_size, icon_size);
            }
        }

        left += icon_size + padding;
    }

    // Draw maps and compasses

    if (show_map_compass) {
        // Draw maps

        sprite_load(db, &quest_items_sprite, 16, 1);

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

        sprite_load(db, &quest_items_sprite, 15, 1);

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

    if (show_mq) {
        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            if (cfg_dungeon_info_mq_need_map && d->has_map &&
                    !z64_file.dungeon_items[d->index].map) {
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
