#include "models.h"

#include "util.h"
#include "z64.h"

#define gi_obj_count 6
#define gi_obj_size 0x1E70

typedef struct {
    uint32_t gi_id;
    uint8_t *buf;
} gi_object_t;

gi_object_t gi_obj_slots[gi_obj_count] = {};
gi_object_t error_gi_obj = {};

void load_gi_object_file(uint32_t object_file_id, uint8_t *buf) {
    z64_object_table_t *entry = &(z64_object_table[object_file_id]);
    uint32_t vrom_start = entry->vrom_start;
    uint32_t size = entry->vrom_end - vrom_start;
    read_file(buf, vrom_start, size);
}


void load_gi_object(gi_object_t *gi_obj, uint32_t gi_id) {
    gi_obj->gi_id = gi_id;
    load_gi_object_file(0x10B, gi_obj->buf);
}

gi_object_t *get_gi_object(uint32_t gi_id) {
    for (int i = 0; i < gi_obj_count; i++) {
        gi_object_t *gi_obj = &(gi_obj_slots[i]);
        if (gi_obj->gi_id == gi_id) {
            return gi_obj;
        }
        if (gi_obj->gi_id == 0) {
            load_gi_object(gi_obj, gi_id);
            return gi_obj;
        }
    }

    return &error_gi_obj;
}

void set_gi_object_segment(gi_object_t *gi_obj) {
    z64_disp_buf_t *xlu = &(z64_ctxt.gfx->poly_xlu);
    gSPSegment(xlu->p++, 6, (uint32_t)(gi_obj->buf));

    z64_disp_buf_t *opa = &(z64_ctxt.gfx->poly_opa);
    gSPSegment(opa->p++, 6, (uint32_t)(gi_obj->buf));
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
    error_gi_obj.gi_id = 0x59;
    error_gi_obj.buf = heap_alloc(0x4D0);
    load_gi_object_file(0x148, error_gi_obj.buf);

    for (int i = 0; i < gi_obj_count; i++) {
        gi_obj_slots[i].gi_id = 0;
        gi_obj_slots[i].buf = heap_alloc(gi_obj_size);
    }
}

void models_reset() {
    for (int i = 0; i < gi_obj_count; i++) {
        gi_obj_slots[i].gi_id = 0;
    }
}

typedef void (*pre_draw_gi_obj_fn)(z64_actor_t *actor, z64_ctxt_t *global_ctxt,
        uint32_t unknown);
#define pre_draw_gi_obj_1 ((pre_draw_gi_obj_fn)0x80022438)
#define pre_draw_gi_obj_2 ((pre_draw_gi_obj_fn)0x80022554)

typedef void (*draw_gi_obj_fn)(z64_ctxt_t *global_ctxt, uint32_t gi_id_minus_1);
#define draw_gi_obj ((draw_gi_obj_fn)0x800570C0)

#define matrix_stack_pointer ((float **)0x80121204)

void models_draw(z64_actor_t *heart_piece_actor, z64_ctxt_t *global_ctxt) {
    int lookup_gi_id = 0x45;
    gi_object_t *gi_obj = get_gi_object(lookup_gi_id);

    pre_draw_gi_obj_1(heart_piece_actor, global_ctxt, 0);
    pre_draw_gi_obj_2(heart_piece_actor, global_ctxt, 0);
    set_gi_object_segment(gi_obj);
    scale_matrix(*matrix_stack_pointer, 16.0);
    draw_gi_obj(global_ctxt, gi_obj->gi_id - 1);
}
