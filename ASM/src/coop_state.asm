PLAYER_ID:
.byte 0x00 ; Written by frontend
COOP_GET_ITEM:
.byte 0x00
PLAYER_NAME_ID:
.byte 0x00
.align 4

.area 8*32, 0xDF
PLAYER_NAMES:
.endarea
