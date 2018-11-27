#include "gfx.h"
#include "quickboots.h"

void handle_quickboots() {
    if (z64_file.link_age == 0) {
        // Prevent quick boots when link is in a state that he wouldn't normally be able to pause to switch boots.

        if ((z64_link.state_flags_1 & BLOCK_QUICK_BOOTS) == 0) {

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
    }
}

void draw_quickboots(z64_disp_buf_t *db) {

    gSPDisplayList(db->p++, setup_db.buf);
    gDPPipeSync(db->p++);
    gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetPrimColor(db->p++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);

    sprite_load(db, &dpad_sprite, 0, 1);
    sprite_draw(db, &dpad_sprite, 0, 269, 60, 8, 8);

    sprite_load(db, &dpad_sprite, 1, 1);
    sprite_draw(db, &dpad_sprite, 0, 277, 60, 8, 8);

    sprite_load(db, &dpad_sprite, 2, 1);
    sprite_draw(db, &dpad_sprite, 0, 269, 68, 8, 8);

    sprite_load(db, &dpad_sprite, 3, 1);
    sprite_draw(db, &dpad_sprite, 0, 277, 68, 8, 8);

    sprite_load(db, &items_sprite, 69, 1);
    sprite_draw(db, &items_sprite, 0, 258, 62, 10, 10);

    sprite_load(db, &items_sprite, 70, 1);
    sprite_draw(db, &items_sprite, 0, 286, 62, 10, 10);

    gDPFullSync(db->p++);
    gSPEndDisplayList(db->p++);
}