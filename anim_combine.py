#!/usr/bin/env python3

import shared
import os
import re
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

OUTPUT = shared.output_dir(__file__)
GROUPS = {}

if not os.path.exists(DIR):
    print('Directory '+DIR+' does not exist')
    exit()

for entry in os.scandir(DIR):
    prefix = PREFIX
    if prefix == None:
        pattern = re.compile(r"(-)?\d+\.png$")
        prefix = pattern.split(entry.name)[0]
    elif not entry.name.startswith(prefix):
        continue

    if GROUPS.get(prefix) is None:
        GROUPS[prefix] = []

    GROUPS[prefix].append(entry.path)

for k in GROUPS:
    new_img = shared.merge_images(GROUPS[k])

    file_name = k
    if not file_name.endswith('.png'):
        file_name += '.png'

    new_img.save(OUTPUT + '/' + file_name)
