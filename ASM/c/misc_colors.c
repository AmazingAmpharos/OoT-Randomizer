#include <stdint.h>
#include "misc_colors.h"
#include "rainbow.h"
#include "z64.h"

#define CYCLE_FRAMES_OUTER 10
#define CYCLE_FRAMES_INNER 12

static uint32_t frames = 0;

extern uint8_t CFG_RAINBOW_SWORD_INNER_ENABLED;
extern uint8_t CFG_RAINBOW_SWORD_OUTER_ENABLED;

void update_sword_trail_colors()
{
    colorRGBA8_t *sword_trail_colors = (colorRGBA8_t*)0x80115DCE;

    if (CFG_RAINBOW_SWORD_INNER_ENABLED)
    {
        colorRGB8_t color_inner = get_rainbow_color(frames, CYCLE_FRAMES_INNER);
        sword_trail_colors[1].color = color_inner;
        sword_trail_colors[3].color = color_inner;
    }

    if (CFG_RAINBOW_SWORD_OUTER_ENABLED)
    {
        colorRGB8_t color_outer = get_rainbow_color(frames, CYCLE_FRAMES_OUTER);
        sword_trail_colors[0].color = color_outer;
        sword_trail_colors[2].color = color_outer;
    }
}

extern colorRGB8_t CFG_BOOM_TRAIL_INNER_COLOR;
extern colorRGB8_t CFG_BOOM_TRAIL_OUTER_COLOR;

extern uint8_t CFG_RAINBOW_BOOM_TRAIL_INNER_ENABLED;
extern uint8_t CFG_RAINBOW_BOOM_TRAIL_OUTER_ENABLED;

void update_boomerang_trail_colors()
{
    z64_actor_t *boomerang = z64_link.boomerang_actor;
    if (boomerang != NULL && boomerang->main_proc != NULL)
    {
        uint32_t effect_index = *((uint32_t*)(((uint32_t)boomerang) + 0x1C8));

        if (effect_index < 31)
        {
            z64_trail_t *trail = ((z64_trail_t*)0x80115C3C) + effect_index - 3;

            if (CFG_RAINBOW_BOOM_TRAIL_INNER_ENABLED)
            {
                trail->fx.p1_start.color = get_rainbow_color(frames, CYCLE_FRAMES_INNER);
                trail->fx.p1_end.color = get_rainbow_color(frames + CYCLE_FRAMES_INNER, CYCLE_FRAMES_INNER);
            }
            else
            {
                trail->fx.p1_start.color = CFG_BOOM_TRAIL_INNER_COLOR;
                trail->fx.p1_end.color = CFG_BOOM_TRAIL_INNER_COLOR;
            }

            if (CFG_RAINBOW_BOOM_TRAIL_OUTER_ENABLED)
            {
                trail->fx.p2_start.color = get_rainbow_color(frames, CYCLE_FRAMES_OUTER);
                trail->fx.p2_end.color = get_rainbow_color(frames + CYCLE_FRAMES_OUTER, CYCLE_FRAMES_OUTER);
            }
            else
            {
                trail->fx.p2_start.color = CFG_BOOM_TRAIL_OUTER_COLOR;
                trail->fx.p2_end.color = CFG_BOOM_TRAIL_OUTER_COLOR;
            }
        }
    }
}

typedef struct
{
    colorRGBA8_t inner;
    colorRGBA8_t outer;
} navi_color_t;

extern uint8_t CFG_RAINBOW_NAVI_IDLE_INNER_ENABLED;
extern uint8_t CFG_RAINBOW_NAVI_IDLE_OUTER_ENABLED;
extern uint8_t CFG_RAINBOW_NAVI_ENEMY_INNER_ENABLED;
extern uint8_t CFG_RAINBOW_NAVI_ENEMY_OUTER_ENABLED;
extern uint8_t CFG_RAINBOW_NAVI_NPC_INNER_ENABLED;
extern uint8_t CFG_RAINBOW_NAVI_NPC_OUTER_ENABLED;
extern uint8_t CFG_RAINBOW_NAVI_PROP_INNER_ENABLED;
extern uint8_t CFG_RAINBOW_NAVI_PROP_OUTER_ENABLED;

void update_navi_colors()
{
    int rainbow_inner_enabled = 0;
    int rainbow_outer_enabled = 0;

    switch (z64_game.target_actor_type)
    {
        case ACTORTYPE_PLAYER:
            rainbow_inner_enabled = CFG_RAINBOW_NAVI_IDLE_INNER_ENABLED;
            rainbow_outer_enabled = CFG_RAINBOW_NAVI_IDLE_OUTER_ENABLED;
            break;
        case ACTORTYPE_ENEMY:
        case ACTORTYPE_BOSS:
            rainbow_inner_enabled = CFG_RAINBOW_NAVI_ENEMY_INNER_ENABLED;
            rainbow_outer_enabled = CFG_RAINBOW_NAVI_ENEMY_OUTER_ENABLED;
            break;
        case ACTORTYPE_NPC:
            rainbow_inner_enabled = CFG_RAINBOW_NAVI_NPC_INNER_ENABLED;
            rainbow_outer_enabled = CFG_RAINBOW_NAVI_NPC_OUTER_ENABLED;
            break;
        default:
            rainbow_inner_enabled = CFG_RAINBOW_NAVI_PROP_INNER_ENABLED;
            rainbow_outer_enabled = CFG_RAINBOW_NAVI_PROP_OUTER_ENABLED;
            break;
    }

    if (!rainbow_inner_enabled && !rainbow_outer_enabled)
        return;

    colorRGB8_t color_inner = get_rainbow_color(frames, CYCLE_FRAMES_INNER);
    colorRGB8_t color_outer = get_rainbow_color(frames, CYCLE_FRAMES_OUTER);

    navi_color_t *navi_ref_colors = (navi_color_t*)0x800E8214;
    if (rainbow_inner_enabled)
        navi_ref_colors[z64_game.target_actor_type].inner.color = color_inner;
    if (rainbow_outer_enabled)
        navi_ref_colors[z64_game.target_actor_type].outer.color = color_outer;

    for (int i = 0; i < 3; i++)
    {
        if (rainbow_inner_enabled)
            z64_game.target_arr[i].color = color_inner;
    }

    z64_actor_t *navi = z64_link.navi_actor;
    if (navi != NULL && navi->main_proc != NULL)
    {
        colorRGBAf_t *navi_colors = (colorRGBAf_t*)(((uint32_t)navi) + 0x234);
        if (rainbow_inner_enabled)
        {
            navi_colors[0].r = color_inner.r;
            navi_colors[0].g = color_inner.g;
            navi_colors[0].b = color_inner.b;
        }
        if (rainbow_outer_enabled)
        {
            navi_colors[1].r = color_outer.r;
            navi_colors[1].g = color_outer.g;
            navi_colors[1].b = color_outer.b;
        }
    }
}

void update_misc_colors()
{
    frames++;
    update_sword_trail_colors();
    update_boomerang_trail_colors();
    update_navi_colors();
}
