.definelabel Shop_Item_Save_Offset, 0xD4 + (0x2C * 0x1C) + 0x10

Check_Sold_Out:
	lh  t6, 0x1c(a0)  

	; if var is under 0x32, never sell out
	addi t5, t6, -0x32
	bltz t5, @@return
	li   v0, 0

	; t2 = bit mask
	andi t1, t5, 0x07
	li   t2, 1
	sllv t2, t2, t1

	; t1 = byte offset
	srl  t1, t5, 3

	; load byte from save
	li   t4, SAVE_CONTEXT
	add  t4, t4, t1
	lb   t3, (Shop_Item_Save_Offset)(t4)

	; mask out the bit flag
	and  t3, t3, t2

	; if not set then, do nothing
	li  v0, 0
	beqz t3, @@return
	nop

	; Else, change to sold out
	li  t5, 0x26
	sh  t5, 0x1c(a0)       ; set item to SOLD OUT
	li  v0, 1              ; return 1

@@return:
	jr  ra
	nop


Set_Sold_Out:
	lh  t6, 0x1c(a1) 

	; if var is under 0x32, never sell out
	addi t5, t6, -0x32
	bltz t5, @@return
	li   v0, 0

	; t2 = bit mask
	andi t1, t5, 0x07
	li   t2, 1
	sllv t2, t2, t1

	; t1 = byte offset
	srl  t1, t5, 3

	; load byte from save
	li   t4, SAVE_CONTEXT	
	add  t4, t4, t1
	lb   t3, (Shop_Item_Save_Offset)(t4)

	; set and save the bit flag
	or   t3, t3, t2
	sb   t3, (Shop_Item_Save_Offset)(t4)

@@return:
	jr  ra
	nop


Shop_Keeper_Init_ID:
    addiu   sp, sp, -0x10
    sw      ra, 0x08 (sp)

	slti    at, a0, 0x32
	beqz    at, @@return
    move    v0, a0

	jalr    t9
   	nop
@@return:
    lw      ra, 0x08 (sp)
    addiu   sp, sp, 0x10
    jr      ra
    nop
