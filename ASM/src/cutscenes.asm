override_great_fairy_cutscene:
    ; a0 = global context
    ; a2 = fairy actor
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    lw      t0, 0x1D2C (a0) ; t0 = switch flags
    li      t1, 1
    sll     t1, t1, 0x18 ; t1 = ZL switch flag
    and     v0, t0, t1
    beqz    v0, @@return ; Do nothing until ZL is played
    nop

    lhu     t2, 0x02DC (a2) ; Load fairy index
    li      t3, SAVE_CONTEXT

    lhu     t4, 0xA4 (a0) ; Load scene number
    beq     t4, 0x3D, @@item_fairy
    nop

    ; Handle upgrade fairies
    addu    t4, a0, t2
    lbu     t5, 0x1D28 (t4) ; t5 = chest flag for this fairy
    bnez    t5, @@refills ; Just refills if the item is already obtained
    nop
    li      t5, 1
    sb      t5, 0x1D28 (t4) ; Mark item as obtained
    addiu   t2, t2, DELAYED_UPGRADE_FAIRIES ; t2 = cutscene override flag
    b       @@give_item
    nop

@@item_fairy:
    li      t4, 1
    sllv    t4, t4, t2 ; t4 = fairy item mask
    lbu     t5, 0x0EF2 (t3) ; t5 = fairy item flags
    and     t6, t5, t4
    bnez    t6, @@refills ; Just refills if the item is already obtained
    nop
    or      t6, t5, t4
    sb      t6, 0x0EF2 (t3) ; Mark item as obtained
    addiu   t2, t2, DELAYED_ITEM_FAIRIES ; t2 = cutscene override flag

@@give_item:
    ; Unset ZL switch
    nor     t1, t1, t1
    and     t0, t0, t1
    sw      t0, 0x1D2C (a0)

    jal     push_delayed_item
    move    a0, t2

@@refills:

    jal     health_and_magic_refill
    nop

@@return:
    lw      ra, 0x10 (sp)
    li      v0, 0 ; Prevent fairy animation

    jr      ra
    addiu   sp, sp, 0x18

;==================================================================================================

; a3 = item ID
override_ocarina_songs:
    addiu   sp, sp, -0x18
    sw      ra, 0x10 (sp)

    jal     push_delayed_item
    addi    a0, a3, -0x5A + DELAYED_OCARINA_SONGS

    li      v0, 0xFF

    lw      ra, 0x10 (sp)
    jr      ra
    addiu   sp, sp, 0x18

;==================================================================================================

override_requiem_song:
    addiu   sp, sp, -0x20
    sw      at, 0x10 (sp)
    sw      v1, 0x14 (sp)
    sw      ra, 0x18 (sp)

    jal     push_delayed_item
    li      a0, DELAYED_REQUIEM

    lw      at, 0x10 (sp)
    lw      v1, 0x14 (sp)
    lw      ra, 0x18 (sp)
    jr      ra
    addiu   sp, sp, 0x20

;==================================================================================================

override_epona_song:
    addiu   sp, sp, -0x20
    sw      a2, 0x10 (sp)
    sw      a3, 0x14 (sp)
    sw      ra, 0x18 (sp)

    lui     at, 0x8012
    addiu   at, at, 0xA5D0 ; v1 = 0x8012A5D0 # save context (sav)
    lb      t0, 0x0EDE (at) ; check learned song from malon flag
    ori     t0, t0, 0x01 ; t9 = "Invited to Sing With Child Malon"
    sb      t0, 0x0EDE (at)

    jal     push_delayed_item
    li      a0, DELAYED_EPONAS_SONG

    lw      a2, 0x10 (sp)
    lw      a3, 0x14 (sp)
    lw      ra, 0x18 (sp)
    jr      ra
    addiu   sp, sp, 0x20

;==================================================================================================

override_suns_song:
    addiu   sp, sp, -0x18
    sw      v1, 0x10 (sp)
    sw      ra, 0x14 (sp)

    lui     at, 0x8012
    addiu   at, at, 0xA5D0 ; v1 = 0x8012A5D0 # save context (sav)
    lb      t0, 0x0EDE (at) ; learned song from sun's song
    ori     t0, t0, 0x04
    sb      t0, 0x0EDE (at)

    jal     push_delayed_item
    li      a0, DELAYED_SUNS_SONG

    lw      v1, 0x10 (sp)
    lw      ra, 0x14 (sp)
    jr      ra
    addiu   sp, sp, 0x18

;==================================================================================================

