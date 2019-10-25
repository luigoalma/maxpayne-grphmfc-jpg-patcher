#!/usr/bin/env python

# First off, yes, this script is a complete mess
# Idea here was just to patch something of static nature, not expecting the DLL to change
# I didn't make something really dynamically adjustable to be exact
# because it's more likely unnecessary too.
# by timestamps, dll hasn't change even since 2001
# still compiled with something has high as MSVC 6.0 for the types of exceptions it got
# the dll is old, and I don't see it change any time soon
# This should at least provide something for those with AMD Ryzen 3rd gen
# A friend was having trouble too, and I decided to make something
# Originally, i was replacing the dll fully, but I'm out of time for now
# This provides a change of dll code to make it link to grphmfc_jpg.dll and JPGLoader from it
# Fix and adjust import directories, tables, idata, pointers, headers, etc, that were already there
# Inject code to the LoadJPG function of the dll to make it call out to the new dll code
# Injected code made from jpg_jumper.asm with NASM or compatible builder
# Expected input file SHA1:  d6cbb14ed284ac7716edafa820ffc95a261c65f0
# Expected output file SHA1: 33ac79cc279f1cbc95907843f750535895b00777
# This checksum is with current asm file, if asm file changes significantly, this output will as well

from struct import unpack
from time import sleep
import hashlib

try:
	file = open("in/grphmfc.dll", "rb")
	dll = bytearray(file.read(98304))
	file.close()
except:
	print("'in/grphmfc.dll' failed to read, make sure it's in place.")
	sleep(2)
	exit(1)

if len(dll) != 98304 or hashlib.sha1(dll).digest() != b'\xd6\xcb\xb1\x4e\xd2\x84\xac\x77\x16\xed\xaf\xa8\x20\xff\xc9\x5a\x26\x1c\x65\xf0':
	print('Bad input grphmfc.dll, too small, possibly not original or already modified.')
	sleep(2)
	exit(1)

try:
	file = open("jpg_jumper", "rb")
	jumper = file.read()
	file.close()
except:
	print("Jumper code failed to read, make sure it was compiled.")
	sleep(2)
	exit(1)

try:
	code_patches = []
	for i in range(0, unpack('<I', jumper[-4:])[0]):
		code_patches += [unpack('<II', jumper[-4-(8*(i+1)):-4-(8*i)])]

	rdata_end = 0x147CC
	to_move_import_tables = 0x136A4
	moved_import_tables = rdata_end
	inject_start = moved_import_tables+24
	new_idata_func = 0x120E4

	zero = b'\x00'*4

	func = b'\x00\x00' + b'JPGLoader\x00'
	func_off = inject_start+8
	dllinject = b'grphmfc_jpg.dll\x00'
	dllinject_off = func_off+len(func)

	# fix header about sizes of import directory and idata
	dll[0x16C:0x170] = b'\xA0\x00\x00\x00'
	dll[0x1C4:0x1C8] = b'\xEC\x00\x00\x00'

	# just for the loadjpg position
	for i in code_patches:
		dll[0x4200+i[0]:0x4200+i[0]+i[1]] = jumper[i[0]:i[0]+i[1]]

	# move a variable right after I data and fix pointers to make space for idata
	dll[0x1284:0x1284+4] = (0x1001215C).to_bytes(4, 'little')
	dll[0x12AC:0x12AC+4] = (0x1001215C).to_bytes(4, 'little')
	dll[0x12D2:0x12D2+4] = (0x1001215C).to_bytes(4, 'little')
	dll[0x12F9:0x12F9+4] = (0x1001215C).to_bytes(4, 'little')
	dll[0x1215C:0x1215C+4] = dll[0x120E8:0x120E8+4]

	# move tables out of the way
	dll[moved_import_tables:moved_import_tables+24] = dll[to_move_import_tables:to_move_import_tables+24]

	# prepare idata space
	dll[new_idata_func:new_idata_func+8] = func_off.to_bytes(4, 'little') + zero

	# fix up rvas for those tables
	dll[0x13654:0x13654+4]  = (moved_import_tables+16).to_bytes(4, 'little')
	dll[0x1367C:0x1367C+4]  = moved_import_tables.to_bytes(4, 'little')
	# add my entry and null entry
	dll[0x13690:0x13690+20] = inject_start.to_bytes(4, 'little') + zero * 2 + dllinject_off.to_bytes(4, 'little') + new_idata_func.to_bytes(4, 'little')
	dll[0x13690+20:0x13690+40] = zero * 5
	# my table
	dll[inject_start:inject_start+8]  = func_off.to_bytes(4, 'little') + zero
	dll[func_off:func_off+len(func)] = func
	dll[dllinject_off:dllinject_off+len(dllinject)] = dllinject

	# determine how much was actually used in the end bit, add up with original .rdata size
	# 32 being moved tables + my added one used size 
	used = 0x27CC + 32 + len(func) + len(dllinject)
	if used % 4:
		used += 4 - (used % 4)
	# set to header
	dll[0x210:0x210+4] = used.to_bytes(4, 'little')
except:
	print("Unexpected error while trying to apply patch.")
	sleep(2)
	exit(1)

try:
	file = open("grphmfc.dll", "wb")
	file.write(dll)
	file.close()
except:
	print("Failed to save patched file.")
	sleep(2)
	exit(1)

print("Patched grphmfc.dll created next to this patcher.")
sleep(2)