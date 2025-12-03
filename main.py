from image_processor import image_to_color_rects, load_image_to_array, compute_mse
from render import render_image, save_image
import numpy as np
import os


def main():
    """Fonction principale du programme."""
    # Dossier contenant les images
    image_dir = "images"  
    if not os.path.exists(image_dir):
        print("Le dossier n'existe pas :", image_dir)
        return

    # Lister les fichiers images du dossier (.jpeg, .jpg, .png)
    images = [
        f for f in os.listdir(image_dir)
        if f.lower().split('.')[-1] in ('png', 'jpg', 'jpeg')
    ]
    if not images:
        print("Aucune image trouvée dans le dossier :", image_dir)
        return

    # Afficher la liste des images disponibles
    print("\n=== Images disponibles ===")
    for i, img_name in enumerate(images, start=1):
        print(f"{i}. {img_name}")
    print("==========================\n")

    # Demander à l'utilisateur de choisir une image
    while True:
        try:
            choice = input(f"Choisissez une image (1-{len(images)}) : ")
            choice_num = int(choice)
            if 1 <= choice_num <= len(images):
                chosen_image = images[choice_num - 1]
                break
            else:
                print(f"Veuillez entrer un nombre entre 1 et {len(images)}")
        except ValueError:
            print("Veuillez entrer un nombre valide")
        except KeyboardInterrupt:
            print("\nOpération annulée.")
            return

    src_path = os.path.join(image_dir, chosen_image)
    print(f"\nImage choisie : {chosen_image}")

    # Proposer des shapes disponibles
    shapes = {
        "1": "rectangle",
        "2": "triangle",
        "3": "circle"
    }
    
    shape_names = {
        "rectangle": "Rectangle",
        "triangle": "Triangle",
        "circle": "Cercle"
    }

    print("\n=== Formes disponibles ===")
    print("1. Rectangle")
    print("2. Triangle")
    print("3. Cercle")
    print("==========================\n")

    # Demander à l'utilisateur de choisir une forme
    chosen_shape = "rectangle"
    while True:
        try:
            shape_choice = input(f"Choisissez une forme (1-{len(shapes)}) : ")
            if shape_choice in shapes:
                chosen_shape = shapes[shape_choice]
                print(f"\nForme choisie : {shape_names[chosen_shape]}")
                break
            else:
                print(f"Veuillez entrer un nombre entre 1 et {len(shapes)}")
        except KeyboardInterrupt:
            print("\nOpération annulée.")
            return

    rects = image_to_color_rects(src_path, grid_cols=16, grid_rows=16)
    src = load_image_to_array(src_path)
    h, w, _ = src.shape

    img_out = render_image(rects, w, h, shape=chosen_shape)
    output_dir = "resultat"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "sortie.png")
    save_image(img_out, output_path)

    mse = compute_mse(src, np.array(img_out))
    print("Image enregistrée :", output_path)
    print("MSE :", mse)

if __name__ == "__main__":
    main()
