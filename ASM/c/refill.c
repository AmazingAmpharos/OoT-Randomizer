#include "refill.h"

#include "z64.h"

void health_and_magic_refill()
{
    z64_file.refill_hearts = 0x140;
    z64_file.magic = z64_file.magic_capacity_set * 0x30;
}
