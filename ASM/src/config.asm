;==================================================================================================
; Settings and tables which the front-end may write
;==================================================================================================

; 0x03480000: Item override table:
;
; This table changes the meaning of a given item ID within a given scene. It must be terminated with
; two 0x00 bytes (which will happen by default as long as you don't fill the allotted space).
;
; Row format (4 bytes):
; SSOONNNN
; SS = Scene
; OO = Old item ID
; NN = New item ID
;
; Generic grotto virtual scene numbers:
;   0x70: Hyrule Field: under boulder west of drawbridge
;   0x72: Hyrule Field: under boulder in remote southern trees
;   0x73: Hyrule Field: open hole outside Lake Hylia fences
;   0x78: Kakariko: open hole behind fence
;   0x79: Zora River: open hole on plateau
;   0x7C: Kokiri Forest: SoS hole by the gossip stone
;   0x84: Lost Woods: under boulder next to Goron City warp
;   0x87: Death Mountain: SoS hole outside Goron City
;   0x8A: Death Mountain Crater: under boulder in circle of rocks near top entrance
;
; Other grotto virtual scene numbers:
;   0x71: Hyrule Field: Underwater heart piece
;   0x76: Hyrule Field: Salesman grotto
;   0x77: Redead grotto
;   0x7D: Wolfos grotto
;   0x83: Deku Theater
;   0x85: Lost Woods: Salesman grotto

.area 0x200, 0
ITEM_OVERRIDES:
.endarea

; 0x03480200: Special items

FAIRY_ITEMS:
.byte 0x00 ; Farore's Wind Fairy
.byte 0x00 ; Din's Fire Fairy
.byte 0x00 ; Nayru's Love Fairy
LIGHT_ARROW_ITEM:
.byte 0x00
.align 4
