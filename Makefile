GCC = i686-w64-mingw32-gcc
STRIP = i686-w64-mingw32-strip
NASM = nasm
PYTHON = python3
CFLAGS = -fno-exceptions -nostartfiles -nostdlib
LDFLAGS = -lmsvcrt -luser32 -lturbojpeg -Wl,--exclude-all-symbols

all: grphmfc_jpg_amdpatch grphmfc_patch
	@echo done

all_noamdpatch: grphmfc_jpg_normal grphmfc_patch
	@echo done

grphmfc_jpg_amdpatch:
	$(GCC) -shared -o grphmfc_jpg.dll -O3 -DAMDR3GENPATCHER $(CFLAGS) jpgloader.c $(LDFLAGS)
	$(STRIP) --strip-unneeded grphmfc_jpg.dll

grphmfc_jpg_normal:
	$(GCC) -shared -o grphmfc_jpg.dll -O3 $(CFLAGS) jpgloader.c $(LDFLAGS)
	$(STRIP) --strip-unneeded grphmfc_jpg.dll

jmpcode:
	$(NASM) -f bin jpg_jumper.asm

grphmfc_patch: jmpcode
	$(PYTHON) patch.py

