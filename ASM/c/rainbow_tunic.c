#include "gfx.h"
#include "util.h"
#include "z64.h"

uint32_t cfg_rainbow_kokiri_tunic = 0;
uint32_t cfg_rainbow_goron_tunic = 0;
uint32_t cfg_rainbow_zora_tunic = 0;
uint32_t frames = 0;

const uint32_t CYCLE_FRAMES = 0x30;

typedef struct
{
	uint8_t r;
	uint8_t g;
	uint8_t b;
} colorRGB_t;


colorRGB_t colors[] =
{
	{ 0xE0, 0x10, 0x10 }, //red
	{ 0xE0, 0xE0, 0x10 }, //yellow
	{ 0x10, 0xE0, 0x10 }, //green
	{ 0x10, 0xE0, 0xE0 }, //cyan
	{ 0x10, 0x10, 0xE0 }, //blue
	{ 0xE0, 0x10, 0xE0 }, //purple
	{ 0xE0, 0x10, 0x10 }, //red
};

colorRGB_t get_color(int index, int f)
{
	float tweenA, tweenB;

	tweenB = ((float)f / CYCLE_FRAMES);
	tweenA = 1 - tweenB;

	uint8_t r, g, b; 

	colorRGB_t cA = colors[index];
	colorRGB_t cB = colors[index + 1];

	r = (uint8_t)((cA.r * tweenA) + (cB.r * tweenB));
	g = (uint8_t)((cA.g * tweenA) + (cB.g * tweenB));
	b = (uint8_t)((cA.b * tweenA) + (cB.b * tweenB));

	return { r, g, b };
}

void update_color()
{
	if (!cfg_rainbow_kokiri_tunic
		|| !cfg_rainbow_goron_tunic
		|| !cfg_zora_zora_tunic )
		return;

	frames++;
	if (frames >= CYCLE_FRAMES * 6)
		frames = 0;

	int index = frames / CYCLE_FRAMES;
	int f = frames % CYCLE_FRAMES;

	colorRGB_t color = get_color(index, f);
}