#include <stdint.h>
#include "heart_colors.h"

extern uint8_t CFG_HEART_COLOR_R;
extern uint8_t CFG_HEART_COLOR_G;
extern uint8_t CFG_HEART_COLOR_B;

colorRGB_t defaultHeart = { 0xFF, 0x46, 0x32 };
colorRGB_t defaultDDHeart = { 0xC8, 0x00, 0x00 };

static colorRGB_t get_color() {
  colorRGB_t ret;
  ret.r = CFG_HEART_COLOR_R;
  ret.g = CFG_HEART_COLOR_G;
  ret.b = CFG_HEART_COLOR_B;
  return ret;
}

void update_heart_colors() {
  colorRGB_t heartColor = get_color();

  colorRGB_t *beating_no_dd = (colorRGB_t *)0x801D8B92;
  beating_no_dd[0] = heartColor;

  colorRGB_t *normal_no_dd = (colorRGB_t *)0x801D8B9E;
  normal_no_dd[0].r = heartColor.r;
  normal_no_dd[0].b = heartColor.g;
  normal_no_dd[1].g = heartColor.b;

  if((defaultHeart.r == heartColor.r) && (defaultHeart.g == heartColor.g) && (defaultHeart.b == heartColor.b)) {
    heartColor.r = defaultDDHeart.r;
    heartColor.g = defaultDDHeart.g;
    heartColor.b = defaultDDHeart.b;
  }
  
  colorRGB_t *beating_dd = (colorRGB_t *)0x8011BD38;
  beating_dd[0] = heartColor;

  colorRGB_t *normal_dd = (colorRGB_t*)0x8011BD50;
  normal_dd[0] = heartColor;
}