adapt_scarecrow:
    lw   at, (FREE_SCARECROW_ENABLED)
    beqz at, @@default_behavior
    nop

; If free_scarecrow
    lhu  t0, 0x670 (v0)         ; Load Link's StateII
    andi at, t0, 0x0800         ; Mask it with playing_ocarina bit
    li   t0, 0x0800
    jr   ra
    nop

@@default_behavior:             ; If not free_scarecrow
    lhu  t0, 0x04C6 (t0)        ; Load last played song id or w/e
    li   at, 0x0B               ; This is the code for scs
    jr   ra
    nop
; Now we can continue with our comparison between t0 and at
; If at != t0, following code will branch to ignore


save_scarecrow_song:
; 80057030
; A0 = Scarecrow Song save address (copy to)
; A1 = Scarecrow Song live location (copy from)
; A2 = 0x80
    lb      t0, 0x0000(a1)
    addiu   t1, t0, 1
    bne     t1, zero, @@copy_song ; if scarecrow song doesn't begin with a rest, copy it to the save data
    nop

    addiu   sp, sp, -0x18
    sw      ra, 0x0014(sp)
    sw      a0, 0x0018(sp)
    sw      a1, 0x001C(sp)

    or      a0, zero, a1
    addiu   a1, a1, 8
    jal     0x57030             ; shift scarecrow song over by 1 note
    addiu   a2, a2, -8
    lw      a0, 0x0018(sp)
    lw      a1, 0x001C(sp)
    li      a2, 0x80
    lw      ra, 0x0014(sp)
    addiu   sp, sp, 0x18
@@copy_song:
    j       0x57030
    nop