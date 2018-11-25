rainbow_bridge:
    lw      t2, RAINBOW_BRIDGE_CONDITION
    beq     t2, r0, @@rainbow_bridge_open
    li      at, 1
    beq     t2, at, @@rainbow_bridge_medallions
    lw      t2, 0x00A4(a3) ; //quest items
    
@@rainbow_bridge_dungeons:
    
    li      at, 0x1C003F ; stones and medallions
    jr      ra
    and     t2, t2, at

@@rainbow_bridge_medallions:

    li      at, 0x3F
    jr      ra
    and     t2, t2, at


@@rainbow_bridge_open:
    li      t2, 0
    jr      ra
    li      at, 0

