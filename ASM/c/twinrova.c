#include "twinrova.h"
#include "z64.h"

extern uint8_t START_TWINROVA_FIGHT;
extern uint32_t TWINROVA_ACTION_TIMER;

void clear_twinrova_vars() {
    START_TWINROVA_FIGHT = 0;
    TWINROVA_ACTION_TIMER = 0;
}
