from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
from PIL import Image
import numpy as np

class Forme(ABC):
    """
    Classe abstraite pour une forme dessinable sur une image.
    """

    @abstractmethod
    def draw_on(self, base_image: Image.Image, blend: bool = True) -> Image.Image:
        pass

    @abstractmethod
    def apply_to_array(self, arr: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def mutate(self, img_width: int, img_height: int) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Forme":
        pass

# Exemple d'intégration avec Rectangle
from formes import Rectangle

class RectangleForme(Forme):
    """
    Adaptateur pour utiliser Rectangle comme une Forme générique.
    """
    def __init__(self, rect: Rectangle):
        self.rect = rect

    def draw_on(self, base_image: Image.Image, blend: bool = True) -> Image.Image:
        return self.rect.draw_on(base_image, blend)

    def apply_to_array(self, arr: np.ndarray) -> np.ndarray:
        return self.rect.apply_to_array(arr)

    def mutate(self, img_width: int, img_height: int) -> None:
        self.rect.mutate(img_width, img_height)

    def to_dict(self) -> Dict[str, Any]:
        d = self.rect.to_dict()
        d["type"] = "rectangle"
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RectangleForme":
        rect = Rectangle.from_dict(d)
        return cls(rect)

    def __repr__(self):
        return f"RectangleForme({repr(self.rect)})"
    
    def add_rectangle(self, rect: Rectangle) -> None:
        rect.clamp_to_canvas(self.width, self.height)
        self.rectangles.append(rect)

def clear(self) -> None:
    """Efface tous les rectangles."""
    self.rectangles.clear()

def render(self, to_array: bool = False, base_image: Optional[Image.Image] = None) -> Image.Image | np.ndarray:
    """
    Construit l'image finale à partir des rectangles.
    - to_array=True : retourne un tableau numpy (HxWx4)
    - base_image : image RGBA servant de fond au lieu d'une couleur unie
    """
    # Créer le fond
    if base_image is not None:
        img = base_image.convert("RGBA").copy()
    else:
        img = Image.new("RGBA", (self.width, self.height), self.background)

    # Dessiner chaque rectangle dans l'ordre
    for rect in self.rectangles:
        img = rect.draw_on(img, blend=True)

    if to_array:
        return np.array(img, dtype=np.uint8)
    return img

def fitness(self, target_img: Image.Image) -> float:
    """
    Calcule la 'distance' entre l'image rendue et une image cible.
    Retourne la MSE (Mean Squared Error) entre les pixels.
    """
    render_arr = np.array(self.render(to_array=True), dtype=np.float32)
    target_arr = np.array(target_img.resize((self.width, self.height)).convert("RGBA"), dtype=np.float32)
    mse = np.mean((render_arr - target_arr) ** 2)
    return mse

def copy(self) -> Canvas:
    """Crée une copie indépendante du canvas."""
    new_canvas = Canvas(self.width, self.height, self.background)
    new_canvas.rectangles = [r.copy() for r in self.rectangles]
    return new_canvas

def __repr__(self):
    return f"<Canvas {self.width}x{self.height} avec {len(self.rectangles)} rectangles>"


