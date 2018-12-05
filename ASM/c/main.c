#include "dungeon_info.h"
#include "file_select.h"
#include "gfx.h"
#include "text.h"
#include "util.h"
#include "quickboots.h"
#include "z64.h"

void c_init() {
    heap_init();
    gfx_init();
    text_init();
    quickboots_init();
}

void c_before_game_state_update() {
    handle_quickboots();
}

void c_after_game_state_update() {
    z64_disp_buf_t *db = &(z64_ctxt.gfx->overlay);

    if (z64_game.pause_state == 6 &&
                z64_game.pause_screen == 0 &&
                !z64_game.pause_screen_changing &&
                z64_ctxt.input[0].raw.a) {
        
        draw_dungeon_info(db);
    }

    draw_quickboots(db);
}
