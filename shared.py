import os
import math
import re
import sys
from PIL import Image
import shutil

OUTPUT = './output/'


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color(str, color):
    return f"{color}{str}{Colors.ENDC}"


def output_dir(file):
    name = os.path.basename(file).split('.')[0]
    path = OUTPUT + name
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path


def exit_if_not_found(dir):
    if not os.path.exists(dir):
        print('Path ' + dir + ' does not exist')
        exit()


def get_sprite_num(sprite_name):
    result = re.findall('[0-9]+', sprite_name)
    if len(result) == 0:
        return sys.maxsize
    return int(result[-1])


def group_sprites(dir, PREFIXES=[]):
    GROUPS = {}
    for entry in os.scandir(dir):
        prefix = find_starting_prefix(entry.name, PREFIXES)
        if prefix == None:
            if len(PREFIXES) == 0:
                pattern = re.compile(r"(-)?\d+\.png$")
                prefix = pattern.split(entry.name)[0]
            else:
                continue

        if GROUPS.get(prefix) is None:
            GROUPS[prefix] = []

        GROUPS[prefix].append(entry.path)

        GROUPS[prefix] = sorted(GROUPS[prefix], key=lambda e: (get_sprite_num(e), e))
    return GROUPS


def find_starting_prefix(name, prefixes):
    for prefix in prefixes:
        if name.startswith(prefix):
           return prefix
    return None


# images should be the same sizes if merging with multiple rows
def merge_images(images, max_columns=-1, use_max_sizes=False):
    imgs = [Image.open(i) for i in images if i.endswith('.png')]
    widths, heights = zip(*(i.size for i in imgs))

    width = max(widths)
    height = max(heights)

    if not use_max_sizes:
        for w in widths:
            if w != width:
                print('Width of one image is not the same', widths)
                exit()

        for h in heights:
            if h != height:
                print('Height of one image is not the same', heights)
                exit()

    rows = 1
    total_width = len(imgs) * width

    if max_columns != -1:
        rows = math.ceil(len(images) / max_columns)
        total_width = min(max_columns, len(images)) * width

    max_height = rows * height
    new_im = Image.new('RGBA', (total_width, max_height))

    print(str(width) + 'x' + str(height) + ', ' +
          str(total_width) + 'x' + str(max_height))

    x_offset = 0
    y_offset = 0
    for im in imgs:
        missing_width = width - im.size[0]
        left_width = math.floor(missing_width / 2)
        new_im.paste(im, (x_offset + left_width, y_offset))
        x_offset += width
        if x_offset >= total_width:
            x_offset = 0
            y_offset += im.size[1]

    return new_im
