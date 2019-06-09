#!/usr/bin/env python3

# pip3 install pysoundfile piexif pillow

import soundfile
import piexif
import PIL, PIL.Image
import os
import random
import shutil
import numpy as np
import zipfile

random.seed(1337)

def bits(data):
    return[int(i) for b in data for i in bin(b)[2:].zfill(8)]

os.makedirs('build', exist_ok=True)


flag = open('stage0/flag.txt').read().strip()


needle_im = PIL.Image.open('stage1/needle.png')
for x in range(needle_im.size[0]):
    for y in range(20):
        c = random.randint(0, 32)
        needle_im.putpixel((x, y), (c, c, c, 255))
for x in range(len(flag)):
    o = ord(flag[x])
    needle_im.putpixel((x + 30, 14), (o, o, o, 255))
p_im = PIL.Image.new("P", needle_im.size)
p_im.putpalette([0, 0, 0] * 128 + [255, 255, 255] * 128)
for x in range(needle_im.size[0]):
    for y in range(needle_im.size[1]):
        p_im.putpixel((x, y), needle_im.getpixel((x, y))[0])
p_im.save('build/stage1.png')


shutil.copy('stage2/egg.jpg', 'build/stage2.jpg')
piexif.insert(piexif.dump({'Exif': {piexif.ExifIFD.MakerNote:
                                    open('build/stage1.png', 'rb').read().hex().encode()}}),
              'build/stage2.jpg')


egg_bytes = open('build/stage2.jpg', 'rb').read()
egg_bits = bits(egg_bytes)
duck_im = PIL.Image.open('stage3/duck.png')
for i in range(len(egg_bits) // 6):
    x, y = i % duck_im.size[0], i // duck_im.size[0]
    r, g, b, a = duck_im.getpixel((x, y))
    seq = egg_bits[i * 6 : i * 6 + 6]
    r = r & ~3 + seq[0] * 2 + seq[1]
    g = g & ~3 + seq[2] * 2 + seq[3]
    b = b & ~3 + seq[4] * 2 + seq[5]
    duck_im.putpixel((x, y), (r, g, b, a))
duck_im.save('build/stage3.bmp')


bunny_sound, rate = soundfile.read('stage4/nu-pogodi.ogg', dtype='int16')
duck_bits = bits(open('build/stage3.bmp', 'rb').read())
for n, b in enumerate(duck_bits):
    bunny_sound[n] = int(bunny_sound[n]) & ~1 + b
for n in range(len(duck_bits), len(bunny_sound)):
    bunny_sound[n] = int(bunny_sound[n]) & ~1
soundfile.write('build/stage4.wav', bunny_sound, rate)


MAPPING = dict(zip('АВЕКМНОРСТХаеорсух',   # cyr
                   'ABEKMHOPCTXaeopcyx'))  # lat
text = open('stage5/text.txt').read()
duck_bits = bits(open('build/stage4.wav', 'rb').read())
bit, text_pos = 0, 0
box_text = ''
while bit < len(duck_bits):
    ch = text[text_pos]
    if ch in MAPPING:
        box_text += (MAPPING[ch] if duck_bits[bit] else ch)
        bit += 1
    else:
        box_text += ch
    text_pos += 1
    if text_pos >= len(text):
        text_pos = 0
open('build/stage5.txt', 'w').write(box_text)


z = zipfile.ZipFile('stage6/oak.docx')
z_target = zipfile.ZipFile('build/stage6.docx', 'w', zipfile.ZIP_DEFLATED)
for f in z.namelist():
    text = z.read(f)
    if f == 'word/activeX/activeX4.xml':
        text += b'\n<!--\n' + open('build/stage5.txt', 'rb').read() + b'\n-->'
    z_target.writestr(f, text)
z_target.close()
z_all = zipfile.ZipFile('build/stage6.zip', 'w', zipfile.ZIP_DEFLATED)
z_all.writestr('oak.docx', open('build/stage6.docx', 'rb').read())
z_all.close()


open('build/stage7.jpg', 'wb').write(open('stage7/island.jpg', 'rb').read() + open('build/stage6.zip', 'rb').read())
