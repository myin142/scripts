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

for key in GROUPS:
    new_img = shared.simple_merge(GROUPS[key])

    name = key.replace("_", "")
    file_name = f'{name}.png'
    new_img.save(OUTPUT + '/' + file_name)

