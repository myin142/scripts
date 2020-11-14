import os
import math
import re
from PIL import Image

OUTPUT = './output/'


def output_dir(file):
    name = os.path.basename(file).split('.')[0]
    path = OUTPUT + name
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def exit_if_not_found(dir):
    if not os.path.exists(dir):
        print('Directory '+dir+' does not exist')
        exit()


def group_sprites(dir, PREFIX=None):
    GROUPS = {}
    for entry in os.scandir(dir):
        prefix = PREFIX
        if prefix == None:
            pattern = re.compile(r"(-)?\d+\.png$")
            prefix = pattern.split(entry.name)[0]
        elif not entry.name.startswith(prefix):
            continue

        if GROUPS.get(prefix) is None:
            GROUPS[prefix] = []

        GROUPS[prefix].append(entry.path)

        # Animations should (hopefully) not have more than 10 sprites
        GROUPS[prefix] = sorted(GROUPS[prefix])
    return GROUPS


# images should be the same sizes if merging with multiple rows
def merge_images(images, max_columns=-1):
    imgs = [Image.open(i) for i in images]
    widths, heights = zip(*(i.size for i in imgs))

    width = max(widths)
    height = max(heights)

    for w in widths:
        if w != width:
            print('Width of one image is not the same', widths)
            exit()

    for h in heights:
        if h != height:
            print('Height of one image is not the same', heights)
            exit()

    rows = 1
    total_width = sum(widths)

    if max_columns != -1:
        rows = math.ceil(len(images) / max_columns)
        total_width = min(max_columns, len(images)) * width

    max_height = rows * height
    new_im = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    y_offset = 0
    for im in imgs:
        new_im.paste(im, (x_offset, y_offset))
        x_offset += im.size[0]
        if x_offset >= total_width:
            x_offset = 0
            y_offset += im.size[1]

    return new_im
