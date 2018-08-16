Check_Sold_Out:
	lh  t6, 0x1c(a0)       ; t0 = var

	li  t1, SHOP_ITEM_SAVE_MASK
	sll t0, t6, 1
	add t1, t1, t0
	lh  t2, 0x00(t1)       ; t2 = shop mask
	li  t1, SAVE_CONTEXT
	lh  t3, 0x0F30(t1)     ; t3 = shop flags
	and t4, t2, t3                        

	li  v0, 0
	beqz t4, @@return      ; if flag is not set, return 0
	nop

	li  t5, 0x26
	sh  t5, 0x1c(a0)       ; set item to SOLD OUT

	li  v0, 1              ; return 1

@@return:
	jr  ra
	nop


Set_Sold_Out:
	lh  t6, 0x1c(a1)       ; t0 = var

	li  t1, SHOP_ITEM_SAVE_MASK
	sll t0, t6, 1
	add t1, t1, t0
	lh  t2, 0x00(t1)       ; t2 = shop mask
	li  t1, SAVE_CONTEXT
	lh  t3, 0x0F30(t1)     ; t3 = shop flags
	or  t4, t2, t3                
	sh  t4, 0x0F30(t1)     ; set shop flag

	jr  ra
	nop
