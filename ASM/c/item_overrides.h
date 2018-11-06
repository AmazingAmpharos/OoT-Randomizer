#ifndef ITEM_OVERRIDES_H
#define ITEM_OVERRIDES_H

#include "z64.h"

typedef struct {
    union {
        uint32_t all;
        struct {
            uint32_t scene     : 8;
            uint32_t flag      : 8;
            uint32_t type      : 3;
            uint32_t player_id : 5;
            uint32_t item_id   : 8;
        };
        struct {
            uint32_t search_key : 19;
            uint32_t payload    : 13;
        };
    };
} override_t;

enum override_type {
    BASE_ITEM = 0,
    CHEST = 1,
    COLLECTABLE = 2,
    SKULL = 3,
    GROTTO_SCRUB = 4,
};

void item_overrides_init();

#endif
