import shared
import argparse
import os
import math
import re
from PIL import Image

parser = argparse.ArgumentParser(
    description='splits a spritesheet into individual sprites. Sprites have to be the same size')
parser.add_argument('-f', '--file', required=True, help='spritesheet file')
parser.add_argument('-s', '--size', required=True,
                    help='number of columns and rows (e.g 30x20)')
parser.add_argument('-g', '--gap', help='gap between column and rows in pixel')

args = parser.parse_args()

FILE = args.file
shared.exit_if_not_found(FILE)

SIZES = args.size.split('x')
if len(SIZES) != 2:
    print('Invalid size')
    exit()

col = int(SIZES[0])
row = int(SIZES[1])
OUTPUT = shared.output_dir(__file__)

print('Size {}x{}'.format(col, row))

img = Image.open(FILE)

print('Image Size {}x{}'.format(img.size[0], img.size[1]))

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

WIDTH = (img.size[0] - COL_GAP) / col
HEIGHT = (img.size[1] - ROW_GAP) / row


if not WIDTH.is_integer():
    print('Width is not a whole number {}'.format(WIDTH))
    exit()

if not HEIGHT.is_integer():
    print('Height is not a whole number {}'.format(HEIGHT))
    exit()

print('Extracting with size {}x{}'.format(WIDTH, HEIGHT))

count = 0
for r in range(row):
    for c in range(col):
        left = c * (WIDTH + gap_pixel)
        upper = r * (HEIGHT + gap_pixel)
        sprite = img.crop((left, upper, left + WIDTH, upper + HEIGHT))
        sprite.save('/'.join([OUTPUT, 'sprite_{}.png'.format(count)]))
        count += 1

print('Extracted ' + str(count) + ' sprites.')
