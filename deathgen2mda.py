from PIL import Image
import json,sys,os

BLOCKW=8
BLOCKH=14

jsonpath=sys.argv[1]
basepath=os.path.splitext(jsonpath)[0]
pngpath=basepath+'-font.png'
fontim=Image.open(pngpath)
outimage=Image.new('RGBA',(256,112))
with open(jsonpath,'rb') as f:
	fontinfo=json.load(f)
for i in range(256):
	dest_x=(i%32)*8
	dest_y=(i//32)*14
	char=fontinfo.get(i,fontinfo.get(str(i)))
	if char is not None:
		x,y=char['x'],char.get('y',0)
		w,h=char['w'],char['h']
		if w>BLOCKW or h>BLOCKH:
			print 'character {} is too big! ({}x{}) it needs fit in ({}x{}), skipping'.format(i,w,h,BLOCKW,BLOCKH)
		else:
			tile=fontim.crop((x,y,x+w,y+h))
			ox=(BLOCKW-w)//2
			oy=BLOCKH-h
			outimage.paste(tile,(ox+dest_x,oy+dest_y),tile)
outimage.save('bigfont.png')