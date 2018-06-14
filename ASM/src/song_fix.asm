;==================================================================================================
; Fixes songs in certain scenes to allow for various song learning function to properly play
; through their scripts. 
;==================================================================================================
suns_song_fix:
	addu	at, at, s3
	addi 	t7, r0, 0x0047
	bne 	t7, t2, @@return

@@sacred_forest_meadow:
	lui 	v0, 0x0056
	addi 	v0, v0, 0x2FE8
	lw 		t7, 0x00A4(s3)
	bne 	t7, v0, @@crater
	lui 	v0, 0x0061
	addiu 	t9, r0, 0x0003

@@crater: 
	addi 	v0, v0, 0x0FE8
	bne 	t7, v0, @@courtyard
	lui 	v0, 0x004A
	addiu 	t9, r0, 0x0003

@@courtyard: 
	addi 	v0, v0, 0x2FE8
	bne 	t7, v0, @@age_check
	lui 	v0, 0x8012
	addiu 	t9, r0, 0x0003

@@age_check: 
	lw 		v0, 0xa5d4(v0)
	bnez 	v0, @@child

@@windmill:
	lui 	v0, 0x0048
	addi 	v0, v0, 0x30E8
	bne 	t7, v0, @@temple_of_time
	lui 	v0, 0x0043
	addiu 	t9, r0, 0x0003

@@temple_of_time: 
	addi 	v0, v0, 0x1EE8
	bne 	t7, v0, @@return
	nop
	addiu 	t9, r0, 0x0003
	b 		@@return
	
@@child: 
	lui 	v0, 0x0063
	addi 	v0, v0, 0x11E8
	bne 	t7, v0, @@return
	nop
	addiu 	t9, r0, 0x0003
	
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