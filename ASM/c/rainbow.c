#include <stdint.h>
#include "rainbow.h"
#include "color.h"

// Massive thanks to Krimtonz for the coding help, and MZX for the tweening function!~

static colorRGB8_t cycle_colors[] =
{
    { 0xE0, 0x10, 0x10 }, // red
    { 0xE0, 0xE0, 0x10 }, // yellow
    { 0x10, 0xE0, 0x10 }, // green
    { 0x10, 0xE0, 0xE0 }, // cyan
    { 0x10, 0x10, 0xE0 }, // blue
    { 0xE0, 0x10, 0xE0 }, // purple
    { 0xE0, 0x10, 0x10 }, // red
};

colorRGB8_t get_rainbow_color(uint32_t f, uint32_t step_frames)
{
    int index;
    float tweenA, tweenB;

    index = (f / step_frames) % 6;

    tweenB = ((float)(f % step_frames) / step_frames);
    tweenA = 1 - tweenB;

    colorRGB8_t cA = cycle_colors[index];
    colorRGB8_t cB = cycle_colors[index + 1];

    colorRGB8_t ret;
    ret.r = (uint8_t)((cA.r * tweenA) + (cB.r * tweenB));
    ret.g = (uint8_t)((cA.g * tweenA) + (cB.g * tweenB));
    ret.b = (uint8_t)((cA.b * tweenA) + (cB.b * tweenB));
    return ret;
}
