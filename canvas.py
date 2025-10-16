try:
    from PIL import Image
except Exception as exc:
    raise RuntimeError(
    ) from exc

import numpy as np


def create_blank_canvas(width, height, color=(255, 255, 255)):
    """Crée une image RGB unie (blanche par défaut) de taille (width, height)."""
    return Image.new("RGB", (width, height), color)


def reconstruct_grid_image(rects, width, height):
    if not rects:
        return Image.new("RGB", (width, height), (0, 0, 0))

    grid_rows = max(r["row"] for r in rects) + 1
    grid_cols = max(r["col"] for r in rects) + 1

    col_widths = [0] * grid_cols
    row_heights = [0] * grid_rows
    for r in rects:
        c = r["col"]
        rw = r["cell_width"]
        if rw > col_widths[c]:
            col_widths[c] = rw
        rr = r["row"]
        rh = r["cell_height"]
        if rh > row_heights[rr]:
            row_heights[rr] = rh

    x_offsets = [0] * (grid_cols + 1)
    y_offsets = [0] * (grid_rows + 1)
    for i in range(grid_cols):
        x_offsets[i + 1] = x_offsets[i] + col_widths[i]
    for j in range(grid_rows):
        y_offsets[j + 1] = y_offsets[j] + row_heights[j]

    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    for r in rects:
        row = r["row"]
        col = r["col"]
        color = r["color"]
        left = x_offsets[col]
        top = y_offsets[row]
        right = min(width, left + r["cell_width"])
        bottom = min(height, top + r["cell_height"])
        if right > left and bottom > top:
            canvas[top:bottom, left:right, :] = color

    return Image.fromarray(canvas, mode="RGB")


__all__ = ["create_blank_canvas", "reconstruct_grid_image"]


