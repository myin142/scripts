#!/usr/bin/env python3
"""
color_stripes.py - Generate a color strip image for UV mapping in Blender.

Usage:
    python color_stripes.py <hex1> <hex2> ... [-s SIZE] [-o OUTPUT]
"""

import argparse
import sys
from math import ceil, isqrt

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: Pillow is required. Install it with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def parse_hex(hex_str: str) -> tuple[int, int, int]:
    """Parse a hex color string (with or without #) into an RGB tuple."""
    original = hex_str
    hex_str = hex_str.lstrip("#")

    if len(hex_str) != 6:
        print(f"Error: Invalid hex color '{original}' — must be 6 hex characters (e.g. FF0000 or #FF0000).", file=sys.stderr)
        sys.exit(1)

    try:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
    except ValueError:
        print(f"Error: Invalid hex color '{original}' — contains non-hex characters.", file=sys.stderr)
        sys.exit(1)

    return (r, g, b)


def best_grid(n: int) -> tuple[int, int]:
    """Return (columns, rows) as the factor pair of n closest to square, columns >= rows."""
    # Find largest factor <= sqrt(n); that becomes rows, n//rows becomes columns
    for rows in range(isqrt(n), 0, -1):
        if n % rows == 0:
            cols = n // rows
            return cols, rows
    return n, 1


def main():
    parser = argparse.ArgumentParser(
        description="Generate a color strip image for UV mapping in Blender."
    )
    parser.add_argument(
        "colors",
        nargs="+",
        metavar="HEX",
        help="One or more hex color codes (e.g. FF0000 or #FF0000).",
    )
    parser.add_argument(
        "-s", "--size",
        type=int,
        default=512,
        metavar="PX",
        help="Output image size in pixels (square, default: 512).",
    )
    parser.add_argument(
        "-o", "--output",
        default="palette.png",
        metavar="FILE",
        help="Output file path (default: palette.png).",
    )

    args = parser.parse_args()

    if args.size < 1:
        print("Error: --size must be at least 1.", file=sys.stderr)
        sys.exit(1)

    # Parse and validate all colors up front
    rgb_colors = [parse_hex(c) for c in args.colors]

    columns, rows = best_grid(len(rgb_colors))

    cell_w = args.size // columns
    cell_h = args.size // rows
    img_width = columns * cell_w
    img_height = rows * cell_h

    image = Image.new("RGB", (img_width, img_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)

    for i, color in enumerate(rgb_colors):
        col = i % columns
        row = i // columns
        x0 = col * cell_w
        y0 = row * cell_h
        x1 = x0 + cell_w - 1
        y1 = y0 + cell_h - 1
        draw.rectangle([x0, y0, x1, y1], fill=color)

    try:
        image.save(args.output)
    except Exception as e:
        print(f"Error: Could not save image to '{args.output}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Saved {len(rgb_colors)} color(s) in a {columns}x{rows} grid to '{args.output}' ({img_width}x{img_height}px).")


if __name__ == "__main__":
    main()
