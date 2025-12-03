# AlgoPaint

Ce projet permet de **reconstruire automatiquement une image** à partir d'une grille de shapes géométriques (rectangles, triangles ou cercles).  
Chaque shape prend la couleur moyenne d'une cellule de l'image originale, créant une version **alternative**, artistique et abstraite.

## 📋 Structure du projet

```
AlgoPaint/
├── shapes.py              → classes abstraites + implémentations (Rectangle, Triangle, Circle)
├── image_processor.py     → analyse d'image, grille, couleurs, MSE
├── render.py              → reconstruction finale à partir des shapes
├── main.py                → interface console + logique principale
├── images/                → dossier contenant les images d'entrée
└── resultat/              → dossier où les images générées sont enregistrées
```

## 🚀 Installation

### 1. Installer les dépendances
```bash
pip install Pillow numpy
```

### 2. Ajouter vos images dans le dossier `images/`

**Formats supportés :**
- `.png`
- `.jpg`
- `.jpeg`

## ✨ Fonctionnalités

- Reconstruction d'une image à l'aide de :
  - **Rectangles**
  - **Triangles**
  - **Cercles**
- Choix du nombre de formes à utiliser :
  - Nombre spécifique (ex: 100, 5, 50)
  - Mode automatique (grille 16×16 = 256 formes)
- Découpage en grille adaptatif selon le nombre choisi
- Calcul automatique de la couleur moyenne par cellule
- Fusion des shapes avec PIL et NumPy
- Calcul de l'erreur **MSE** (Mean Squared Error)
- Interface console simple pour sélectionner :
  - l'image source
  - la shape de reconstruction
  - le nombre de formes

## 🎮 Utilisation

### Lancer le programme
```bash
python3 main.py
```

### Le programme vous guide pour :

1. **Choisir une image** dans le dossier `images/`
2. **Choisir une shape** :
   - `1` = Rectangle
   - `2` = Triangle
   - `3` = Cercle
3. **Choisir le nombre de formes** :
   - Entrer un nombre (ex: `100`, `5`, `50`) pour un nombre spécifique
   - Entrer `auto` pour utiliser la grille automatique (16×16 = 256 formes)
4. **Générer une reconstruction** basée sur les couleurs moyennes
5. **Sauvegarder le résultat** automatiquement dans `resultat/sortie.png`
6. **Afficher la MSE** entre l'image originale et la reconstruction

**Note :** Le programme affiche le nombre réel de formes générées. Si vous demandez un nombre qui ne peut pas être exactement atteint (ex: 7), le programme utilisera la combinaison la plus proche possible (ex: 6 formes).

## ⚙️ Fonctionnement

1. L'image est découpée en une grille
2. Chaque cellule fournit sa couleur moyenne
3. Une shape est générée selon la shape choisie
4. Les shapes sont fusionnées via un masque (PIL + NumPy)
5. L'image finale est normalisée et exportée
6. La MSE est calculée

## 📚 Détails du code

### `shapes.py`
- Classe abstraite `Shape`
- Classes `RectangleShape`, `TriangleShape`, `CircleShape`
- Factory `create_shape()` pour instancier les shapes

### `image_processor.py`
- Chargement d'image (`load_image_to_array`)
- Découpage en grille (`image_to_color_rects`)
- Calcul des couleurs moyennes
- Calcul de l'erreur MSE (`compute_mse`)
- Définition dynamique de la grille (`_compute_grid_from_limit`) :
  - Calcule les dimensions optimales (colonnes × lignes) pour un nombre donné
  - Respecte le ratio de l'image
  - Priorise les combinaisons exactes quand possible

### `render.py`
- Dessin et superposition des shapes géométriques
- Génération de l'image finale via un système de masque
- Fonctions d'affichage et de sauvegarde

### `main.py`
- Menu interactif console
- Gestion du choix de l'image, de la forme et du nombre de formes
- Reconstruction avec le nombre de formes choisi
- Affichage du nombre réel de formes générées
- Calcul de la MSE
- Sauvegarde dans `resultat/sortie.png`
