Save_Child_B_Equip:
; t0 = save context
LW at, 0x04 (t0)
BEQZ at, @@return ; Only do this as child
NOP
LBU at, 0x68 (t0) ; Load current B equip
SB at, 0x40 (t0) ; Save B equip, will be loaded on next adult -> child transition
@@return:
JR ra
SB t6, 0x68 (t0) ; Displaced code
