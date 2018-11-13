#ifndef EXTENDED_ITEMS_H
#define EXTENDED_ITEMS_H

#include "z64.h"

typedef uint8_t (*upgrade_fn)(z64_file_t *save, uint8_t item_id);
typedef void (*effect_fn)(z64_file_t *save, int8_t arg1, int8_t arg2);

typedef struct {
    int8_t base_item_id;
    uint8_t action_id;
    int8_t graphic_id;
    uint8_t text_id;
    uint16_t object_id;
    int8_t effect_arg1;
    int8_t effect_arg2;
    effect_fn effect;
    upgrade_fn upgrade;
} item_row_t;

uint8_t resolve_extended_item(uint8_t item_id);
item_row_t *get_extended_item_row(uint8_t item_id);

#endif
