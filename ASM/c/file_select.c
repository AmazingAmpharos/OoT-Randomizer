#include "file_select.h"

#include "gfx.h"
#include "text.h"
#include "util.h"
#include "z64.h"

void draw_file_select_hash(uint32_t fade_out_alpha) {
    z64_disp_buf_t *db = &(z64_ctxt.gfx->poly_opa);

    // Call setup display list
    gSPDisplayList(db->p++, setup_db.buf);

    // Fade out once a file is selected

    gDPSetCombineMode(db->p++, G_CC_PRIMITIVE, G_CC_PRIMITIVE);
    gDPSetPrimColor(db->p++, 0, 0, 0x00, 0x00, 0x00, fade_out_alpha);
    gSPTextureRectangle(db->p++,
            0, 0,
            Z64_SCREEN_WIDTH<<2, Z64_SCREEN_HEIGHT<<2,
            0,
            0, 0,
            1<<10, 1<<10);
}
