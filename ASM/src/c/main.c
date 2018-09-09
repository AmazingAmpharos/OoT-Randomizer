#include "z64.h"

#define z64_menu_state (z64_ctxt_addr + 0x10934)

#define array_size(a) (sizeof(a) / sizeof(a[0]))

extern char C_HEAP;
char *heap_next = NULL;

void heap_init() {
    heap_next = &C_HEAP;
}

void *heap_alloc(uint32_t bytes) {
    int rem = bytes % 16;
    if (rem) bytes += 16 - rem;

    void *result = heap_next;
    heap_next += bytes;
    return result;
}

typedef struct {
    Gfx *buf;
    Gfx *p;
    uint32_t buf_size;
} displaylist_t;

void displaylist_init(displaylist_t *dl, uint32_t size) {
    dl->buf = heap_alloc(sizeof(Gfx) * size);
    dl->p = dl->buf;
    dl->buf_size = size;
}

displaylist_t reset_dl = {};

#define text_bucket_count 3
#define text_bucket_size 32

typedef struct {
    displaylist_t main;
    displaylist_t text[text_bucket_count];
} dungeon_info_dls_t;

dungeon_info_dls_t dungeon_info_dls[2] = {};
int next_dl_index = 0;

#define stones_texture_vaddr 0x01A2C300
#define medals_texture_vaddr 0x01A04980
#define quest_items_texture_vaddr 0x0084DE00
extern char FONT_TEXTURE;
#define font_texture_raw ((uint8_t *)&FONT_TEXTURE)

typedef struct {
    uint8_t *buf;
    uint16_t tile_w;
    uint16_t tile_h;
    uint16_t tile_count;
    uint8_t im_fmt;
    uint8_t im_siz;
    uint8_t bytes_per_texel;
} sprite_t;

sprite_t stones_sprite = {
    NULL, 16, 16, 3,
    G_IM_FMT_RGBA, G_IM_SIZ_32b, 4
};

sprite_t medals_sprite = {
    NULL, 16, 16, 6,
    G_IM_FMT_IA, G_IM_SIZ_8b, 1
};

sprite_t quest_items_sprite = {
    NULL, 24, 24, 4,
    G_IM_FMT_RGBA, G_IM_SIZ_32b, 4
};

sprite_t font_sprite = {
    NULL, 8, 14, 95,
    G_IM_FMT_IA, G_IM_SIZ_8b, 1
};

uint32_t sprite_bytes_per_tile(sprite_t *sprite) {
    return sprite->tile_w * sprite->tile_h * sprite->bytes_per_texel;
}

uint32_t sprite_bytes(sprite_t *sprite) {
    return sprite->tile_count * sprite_bytes_per_tile(sprite);
}

typedef void (*load_file_fn_t)(uint32_t mem_addr, uint32_t rom_addr,
        uint32_t bytes);
load_file_fn_t load_file = (load_file_fn_t)0x80000DF0;

void sprite_read(sprite_t *sprite, uint32_t rom_vaddr) {
    uint32_t bytes = sprite_bytes(sprite);
    sprite->buf = heap_alloc(bytes);

    (*load_file)((uint32_t)(sprite->buf), rom_vaddr, bytes);
}

void sprite_load(displaylist_t *dl, sprite_t *sprite,
        uint32_t start_tile, uint32_t tile_count) {
    gDPLoadTextureBlock(dl->p++,
            sprite->buf + (start_tile * sprite_bytes_per_tile(sprite)),
            sprite->im_fmt, sprite->im_siz,
            sprite->tile_w, tile_count * sprite->tile_h,
            0,
            G_TX_WRAP, G_TX_WRAP,
            G_TX_NOMASK, G_TX_NOMASK,
            G_TX_NOLOD, G_TX_NOLOD);
}

void sprite_draw(displaylist_t *dl, sprite_t *sprite, uint32_t tile_index,
        uint32_t left, uint32_t top, uint32_t width, uint32_t height) {
    uint32_t width_factor = (1<<10) * sprite->tile_w / width;
    uint32_t height_factor = (1<<10) * sprite->tile_h / height;

    gSPTextureRectangle(dl->p++,
            left<<2, top<<2,
            (left + width)<<2, (top + height)<<2,
            0,
            0, (tile_index * sprite->tile_h)<<5,
            width_factor, height_factor);
}

