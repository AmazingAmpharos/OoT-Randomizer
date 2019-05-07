#include "fog.h"

#include "z64.h"

extern uint8_t NO_FOG_STATE;

void override_fog_state() {
    if (NO_FOG_STATE) {
        z64_fog_state = 0;
    }
}
