#include "dungeon_info.h"
#include "file_select.h"
#include "gfx.h"
#include "text.h"
#include "util.h"
#include "z64.h"

void c_init() {
    heap_init();
    gfx_init();
    text_init();
}

_Bool zu_in_game(void)
{
	return (uint32_t)z64_ctxt.state_dtor == z64_state_ovl_tab[3].vram_dtor;
}

static uint16_t pad_pressed_raw, pad_released, pad, pad_pressed;
static int button_time[16];
void c_after_game_state_update() {
    if (z64_game.pause_state == 6 &&
                z64_game.pause_screen == 0 &&
                !z64_game.pause_screen_changing &&
                z64_ctxt.input[0].raw.a) {
        z64_disp_buf_t *db = &(z64_ctxt.gfx->overlay);
        draw_dungeon_info(db);
    }

	uint16_t z_pad = z64_input_direct.raw.pad;
	pad_pressed_raw = (pad ^ z_pad) & z_pad;
	pad_released = (pad ^ z_pad) & ~z_pad;
	pad = z_pad;
	pad_pressed = 0;
	for (int i = 0; i < 16; ++i) {
		uint16_t p = 1 << i;
		if (pad & p)
			++button_time[i];
		else
			button_time[i] = 0;
		if ((pad_pressed_raw & p) || button_time[i] >= 8)
			pad_pressed |= p;
	}

	if (zu_in_game() && z64_file.link_age==0) {

		

		/*if (z64_ctxt.input[0].raw.dl) {
			z64_file.equip_boots = 1;
			z64_UpdateEquipment(&z64_game, &z64_link);
		}*/

		if (pad_released & 0x0200 && z64_file.iron_boots) {
			if (z64_file.equip_boots == 2) z64_file.equip_boots = 1;
			else z64_file.equip_boots = 2;
			z64_UpdateEquipment(&z64_game, &z64_link);
		}

		if ((pad_released & 0x0100) && z64_file.hover_boots) {
			if (z64_file.equip_boots == 3) z64_file.equip_boots = 1;
			else z64_file.equip_boots = 3;
			z64_UpdateEquipment(&z64_game, &z64_link);
		}
	}
}