typedef struct {
    uint8_t index;
    char label[3];
    struct {
        uint8_t has_keys : 1;
        uint8_t has_boss_key : 1;
        uint8_t has_map : 1;
        uint8_t has_compass : 1;
    };
} dungeon_entry_t;

dungeon_entry_t dungeons[] = {
    {  0, "De", 0, 0, 1, 1 }, // Deku Tree
    {  1, "DC", 0, 0, 1, 1 }, // Dodongo's Cavern
    {  2, "Ja", 0, 0, 1, 1 }, // Jabu

    {  3, "Fo", 1, 1, 1, 1 }, // Forest
    {  4, "Fi", 1, 1, 1, 1 }, // Fire
    {  5, "Wa", 1, 1, 1, 1 }, // Water
    {  7, "Sh", 1, 1, 1, 1 }, // Shadow
    {  6, "Sp", 1, 1, 1, 1 }, // Spirit

    {  8, "BW", 1, 0, 1, 1 }, // BOTW
    {  9, "IC", 0, 0, 1, 1 }, // Ice Cavern
    { 11, "TG", 1, 0, 0, 0 }, // GTG
    { 12, "GF", 1, 0, 0, 0 }, // Gerudo Fortress
    { 13, "GC", 1, 1, 0, 0 }, // Ganon's Castle
};

typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} medal_color_t;

medal_color_t medal_colors[] = {
    { 0x11, 0xC2, 0x2D }, // Forest
    { 0xD4, 0x43, 0x22 }, // Fire
    { 0x08, 0x54, 0xCE }, // Water
    { 0xD1, 0x75, 0x1A }, // Spirit
    { 0xA9, 0x3A, 0xEA }, // Shadow
    { 0xA4, 0xAB, 0x21 }, // Light
};

// FIXME: Make dynamic
uint8_t rewards[] = { 4, 1, 7, 5, 0, 8, 6, 2, -1, -1, -1, -1, -1, -1 };
uint8_t dungeon_is_mq[] = { 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0 };

void c_init() {
    heap_init();

    sprite_read(&stones_sprite, stones_texture_vaddr);
    sprite_read(&medals_sprite, medals_texture_vaddr);
    sprite_read(&quest_items_sprite, quest_items_texture_vaddr);

    int font_bytes = sprite_bytes(&font_sprite);
    font_sprite.buf = heap_alloc(font_bytes);
    for (int i = 0; i < font_bytes / 2; i++) {
        font_sprite.buf[2*i] = (font_texture_raw[i] >> 4) | 0xF0;
        font_sprite.buf[2*i + 1] = font_texture_raw[i] | 0xF0;
    }

    for (int i = 0; i < 2; i++) {
        dungeon_info_dls_t *di_dls = &(dungeon_info_dls[i]);
        displaylist_init(&(di_dls->main), 512);
        for (int j = 0; j < text_bucket_count; j++) {
            displaylist_init(&(di_dls->text[j]), 256);
        }
    }

    displaylist_t *r = &reset_dl;
    displaylist_init(r, 32);

    gDPPipeSync(r->p++);
    gSPLoadGeometryMode(r->p++, 0);
    gDPSetScissor(r->p++, G_SC_NON_INTERLACE,
                  0, 0, Z64_SCREEN_WIDTH, Z64_SCREEN_HEIGHT);
    gDPSetAlphaDither(r->p++, G_AD_DISABLE);
    gDPSetColorDither(r->p++, G_CD_DISABLE);
    gDPSetAlphaCompare(r->p++, G_AC_NONE);
    gDPSetDepthSource(r->p++, G_ZS_PRIM);
    gDPSetCombineKey(r->p++, G_CK_NONE);
    gDPSetTextureConvert(r->p++, G_TC_FILT);
    gDPSetTextureDetail(r->p++, G_TD_CLAMP);
    gDPSetTexturePersp(r->p++, G_TP_NONE);
    gDPSetTextureLOD(r->p++, G_TL_TILE);
    gDPSetTextureLUT(r->p++, G_TT_NONE);
    gDPPipelineMode(r->p++, G_PM_NPRIMITIVE);
    gSPEndDisplayList(r->p++);
}

