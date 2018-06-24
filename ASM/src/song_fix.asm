;==================================================================================================
; Fixes songs in certain scenes to allow for various song learning function to properly play
; through their scripts. 
;==================================================================================================
suns_song_fix_event:
	addu	at, at, s3
	addi 	t7, r0, 0x0047
	bne 	t7, t2, @@return
	lui 	v0, 0x8012
	lw 		v0, 0xA5D4(v0)
	lw 		t7, 0x00A4(s3)
	sra		t7,	t7, 8
	bnez 	v0, @@child
	li 		v0, 0x4830
	bne 	t7, v0, @@return
	nop
	addiu 	t9, r0, 0x0003
	b 		@@return

@@child: 
	li 	v0, 0x6311
	bne 	t7, v0, @@return
	nop
	addiu 	t9, r0, 0x0003

@@return: 
	jr 		ra
	nop
	
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
	lw 		v0, 0xA5D4(v0)
	lw 		t7, 0x00A4(s3)
	sra		t7,	t7, 8
	bnez 	v0, @@child
	li 		v0, 0x4830
	bne 	t7, v0, @@return
	nop
	addiu 	t9, r0, 0x0003
	b 		@@return

@@child: 
	li 	v0, 0x6311
	bne 	t7, v0, @@return
	nop
	addiu 	t9, r0, 0x0003

@@return: 
	jr 		ra
	nop