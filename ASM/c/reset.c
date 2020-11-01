#include "reset.h"
typedef void(*title_init)();
#define title_init  ((title_init) 0x808007B0)
typedef void(*file_init)();	
#define z64_file_init ((file_init) 0x80051aa0)

static unsigned int s_reset_delay = 10;

void wait_for_reset_combo(){
	z64_controller_t pad_pressed = z64_game.common.input[0].raw;
	if ((pad_pressed.pad.cr) && (pad_pressed.pad.b) && (pad_pressed.pad.s)) {
		if (s_reset_delay != 0) {
			s_reset_delay--;
		}
		else {
			
			z64_file_init();
			z64_game.common.state_continue = 0;
			z64_game.common.next_ctor = (void*)title_init;
			z64_game.common.next_size = sizeof(char[0x1E8]);
		}
	}
	else {
		s_reset_delay = 10;
	}
}