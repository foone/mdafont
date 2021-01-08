import os,sys,argparse
from PIL import Image
from array import array

CHARACTERS_ACROSS = 32 
BIG_FONT_TOP_HALF_OFFSET=0
BIG_FONT_BOTTOM_HALF_OFFSET=32*8*8

CGA_THICK_FONT_OFFSET=32*8*24
CGA_THIN_FONT_OFFSET=32*8*16

parser = argparse.ArgumentParser(description='Extract and recreate MDA/CGA font ROM images')
main_action = parser.add_mutually_exclusive_group(required=True)
main_action.add_argument('-e','--extract',action='store_true',help='Extract font PNGs from ROM')
main_action.add_argument('-r','--rebuild',action='store_true',help='Create ROM file from PNGs')
parser.add_argument('romfile', type=str, help='ROM file to read or create')

args = parser.parse_args()

def load_image_with_checked_size(filename,expected_size):
	print('Loading {}...'.format(filename))
	im = Image.open(filename)
	if im.size!=expected_size:
		print "ERROR: Expected {} to be {e[0]}x{e[1]}, but it's {a[0]}x{a[1]}!".format(filename,e=expected_size,a=im.size)
		sys.exit()
	return im.convert('L')

def extract_chunk(im, start_index, start_x, start_y):
	for i in range(CHARACTERS_ACROSS):
		for y in range(8):
			b=fontrom[start_index+(i*8)+y]
			for x in range(8):
				if b&(1<<x):
					im.putpixel((start_x+i*8+(7-x),start_y+y),1)

def build_chunk(im, start_index, start_x, start_y, last_line=8):
	for i in range(CHARACTERS_ACROSS):
		for y in range(last_line):
			b=0
			for x in range(8):
				brightness=im.getpixel((start_x+i*8+(7-x),start_y+y))
				if brightness>127:
					b|=(1<<x)
			fontrom[start_index+(i*8)+y]=b



if args.extract:
	fontrom = array('B')
	with open(args.romfile,'rb') as f:
		f.seek(0,os.SEEK_END)
		file_length = f.tell()
		f.seek(0)
		fontrom.fromfile(f,file_length)

	bigfont=Image.new('1',(8*CHARACTERS_ACROSS,14*8))

	for line in range(8):
		extract_chunk(bigfont, BIG_FONT_TOP_HALF_OFFSET+line*CHARACTERS_ACROSS*8,0,14*line)
		extract_chunk(bigfont, BIG_FONT_BOTTOM_HALF_OFFSET+line*CHARACTERS_ACROSS*8,0,14*line+8)

	bigfont.save('bigfont.png')
	print("Created bigfont.png")

	for name,offset in [('thick',CGA_THICK_FONT_OFFSET),('thin',CGA_THIN_FONT_OFFSET)]:
		cgafont=Image.new('1',(8*CHARACTERS_ACROSS,8*8))

		for line in range(8):
			extract_chunk(cgafont, offset+line*CHARACTERS_ACROSS*8,0,8*line)

		filename=name+'font.png'
		cgafont.save(filename)
		print("Created {}".format(filename))

if args.rebuild:
	fontrom=array('B',[0]*8192)
	bigfont=load_image_with_checked_size('bigfont.png',(256,112))

	for line in range(8):
		build_chunk(bigfont, BIG_FONT_TOP_HALF_OFFSET+line*CHARACTERS_ACROSS*8,0,14*line)
		build_chunk(bigfont, BIG_FONT_BOTTOM_HALF_OFFSET+line*CHARACTERS_ACROSS*8,0,14*line+8,last_line=6)

	for name,offset in [('thick',CGA_THICK_FONT_OFFSET),('thin',CGA_THIN_FONT_OFFSET)]:
		cgafont=load_image_with_checked_size(name+'font.png',(256,64))
		for line in range(8):
			build_chunk(cgafont, offset+line*CHARACTERS_ACROSS*8,0,8*line)

	with open(args.romfile,'wb') as f:
		fontrom.tofile(f)