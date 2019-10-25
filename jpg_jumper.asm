	bits 32
jmpstart:
	call start
jmpend:
	times 0x4E-$+jmpstart db 0xCC ; padding
reloc_ptr: ; at this position, there's a .reloc'd pointer to .rdata, using that as reference
	dd 0xDEADBEEF
	times 0x111-$+jmpstart db 0xCC ; padding
start:
	pop  eax
	push ebp
	mov  ebp, esp
	push ecx
	; get our function pointer from idata
	mov  eax, [eax+(reloc_ptr-jmpend)]
	sub  eax, 0x11AC ; from that earlier pointer position, -0x11AC we get idata for injected dll entry function
	mov  eax, [eax]
	; set arguments and call
	mov  ecx, [ebp+12]
	push ecx
	mov  ecx, [ebp+8]
	push ecx
	mov  ecx, [ebp-4]
	call eax ; __thiscall (G_Image*, void*, u32)
	; 0 is success, 1 we error.
	test eax, eax
	jz   success
	sub  esp, 0x50 ; make enough space for exception part of original function
	jmp  jmpstart+0x79 ; recycling previous code for exception throw
success:
	pop  ecx
	mov  esp, ebp
	pop  ebp
	ret  8
end:
	align 0x10
	; this is for python to know what to take and do
	; file position and size
patcher_info:
	dd jmpstart
	dd jmpend-jmpstart
	dd start
	dd end-start
patcher_count:
	dd (patcher_count-patcher_info) / 8
