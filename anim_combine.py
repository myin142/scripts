#!/usr/bin/env python3

import os
import re
import sys
from PIL import Image

if len(sys.argv) < 3:
    print('Missing arguments')
    exit()

DIR = sys.argv[1]
OUTPUT = sys.argv[2]
GROUPS = {}
PREFIX = ''

if len(sys.argv) >= 4:
    PREFIX = sys.argv[3]

if not os.path.exists(DIR):
    print('Directory '+DIR+' does not exist')
    exit()

if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)

for entry in os.scandir(DIR):
    prefix = PREFIX
    if prefix == '':
        pattern = re.compile(r"\d+\.png$")
        prefix = pattern.split(entry.name)[0]
    elif not entry.name.startswith(prefix):
        continue

    if GROUPS.get(prefix) is None:
        GROUPS[prefix] = []

    GROUPS[prefix].append(entry.path)

for k in GROUPS:
    images = [Image.open(x) for x in GROUPS[k]]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    file_name = k
    if not file_name.endswith('.png'):
        file_name += '.png'

    new_im.save(OUTPUT + '/' + file_name)
