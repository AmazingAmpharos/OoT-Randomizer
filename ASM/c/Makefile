CC = mips64-gcc
LD = mips64-ld
OBJDUMP = mips64-objdump

CFLAGS = -O1 -fno-reorder-blocks -march=vr4300 -mtune=vr4300 -mabi=32 -mno-gpopt -mdivide-breaks \
	-mexplicit-relocs

OBJECTS = $(patsubst %.c,%.o,$(sort $(wildcard *.c)))

OUTDIR = ../build

.PHONY: all clean bundle symbols

all: clean bundle symbols

%.o: %.c
	$(CC) -c $< $(CFLAGS)

bundle: $(OBJECTS)
	$(LD) -o $(OUTDIR)/bundle.o -i -L. $(patsubst %.o,-l:%.o,$(OBJECTS))

symbols: bundle
	$(OBJDUMP) -t $(OUTDIR)/bundle.o | tr -d '\015' > $(OUTDIR)/c_symbols.txt
	$(OBJDUMP) -d $(OUTDIR)/bundle.o | tr -d '\015' > $(OUTDIR)/bundle_d.txt
	$(OBJDUMP) -r $(OUTDIR)/bundle.o | tr -d '\015' > $(OUTDIR)/bundle_r.txt

clean:
	rm -f *.o
