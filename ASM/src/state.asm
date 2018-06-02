;==================================================================================================
; Global variable storage for new code
;==================================================================================================

; Stores the ITEM_DATA row of the current extended item.
EXTENDED_ITEM_DATA:
.word 0x00000000, 0x00000000, 0x00000000, 0x00000000

PENDING_SPECIAL_ITEM:
.byte 0x00
.align 4
