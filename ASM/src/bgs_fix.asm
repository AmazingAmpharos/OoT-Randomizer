;Big Goron Fix
;Zero out the pointer to the actor that big goron is interacting with
;This change is done in the 1.2 version of the game 

bgs_fix:

	addiu    t6, t6, 0xD9C4 ;displaced
	sw       r0, 0x0118(a0) ;zero out pointer in big goron instance
	jr       ra             ;return
	nop
