#include "agony.h"
#include "gfx.h"
#include "z64.h"

typedef struct {
    unsigned char alpha_level;
    unsigned char num_frames;
    unsigned char vibrate;
    unsigned char next;
} alpha_data_t;

static const alpha_data_t ALPHA_DATA[] = {
    {0x00,  0, 0,  0}, // 0 - Terminates here
    {0x33,  2, 1,  2}, // 1 - Animation starts here
    {0x66,  1, 1,  3}, // 2
    {0x99,  1, 1,  4}, // 3
    {0xCC,  1, 1,  5}, // 4
    {0xFF,  5, 1,  6}, // 5 - Hold here at full vibrate
    {0xE0,  1, 1,  7}, // 6 - Then go to hold step
    {0xC2,  1, 1,  8}, // 7
    {0xA3,  1, 1,  9}, // 8
    {0x85,  1, 1, 10}, // 9
    {0x66, 99, 0, 11}, // 10 - Wait here for another vibrate
    {0x44,  1, 0, 12}, // 11 - After 99 frames of waiting, fade out
    {0x22,  1, 0,  0}, // 12 - Stop after this
    {0x85,  2, 1, 14}, // 13 - Go here if new vibration received mid-animation
    {0xA3,  1, 1, 15}, // 14
    {0xC2,  1, 1, 16}, // 15
    {0xE0,  1, 1,  5}  // 16 - Then go to hold step
};

#define ALPHA_ANIM_TERMINATE  0
#define ALPHA_ANIM_START      1
#define ALPHA_ANIM_INTERRUPT 13

static unsigned char alpha_index = 0;
static unsigned char alpha_frame = 0;
static signed char alpha_pos = 1;

static void advance_alpha_major_step() {
    alpha_index = ALPHA_DATA[alpha_index].next;
    alpha_frame = 0;
}

static void advance_alpha_minor_step() {
    ++alpha_frame;
    if (alpha_frame >= ALPHA_DATA[alpha_index].num_frames) {
        advance_alpha_major_step();
    }
}

static void advance_alpha() {
    advance_alpha_minor_step();

    // terminate if alpha level prohibited (changed areas)
    unsigned char maxalpha = (unsigned char)z64_game.hud_alpha_channels.minimap;
    if (maxalpha == 0xAA) maxalpha = 0xFF;

    if (ALPHA_DATA[alpha_index].alpha_level > maxalpha) {
        alpha_index = ALPHA_ANIM_TERMINATE;
    }
}

void agony_vibrate_setup() {
    if (alpha_index == ALPHA_ANIM_TERMINATE) {
        alpha_index = ALPHA_ANIM_START;
    }
    else {
        alpha_index = ALPHA_ANIM_INTERRUPT;
    }
}

void draw_agony_graphic(int offset, unsigned char alpha) {
    z64_disp_buf_t *db = &(z64_ctxt.gfx->overlay);
    gSPDisplayList(db->p++, &setup_db);
    gDPPipeSync(db->p++);
    gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetPrimColor(db->p++, 0, 0, 0xFF, 0xFF, 0xFF, alpha);
    sprite_load(db, &quest_items_sprite, 9, 1);
    sprite_draw(db, &quest_items_sprite, 0, 26+offset, 190, 16, 16);
    gDPPipeSync(db->p++);
}

void draw_agony() {
    if (alpha_index != ALPHA_ANIM_TERMINATE) {
        int pos = 0;
        if (ALPHA_DATA[alpha_index].vibrate) {
            alpha_pos = -alpha_pos;
            pos = alpha_pos;
        }
        advance_alpha();
        draw_agony_graphic(pos, ALPHA_DATA[alpha_index].alpha_level);
    }
}

