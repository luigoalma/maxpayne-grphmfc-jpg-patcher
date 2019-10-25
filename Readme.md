# Max Payne's grphmfc jpg patcher

This is mainly a "silencer" and a passthrough for the AMD Ryzen 3rd gen people.\
Game has been crashing at jpg loads.

The game is getting jpg data passed to the jpg loader function corrupted time to time.\
Unknown why exactly, but while so, this patch adds a jumper to a new dll with loader code.\
This new code will suppress the error, only if it manages to get header decompressed.\
If header comes corrupted too, nothing will be done, unless we fake width and height as well.\
But only data seems to cause issue, headers seem fine.\
Corruption happens before it gets to the loader.\
So in the event of a bad jpg with an okay header, will get instead replaced with white image data.\
This means some missing textures, but the game SHOULD run.\
If a header gets corrupted, then we run to an issue.

Don't know to what extent the jpgs are failing within the game on these CPUs, and only had one friend to shortly test it out.

This is not very polished on the applying scripts, and not really intended to be, just good to apply it and make dll ready to the let game run with new code.

Maybe someone will want to use this to determine what image is _supposed_ to be loaded, and load it some other way here.

For other people without the problem, this may come just as a possible little boost of speed.

# Applying

Have the game's `grphmfc.dll` in the `in` folder.\
This needs [NASM](https://www.nasm.us), [Mingw-w64](http://mingw-w64.org)'s gcc, [Python](https://www.python.org) 3, [libjpeg-turbo](https://github.com/libjpeg-turbo/libjpeg-turbo) on lib and include paths of mingw-w64, and make.\
Just run `make` if all set.\
If need just the dll patching and not the extra dll, run `make grphmfc_patch` or `python3 patch.py`.

# License & Distribution

This code itself is under the Unlicensed (check `LICENSE.txt`).\
At binary distribution, please comply with the 3rd party code license rules, and avoid distributing the patched `grphmfc.dll`, instead, include `patch.py` and needed libs.

## 3rd party code licenses

Original implementation uses libjpeg-turbo.\
To comply with libjpeg-turbo license, a text file, or some other form of documentation, should be included at binary distribution, following the guidelines given on it's `LICENSE.md` of the distributed version of libjpeg-turbo.\
In the event code is modified and use a different lib, then you'll shall follow it's guidelines instead.
