try:
    from PIL import Image
except Exception as exc:
    raise RuntimeError(
    ) from exc

import numpy as np
import math


def _average_color(region):
    small = region.copy()
    small.thumbnail((1, 1))
    px = small.getpixel((0, 0))
    if isinstance(px, int):
        return (px, px, px)
    if isinstance(px, tuple) and len(px) >= 3:
        return (int(px[0]), int(px[1]), int(px[2]))
    return (0, 0, 0)


def load_image_to_array(path):
    with Image.open(path) as im:
        img = im.convert("RGB")
    return np.array(img, dtype=np.uint8)


def _compute_grid_from_limit(max_rectangles, width, height):
    if max_rectangles is None or max_rectangles <= 0:
        return 16, 16
    ratio = width / float(height) if height else 1.0
    cols = max(1, int(round(math.sqrt(max_rectangles * ratio))))
    rows = max(1, max_rectangles // cols)
    while cols * rows > max_rectangles and rows > 1:
        rows -= 1
    if cols * rows > max_rectangles and cols > 1:
        cols = max(1, max_rectangles // rows)
    cols = max(1, cols)
    rows = max(1, rows)
    return cols, rows


def image_to_color_rects(path, grid_cols=16, grid_rows=16, max_rectangles=None):
    if grid_cols <= 0 or grid_rows <= 0:
        raise ValueError("grid_cols et grid_rows doivent être > 0")

    with Image.open(path) as im:
        img = im.convert("RGB")

    width, height = img.size
    if max_rectangles is not None:
        grid_cols, grid_rows = _compute_grid_from_limit(int(max_rectangles), width, height)
    cell_w = max(1, width // grid_cols)
    cell_h = max(1, height // grid_rows)

    rects = []
    for r in range(grid_rows):
        for c in range(grid_cols):
            left = c * cell_w
            top = r * cell_h
            right = width if c == grid_cols - 1 else (c + 1) * cell_w
            bottom = height if r == grid_rows - 1 else (r + 1) * cell_h
            region = img.crop((left, top, right, bottom))
            color = _average_color(region)
            rects.append(
                {
                    "row": r,
                    "col": c,
                    "color": color,
                    "cell_width": right - left,
                    "cell_height": bottom - top,
                }
            )

    return rects


def compute_mse(a, b):
    if a.shape != b.shape:
        raise ValueError("Les deux images doivent avoir la même shape")
    diff = a.astype(np.float32) - b.astype(np.float32)
    return float(np.mean(diff * diff))


__all__ = [
    "load_image_to_array",
    "image_to_color_rects",
    "compute_mse",
]