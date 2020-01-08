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
    {0x00,255, 0,  0}, // 0 - Terminates here
    {0x33,  0, 1,  2}, // 1 - Animation starts here
    {0x66,  0, 1,  3}, // 2
    {0x99,  0, 1,  4}, // 3
    {0xCC,  0, 1,  5}, // 4
    {0xFF,  4, 1,  6}, // 5 - Hold here at full vibrate
    {0xE0,  0, 1,  7}, // 6 - Then go to hold step
    {0xC2,  0, 1,  8}, // 7
    {0xA3,  0, 1,  9}, // 8
    {0x85,  0, 1, 10}, // 9
    {0x66,255, 0, 10}, // 10 - Wait here for another vibrate
    {0x44,  0, 0, 12}, // 11 - Jump here to fade out
    {0x22,  0, 0,  0}, // 12 - Stop after this
    {0x85,  0, 1, 14}, // 13 - Jump here if new vibration received mid-animation
    {0xA3,  0, 1, 15}, // 14
    {0xC2,  0, 1, 16}, // 15
    {0xE0,  0, 1,  5}  // 16 - Then go to hold step
};

#define ALPHA_ANIM_TERMINATE  0
#define ALPHA_ANIM_START      1
#define ALPHA_ANIM_HOLD      10
#define ALPHA_ANIM_FADE      11
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
    if (alpha_frame > ALPHA_DATA[alpha_index].num_frames) {
        advance_alpha_major_step();
    }
}

static void advance_alpha() {
    advance_alpha_minor_step();
}

void agony_inside_radius_setup() {
}

void agony_outside_radius_setup()
{
    if (alpha_index == ALPHA_ANIM_HOLD) {
        alpha_index = ALPHA_ANIM_FADE;
        alpha_frame = 0;
    }
}

void agony_vibrate_setup() {
    if (alpha_index == ALPHA_ANIM_TERMINATE) {
        alpha_index = ALPHA_ANIM_START;
    }
    else {
        alpha_index = ALPHA_ANIM_INTERRUPT;
    }
    alpha_frame = 0;
}

void draw_agony_graphic(int offset, unsigned char alpha) {
    // terminate if alpha level prohibited (changed areas)
    unsigned char maxalpha = (unsigned char)z64_game.hud_alpha_channels.minimap;
    if (maxalpha == 0xAA) maxalpha = 0xFF;

    if (alpha > maxalpha) {
        alpha = maxalpha;
    }

    z64_disp_buf_t *db = &(z64_ctxt.gfx->overlay);
    gSPDisplayList(db->p++, &setup_db);
    gDPPipeSync(db->p++);
    gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetPrimColor(db->p++, 0, 0, 0xFF, 0xFF, 0xFF, alpha);
    sprite_load(db, &quest_items_sprite, 9, 1);
    sprite_draw(db, &quest_items_sprite, 0, 27+offset, 189, 16, 16);
    gDPPipeSync(db->p++);
}

void draw_agony() {
    if (alpha_index != ALPHA_ANIM_TERMINATE) {
        int pos = 0;
        if (ALPHA_DATA[alpha_index].vibrate) {
            alpha_pos = -alpha_pos;
            pos = alpha_pos;
        }
        draw_agony_graphic(pos, ALPHA_DATA[alpha_index].alpha_level);
        advance_alpha();
    }
}

