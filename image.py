from argparse import ArgumentParser
from PIL import Image
import shared

parser = ArgumentParser(description='creates a spritesheet from a folder with sprites')
parser.add_argument('operation')
parser.add_argument('args', nargs='*')

args = parser.parse_args()

OUTPUT = shared.output_dir(__file__)

op = args.operation
if op == 'scale':
    if len(args.args) != 2:
        exit()

    file = args.args[0]
    scale_value = float(args.args[1])

    img = Image.open(file)
    new_size = (img.size[0] * scale_value, img.size[1] * scale_value)

    img.thumbnail(new_size, Image.ANTIALIAS)
    img.save('/'.join([OUTPUT, 'scaled.png']))