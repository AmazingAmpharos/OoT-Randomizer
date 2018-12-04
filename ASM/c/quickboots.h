#ifndef QUICKBOOTS_H
#define QUICKBOOTS_H

#include "z64.h"

#define BLOCK_QUICK_BOOTS (0x00000001 | \
	0x00000002 | \
    0x00000080 | \
    0x00000400 | \
    0x10000000 | \
    0x20000000)

#define DPAD_L 0x0200
#define DPAD_R 0x0100
#define DPAD_D 0x0400

void handle_quickboots();
void draw_quickboots(z64_disp_buf_t*);
void quickboots_init();

#endif