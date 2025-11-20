from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
from PIL import Image, ImageDraw
import numpy as np


class Shape(ABC):
    """
    Classe abstraite pour une shape dessinable sur une image.
    """

    @abstractmethod
    def create_mask(
        self,
        width: int,
        height: int,
        center_x: float,
        center_y: float,
        cell_w: float,
        cell_h: float,
        row: int = 0,
    ) -> np.ndarray:
        """
        Crée un masque numpy (0-1) pour cette shape.

        Args:
            width, height: dimensions de l'image
            center_x, center_y: centre de la shape
            cell_w, cell_h: dimensions de la cellule
            row: numéro de ligne (pour ajustements spécifiques)

        Returns:
            Masque numpy de shape (height, width) avec valeurs entre 0 et 1
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Shape":
        pass


class RectangleShape(Shape):
    """Shape rectangulaire."""

    def __init__(self, overlap: float = 1.0):
        self.overlap = overlap

    def create_mask(
        self,
        width: int,
        height: int,
        center_x: float,
        center_y: float,
        cell_w: float,
        cell_h: float,
        row: int = 0,
    ) -> np.ndarray:
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)

        expand_w = cell_w * self.overlap
        expand_h = cell_h * self.overlap
        left = center_x - cell_w / 2
        top = center_y - cell_h / 2

        shape_left = max(0, left - expand_w / 2)
        shape_top = max(0, top - expand_h / 2)
        shape_right = min(width, left + cell_w / 2 + expand_w / 2)
        shape_bottom = min(height, top + cell_h / 2 + expand_h / 2)

        shape_draw.rectangle(
            [shape_left, shape_top, shape_right, shape_bottom], fill=255
        )
        mask = np.array(shape_img, dtype=np.float32) / 255.0
        return mask

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "rectangle", "overlap": self.overlap}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RectangleShape":
        return cls(overlap=d.get("overlap", 1.0))


class TriangleShape(Shape):
    """Shape triangulaire."""

    def __init__(self, size_multiplier: float = 3.5, first_row_multiplier: float = 4.5):
        self.size_multiplier = size_multiplier
        self.first_row_multiplier = first_row_multiplier

    def create_mask(
        self,
        width: int,
        height: int,
        center_x: float,
        center_y: float,
        cell_w: float,
        cell_h: float,
        row: int = 0,
    ) -> np.ndarray:
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)

        triangle_size = max(cell_w, cell_h) * self.size_multiplier
        if row == 0:
            triangle_size = max(cell_w, cell_h) * self.first_row_multiplier

        x1 = center_x
        y1 = center_y - triangle_size / 2
        x2 = center_x - triangle_size / 2
        y2 = center_y + triangle_size / 2
        x3 = center_x + triangle_size / 2
        y3 = center_y + triangle_size / 2

        shape_draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=255)
        mask = np.array(shape_img, dtype=np.float32) / 255.0
        return mask

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "triangle",
            "size_multiplier": self.size_multiplier,
            "first_row_multiplier": self.first_row_multiplier,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TriangleShape":
        return cls(
            size_multiplier=d.get("size_multiplier", 3.5),
            first_row_multiplier=d.get("first_row_multiplier", 4.5),
        )


class CircleShape(Shape):
    """Shape circulaire."""

    def __init__(self, radius_multiplier: float = 1.2):
        self.radius_multiplier = radius_multiplier

    def create_mask(
        self,
        width: int,
        height: int,
        center_x: float,
        center_y: float,
        cell_w: float,
        cell_h: float,
        row: int = 0,
    ) -> np.ndarray:
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)

        radius = max(cell_w, cell_h) * self.radius_multiplier
        shape_draw.ellipse(
            [
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
            ],
            fill=255,
        )
        mask = np.array(shape_img, dtype=np.float32) / 255.0
        return mask

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "circle", "radius_multiplier": self.radius_multiplier}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CircleShape":
        return cls(radius_multiplier=d.get("radius_multiplier", 1.2))


def create_shape(shape_type: str) -> Shape:
    """Factory pour créer une shape à partir de son type."""
    if shape_type == "rectangle":
        return RectangleShape()
    elif shape_type == "triangle":
        return TriangleShape()
    elif shape_type == "circle":
        return CircleShape()
    else:
        raise ValueError(f"Type de shape inconnu: {shape_type}")


__all__ = ["Shape", "RectangleShape", "TriangleShape", "CircleShape", "create_shape"]
