#include "gfx.h"
#include "quickboots.h"

static uint16_t pad_pressed_raw,
pad,
pad_pressed;

static _Bool display_active;

void handle_quickboots() {
    uint16_t z_pad = z64_ctxt.input[0].raw.pad;
    pad_pressed_raw = (pad ^ z_pad) & z_pad;
    pad = z_pad;
    pad_pressed = 0;
    pad_pressed |= pad_pressed_raw;

    if (CAN_USE_QUICKBOOTS) {
        if (pad_pressed & DPAD_L && z64_file.iron_boots) {
            if (z64_file.equip_boots == 2) z64_file.equip_boots = 1;
            else z64_file.equip_boots = 2;
            z64_UpdateEquipment(&z64_game, &z64_link);
        }

        if ((pad_pressed & DPAD_R) && z64_file.hover_boots) {
            if (z64_file.equip_boots == 3) z64_file.equip_boots = 1;
            else z64_file.equip_boots = 3;
            z64_UpdateEquipment(&z64_game, &z64_link);
        }
    }
    if (pad_pressed & DPAD_D) {
        display_active = !display_active;
    }
}

void draw_quickboots() {
    z64_disp_buf_t *db = &(z64_ctxt.gfx->overlay);
    if (DISPLAY_QUICKBOOTS && display_active) {
        gSPDisplayList(db->p++, setup_db.buf);
        gDPPipeSync(db->p++);
        gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
        uint16_t alpha = z64_game.hud_alpha_channels.minimap;
        if (alpha == 0xAA) alpha = 0xFF;
        gDPSetPrimColor(db->p++, 0, 0, 0xFF, 0xFF, 0xFF, alpha);

        sprite_load(db, &dpad_sprite, 0, 1);
        sprite_draw(db, &dpad_sprite, 0, 269, 60, 8, 8);

        sprite_load(db, &dpad_sprite, 1, 1);
        sprite_draw(db, &dpad_sprite, 0, 277, 60, 8, 8);

        sprite_load(db, &dpad_sprite, 2, 1);
        sprite_draw(db, &dpad_sprite, 0, 269, 68, 8, 8);

        sprite_load(db, &dpad_sprite, 3, 1);
        sprite_draw(db, &dpad_sprite, 0, 277, 68, 8, 8);

        if (z64_file.iron_boots) {
            sprite_load(db, &items_sprite, 69, 1);
            if (z64_file.equip_boots == 2) {
                sprite_draw(db, &items_sprite, 0, 257, 61, 12, 12);
            }
            else {
                sprite_draw(db, &items_sprite, 0, 258, 62, 10, 10);
            }
        }

        if (z64_file.hover_boots) {
            sprite_load(db, &items_sprite, 70, 1);
            if (z64_file.equip_boots == 3) {
                sprite_draw(db, &items_sprite, 0, 287, 61, 12, 12);
            }
            else {
                sprite_draw(db, &items_sprite, 0, 286, 62, 10, 10);
            }
        }

        //gDPFullSync(db->p++);
    }
}

void quickboots_init() {
    pad_pressed_raw = 0;
    pad = 0;
    pad_pressed = 0;
    display_active = 1;
}