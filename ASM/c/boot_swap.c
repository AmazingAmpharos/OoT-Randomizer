#include "boot_swap.h"

#include "z64.h"

#define BLOCK_QUICK_BOOTS (0x00000001 | \
    0x00000002 | \
    0x00000080 | \
    0x00000400 | \
    0x10000000 | \
    0x20000000)

uint16_t pad_pressed_raw = 0;
uint16_t pad = 0;
uint16_t pad_pressed = 0;

void check_boot_swap() {
    uint16_t z_pad = z64_ctxt.input[0].raw.pad;
    pad_pressed_raw = (pad ^ z_pad) & z_pad;
    pad = z_pad;
    pad_pressed = 0;
    pad_pressed |= pad_pressed_raw;

    if (z64_file.link_age==0) {
        // Prevent quick boots when link is in a state that he wouldn't normally be able to pause to switch boots.

        if ((z64_link.state_flags_1 & BLOCK_QUICK_BOOTS) == 0) {
            if (pad_pressed & 0x0200 && z64_file.iron_boots) {
                if (z64_file.equip_boots == 2) z64_file.equip_boots = 1;
                else z64_file.equip_boots = 2;
                z64_UpdateEquipment(&z64_game, &z64_link);
            }

            if ((pad_pressed & 0x0100) && z64_file.hover_boots) {
                if (z64_file.equip_boots == 3) z64_file.equip_boots = 1;
                else z64_file.equip_boots = 3;
                z64_UpdateEquipment(&z64_game, &z64_link);
            }
        }
    }
}
