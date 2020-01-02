; 0x00E2D714 (bombchu bowling hook)

logic_chus__bowling_lady_1:
; Change Bowling Alley check to Bombchus or Bomb Bag (Part 1)

    lb      t7, BOMBCHUS_IN_LOGIC
    beq     t7, r0, @@logic_chus_false
    nop

@@logic_chus_true:
    lb      t7, lo(0x8011A64C)(t7)
    li      t8, 0x09; Bombchus

    beq     t7, t8, @@return
    li      t8, 1
    li      t8, 0

@@return:
    jr      ra
    nop

@@logic_chus_false:
    lw      t7, lo(0x8011A670)(t7)
    andi    t8, t7, 0x18
    jr      ra
    nop


logic_chus__bowling_lady_2:
; Change Bowling Alley check to bombchus or Bomb Bag (Part 2)

    lb      t3, BOMBCHUS_IN_LOGIC
    beq     t3, r0, @@logic_chus_false
    nop

@@logic_chus_true:
    lb      t3, lo(0x8011A64C)(t3)
    li      t4, 0x09; Bombchus

    beq     t3, t4, @@return
    li      t4, 1
    li      t4, 0

@@return:
    jr      ra
    nop
    
@@logic_chus_false:
    lw      t3, lo(0x8011A670)(t3)
    andi    t4, t3, 0x18
    jr      ra
    nop


logic_chus__shopkeeper:
; Cannot buy bombchu refills without Bomb Bag

    lb      t1, BOMBCHUS_IN_LOGIC
    beq     t1, r0, @@logic_chus_false
    nop
    
@@logic_chus_true:
    lui     t1, hi(SAVE_CONTEXT + 0x7C)
    lb      t2, lo(SAVE_CONTEXT + 0x7C)(t1) ; bombchu item
    li      t3, 9
    beq     t2, t3, @@return ; if has bombchu, return 0 (can buy)
    li      v0, 0
    jr      ra
    li      v0, 2 ; else, return 2 (can't buy)

@@logic_chus_false:
    lui     t1, hi(SAVE_CONTEXT + 0xA3)
    lb      t2, lo(SAVE_CONTEXT + 0xA3)(t1) ; bombbag size
    andi    t2, t2, 0x38
    bnez    t2, @@return       ; If has bombbag, return 0 (can buy)
    li      v0, 0
    li      v0, 2              ; else, return 2, (can't buy)

@@return:
    jr      ra
    nop


logic_chus__carpet_salesman_purchase:
; Prevent bombchu purchase if:    money < 200 rupees
;                              OR (you don't have Bombchus and BOMBCHUS_IN_LOGIC)
;                              OR max Bombchu ammo
; modifies t6
; returns value in a1 (0 to allow purchase, textID otherwise)

    lb      t6, BOMBCHUS_IN_LOGIC
    beq     t6, r0, @@check_rupees ; allow purchase if BOMBCHUS_IN_LOGIC == 0
    lui     t6, hi(SAVE_CONTEXT + 0x7C)
    lb      a1, lo(SAVE_CONTEXT + 0x7C)(t6) ; bombchu item
    ori     t6, r0, 9
    bne     a1, t6, @@return
    ori     a1, r0, 0x718F; returns DENY with textID 0x718F

@@check_rupees:
    lui     t6, hi(SAVE_CONTEXT + 0x34)
    lh      a1, lo(SAVE_CONTEXT + 0x34)(t6) ; number of rupees
    slti    t6, a1, 200 ; t6 is set if less than 200 rupees
    bnez    t6, @@return
    ori     a1, r0, 0x6075 ; returns DENY with textID 0x6075

@@check_if_bombchus_full:
    lui     t6, hi(SAVE_CONTEXT + 0x94)
    lb      a1, lo(SAVE_CONTEXT + 0x94)(t6) ; bombchu ammo
    slti    t6, a1, 50 ; set t6 if bombchus not full
    beqz    t6, @@return
    ori     a1, r0, 0x401E ; returns DENY with textID 0x401E

    ori     a1, r0, 0 ; returns ALLOW

@@return:
    jr      ra
    nop
