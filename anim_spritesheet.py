import shared
import argparse
import os
import math
import re

parser = argparse.ArgumentParser(
    description='creates a spritesheet from a folder with sprites')
parser.add_argument('-d', '--directory', required=True, action='append',
                    help='directory where animation sprites are located')
parser.add_argument('-c', '--columns', type=int,
                    help='How many columns the spritesheet should have. Leave empty to have only one row')

args = parser.parse_args()

DIRS = args.directory
COL = args.columns if args.columns else -1

GROUPS = {}
for DIR in DIRS:
    shared.exit_if_not_found(DIR)
    dir_groups = shared.group_sprites(
        DIR, ['color_green_', 'color_purple_', 'color_red_', 'color_yellow_', 'color_z_'])

    for k in dir_groups:
        if GROUPS.get(k) == None:
            GROUPS[k] = []

        GROUPS[k] += dir_groups[k]

OUTPUT = shared.output_dir(__file__)

files = []
for k in GROUPS:
    files += GROUPS[k]

spritesheet = shared.merge_images(files, COL, True)
spritesheet.save('/'.join([OUTPUT, 'spritesheet.png']))
