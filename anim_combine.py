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
    '--prefix', help='combine sprites starting with prefix into single sprite')

args = parser.parse_args()

DIR = args.directory
PREFIX = args.prefix

shared.exit_if_not_found(DIR)

OUTPUT = shared.output_dir(__file__)
GROUPS = shared.group_sprites(DIR, [PREFIX])

for k in GROUPS:
    new_img = shared.merge_images(GROUPS[k])

    file_name = k
    if not file_name.endswith('.png'):
        file_name += '.png'

    new_img.save(OUTPUT + '/' + file_name)
