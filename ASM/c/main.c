#include "dungeon_info.h"
#include "gfx.h"
#include "text.h"
#include "util.h"
#include "z64.h"

void c_init() {
    heap_init();
    gfx_init();
    text_init();
}

void overlay_swap(z64_disp_buf_t *db, Gfx *buf, uint32_t size) {
    if (z64_game.pause_state == 6 &&
                z64_game.pause_screen == 0 &&
                !z64_game.pause_screen_changing &&
                z64_ctxt.input[0].raw.a) {
        draw_dungeon_info(db);
    }

    disp_buf_init(db, buf, size);
}
