extended_object_lookup_GI:
    BGE     T8, 0x192, @@extended_item
    nop
    @@normal_item:
    LUI     T0, 0x8010
    JR RA
    ADDIU   T0, T0, 0x8FF8
    @@extended_item:
    LA      T0, EXTENDED_OBJECT_TABLE
    JR      RA
    ADDIU   T8, T8, -0x193

extended_object_lookup_load:
    ADDU    V1, A0, T6  ; displaced
    BGE     A2, 0x192, @@extended_item
    nop
    @@normal_item:
    LUI     T9, 0x8010
    JR      RA
    ADDIU   T9, T9, 0x8FF8
    @@extended_item:
    LA      T9, EXTENDED_OBJECT_TABLE
    JR      RA
    ADDIU   A2, A2, -0x193
    

