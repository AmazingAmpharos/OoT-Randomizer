#include "reset.h"
typedef void(*Open_Init)();
#define openInit  ((Open_Init) 0x808007B0)

void waitForResetCombo(){
	z64_controller_t pad_pressed = z64_game.common.input[0].raw;
	if ((pad_pressed.pad.cr) && (pad_pressed.pad.b) && (pad_pressed.pad.s)) {
		z64_game.common.state_continue = 0;
		z64_game.common.next_ctor = (void*)openInit;
		z64_game.common.next_size = sizeof(char[0x1E8]);
	}
}