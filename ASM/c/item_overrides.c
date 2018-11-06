#include "item_overrides.h"

#include "extended_items.h"
#include "util.h"
#include "z64.h"

override_t cfg_item_overrides[512] = { 0 };
int item_overrides_count = 0;

typedef struct {
    union {
        uint32_t all;
        struct {
            uint8_t item_id;
            uint8_t scene;
            uint8_t source_tag;
            uint8_t padding_;
        };
    };
} pending_item_t;

pending_item_t pending_item_queue[3] = { 0 };
z64_actor_t *dummy_actor = NULL;

int item_is_extended = 0;
item_row_t extended_item_data = { 0 };

// Pointers into extended_item_data for convenience in ASM
int8_t *ext_base_item_id = &(extended_item_data.base_item_id);
int8_t *ext_action_id = &(extended_item_data.action_id);
int8_t *ext_graphic_id = &(extended_item_data.graphic_id);
int8_t *ext_text_id = &(extended_item_data.text_id);
int16_t *ext_object_id = &(extended_item_data.object_id);
int8_t *ext_effect_arg1 = &(extended_item_data.effect_arg1);
int8_t *ext_effect_arg2 = &(extended_item_data.effect_arg2);
effect_fn *ext_effect = &(extended_item_data.effect);

void item_overrides_init() {
    while (cfg_item_overrides[item_overrides_count].all != 0) {
        item_overrides_count++;
    }

    // Create an actor satisfying the minimum requirements to give the player an item
    dummy_actor = heap_alloc(sizeof(z64_actor_t));
    dummy_actor->main_proc = (void *)1;
}

void give_pending_item() {
    pending_item_t first = pending_item_queue[0];
    if (first.all == 0) {
        return;
    }

    // Don't give pending item if the player is already receiving an item.
    if (z64_link.actor_giving_item != 0) {
        return;
    }
    // Don't give pending item during cutscene. This can lead to a crash when giving an item
    // during another item cutscene.
    if (z64_link.state_flags_1 & 0x20) {
        return;
    }
    // Don't give an item if link's camera is not being used
    // If an item is given in this state then it will cause the
    // Walking-While-Talking glitch.
    if (z64_game.camera_2) {
        return;
    }

    z64_link.received_item_id = first.item_id;
    z64_link.actor_giving_item = dummy_actor;
}

// Source tags:
// 1: incoming co-op item
// 2: great fairy
// 3: light arrow cutscene
// 4: fairy ocarina cutscene
// 5: ocarina songs

void push_pending_item(uint8_t item_id, uint8_t source_tag) {
    for (int i = 0; i < array_size(pending_item_queue); i++) {
        pending_item_t *entry = &(pending_item_queue[i]);
        if (entry->all == 0) {
            entry->item_id = item_id;
            entry->scene = z64_game.scene_index;
            entry->source_tag = source_tag;
            break;
        }
        if (entry->source_tag == source_tag) {
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

void item_received() {
    if (z64_link.actor_giving_item == dummy_actor) {
        pop_pending_item();
    }
}

override_t get_override_search_key(uint8_t scene, uint8_t item_id, z64_actor_t *actor) {
    override_t result = { 0 };
    result.scene = scene;

    if (actor->actor_id == 0x0A) {
        // Don't override WINNER heart piece in the chest minigame scene
        if (scene == 0x10 && item_id == 0x75) {
            return (override_t){ .all = -1 };
        }

        result.type = CHEST;
        result.flag = actor->variable & 0x1F;
    } else if (actor->actor_id == 0x15) {
        // Only override heart pieces and keys
        if (item_id != 0x3E && item_id != 0x42) {
            return (override_t){ .all = -1 };
        }

        result.type = COLLECTABLE;
        result.flag = *((uint8_t *)(actor + 0x141));
    } else if (actor->actor_id == 0x19C) {
        result.type = SKULL;
        result.flag = actor->variable & 0xFF;
        result.scene = (actor->variable >> 8) & 0x1F;
    } else if (scene == 0x3E && actor->actor_id == 0x011A) {
        result.type = GROTTO_SCRUB;
        result.flag = item_id;
        result.scene = z64_file.grotto_id;
    } else {
        result.type = BASE_ITEM;
        result.flag = item_id;
    }

    return result;
}

int search_item_overrides(override_t key) {
    int start = 0;
    int end = item_overrides_count - 1;
    while (start <= end) {
        int mid = (start + end) / 2;
        override_t *mid_entry = &(cfg_item_overrides[mid]);
        if (key.search_key < mid_entry->search_key) {
            end = mid - 1;
        } else if (key.search_key > mid_entry->search_key) {
            start = mid + 1;
        } else {
            return mid;
        }
    }
    return -1;
}

uint8_t resolve_extended_item(uint8_t item_id) {
    for (;;) {
        if (item_id < 0x80) {
            return item_id;
        }

        item_row_t *item = get_extended_item_row(item_id);
        uint8_t new_item_id = item->upgrade(&z64_file, item_id);
        if (new_item_id == item_id) {
            return item_id;
        }
        item_id = new_item_id;
    }
}

void store_item_data() {
    item_is_extended = 0;
    extended_item_data = (item_row_t){ 0 };

    int8_t item_id = z64_link.received_item_id;
    if (item_id == 0) {
        return;
    }
    if (item_id < 0) {
        item_id = -item_id;
    }

    if (item_id == 0x7F) {
        // Do co-op stuff
    }

    z64_actor_t *actor = z64_link.actor_giving_item;
    uint8_t scene = actor == dummy_actor ?
        pending_item_queue[0].scene :
        z64_game.scene_index;

    override_t search_key = get_override_search_key(scene, item_id, actor);
    if (search_key.all == -1) {
        return;
    }

    int override_index = search_item_overrides(search_key);
    if (override_index == -1) {
        return;
    }
    override_t *override = &(cfg_item_overrides[override_index]);

    if (override->player_id != 0) {
        // Do co-op stuff
        //return;
    }

    uint8_t resolved_item_id = resolve_extended_item(override->item_id);
    int8_t new_base_item_id = resolved_item_id;
    if (resolved_item_id >= 0x80) {
        item_is_extended = 1;
        extended_item_data = *(get_extended_item_row(resolved_item_id));
        new_base_item_id = extended_item_data.base_item_id;
    }

    if (actor->actor_id == 0x0A) {
        // Update chest contents
        actor->variable = (actor->variable & 0xF01F) | (new_base_item_id << 5);
    }

    if (z64_link.received_item_id < 0) {
        new_base_item_id = -new_base_item_id;
    }
    z64_link.received_item_id = new_base_item_id;
}
