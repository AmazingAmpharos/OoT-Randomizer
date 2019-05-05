; Override the initial salesman bean count check if the salesman is randomized
; t1 = bean count value to use
bean_initial_check:
    addu    v0, v0, t7          ; v0 = save context    
    lb      t1, SHUFFLE_BEANS
    beqz    t1, @@return
    lb      v0, -0x59A4(v0)     ; if the salesman isn't randomized, use the current bean count in save context (default code)

    la      t2, SAVE_CONTEXT
    lb      t1, 0xA18(t2)       ; load scene collectible flags (Zora River)
    andi    at, t1, 0x01        ; check 0x01 flag (normally unused flag)
    bnez    at, @@return
    li      v0, 0xA             ; if the flag is set, return with bean count = 10 (results in sold out)
    li      v0, 0               ; else, return with bean count = 0 (results in sell first bean)

@@return:
    jr      ra
    nop

; Override the price used in the "has enough rupees" check if the salesman is randomized
; t1 = price index to use (0-9)
bean_enough_rupees_check:
    addu    t0, v0, t9          ; t0 = save context
    lb      t2, SHUFFLE_BEANS
    beqz    t2, @@return
    lb      t1, 0x008C(t0)      ; if the salesman isn't randomized, use the price for the current bean count (default code)
    li      t1, 0               ; else, always use the price for the first bean

@@return:
    jr      ra
    nop

; Override the amount of rupees taken when buying the item if the salesman is randomized
; t7 = price index to use (0-9)
bean_rupees_taken:
    addu    t7, t7, t6          ; t7 = save context
    lb      t2, SHUFFLE_BEANS
    beqz    t2, @@return
    lb      t7, -0x59A4(t7)     ; if the salesman isn't randomized, use the price for the current bean count (default code)
    li      t7, 0               ; else, always use the price for the first bean

@@return:
    jr      ra
    nop

; Set the salesman scene collectible flag on purchase if the salesman is randomized
bean_buy_item_hook:
    lb      t1, SHUFFLE_BEANS
    beqz    t1, @@return        ; Skip if the salesman isn't randomized

    la      t2, SAVE_CONTEXT
    lb      t1, 0xA18(t2)       ; load scene collectible flags (Zora River)
    ori     t1, t1, 0x01        ; set 0x01 flag (custom bean salesman flag)
    sb      t1, 0xA18(t2)

@@return:
    jr      ra
    sw      a1, 0x24(sp)        ; displaced code
