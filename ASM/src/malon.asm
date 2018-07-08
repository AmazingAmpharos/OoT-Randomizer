;==========================================================================================================
; Hacks to make Malon fast, and allow you to always get her item at the vines, even if you've rescued Talon
;==========================================================================================================

; 0xD7E344 starts a function that checks if Malon should spawn
;   + 0x54 is after credits and age have been checked
; at this point, we have the following:
;   a0 = pointer to the save context
;   a1 = pointer to the global context
;   a2 = 3
;   a3 = 1
;   v0 = not sure, but it's checked to be equal to 3 in the original code, probably has to do with credits
;   v1 = the current scene number
; the function has pushed nothing to the stack (so nothing needs to be restored)
; we are expected to return 1 if Malon should spawn, and 0 if she should not

.org 0xD7E398
                                ; this is the state we need for Malon to move to Lon Lon Ranch
    lhu  t1,0x0ed6(a0)          ; this half holds both the following flags
    andi t0,t1,0x10             ; t0 = "Talon has fled castle"
    andi t1,t1,0x04             ; t1 = "Obtained Malon's Item"
    or   t0,t0,t1               ; t0 = combination of the flags
    li   t1,0x14                ; t1 = 0x14 which is the value if both flags are set

@@hyrule_check:                 ; she should spawn at castle until Talon has fled and Item has been given
    li   at,0x5f                ; at = 0x5f (Hyrule Castle)
    bne  at,v1,@@lon_lon_check  ; if not in Hyrule Castle, try Lon Lon instead
    nop
    beq  t0,t1,@@lon_lon_check  ; if Talon and Item, try Lon Lon instead
    nop
    li   v0,1
    jr   ra                      ; return true
    nop

@@lon_lon_check:                ; she should spawn at Lon Lon only once Talon has fled and Item has been given
    bne  a2,v0,@@return_false   ; this test is in the original code, it's probably for the credits
    li   at,0x63                ; at = 0x63 (Lon Lon Ranch)
    bne  at,v1,@@return_false   ; if not in Lon Lon Ranch, return false
    lw   t2,0x10(a0)            ; t2 = is night time
    bnez t2,@@return_false      ; Malon does not spawn at Ranch at night
    nop
    bne  t0,t1,@@return_false   ; make sure Talon has fled and Item has been given
    li   v0,1                    
    jr   ra                     ; return true
    nop

@@return_false:
    li  v0,0
    jr ra                       ; return false
    nop


; 0xD7E110 starts a function that decides which text id Malon should use when spoken to
;   + 0x50 is after ocarina check and song check
; at this point, we have the following:
;   a0 = pointer to the global context
;   v1 = pointer to the save context
; the function needs to restore the stack and return pointer before returning
; we are expected to return a text id

.org 0xD7E160
    lh  t0,0xA4(a0)     ; t0 = current scene number
    li  at,0x63         ; at = 0x63 (Lon Lon Ranch)
    bne at,t0,@@not_in_ranch ; if not in Lon Lon, she's in Hyrule Castle
    li  v0,0x2049       ; v0 = 0x2049 ('... Let's sing together.')
    b   @@return
    nop

@@not_in_ranch:
    lhu  t1,0x0ed6(v1)  ; this half holds the following flag
    andi t1,t1,0x04     ; t1 = "Obtained Malon's Item"
    bnez t1,@@return    ; if we haven't obtained the item, give the item
    li  v0,0x2044       ; v = 0x2044 'Set the egg to C to incubate it...'
    li  v0,0x2043       ; v = 0x2043 '... Would you mind finding my dad? ... <gives item>'

@@return:
return_from_the_other_function:
    lw  ra,20(sp)
    addiu   sp,sp,24    ; restore stack
    jr  ra              ; return v0 (whatever text id was chosen)
    nop



; 0xD7E818 is a function that sets a value in Malon's actor that makes Link get the item from her (cb0)
;   + 0x74 is where the flag/scene checks take place
; at this point, we have the following:
;   a0 = pointer to the Malon actor
;   a2 = pointer to the global context
;   t1 = current scene number
;   at = 0x5f (Hyrule Castle)

.org 0xD7E88C
.area 0x5C, 0
    lui   v0,0x8012
    bne   t1,at,@@not_hyrule    ; if scene is not Hyrule Castle
    addiu v0,v0,-23088          ; v0 = 0x8012a5d0 # save context
    lhu   t2,0x0ed6(v0)         ; this byte holds the two flags below
    andi  t3,t2,0x10            ; t3 = "Talon has fled castle"
    andi  t2,t2,0x04            ; t2 = "Obtained Malon's Item"
    or    t2,t2,t3              ; t2 = combination of the flags
    li    t3,0x14               ; t3 = 0x14 which is the value if both flags are set
    bne   t2,t3,@@not_hyrule    ; check that both flags are true to continue this path
    nop
    b     return_from_the_other_function
    lw    ra,20(sp)             ; jump to return

@@not_hyrule:
    lui   t4,0x8010
    lw    t4,0x8c24(t4)         ; t4 = *(0x80108c24)
    lw    t5,0xa4(v0)           ; t5 = quest status
    and   t6,t5,t4              ; t6 = "Has Epona's Song"
    bnez  t6,return_from_the_other_function           ; return if we already have epona's song
    nop
.endarea


; 0xD7E670 is Malon's initialization function
; the original check sets event to cb0 if Talon has fled, or Epona's Song is owned, and sets cb1 otherwise
; instead, we will check if we are in Hyrule castle, or Epona's song is owned, for event cb0

; Replaces:
;   addiu v0,v0,0xa5d0
.org 0xD7E760
    lw    t8,68(sp)         ; t8 = global context

; Replaces:
;   lhu   t8,3798(v0)
.org 0xD7E76C
    lh    t8,0xA4(t8)       ; t8 = current scene number

; Replaces:
;   andi  t9,t8,0x10
;   beqz  t9,ev_egg
.org 0xD7E778
    li    t9,0x5f           ; t9 = 0x5f (Hyrule Castle)
    beq   t8,t9,ev_egg      ; jump if the scene is Hyrule Castle

; Replace:
;   lw  t1,164(v0)
.org 0xD7E788 
    lw  t1,0xA674(v0)       ; t1 = quest status

.org 0xD7E7A0
ev_egg: