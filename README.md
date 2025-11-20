# AlgoPaint

## Installation

### 1. Installer les dépendances
```bash
pip install pillow numpy
```
### 2. Ajouter vos images dans le dossier /images/

Formats supportés :
.png
.jpg
.jpeg

Ce projet permet de **reconstruire automatiquement une image** à partir d’une grille de formes géométriques (rectangles, triangles ou cercles).  
Chaque forme prend la couleur moyenne d’une cellule de l’image originale, créant une version **alternative**, artistique et abstraite.

Projet Reconstruction
├── formes.py → classes abstraites + intégration Rectangle  
├── image_processor.py → analyse d'image, grille, couleurs, MSE   
├── render.py → reconstruction finale à partir des formes  
├── main.py → interface console + logique principale  
├── images/ → dossier contenant les images d'entrée  
└── resultat/ → dossier où les images générées sont enregistrées  

## Fonctionnalités
- Reconstruction d’une image à l’aide de :
  - **Rectangles**
  - **Triangles**
  - **Cercles**
- Découpage en grille (par défaut 16×16)
- Calcul automatique de la couleur moyenne par cellule
- Fusion des formes avec PIL et NumPy
- Calcul de l’erreur **MSE** (Mean Squared Error)
- Interface console simple pour sélectionner :
  - l’image source
  - la forme de reconstruction

## Lancer le programme : 
```bash
python main.py
```

## Le programme vous guide pour :

1- Choisir une image dans le dossier images

2- Choisir une forme :  
        1 = Rectangle  
        2 = Triangle  
        3 = Cercle  

3-Générer une reconstruction basée sur les couleurs moyennes

4-Sauvegarder le résultat automatiquement dans : resultat/sortie.png

5-Afficher la MSE entre l’image originale et la reconstruction.

## Fonctionnement : 

1-L'image est découpée en une grille  
2-Chaque cellule fournit sa couleur moyenne  
3-Une forme est générée selon la forme choisis  
4-Les formes sont fusionées via un masque (PIL + NumPy)  
5-L'image finale est normalisée et exportée  
6-La MSE est calculée  

## Détails du code

### formes.py
Classe abstraite Forme  
Classe RectangleForme permettant d'utiliser un rectangle comme forme générique

### image_processor.py
Chargement d’image (load_image_to_array)  
Découpage en grille (image_to_color_rects)  
Calcul des couleurs moyennes  
Calcul de l’erreur MSE (compute_mse)  
Définition dynamique de la grille (_compute_grid_from_limit)

### render.py

Dessin et superposition des formes géométriques  
Génération du canevas final via un système de masque

### main.py

Menu interactif console
Gestion du choix de l’image et de la forme
Reconstruction
Calcul de la MSE
Sauvegarde dans resultat/sortie.png
