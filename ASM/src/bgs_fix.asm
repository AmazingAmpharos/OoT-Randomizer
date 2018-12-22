;Big Goron Fix
;Zero out the pointer to the actor that big goron is interacting with
;This change is done in the 1.2 version of the game 

bgs_fix:
    addiu    sp, sp, -0x10
    sw       t0, 0x04(sp)
    sw       t1, 0x08(sp)
    la       t0, 0x800EBAF0
    lw       t0, 0x10(t0)   ; overlay location in ram 
    li       t1, 0x4464     ; offset of displaced instructions
    add      t6, t0, t1
    sw       r0, 0x0118(a0) ;zero out pointer in goron instance
    lw       t1, 0x08(sp)
    lw       t0, 0x04(sp)
    jr       ra             ;return
    addiu    sp, sp, 0x10