void text_print(displaylist_t text_dls[],
        char *s, uint16_t left, uint16_t top) {
    char c;
    while (c = *(s++)) {
        int bucket = (c - 32) / text_bucket_size;
        int tile_index = (c - 32) % text_bucket_size;

        displaylist_t *text = &(text_dls[bucket]);
        if (text->p - text->buf >= text->buf_size - 2) break;

        sprite_draw(text, &font_sprite, tile_index,
                left, top, font_sprite.tile_w, font_sprite.tile_h);
        left += font_sprite.tile_w;
    }
}

void text_flush(displaylist_t *main, displaylist_t text_dls[]) {
    for (int i = 0; i < text_bucket_count; i++) {
        displaylist_t *text = &(text_dls[i]);
        gSPEndDisplayList(text->p++);
        text->p = text->buf;

        sprite_load(main, &font_sprite,
                i * text_bucket_size, text_bucket_size);
        gSPDisplayList(main->p++, text->buf);
    }
}

void dungeon_info_draw(z64_disp_buf_t *overlay) {
    dungeon_info_dls_t *di_dls = &(dungeon_info_dls[next_dl_index]);
    next_dl_index = (next_dl_index + 1) % 2;
    displaylist_t *main = &(di_dls->main);
    main->p = main->buf;

    // The last 2 entries in the parent display list will be:
    //   gDPFullSync
    //   gSPEndDisplayList
    // Overwrite these commands with a jump to our new display list.
    overlay->p -= 2;
    gSPBranchList(overlay->p++, main->buf);

    // Call reset display list
    gSPDisplayList(main->p++, reset_dl.buf);

    // Draw backdrop

    gDPSetCycleType(main->p++, G_CYC_FILL);
    gDPSetRenderMode(main->p++, G_RM_NOOP, G_RM_NOOP2);
    gDPSetFillColor(main->p++,
            GPACK_RGBA5551(0,0,0,1)<<16 | GPACK_RGBA5551(0,0,0,1)); 
    gDPFillRectangle(main->p++,
            24, 65, 293, 195);
    gDPPipeSync(main->p++);
    gDPSetFillColor(main->p++,
            GPACK_RGBA5551(255,255,255,1)<<16 | GPACK_RGBA5551(255,255,255,1)); 
    gDPFillRectangle(main->p++,
            24 + 18, 65, 24 + 18, 195);
    gDPPipeSync(main->p++);

    // Set up to draw textures

    gDPSetCycleType(main->p++, G_CYC_1CYCLE);
    gDPSetRenderMode(main->p++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
    gDPSetCombineMode(main->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);

    int start_left = 25;
    int start_top = 66;
    int left = start_left;
    int top = start_top;
    int padding = 3;
    int dungeon_count = array_size(dungeons);

    // Draw stones

    gDPSetTextureFilter(main->p++, G_TF_BILERP);
    gDPSetPrimColor(main->p++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
    sprite_load(main, &stones_sprite, 0, stones_sprite.tile_count);

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        int reward = rewards[d->index];
        if (reward < 0 || reward >= 3) continue;

        left = start_left + ((16 + padding) * (i + 1));
        sprite_draw(main, &stones_sprite, reward,
                left, top, 16, 16);

    }

    gDPPipeSync(main->p++);

    // Draw medals

    sprite_load(main, &medals_sprite, 0, medals_sprite.tile_count);

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        int reward = rewards[d->index];
        if (reward < 3) continue;
        reward -= 3;

        medal_color_t *c = &(medal_colors[reward]);
        gDPSetPrimColor(main->p++, 0, 0, c->r, c->g, c->b, 0xFF);

        left = start_left + ((16 + padding) * (i + 1));
        sprite_draw(main, &medals_sprite, reward,
                left, top, 16, 16);
    }

    gDPPipeSync(main->p++);
    gDPSetPrimColor(main->p++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);

    // Draw master quest dungeons

    top += 16 + padding;
    left = start_left + 16 + padding;

    for (int i = 0; i < dungeon_count; i++) {
        dungeon_entry_t *d = &(dungeons[i]);
        text_print(di_dls->text, d->label, left, top);
        left += 16 + padding;
    }

    int show_mq = 1;
    if (show_mq) {
        top += 16 + padding;
        left = start_left;

        text_print(di_dls->text, "MQ", left, top);
        for (int i = 0; i < dungeon_count; i++) {
            dungeon_entry_t *d = &(dungeons[i]);
            int is_mq = dungeon_is_mq[d->index];
            left += 16 + padding;
            char *str = is_mq ? "Y" : "N";
            text_print(di_dls->text, str, left + 4, top);
        }
    }

    // Draw key counts

    top += 16 + padding;
    left = start_left;

    sprite_load(main, &quest_items_sprite, 3, 1);
    sprite_draw(main, &quest_items_sprite, 0,
            left, top, 16, 16);

    for (int i = 0; i < dungeon_count; i++) {
        left += 16 + padding;
        dungeon_entry_t *d = &(dungeons[i]);
        if (!d->has_keys) continue;

        int8_t keys = z64_file.dungeon_keys[d->index];
        if (keys < 0) keys = 0;
        if (keys > 9) keys = 9;

        char count[2] = "0";
        count[0] += keys;
        text_print(di_dls->text, count, left + 4, top);
    }

    // Draw boss keys

    top += 16 + padding;
    left = start_left;

    sprite_load(main, &quest_items_sprite, 0, 1);
    sprite_draw(main, &quest_items_sprite, 0,
            left, top, 16, 16);

    for (int i = 0; i < dungeon_count; i++) {
        left += 16 + padding;
        dungeon_entry_t *d = &(dungeons[i]);
        if (!d->has_boss_key) continue;

        if (z64_file.dungeon_items[d->index].boss_key) {
            sprite_draw(main, &quest_items_sprite, 0,
                    left, top, 16, 16);
        }
    }

    // Draw maps and compasses

    int draw_maps_and_compasses = 1;
    if (draw_maps_and_compasses) {
        // Draw maps

        top += 16 + padding;
        left = start_left;

        sprite_load(main, &quest_items_sprite, 2, 1);
        sprite_draw(main, &quest_items_sprite, 0,
                left, top, 16, 16);

        for (int i = 0; i < dungeon_count; i++) {
            left += 16 + padding;
            dungeon_entry_t *d = &(dungeons[i]);
            if (!d->has_map) continue;

            if (z64_file.dungeon_items[d->index].map) {
                sprite_draw(main, &quest_items_sprite, 0,
                        left, top, 16, 16);
            }
        }

        // Draw compasses

        top += 16 + padding;
        left = start_left;

        sprite_load(main, &quest_items_sprite, 1, 1);
        sprite_draw(main, &quest_items_sprite, 0,
                left, top, 16, 16);

        for (int i = 0; i < dungeon_count; i++) {
            left += 16 + padding;
            dungeon_entry_t *d = &(dungeons[i]);
            if (!d->has_compass) continue;

            if (z64_file.dungeon_items[d->index].compass) {
                sprite_draw(main, &quest_items_sprite, 0,
                        left, top, 16, 16);
            }
        }
    }


    // Finish

    gDPPipeSync(main->p++);
    gDPSetTextureFilter(main->p++, G_TF_POINT);
    text_flush(main, di_dls->text);

    gDPFullSync(main->p++);
    gSPEndDisplayList(main->p++);
}

void overlay_swap(z64_disp_buf_t *disp_buf, Gfx *buf, uint32_t size) {
    if (z64_game.pause_state == 6 &&
                z64_game.pause_screen == 0 &&
                !z64_game.pause_screen_changing &&
                z64_ctxt.input[0].raw.a) {
        dungeon_info_draw(disp_buf);
    }

    disp_buf->size = size;
    disp_buf->buf = buf;
    disp_buf->p = buf;
    disp_buf->d = (void*)((char*)buf + size);
}
