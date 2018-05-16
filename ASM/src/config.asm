;==================================================================================================
; Settings and tables which the front-end may write
;==================================================================================================

; Item override table:
;
; This table changes the meaning of a given item ID within a given scene. It must be terminated with
; two 0x00 bytes (which will happen by default as long as you don't fill the allotted space).
;
; Generic grotto virtual scene numbers:
;   0x70: Hyrule Field: under boulder west of drawbridge
;   0x72: Hyrule Field: under boulder between Kokiri Forest and Lake Hylia
;   0x73: Hyrule Field: open hole outside Lake Hylia fences
;   0x78: Kakariko: open hole behind fence
;   0x79: Zora River: open hole on the high ground
;   0x7C: Kokiri Forest: SoS hole by the gossip stone
;   0x84: Lost Woods: under boulder next to Goron City warp
;   0x87: Death Mountain: SoS hole outside Goron City
;   0x8A: Death Mountain Crater: under boulder in circle of rocks near top entrance

.area 0x180, 0
ITEM_OVERRIDES:
; SS = Scene
; OO = Old item ID
; NN = New item ID
;     SS    OO    NN
.db 0x28, 0x2C, 0x84
.db 0x28, 0x2D, 0x84
.db 0x28, 0x29, 0x84
.db 0x28, 0x2A, 0x84
.endarea