override_song_of_time:
    addiu   sp, sp, -0x28
    sw      a0, 0x10 (sp)
    sw      v0, 0x14 (sp)
    sw      t7, 0x18 (sp)
    sw      ra, 0x20 (sp)

    jal     push_delayed_item
    li      a0, DELAYED_SONG_OF_TIME

    li      a1, 3 ; Displaced code

    lw      a0, 0x10 (sp)
    lw      v0, 0x14 (sp)
    lw      t7, 0x18 (sp)
    lw      ra, 0x20 (sp)
    jr      ra
    addiu   sp, sp, 0x28

;==================================================================================================

override_saria_song_check:
    move    t7, v1
    lb      t4, 0x0EDF(t7)
    andi    t6, t4, 0x80
    beqz    t6, @@get_item
    li      v1, 5

    jr      ra
    li      v0, 2

@@get_item:
    jr      ra
    move    v0, v1

;==================================================================================================

set_saria_song_flag:
    lh      v0, 0xa4(t6)       ; v0 = scene
    li      t0, SAVE_CONTEXT
    lb      t1, 0x0EDF(t0)
    ori     t1, t1, 0x80
    sb      t1, 0x0EDF(t0)
    jr      ra
    nop

;==================================================================================================

; Injection for talking to the Altar in the Temple of Time
; Should set flag in save that it has been spoken to.
set_dungeon_knowledge:
    addiu   sp, sp, -0x10
    sw      ra, 0x04(sp)

    ; displaced instruction
    jal     0xD6218
    nop

    li      t4, SAVE_CONTEXT
    lh      t5, 0x0F2E(t4) ; flags
    lw      t8, 0x0004(t4) ; age

    beqz    t8, @@set_flag
    li      t6, 0x0001 ; adult bit
    li      t6, 0x0002 ; child bit

@@set_flag:
    or      t5, t5, t6
    sh      t5, 0x0F2E(t4) ; set the flag

    lw      ra, 0x04(sp)
    addiu   sp, sp, 0x10

    jr      ra
    nop

;Break free of the talon cutscene after event flag is set

talon_break_free:

    ;displaced code
    addiu    t1, r0, 0x0041

    ;preserve registers (t0, t1, t2, t4)
    addiu    sp, sp, -0x20
    sw       t0, 0x04(sp)
    sw       t1, 0x08(sp)
    sw       t2, 0x0C(sp)
    sw       t4, 0x10(sp)

    lui    t2, 0xFFFF
    sra    t2, t2, 0x10   ;shift right 2 bytes
    lui    t0, 0x801D
    lh     t4, 0x894C(t0) ;load current value @z64_game.event_flag
    beq    t4, t2, @@msg  ;if in non-cs state, jump to next check
    nop
    sh     r0, 0x894C(t0) ;store 0 to z64_game.event_flag

@@msg:
    lui    t0, 0x801E
    lb     t2, 0x887C(t0)
    beqz   t2, @@return   ;return if msg_state_1 is 0
    nop
    lui    t1, 0x0036
    sra    t1, t1, 0x10   ;shift right 2 bytes
    sb     t1, 0x887C(t0) ;store 0x36 to msg_state_1
    lui    t1, 0x0002
    sra    t1, 0x10       ;shift right 2 bytes
    sb     t1, 0x895F(t0) ;store 0x02 to msg_state_3
    lui    t0, 0x801F
    sb     r0, 0x8D38(t0) ;store 0x00 to msg_state_2

@@return:
    lw       t4, 0x10(sp)
    lw       t2, 0x0C(sp)
    lw       t1, 0x08(sp)
    lw       t0, 0x04(sp)
    jr     ra
    addiu    sp, sp, 0x20

warp_speedup:

    la     t2, 0x800FE49C ;pointer to links overlay in RAM 
    lw     t2, 0(t2)
    beqz   t2, @@return
    nop
    la     t0, GLOBAL_CONTEXT 
    lui    t3, 0x0001
    ori    t3, t3, 0x04C4 ;offset of warp song played
    add    t0, t0, t3
    lh     t1, 0x0(t0)
    lui    t3, 0x0002
    ori    t3, t3, 0x26CC
    add    t2, t2, t3     ;entrance Table of Warp songs
    sll    t1, t1, 1
    addu   t2, t1, t2 
    lh     t1, 0x0(t2) 
    sh     t1, 0x1956(t0) ;next entrance 
    li     t1, 0x14
    sb     t1, 0x1951(t0) ;scene load flag
    la     t0, SAVE_CONTEXT
    lh     t1, 0x13D2(t0) ; Timer 2 state
    beqz   t1, @@return
    nop

    li     t1, 0x01
    sh     t1, 0x13D4(t0) ; Timer 2 value
    
@@return: 
    jr     ra
    nop

; Prevent hyrule castle guards from causing a softlock.
guard_catch:
    la      v0, GLOBAL_CONTEXT
    lui     at, 0x0001
    add     v0, v0, at
    li	    at, 0x047e
    sh      at, 0x1E1A(v0) ;entrance index = caught by guard
    li      at, 0x14
    jr      ra
    sb      at, 0x1E15(v0) ; trigger load

