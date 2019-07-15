#include "triforce.h"
#include "gfx.h"
#include "text.h"
#include "util.h"
#include "z64.h"

static uint32_t frames = 0;
#define FRAMES_PER_CYCLE 2
#define TRIFORCE_SPRITE_FRAMES 16
extern uint32_t RAINBOW_BRIDGE_CONDITION;

void draw_triforce_count(z64_disp_buf_t *db) {

    // Must be paused and mode should be triforce hunt
    if (z64_game.pause_ctxt.state != 6 || RAINBOW_BRIDGE_CONDITION != 6 || z64_game.pause_ctxt.changing) {
        return;
    }

    // Call setup display list and setup draw coords
    gSPDisplayList(db->p++, &setup_db);

    int total_w = 2 * font_sprite.tile_w + triforce_sprite.tile_w;
    int draw_x = Z64_SCREEN_WIDTH / 2 - total_w / 2;
    int draw_y_text = Z64_SCREEN_HEIGHT - (font_sprite.tile_h * 1.5) + 1;
    int draw_y_triforce = Z64_SCREEN_HEIGHT - (triforce_sprite.tile_h * 1.5) + 3 + 1;

    gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetPrimColor(db->p++, 0, 0, 0xF4, 0xEC, 0x30, 0xFF);

    // Draw count
    int pieces = z64_file.scene_flags[0x48].unk_00_; //Unused word in scene x48. 
    int tens_place = (pieces / 10) % 10;
    int ones_place = pieces % 10;
    char text[] = { (char) (tens_place + 48), (char) (ones_place + 48) };
    text_print(text , draw_x, draw_y_text);
    draw_x += 2 * font_sprite.tile_w;

    // Draw triforce
    int sprite = (frames / FRAMES_PER_CYCLE) % TRIFORCE_SPRITE_FRAMES;
    frames++;
    frames = frames % (TRIFORCE_SPRITE_FRAMES * FRAMES_PER_CYCLE);
    sprite_load(db, &triforce_sprite, sprite, 1);
    sprite_draw(db, &triforce_sprite, 0, draw_x, draw_y_triforce, triforce_sprite.tile_w, triforce_sprite.tile_h);

    text_flush(db);
    gDPFullSync(db->p++);
    gSPEndDisplayList(db->p++);
}
