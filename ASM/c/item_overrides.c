#include "item_overrides.h"

#include "extended_items.h"
#include "util.h"
#include "z64.h"

enum override_type {
    BASE_ITEM = 0,
    CHEST = 1,
    COLLECTABLE = 2,
    SKULL = 3,
    GROTTO_SCRUB = 4,
    DELAYED = 5,
};

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

override_t cfg_item_overrides[512] = { 0 };
int item_overrides_count = 0;

override_t pending_item_queue[3] = {
    { .all = 0 },
    { .all = 0 },
    { .all = 0 },
};
z64_actor_t *dummy_actor = NULL;

item_row_t *extended_item_row = NULL;
// Split extended_item_row into variables for convenience in ASM
uint32_t ext_base_item_id = 0;
uint32_t ext_action_id = 0;
uint32_t ext_graphic_id = 0;
uint32_t ext_text_id = 0;
uint32_t ext_object_id = 0;

void activate_extended_item(item_row_t *item_row) {
    extended_item_row = item_row;
    ext_base_item_id = item_row->base_item_id;
    ext_action_id = item_row->action_id;
    ext_graphic_id = item_row->graphic_id;
    ext_text_id = item_row->text_id;
    ext_object_id = item_row->object_id;
}

void clear_extended_item() {
    extended_item_row = NULL;
    ext_base_item_id = 0;
    ext_action_id = 0;
    ext_graphic_id = 0;
    ext_text_id = 0;
    ext_object_id = 0;
}

void item_overrides_init() {
    while (cfg_item_overrides[item_overrides_count].all != 0) {
        item_overrides_count++;
    }

    // Create an actor satisfying the minimum requirements to give the player an item
    dummy_actor = heap_alloc(sizeof(z64_actor_t));
    dummy_actor->main_proc = (void *)1;
}

override_t get_override_search_key(uint8_t scene, uint8_t item_id, z64_actor_t *actor) {
    if (actor->actor_id == 0x0A) {
        // Don't override WINNER heart piece in the chest minigame scene
        if (scene == 0x10 && item_id == 0x75) {
            return (override_t){ .all = 0 };
        }

        return (override_t){
            .scene = scene,
            .type = CHEST,
            .flag = actor->variable & 0x1F,
        };
    } else if (actor->actor_id == 0x15) {
        // Only override heart pieces and keys
        if (item_id != 0x3E && item_id != 0x42) {
            return (override_t){ .all = 0 };
        }

        return (override_t){
            .scene = scene,
            .type = COLLECTABLE,
            .flag = *((uint8_t *)(actor + 0x141)),
        };
    } else if (actor->actor_id == 0x19C) {
        return (override_t){
            .scene = (actor->variable >> 8) & 0x1F,
            .type = SKULL,
            .flag = actor->variable & 0xFF,
        };
    } else if (scene == 0x3E && actor->actor_id == 0x011A) {
        return (override_t){
            .scene = z64_file.grotto_id,
            .type = GROTTO_SCRUB,
            .flag = item_id,
        };
    } else {
        return (override_t) {
            .scene = scene,
            .type = BASE_ITEM,
            .flag = item_id,
        };
    }
}

override_t lookup_override_by_key(override_t key) {
    int start = 0;
    int end = item_overrides_count - 1;
    while (start <= end) {
        int mid_index = (start + end) / 2;
        override_t mid_entry = cfg_item_overrides[mid_index];
        if (key.search_key < mid_entry.search_key) {
            end = mid_index - 1;
        } else if (key.search_key > mid_entry.search_key) {
            start = mid_index + 1;
        } else {
            return mid_entry;
        }
    }
    return (override_t){ .all = 0 };
}

override_t lookup_override(uint8_t scene, uint8_t item_id, z64_actor_t *actor) {
    override_t search_key = get_override_search_key(scene, item_id, actor);
    if (search_key.all == 0) {
        return (override_t){ .all = 0 };
    }

    return lookup_override_by_key(search_key);
}

int8_t activate_override(override_t override) {
    uint8_t resolved_item_id = resolve_extended_item(override.item_id);
    item_row_t *item_row = get_extended_item_row(resolved_item_id);
    if (item_row) {
        activate_extended_item(item_row);
        return item_row->base_item_id;
    } else {
        clear_extended_item();
        return resolved_item_id;
    }
}

void get_item(z64_actor_t *from_actor, z64_link_t *link, int8_t incoming_item_id) {
    override_t override = { .all = 0 };
    int incoming_negative = incoming_item_id < 0;

    if (from_actor && incoming_item_id != 0) {
        int8_t item_id = incoming_negative ? -incoming_item_id : incoming_item_id;
        override = lookup_override(z64_game.scene_index, item_id, from_actor);
    }

    if (override.all == 0) {
        clear_extended_item();
        link->incoming_item_id = incoming_item_id;
        return;
    }

    int8_t base_item_id = activate_override(override);

    if (from_actor->actor_id == 0x0A) {
        // Update chest contents
        from_actor->variable = (from_actor->variable & 0xF01F) | (base_item_id << 5);
    }

    link->incoming_item_id = incoming_negative ? -base_item_id : base_item_id;
}

void give_pending_item() {
    override_t override = pending_item_queue[0];

    // Don't give pending item if:
    // - Already receiving an item from an ordinary source
    // - Link is in cutscene state (causes crash)
    // - Link's camera is not being used (causes walking-while-talking glitch)
    int no_pending = override.all == 0 ||
        (z64_link.incoming_item_actor && z64_link.incoming_item_id > 0) ||
        z64_link.state_flags_1 & 0x20000000 ||
        z64_game.camera_2;
    if (no_pending) {
        return;
    }

    if (override.item_id == 0x7F) {
        // Do co-op stuff
    }

    if (override.player_id != 1) {
        // Do co-op stuff
    }

    int8_t base_item_id = activate_override(override);

    z64_link.incoming_item_actor = dummy_actor;
    z64_link.incoming_item_id = base_item_id;
}

void push_pending_item(override_t override) {
    for (int i = 0; i < array_size(pending_item_queue); i++) {
        if (pending_item_queue[i].all == 0) {
            pending_item_queue[i] = override;
            break;
        }
        if (pending_item_queue[i].all == override.all) {
            // Prevent duplicate entries
            break;
        }
    }
}

void pop_pending_item() {
    pending_item_queue[0] = pending_item_queue[1];
    pending_item_queue[1] = pending_item_queue[2];
    pending_item_queue[2].all = 0;
}

void give_delayed_item(uint8_t flag) {
    override_t search_key = { .all = 0 };
    search_key.scene = 0xFF;
    search_key.type = DELAYED;
    search_key.flag = flag;
    override_t override = lookup_override_by_key(search_key);
    if (override.all != 0) {
        push_pending_item(override);
    }
}

void item_received() {
    clear_extended_item();
    if (z64_link.incoming_item_actor == dummy_actor) {
        pop_pending_item();
    }
}
