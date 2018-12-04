rainbow_bridge:
    lw      t2, RAINBOW_BRIDGE_CONDITION
    beq     t2, r0, @@rainbow_bridge_open
    li      at, 1
    beq     t2, at, @@rainbow_bridge_medallions
    lw      t2, 0x00A4(a3) ; //quest items

	li		at, 3
	beq		t2, at, @@rainbow_bridge_stones
	li		at, 0x1C0000 ; stones

	li		at, 4
	beq		t2, at, @@rainbow_bridge_vanilla
	li		at, 0x18

    
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

@@rainbow_bridge_vanilla:
	lbu		t7, 0x74(a3) ; Light arrow slot
	li		t9, 0x12 
	and		t2, t2, at
	bne		t2, at, @@return
	li		t2, 0x00
	li		t2, 0x18
@@return:
	jr		ra
	nop


@@rainbow_bridge_stones:
	jr		ra
	and		t2, t2, at 