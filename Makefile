GCC = i686-w64-mingw32-gcc
STRIP = i686-w64-mingw32-strip
NASM = nasm
PYTHON = python3

all: grphmfc_jpg grphmfc_patch
	@echo done

grphmfc_jpg:
	$(GCC) -shared -o grphmfc_jpg.dll -O3 jpgloader.c -fno-exceptions -nostartfiles -nostdlib -lmsvcrt -luser32 -lturbojpeg -Wl,--exclude-all-symbols
	$(STRIP) --strip-unneeded grphmfc_jpg.dll

jmpcode:
	$(NASM) -f bin jpg_jumper.asm

grphmfc_patch: jmpcode
	$(PYTHON) patch.py

