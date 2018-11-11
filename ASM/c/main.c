#include "dungeon_info.h"
#include "file_select.h"
#include "gfx.h"
#include "text.h"
#include "util.h"
#include "z64.h"

#define BLOCK_QUICK_BOOTS (0x00000001 | \
	0x00000002 | \
    0x00000080 | \
    0x00000400 | \
    0x10000000 | \
    0x20000000)     

static uint16_t pad_pressed_raw, 
	pad, 
	pad_pressed;

void c_init() {
	pad_pressed_raw = 0;
	pad = 0;
	pad_pressed = 0;
    heap_init();
    gfx_init();
    text_init();
}

void c_after_game_state_update() {
    if (z64_game.pause_state == 6 &&
                z64_game.pause_screen == 0 &&
                !z64_game.pause_screen_changing &&
                z64_ctxt.input[0].raw.a) {
        z64_disp_buf_t *db = &(z64_ctxt.gfx->overlay);
        draw_dungeon_info(db);
    }

	uint16_t z_pad = z64_ctxt.input[0].raw.pad;
	pad_pressed_raw = (pad ^ z_pad) & z_pad;
	pad = z_pad;
	pad_pressed = 0;
	pad_pressed |= pad_pressed_raw;
	

	if (z64_file.link_age==0) {
		// Prevent quick boots when link is in a state that he wouldn't normally be able to pause to switch boots.

		if ((z64_link.state_flags_1 & BLOCK_QUICK_BOOTS) == 0) {

			if (pad_pressed & 0x0200 && z64_file.iron_boots) {
				if (z64_file.equip_boots == 2) z64_file.equip_boots = 1;
				else z64_file.equip_boots = 2;
				z64_UpdateEquipment(&z64_game, &z64_link);
			}

			if ((pad_pressed & 0x0100) && z64_file.hover_boots) {
				if (z64_file.equip_boots == 3) z64_file.equip_boots = 1;
				else z64_file.equip_boots = 3;
				z64_UpdateEquipment(&z64_game, &z64_link);
			}
		}
	}
}
