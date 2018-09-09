CC=mips64-gcc
CFLAGS=-march=vr4300 -mtune=vr4300 -mabi=32 -mno-gpopt \
       -O1 -fno-reorder-blocks \
       -DZ64_VERSION=Z64_OOT10

main:
	$(CC) -c main.c $(CFLAGS)
