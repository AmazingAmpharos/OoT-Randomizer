#include "triforce.h"
#include "gfx.h"
#include "text.h"
#include "util.h"
#include "z64.h"

static uint32_t frames = 0;
static uint32_t render_triforce_flag = 0;
#define FRAMES_PER_CYCLE 2
#define TRIFORCE_SPRITE_FRAMES 16
#define TRIFORCE_FRAMES_VISIBLE 100 // About 5 seconds
#define TRIFORCE_FRAMES_FADE_AWAY 80 // About 4 seoconds
#define TRIFORCE_FRAMES_FADE_INTO 20 // About 1 second
extern uint32_t RAINBOW_BRIDGE_CONDITION;
extern uint32_t TRIFORCE_PIECES_REQUIRED;

#define MY_DEBUG_POINT ( (uint32_t*) 0x80480000 )

void set_triforce_render() {
    render_triforce_flag = 1;
}

void draw_triforce_count(z64_disp_buf_t *db) {
    
    // Must be triforce hunt and triforce should be drawable, and we should either be on the pause screen or the render triforce flag should be set
    if (!(RAINBOW_BRIDGE_CONDITION == 6 && CAN_DRAW_TRIFORCE && (render_triforce_flag == 1 || z64_game.pause_ctxt.state == 6))) {
        return;
    }
    
    uint8_t alpha;
    // In the pause screen always draw
    if (z64_game.pause_ctxt.state == 6) {
        alpha = 255;
        frames = frames % (TRIFORCE_SPRITE_FRAMES * FRAMES_PER_CYCLE);
    } else {
        // Do a fade in/out effect if not in pause screen
        if ( frames <= TRIFORCE_FRAMES_FADE_INTO ) {
            alpha = frames * 255 / TRIFORCE_FRAMES_FADE_INTO;
        } else if (frames <= TRIFORCE_FRAMES_FADE_INTO + TRIFORCE_FRAMES_VISIBLE ) {
            alpha = 255;
        } else if (frames <= TRIFORCE_FRAMES_FADE_INTO + TRIFORCE_FRAMES_VISIBLE + TRIFORCE_FRAMES_FADE_AWAY) {
            alpha = frames * 255 /  TRIFORCE_FRAMES_FADE_AWAY;
            alpha = 255 - alpha;
        } else {
            render_triforce_flag = 0;
            frames = 0;
            return;
        }
    }

    frames++;

    // Call setup display list and setup draw coords
    gSPDisplayList(db->p++, &setup_db);

    int total_w = 5 * font_sprite.tile_w + triforce_sprite.tile_w;
    int draw_x = Z64_SCREEN_WIDTH / 2 - total_w / 2;
    int draw_y_text = Z64_SCREEN_HEIGHT - (font_sprite.tile_h * 1.5) + 1;
    int draw_y_triforce = Z64_SCREEN_HEIGHT - (triforce_sprite.tile_h * 1.5) + 3 + 1;

    gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetPrimColor(db->p++, 0, 0, 0xDA, 0xD3, 0x0B, alpha);

    // Draw count
    int pieces = z64_file.scene_flags[0x48].unk_00_; //Unused word in scene x48. 
    int tens_place = (pieces / 10) % 10;
    int ones_place = pieces % 10;

    int required_tens_place = (TRIFORCE_PIECES_REQUIRED / 10) % 10;
    int required_ones_place = TRIFORCE_PIECES_REQUIRED % 10;

    char text[] = { (char) (tens_place + 48), (char) (ones_place + 48), (char) 0x2F , (char) (required_tens_place + 48), (char) (required_ones_place + 48)  };
    text_print(text , draw_x, draw_y_text);
    draw_x += 5 * font_sprite.tile_w;

    gDPSetPrimColor(db->p++, 0, 0, 0xF4, 0xEC, 0x30, alpha);
    // Draw triforce
    int sprite = (frames / FRAMES_PER_CYCLE) % TRIFORCE_SPRITE_FRAMES;
    sprite_load(db, &triforce_sprite, sprite, 1);
    sprite_draw(db, &triforce_sprite, 0, draw_x, draw_y_triforce, triforce_sprite.tile_w, triforce_sprite.tile_h);

    text_flush(db);
    gDPFullSync(db->p++);
    gSPEndDisplayList(db->p++);
}