; Allow any entrance to kak to play burning cutscene
burning_kak:
    addiu   sp, sp, -0x18
    sw      ra, 0x14(sp)
    sw      a0, 0x18(sp)
    lw      t9, 0x0004(s0)
    bnez    t9, @@default
    lw      t9, 0x0000(s0)
    li      at, 0x800F9C90 ; entrance table
    sll     t9, t9, 2
    add     at, t9, at
    lbu     at, 0x00(at)
    li      t9, 0x52
    bne     t9, at, @@default
    lw      t9, 0x0000(s0)
    lhu     v0, 0x00A6(s0)
    andi    t4, v0, 0x0007
    xori    t4, t4, 0x0007
    bnez    t4, @@default
    addiu   a0, r0, 0xAA
    jal     0x800288B4
    nop
    bnez    v0, @@default    ; Burning Kak already Watched
    lw      t9, 0x0000(s0)
    li      t9, 0xDB
    b       @@return
    sw      t9, 0x0000(s0)

@@default:  
    li      at, 0x01E1

@@return:
    lw      ra, 0x14(sp)
    lw      a0, 0x18(sp)
    jr      ra
    addiu   sp, sp, 0x18

; In ER, set the "Obtained Epona" Flag after winning Ingo's 2nd race
ingo_race_win:
    lb      t0, OVERWORLD_SHUFFLED
    beqz    t0, @@return                ; only apply this patch in Overworld ER

    la      at, SAVE_CONTEXT
    lb      t0, 0x0ED6(at)
    ori     t0, t0, 0x01                ; "Obtained Epona" Flag
    sb      t0, 0x0ED6(at)

@@return:
    li      t0, 0
    jr      ra
    sw      t9, 0x0000(t7)              ; Displaced Code

; Rectify the "Getting Caught By Gerudo" entrance index if necessary, based on the age and current scene
; In ER, Adult should be placed at the fortress entrance when getting caught in the fortress without a hookshot, instead of being thrown in the valley
; Child should always be thrown in the stream when caught in the valley, and placed at the fortress entrance from valley when caught in the fortress
; Registers safe to override: t3-t8
gerudo_caught_entrance:
    la      t3, GLOBAL_CONTEXT
    lh      t3, 0x00A4(t3)              ; current scene number
    li      t4, 0x005A                  ; Gerudo Valley scene number
    bne     t3, t4, @@fortress          ; if we are not in the valley, then we are in the fortress

    li      t3, 0x01A5                  ; else, use the thrown out in valley entrance index, even if you have a hookshot
    sh      t3, 0x1E1A(at)
    b       @@return

@@fortress:
    la      t4, SAVE_CONTEXT
    lw      t4, 0x0004(t4)              ; current age
    bnez    t4, @@fortress_entrance     ; if child, change to the fortress entrance no matter what, even if you have a hookshot

    lb      t3, OVERWORLD_SHUFFLED
    beqz    t3, @@return                ; else (if adult), only rectify entrances from inside the fortress in Overworld ER

    lh      t3, 0x1E1A(at)              ; original entrance index
    li      t4, 0x01A5                  ; "Thrown out of Fortress" entrance index
    beq     t3, t4, @@fortress_entrance ; if adult would be thrown in the valley, change to the fortress entrance (no hookshot)
    nop
    b       @@return                    ; else, keep the jail entrance index (owned hookshot)

@@fortress_entrance:
    li      t3, 0x0129                  ; Fortress from Valley entrance index
    sh      t3, 0x1E1A(at)

@@return:
    jr      ra
    nop

; Override Demo_Effect init data for medallions
demo_effect_medal_init:
    sh      t8, 0x17C(a0)      ; displaced code

    la      t0, GLOBAL_CONTEXT
    lh      t1, 0xA4(t0)       ; current scene
    li      t2, 0x02
    bne     t1, t2, @@return   ; skip overrides if scene isn't "Inside Jabu Jabu's Belly"

    lw      t1, 0x138(a0)      ; pointer to actor overlay table entry
    lw      t1, 0x10(t1)       ; actor overlay loaded ram address
    addiu   t2, t1, 0x3398
    sw      t2, 0x184(a0)      ; override update routine to child spritiual stone (8092E058)
    li      t3, 1
    sh      t3, 0x17C(a0)      ; set cutscene NPC id to child ruto

    addiu   sp, sp, -0x18
    sw      ra, 0x14(sp)
    li      a1, 0.1
    jal     0x80020F88         ; set actor scale to 0.1
    nop
    lw      ra, 0x14(sp)
    addiu   sp, sp, 0x18

@@return:
    jr      ra
    nop
