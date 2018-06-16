;==================================================================================================
; Fixes songs in certain scenes to allow for various song learning function to properly play
; through their scripts. 
;==================================================================================================
suns_song_fix:
	lw		t5, 0x8AA0(t5)
	li		v0, 0x8000
	beq		v0, t5, @@check_suns_status
	nop
	b		@@return
	
@@check_suns_status:
	li		t7,	0x801D84A0
	lb		v0, 0x1CBF(t7)
	andi	v0, 0x0001
	beqz	v0, @@disable_suns
	nop
	b		@@return
	
@@disable_suns:
	li		v0, 0x0001
	sb		v0, 0x1CBF(t7)

@@return: 
	jr 		ra
	nop
	
;==================================================================================================	
warp_song_fix:
	addu	at, at, s3
	lui 	v0, 0x8012
	lw 		v0, 0xa5d4(v0)
	bnez 	v0, @@child
	lw 		t7, 0x00a4(s3)
	lui 	v0, 0x0048
	addi 	v0, v0, 0x30e8
	bne 	t7, v0, @@return
	nop
	addiu 	t9, r0, 0x0003
	b 		@@return

@@child: 
	lui 	v0, 0x0063
	addi 	v0, v0, 0x11e8
	bne 	t7, v0, @@return
	nop
	addiu 	t9, r0, 0x0003

@@return: 
	jr 		ra
	nop