#include "twinrova.h"
#include "z64.h"

extern uint8_t START_TWINROVA_FIGHT;
extern uint8_t TWINROVA_MOVE_TIMER;

void clear_twinrova_flag() {
    START_TWINROVA_FIGHT = 0;
    TWINROVA_MOVE_TIMER = 0;
}

