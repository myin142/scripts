import shared
import argparse
import os
import math
import re
from PIL import Image

parser = argparse.ArgumentParser(
    description='splits a spritesheet into individual sprites. Sprites have to be the same size')
parser.add_argument('-f', '--file', required=True, help='spritesheet file')
parser.add_argument('-s', '--size', help='number of columns and rows (e.g 30x20)')
parser.add_argument('-g', '--gap', help='gap between column and rows in pixel')
parser.add_argument('--sprite-size', help='e.g 32x32')
parser.add_argument('--prefix', help='Prefix of file names', default='sprite')
parser.add_argument('--output-same-dir', default=False, action='store_true')
parser.add_argument('--start-index', type=int, default=0)

args = parser.parse_args()

FILE = args.file
shared.exit_if_not_found(FILE)

SIZES = args.size.split('x') if args.size else []
SPRITE_SIZES = args.sprite_size.split('x') if args.sprite_size else []
if len(SIZES) != 2 and len(SPRITE_SIZES) != 2:
    print('Invalid size')
    exit()

OUTPUT = shared.output_dir(__file__)
if args.output_same_dir:
    full_file_path = os.path.realpath(FILE)
    OUTPUT = os.path.dirname(full_file_path)

img = Image.open(FILE)
print('Image Size {}x{}'.format(img.width, img.height))

if len(SIZES) > 0:
    col = int(SIZES[0])
    row = int(SIZES[1])
    print('Size {}x{}'.format(col, row))
else:
    sprite_x = int(SPRITE_SIZES[0])
    sprite_y = int(SPRITE_SIZES[1])

    if img.width % sprite_x != 0:
        print("Width not divisible")
        exit()
    if img.height % sprite_y != 0:
        print("Height not divisible")
        exit()

    col = int(img.width / sprite_x)
    row = int(img.height / sprite_y)
    print('Sprite Size {}x{}'.format(col, row))

GAP = args.gap
ROW_GAP = 0
COL_GAP = 0
gap_pixel = 0
if GAP is not None:
    gap_pixel = int(GAP)
    ROW_GAP = (row - 1) * gap_pixel
    COL_GAP = (col - 1) * gap_pixel
    print('Gap size {}x{} with a gap of {} pixel'.format(
        COL_GAP, ROW_GAP, gap_pixel))

WIDTH = (img.width - COL_GAP) / col
HEIGHT = (img.height - ROW_GAP) / row


if not WIDTH.is_integer():
    print('Width is not a whole number {}'.format(WIDTH))
    exit()

if not HEIGHT.is_integer():
    print('Height is not a whole number {}'.format(HEIGHT))
    exit()

print('Extracting with size {}x{}'.format(WIDTH, HEIGHT))

count = args.start_index
for r in range(row):
    for c in range(col):
        left = c * (WIDTH + gap_pixel)
        upper = r * (HEIGHT + gap_pixel)
        sprite = img.crop((left, upper, left + WIDTH, upper + HEIGHT))
        alpha = sprite.getchannel('A')
        alpha_data = alpha.getdata()
        if alpha_data[0] == 0 and all(x == alpha_data[0] for x in alpha_data):
            print('Skip')
            continue

        sprite.save('/'.join([OUTPUT, '{}_{}.png'.format(args.prefix, count)]))
        count += 1

print('Extracted ' + str(count) + ' sprites.')
