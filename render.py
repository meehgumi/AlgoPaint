"""Module pour le rendu et l'affichage des images générées."""

try:
    from PIL import Image
except Exception as exc:
    raise RuntimeError(
        "Pillow (PIL) n'est pas installé. Installez-le avec 'pip install Pillow'."
    ) from exc

import numpy as np
from shapes import create_shape


def render_image(rects, width, height, shape="rectangle"):
    """
    Rend une image à partir d'une liste de rectangles de grille avec différentes shapes.
    Les shapes se chevauchent pour recréer l'image originale.
    
    Args:
        rects: Liste de dictionnaires contenant les rectangles avec leurs couleurs
        width: Largeur de l'image finale
        height: Hauteur de l'image finale
        shape: Shape à utiliser ("rectangle", "triangle", "circle")
    
    Returns:
        Image PIL RGB
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
    
    shape_obj = create_shape(shape)

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
        
        mask = shape_obj.create_mask(width, height, center_x, center_y, cell_w, cell_h, row)
        
        for c in range(3):
            canvas[:, :, c] += mask * color[c]
        weight_map += mask

    weight_map = np.maximum(weight_map, 1e-6)
    for c in range(3):
        canvas[:, :, c] /= weight_map
    
    canvas = np.clip(canvas, 0, 255).astype(np.uint8)
    return Image.fromarray(canvas, mode="RGB")


def show_image(img: Image.Image) -> None:
    """Affiche l'image via le visualiseur par défaut du système."""
    img.show()


def save_image(img: Image.Image, path: str) -> None:
    """Enregistre l'image au chemin donné."""
    img.save(path)


__all__ = ["render_image", "show_image", "save_image"]