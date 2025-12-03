from image_processor import image_to_color_rects, load_image_to_array, compute_mse, apply_grayscale
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

    src = load_image_to_array(src_path)

    # Choix du filtre
    print("\n Options de Filtre")
    filter_choice = input("Appliquer le filtre Noir et Blanc ? (y/n) : ").strip().lower()
    if filter_choice == 'y': 
        src = apply_grayscale(src)
        print("Filtre Noir et Blanc appliqué.")

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

    # Demander le nombre de formes à utiliser
    print("\n=== Nombre de formes ===")
    print("Entrez un nombre (ex: 100, 5) ou 'auto' pour le calcul automatique")
    print("==========================\n")
    
    max_rectangles = None
    while True:
        try:
            nb_choice = input("Nombre de formes (ou 'auto') : ").strip().lower()
            if nb_choice == "auto":
                print("\nMode automatique sélectionné (grille 16x16)")
                break
            else:
                nb = int(nb_choice)
                if nb > 0:
                    max_rectangles = nb
                    print(f"\nNombre de formes choisi : {nb}")
                    break
                else:
                    print("Veuillez entrer un nombre positif")
        except ValueError:
            print("Veuillez entrer un nombre valide ou 'auto'")
        except KeyboardInterrupt:
            print("\nOpération annulée.")
            return

    # Génération de la grille selon le nombre de formes ou automatique 
    if max_rectangles is not None:
        rects = image_to_color_rects(src_path, max_rectangles=max_rectangles, src_img=src)
        print(f"Grille générée : {len(rects)} formes")
    else:
        rects = image_to_color_rects(src_path, grid_cols=16, grid_rows=16, src_img=src)
        print(f"Grille générée : {len(rects)} formes (16x16)")
    
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
