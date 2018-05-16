.macro Grow_Stack, count
  ADDIU sp, sp, -0x04 * count
.endmacro

.macro Shrink_Stack, count
  ADDIU sp, sp, 0x04 * count
.endmacro

.macro Push, reg, index
  SW reg, 0x04 * index (sp)
.endmacro

.macro Pop, reg, index
  LW reg, 0x04 * index (sp)
.endmacro
