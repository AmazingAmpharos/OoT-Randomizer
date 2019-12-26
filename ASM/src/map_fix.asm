write_dungeon_entrance_marker:
    ; t6 has upper word of graphics command: (cmd << 24) | (right << 12) | bottom
    ; t8 is available as scratch
    lh      v1, 0x0000(t3) ; displaced code
    lw      t7, 0x004C(a0) ; displaced code
    or      t8, t6, r0 ; original graphics command upper word
    srl     t6, t6, 12
    andi    t6, t6, 0x0FFF ; get right x-coordinate of dungeon entrance marker
    sltiu   t6, t6, 0x0100 ; check if marker is in the leftmost 64 pixels of the screen
    beqz    t6, @@done
    sll     t6, t8, 8
    srl     t8, t6, 8 ; set upper 8 bits to 0x00, a no-op graphics command
@@done:
    jr      ra
    sw      t8, 0x0000(v0)
