shooting_gallery_init:
	li t0, SAVE_CONTEXT
	lw t1, 0x00(t0) ; entrance index

	beq t1, at, @@remove_shop ; Kakariko Child Day
	li at, 0x003B
	beq t1, at, @@remove_shop ; Kakariko Child Night
	li at, 0x003C
	beq t1, at, @@remove_shop ; Market Adult Day
	li at, 0x016F
	bne t1, at, @@return      ; Market Adult Night
	li at, 0x0170

@@remove_shop:
	li t2, 0xC47A0000 ; -1000.0
	sw t2, 0x28(a0) ; Y-Position

@@return:
	; Displaced Code
	jr ra
	li   t6, 0x0001
