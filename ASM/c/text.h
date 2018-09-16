#ifndef TEXT_H
#define TEXT_H

#include "z64.h"

void text_init();
void text_print(char *s, int left, int top);
void text_flush(z64_disp_buf_t *db);

#endif
