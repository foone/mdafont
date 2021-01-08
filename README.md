# mdafont
 This tool can split the IBM Font ROM (included here for ease of use as IBM_5788005_AM9264_1981_CGA_MDA_CARD)
 into several PNG images, and then rebuild them back into the ROM binary for flashing onto an EPROM/EEPROM.

 This rom file is used on both the IBM Monochrome Display Adapter and the IBM Color Graphics Adapter.


 The three files created are bigfont.png, thickfont.png, thinfont.png.

 bigfont.png is the MDA font, and thickfont.png is the CGA font. (thinfont.png is normally unused.)

 
# Usage:

1. First, split the rom file:

   # python mdafont.py -e IBM_5788005_AM9264_1981_CGA_MDA_CARD.bin

   This will create several files: bigfont.png, thickfont.png, thinfont.png 

2. Edit them however you want

3. Rebuild the font file:

   # python mdafont.py -r modified_font_file.bin

4. Burn the font file onto an 8K (or larger) EPROM/EEPROM.

5. Connect the EPROM/EEPROM to your MDA/CGA card. It uses a 9264 pinout, which is annoying. The easiest way to do this is to get a standard 27(C)64 or 27(C)64, and an adapter. I used the 2364 adapter from RETRO Innovations: http://store.go4retro.com/2364-adapter/

# deathgen2mda

This is a basic proof of concept to take a [Death Generator](https://github.com/foone/SierraDeathGenerator) json/font pair and convert it to an MDA font image. It doesn't yet support "default" functionality or any other special functionality, and you will have to modify the resulting image before it's acceptable, but it should hopefully give you a starting point. To use it, run:

    python deathgen2mda.py SierraDeathGenerator/games/foobar/foobar.json

and it will generate the bigfont.png file.

# Requirements:

* Python 2.7
* PIL/Pillow

# License

All code is licensed under the GPL version 3, and the data file IBM_5788005_AM9264_1981_CGA_MDA_CARD.BIN is copyright 1981 IBM. 