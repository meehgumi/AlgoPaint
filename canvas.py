try:
    from PIL import Image, ImageDraw
except Exception as exc:
    raise RuntimeError(
    ) from exc

import numpy as np


def create_blank_canvas(width, height, color=(255, 255, 255)):
    """Crée une image RGB unie (blanche par défaut) de taille (width, height)."""
    return Image.new("RGB", (width, height), color)


def reconstruct_grid_image(rects, width, height, shape="rectangle"):
    """
    Reconstruit une image à partir de rectangles de couleur avec différentes formes.
    Les formes se chevauchent pour recréer l'image originale.
    
    Args:
        rects: Liste de dictionnaires contenant les rectangles avec leurs couleurs
        width: Largeur de l'image finale
        height: Hauteur de l'image finale
        shape: Forme à utiliser ("rectangle", "triangle", "circle")
    """
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

    canvas = np.zeros((height, width, 3), dtype=np.float32)
    weight_map = np.zeros((height, width), dtype=np.float32)

    for r in rects:
        row = r["row"]
        col = r["col"]
        color = np.array(r["color"], dtype=np.float32)
        left = x_offsets[col]
        top = y_offsets[row]
        right = min(width, left + r["cell_width"])
        bottom = min(height, top + r["cell_height"])
        
        if right <= left or bottom <= top:
            continue
        
        center_x = (left + right) / 2.0
        center_y = (top + bottom) / 2.0
        cell_w = right - left
        cell_h = bottom - top
        
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)
        
        if shape == "rectangle":
            overlap = 1.0
            expand_w = cell_w * overlap
            expand_h = cell_h * overlap
            shape_left = max(0, left - expand_w / 2)
            shape_top = max(0, top - expand_h / 2)
            shape_right = min(width, right + expand_w / 2)
            shape_bottom = min(height, bottom + expand_h / 2)
            shape_draw.rectangle([shape_left, shape_top, shape_right, shape_bottom], fill=255)
            
        elif shape == "triangle":
            triangle_size = max(cell_w, cell_h) * 3.5  
            if row == 0:
                triangle_size = max(cell_w, cell_h) * 4.5
            x1 = center_x
            y1 = center_y - triangle_size / 2  
            x2 = center_x - triangle_size / 2
            y2 = center_y + triangle_size / 2
            x3 = center_x + triangle_size / 2
            y3 = center_y + triangle_size / 2
            shape_draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=255)
                        
        elif shape == "circle":
            radius = max(cell_w, cell_h) * 1.2
            shape_draw.ellipse(
                [center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius],
                fill=255
            )
        
        # Convertir le masque PIL en numpy
        mask = np.array(shape_img, dtype=np.float32) / 255.0
        
        for c in range(3):
            canvas[:, :, c] += mask * color[c]
        weight_map += mask

    weight_map = np.maximum(weight_map, 1e-6)
    for c in range(3):
        canvas[:, :, c] /= weight_map
    
    # Convertir en uint8 et créer l'image
    canvas = np.clip(canvas, 0, 255).astype(np.uint8)
    return Image.fromarray(canvas, mode="RGB")


__all__ = ["create_blank_canvas", "reconstruct_grid_image"]


