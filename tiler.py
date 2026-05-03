#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import os, math, argparse, sys, random
from datetime import datetime


# -------------------------
# Color parsing
# -------------------------
def parse_color(s):
    if s.startswith("#"):
        s = s.lstrip("#")
        return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
    else:
        return tuple(map(int, s.split(",")))


# -------------------------
# Image discovery
# -------------------------
def find_images(folder, recursive=False):
    paths = []
    if recursive:
        for root, _, files in os.walk(folder):
            for f in files:
                if f.lower().endswith(".png"):
                    paths.append(os.path.join(root, f))
    else:
        paths = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".png")]

    if not paths:
        raise ValueError("No PNG images found.")
    return sorted(paths)


# -------------------------
# Ordering
# -------------------------
def sort_paths(paths, mode):
    if mode == "random":
        random.shuffle(paths)
        return paths

    if mode == "name":
        return sorted(paths)

    imgs = [(p, Image.open(p)) for p in paths]

    if mode == "aspect":
        imgs.sort(key=lambda x: x[1].width / x[1].height)
    elif mode == "area":
        imgs.sort(key=lambda x: x[1].width * x[1].height)

    return [p for p, _ in imgs]


# -------------------------
# Styling helpers
# -------------------------
def add_border(img, border, color):
    if border <= 0:
        return img
    w, h = img.size
    new = Image.new("RGB", (w + 2*border, h + 2*border), color)
    new.paste(img, (border, border))
    return new


def add_caption(canvas, text, location):
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()

    text_w, text_h = draw.textbbox((0, 0), text, font=font)[2:]

    W, H = canvas.size

    if location == "top":
        new = Image.new("RGB", (W, H + text_h + 10), (255, 255, 255))
        new.paste(canvas, (0, text_h + 10))
        draw = ImageDraw.Draw(new)
        draw.text(((W - text_w)//2, 5), text, fill=(0, 0, 0), font=font)
        return new

    elif location == "below":
        new = Image.new("RGB", (W, H + text_h + 10), (255, 255, 255))
        new.paste(canvas, (0, 0))
        draw = ImageDraw.Draw(new)
        draw.text(((W - text_w)//2, H + 5), text, fill=(0, 0, 0), font=font)
        return new

    elif location == "center":
        draw.text(((W - text_w)//2, (H - text_h)//2), text, fill=(0, 0, 0), font=font)
        return canvas

    return canvas


# -------------------------
# Layouts (modified to include border)
# -------------------------
def layout_grid(images, cell_size, padding, bg_color, border, border_color):
    images = [add_border(img, border, border_color) for img in images]

    cell_w, cell_h = cell_size
    n = len(images)

    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    out_w = cols * cell_w + (cols - 1) * padding
    out_h = rows * cell_h + (rows - 1) * padding

    canvas = Image.new("RGB", (out_w, out_h), bg_color)

    for i, img in enumerate(images):
        row, col = divmod(i, cols)

        ratio = min(cell_w / img.width, cell_h / img.height)
        size = (int(img.width * ratio), int(img.height * ratio))
        resized = img.resize(size, Image.LANCZOS)

        x = col * (cell_w + padding) + (cell_w - size[0]) // 2
        y = row * (cell_h + padding) + (cell_h - size[1]) // 2

        canvas.paste(resized, (x, y))

    return canvas


def layout_adaptive(images, target_row_height, max_width, padding, bg_color, border, border_color):
    images = [add_border(img, border, border_color) for img in images]

    rows, current = [], []
    width_acc = 0

    for img in images:
        aspect = img.width / img.height
        w = aspect * target_row_height

        if current and width_acc + w > max_width:
            rows.append(current)
            current, width_acc = [], 0

        current.append(img)
        width_acc += w + padding

    if current:
        rows.append(current)

    y = 0
    layout = []

    for row in rows:
        total_aspect = sum(img.width / img.height for img in row)
        row_h = (max_width - padding * (len(row) - 1)) / total_aspect

        x = 0
        for img in row:
            w = int(row_h * (img.width / img.height))
            h = int(row_h)
            layout.append((img, int(x), int(y), w, h))
            x += w + padding

        y += row_h + padding

    canvas = Image.new("RGB", (max_width, int(y)), bg_color)

    for img, x, y, w, h in layout:
        r = img.resize((w, h), Image.LANCZOS)
        canvas.paste(r, (x, y))

    return canvas


def layout_packed(images, column_width, n_columns, padding, bg_color, border, border_color):
    images = [add_border(img, border, border_color) for img in images]

    cols = [[] for _ in range(n_columns)]
    heights = [0] * n_columns

    for img in images:
        h = int(column_width * (img.height / img.width))
        i = heights.index(min(heights))
        cols[i].append((img, h))
        heights[i] += h + padding

    canvas_h = max(heights)
    canvas_w = n_columns * column_width + (n_columns - 1) * padding
    canvas = Image.new("RGB", (canvas_w, canvas_h), bg_color)

    for i, col in enumerate(cols):
        x = i * (column_width + padding)
        y = 0
        for img, h in col:
            r = img.resize((column_width, h), Image.LANCZOS)
            canvas.paste(r, (x, y))
            y += h + padding

    return canvas


# -------------------------
# MAIN
# -------------------------
def main():
    p = argparse.ArgumentParser()

    p.add_argument("-i", "--input", default=".")
    p.add_argument("-o", "--output", default="tiled.png")
    p.add_argument("--mode", choices=["grid", "adaptive", "packed"], default="grid")

    p.add_argument("--background", default="255,255,255")
    p.add_argument("--border", type=int, default=0)
    p.add_argument("--border-color", default="0,0,0")

    p.add_argument("--caption")
    p.add_argument("--caption-location", choices=["top", "center", "below"], default="top")

    p.add_argument("--padding", type=int, default=10)

    # layout params
    p.add_argument("--cell_size", type=int, nargs=2, default=[256, 256])
    p.add_argument("--target_row_height", type=int, default=250)
    p.add_argument("--max_width", type=int, default=1200)
    p.add_argument("--column_width", type=int, default=300)
    p.add_argument("--columns", type=int, default=4)

    args = p.parse_args()

    bg_color = parse_color(args.background)
    border_color = parse_color(args.border_color)

    paths = find_images(args.input)
    images = [Image.open(p) for p in paths]

    if args.mode == "grid":
        canvas = layout_grid(images, tuple(args.cell_size), args.padding, bg_color, args.border, border_color)
    elif args.mode == "adaptive":
        canvas = layout_adaptive(images, args.target_row_height, args.max_width, args.padding, bg_color, args.border, border_color)
    else:
        canvas = layout_packed(images, args.column_width, args.columns, args.padding, bg_color, args.border, border_color)

    if args.caption:
        canvas = add_caption(canvas, args.caption, args.caption_location)

    canvas.save(args.output)
    print(f"Saved → {args.output}")


if __name__ == "__main__":
    main()
