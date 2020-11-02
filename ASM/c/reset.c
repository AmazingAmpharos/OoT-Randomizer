#include "reset.h"

typedef void(*title_init_setup)(z64_ctxt_t* ctxt);
#define title_init_setup  ((title_init_setup) 0x800A0748)
typedef void (*set_bgm)(unsigned int ID);
#define SET_BGM ((set_bgm) 0x800CAA70)
#define BGM_STOP 0x100000FF

static unsigned short s_reset_delay = 10;

void wait_for_reset_combo(){
	z64_controller_t pad_pressed = z64_game.common.input[0].raw;
	if ((pad_pressed.pad.cr) && (pad_pressed.pad.b) && (pad_pressed.pad.s)) {
		if (s_reset_delay != 0) {
			s_reset_delay--;
		}
		else {
			SET_BGM(BGM_STOP);
			title_init_setup(&z64_game.common);
		}
	}
	else {
		s_reset_delay = 10;
	}
}
