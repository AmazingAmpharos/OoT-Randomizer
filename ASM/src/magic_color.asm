magic_colors:
    lb    t8, CFG_MAGIC_COLOR_RED
    sb    t8, 0x0795 (t6)
    lb    t8, CFG_MAGIC_COLOR_GREEN
    sb    t8, 0x0797 (t6)
    lb    t8, CFG_MAGIC_COLOR_BLUE
    sb    t8, 0x0799 (t6)
    addu  t8, r0, t6
    jr    ra