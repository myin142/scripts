import shared
import argparse
import os
import math

parser = argparse.ArgumentParser(
    description='creates a spritesheet from a folder with sprites')
parser.add_argument('-d', '--directory', required=True,
                    help='directory where animation sprites are located')
parser.add_argument('-c', '--columns', type=int,
                    help='How many columns the spritesheet should have. Leave empty to have only one row')

args = parser.parse_args()

DIR = args.directory
COL = args.columns if args.columns else 1

if not os.path.exists(DIR):
    print('Directory '+DIR+' does not exist')
    exit()

OUTPUT = shared.output_dir(__file__)

files = [entry.path for entry in os.scandir(DIR)]
spritesheet = shared.merge_images(files, COL)
spritesheet.save('/'.join([OUTPUT, 'spritesheet.png']))

print(str(COL) + 'x' + str(math.ceil(len(files)/COL)))
