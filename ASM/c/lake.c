#include "lake.h"

#include "z64.h"

uint8_t NO_LAKE_FILL_CUTSCENE = 0;

void check_lake_fill() {
    if (NO_LAKE_FILL_CUTSCENE && (z64_file.event_chk_inf[4] & 0x400)) {
        z64_file.event_chk_inf[6] |= 0x200;
    }
}
