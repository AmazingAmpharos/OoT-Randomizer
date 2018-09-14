CC = mips64-gcc
LD = mips64-ld
OBJDUMP = mips64-objdump

CFLAGS = -march=vr4300 -mtune=vr4300 -mabi=32 -mno-gpopt \
	 -O1 -fno-reorder-blocks \
	 -DZ64_VERSION=Z64_OOT10

OBJECTS = $(patsubst %.c,%.o,$(wildcard *.c))
HEADERS = $(wildcard *.h)

.PHONY: all clean bundle debug

all: clean bundle debug

%.o: %.c $(HEADERS)
	$(CC) -c $< $(CFLAGS)

bundle: $(OBJECTS)
	$(LD) -o output/bundle.o -i -L. $(patsubst %.o,-l:%.o,$(OBJECTS))

debug: bundle
	$(OBJDUMP) -t output/bundle.o > output/debug.txt

clean:
	rm -f *.o output/*
