#include "models.h"

#include "util.h"
#include "z64.h"

#define slot_count 6
#define object_size 0x1E70

typedef struct {
    uint32_t graphic_id;
    uint8_t *buf;
} loaded_object_t;

loaded_object_t slots[slot_count] = { 0 };
loaded_object_t error_object = { 0 };

void load_object_file(uint32_t object_file_id, uint8_t *buf) {
    z64_object_table_t *entry = &(z64_object_table[object_file_id]);
    uint32_t vrom_start = entry->vrom_start;
    uint32_t size = entry->vrom_end - vrom_start;
    read_file(buf, vrom_start, size);
}

void load_object(loaded_object_t *object, uint32_t graphic_id) {
    object->graphic_id = graphic_id;
    load_object_file(0x10B, object->buf);
}

loaded_object_t *get_object(uint32_t graphic_id) {
    for (int i = 0; i < slot_count; i++) {
        loaded_object_t *object = &(slots[i]);
        if (object->graphic_id == graphic_id) {
            return object;
        }
        if (object->graphic_id == 0) {
            load_object(object, graphic_id);
            return object;
        }
    }

    return &error_object;
}

void set_object_segment(loaded_object_t *object) {
    z64_disp_buf_t *xlu = &(z64_ctxt.gfx->poly_xlu);
    gSPSegment(xlu->p++, 6, (uint32_t)(object->buf));

    z64_disp_buf_t *opa = &(z64_ctxt.gfx->poly_opa);
    gSPSegment(opa->p++, 6, (uint32_t)(object->buf));
}

void scale_matrix(float *matrix, float scale_factor) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            matrix[4*i + j] *= scale_factor;
        }
    }
}

void models_init() {
    // Use SOLD OUT model to indicate that an error occured
    error_object.graphic_id = 0x59;
    error_object.buf = heap_alloc(0x4D0);
    load_object_file(0x148, error_object.buf);

    for (int i = 0; i < slot_count; i++) {
        slots[i].graphic_id = 0;
        slots[i].buf = heap_alloc(object_size);
    }
}

void models_reset() {
    for (int i = 0; i < slot_count; i++) {
        slots[i].graphic_id = 0;
    }
}

typedef void (*pre_draw_fn)(z64_actor_t *actor, z64_ctxt_t *global_ctxt,
        uint32_t unknown);
#define pre_draw_1 ((pre_draw_fn)0x80022438)
#define pre_draw_2 ((pre_draw_fn)0x80022554)

typedef void (*draw_fn)(z64_ctxt_t *global_ctxt, uint32_t gi_id_minus_1);
#define draw_model ((draw_fn)0x800570C0)

#define matrix_stack_pointer ((float **)0x80121204)

void models_draw(z64_actor_t *heart_piece_actor, z64_ctxt_t *global_ctxt) {
    int lookup_graphic_id = 0x45;
    loaded_object_t *object = get_object(lookup_graphic_id);

    pre_draw_1(heart_piece_actor, global_ctxt, 0);
    pre_draw_2(heart_piece_actor, global_ctxt, 0);
    set_object_segment(object);
    scale_matrix(*matrix_stack_pointer, 16.0);
    draw_model(global_ctxt, object->graphic_id - 1);
}
