#include <stdint.h>
#include "rainbow_sword.h"

// Massive thanks to Krimtonz for the coding help, and MZX for the tweening function!~

static uint32_t frames = 0;

const static uint32_t CYCLE_FRAMES = 10;
const static uint32_t CYCLE_FRAMES_2 = 12;

extern uint8_t RAINBOW_SWORD_ENABLED;

static colorRGB_t get_color(uint32_t f, uint32_t step_frames)
{
    int index;
    float tweenA, tweenB;

    index = (f / step_frames) % 6;

    tweenB = ((float)(f % step_frames) / step_frames);
    tweenA = 1 - tweenB;

    colorRGB_t cA = colors[index];
    colorRGB_t cB = colors[index + 1];

    colorRGB_t ret;
    ret.r = (uint8_t)((cA.r * tweenA) + (cB.r * tweenB));
    ret.g = (uint8_t)((cA.g * tweenA) + (cB.g * tweenB));
    ret.b = (uint8_t)((cA.b * tweenA) + (cB.b * tweenB));
    return ret;
}

void update_color()
{
    if (RAINBOW_SWORD_ENABLED)
    {
        frames++;
        colorRGB_t colorOuter = get_color(frames, CYCLE_FRAMES);
        colorRGB_t colorInner = get_color(frames, CYCLE_FRAMES_2);

        colorRGBA_t *sword_trail = (colorRGBA_t*)0x80115DCE;
        sword_trail[0].color = colorOuter;
        sword_trail[1].color = colorInner;
        sword_trail[2].color = colorOuter;
        sword_trail[3].color = colorInner;
    }
}