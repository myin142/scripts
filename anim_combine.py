#!/usr/bin/env python3

import shared
import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='merges animation sprites that ends with frame numbers on default')
parser.add_argument('-d', '--directory', required=True,
                    help='directory where animation sprites are located')
parser.add_argument(
    '-p', '--prefix', help='combine sprites starting with prefix into single sprite', nargs='+', default=[])

args = parser.parse_args()

DIR = args.directory
PREFIXES = args.prefix

shared.exit_if_not_found(DIR)

OUTPUT = shared.output_dir(__file__)
GROUPS = shared.group_sprites(DIR, PREFIXES)

MERGED = []
for k in GROUPS:
    for img in GROUPS[k]:
        MERGED.append(img)

new_img = shared.merge_images(MERGED)

file_name = 'sprite.png'
new_img.save(OUTPUT + '/' + file_name)
