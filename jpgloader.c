#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <turbojpeg.h>

typedef uint8_t u8;
typedef uint32_t u32;

#define PACKED __attribute__((packed))

struct G_Image;
struct G_Color { // seems bgra
	u8 c[4];
};

struct G_Image_vtable {
	struct G_Image* (__thiscall* scalar_delete)(struct G_Image* type, char action);
};

struct G_Image {
	const struct G_Image_vtable* vtable;
	u8 hasimage; // ?
	struct G_Color* image;
	u32 dword9;
	u32 dwordD;
	void* imageraw; // ?
	u32 imagerawsize; // ?
	u32 Width;
	u32 Height;
} PACKED;

static void ErrorMesssage(int jpeg, const char* message) {
	if(!message) message = "Didn't get a message error.\nAs effect, can't say what's wrong.";
	MessageBoxA(NULL, message, jpeg ? "Jpeg gave an error" : "General error", MB_ICONERROR);
}

#if LOADER_DEBUG == 1
static void Debug(u8* buffer, u32 size, u32 count) {
	volatile static u32 dumpcount = 0;
	char dumpname[32];
	char info[256];
	_snprintf(info, 256, "Buffer PTR: 0x%08p\nSize: %lu\nCount call: %lu", buffer, size, count);
	MessageBoxA(NULL, info, "Debug", MB_ICONINFORMATION);
	_snprintf(dumpname, 32, "dumpjpg%lu.bin", dumpcount);
	dumpcount++;
	FILE* fp = fopen(dumpname, "wb");
	if(!fp) {
		ErrorMesssage(0, "Failed to debug dump.");
		return;
	}
	fwrite(buffer, 1, size, fp);
	fclose(fp);
}
#else
static void Debug(u8* buffer, u32 size, u32 count) {}
#endif

__declspec(dllexport) int __thiscall JPGLoader(struct G_Image* This, u8* buffer, u32 size) {
	volatile static u32 count = 0;
	count++;
	int width, height;
	tjhandle tjInstance = tjInitDecompress();
	if(!tjInstance) {
		ErrorMesssage(0, "Can't get decompress instance.");
		return 1;
	}
	if(tjDecompressHeader(tjInstance, buffer, size, &width, &height) < 0) {
		tjDestroy(tjInstance);
		ErrorMesssage(1, tjGetErrorStr2(tjInstance));
		Debug(buffer, size, count);
		return 1;
	}
	struct G_Color* image = malloc(width*height*4);
	if(!image) {
		tjDestroy(tjInstance);
		ErrorMesssage(0, "Not enough memory.");
		return 1;
	}
	if(tjDecompress2(tjInstance, buffer, size, (u8*)image, width, 0, height, TJPF_BGRX, TJFLAG_ACCURATEDCT) < 0) {
		//tjDestroy(tjInstance);
		//ErrorMesssage(1, tjGetErrorStr2(tjInstance));
		Debug(buffer, size, count);
		//free(image);
		//return 1;
		memset(image, 0xFF, width*height*4); // fake it, set it all to FF, aka white
	}
	tjDestroy(tjInstance);
	This->image = image;
	This->Width = width;
	This->Height = height;
	//This->hasimage = 1; //I'd imagine this would be set at successful load, but isn't
	return 0;
}

BOOL WINAPI DllMainCRTStartup(HANDLE hDllHandle, DWORD dwReason, LPVOID lpreserved) {
	return TRUE;
}
