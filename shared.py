import os
import math
from PIL import Image

OUTPUT = './output/'


def output_dir(file):
    name = os.path.basename(file).split('.')[0]
    path = OUTPUT + name
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# images should be the same sizes if merging with multiple rows
def merge_images(images, max_columns=-1):
    imgs = [Image.open(i) for i in images]
    widths, heights = zip(*(i.size for i in imgs))

    width = max(widths)
    height = max(heights)

    rows = 1 if max_columns == -1 else math.ceil(len(images) / max_columns)
    total_width = sum(widths) if max_columns == -1 else max_columns * width
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
