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
        pa

# Exemple d'intégration avec Rectangle
from rectangle import Rectangle

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