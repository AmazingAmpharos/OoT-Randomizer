.macro ItemMenu_Description_ID, dest_reg, base_reg
LBU    dest_reg, 0x0074 (base_reg)     ; Load the item ID at the selected menu slot
ADDIU  AT, R0, 0xFF                    ; 0xFF indicates an empty menu slot
BNE    dest_reg, AT, @@return          ; If the slot is not empty, return to default behavior
NOP
ADDIU  dest_reg, R0, 0x2C              ; 0x2C = "SOLD OUT"
@@return:
.endmacro

ItemMenu_Description_ID_Periodic:
ItemMenu_Description_ID T9, T8
JR     RA
SH     T9, 0x009A (SP)

ItemMenu_Description_ID_Immediate1:
ItemMenu_Description_ID T4, T9
JR     RA
NOP

ItemMenu_Description_ID_Immediate2:
ItemMenu_Description_ID T6, T5
JR     RA
SH     T6, 0x009A (SP)

ItemMenu_Description_ID_Immediate3:
ItemMenu_Description_ID T7, T6
JR     RA
SH     T7, 0x009A (SP)
