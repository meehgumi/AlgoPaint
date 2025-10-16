from image_processor import image_to_color_rects, load_image_to_array, compute_mse
from canvas import reconstruct_grid_image
import numpy as np
import os

def main():
    src_path = "/Users/mehdo/Desktop/b022cbe93f079c00a9411e18aaaecac8.jpg"  # bon chemin pour l'image
    rects = image_to_color_rects(src_path, grid_cols=16, grid_rows=16)

    src = load_image_to_array(src_path)
    h, w, _ = src.shape

    img_out = reconstruct_grid_image(rects, w, h)
    output_dir = "resultat"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "sortie.png")
    img_out.save(output_path)

    mse = compute_mse(src, np.array(img_out))
    print("Image enregistrée:", output_path)
    print("MSE:", mse)

if __name__ == "__main__":
    main()