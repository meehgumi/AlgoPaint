from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
from PIL import Image, ImageDraw
import numpy as np


class Shape(ABC):
    """Classe abstraite pour une forme dessinable sur une image."""

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
        """Crée un masque numpy (0-1) pour cette forme."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Shape":
        pass


class RectangleShape(Shape):
    """Forme rectangulaire."""

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
        """Crée un masque rectangulaire."""
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)

        # Calcul des dimensions avec overlap
        expand_w = cell_w * self.overlap
        expand_h = cell_h * self.overlap
        left = center_x - cell_w / 2
        top = center_y - cell_h / 2

        # Calcul des coordonnées du rectangle
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
    """Forme triangulaire."""

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
        """Crée un masque triangulaire."""
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)

        # Calcul de la taille du triangle
        triangle_size = max(cell_w, cell_h) * self.size_multiplier
        if row == 0:
            triangle_size = max(cell_w, cell_h) * self.first_row_multiplier

        # Calcul des trois points du triangle
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
    """Forme circulaire."""

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
        """Crée un masque circulaire."""
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)

        # Calcul du rayon du cercle
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
    
class DiamondShape(Shape):
    """Forme losange (polygone à 4 points)."""

    def __init__(self, size_multiplier: float = 1.8):
        self.size_multiplier = size_multiplier

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
        """Crée un masque losange."""
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)

        # Calcul de la moitié des dimensions du losange
        # Utiliser la plus grande dimension de la cellule comme base pour la taille
        size = max(cell_w, cell_h) * self.size_multiplier
        half_w = size / 2.0
        half_h = size / 2.0

        # Calcul des quatre points du losange (polygone)
        # Point supérieur (milieu_x, milieu_y - moitié_h)
        p1 = (center_x, center_y - half_h)
        # Point droit (milieu_x + moitié_w, milieu_y)
        p2 = (center_x + half_w, center_y)
        # Point inférieur (milieu_x, milieu_y + moitié_h)
        p3 = (center_x, center_y + half_h)
        # Point gauche (milieu_x - moitié_w, milieu_y)
        p4 = (center_x - half_w, center_y)

        shape_draw.polygon([p1, p2, p3, p4], fill=255)
        mask = np.array(shape_img, dtype=np.float32) / 255.0
        return mask

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "diamond", "size_multiplier": self.size_multiplier}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DiamondShape":
        return cls(size_multiplier=d.get("size_multiplier", 1.2))
        
class StarShape(Shape):
    """Forme d'étoile à cinq branches."""

    def __init__(self, size_multiplier: float = 1.6, points: int = 5):
        self.size_multiplier = size_multiplier
        self.points = points

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
        """Crée un masque en forme d'étoile."""
        shape_img = Image.new("L", (width, height), 0)
        shape_draw = ImageDraw.Draw(shape_img)

        # Le rayon extérieur de l'étoile
        outer_radius = max(cell_w, cell_h) * self.size_multiplier / 2.0
        # Le rayon intérieur (pointes intérieures de l'étoile), généralement environ 40% du rayon extérieur
        inner_radius = outer_radius * 0.4

        polygon_points = []
        # Angle de départ pour que l'une des pointes soit en haut (angle 90 degrés ou pi/2)
        start_angle = np.pi / 2.0 
        
        for i in range(self.points * 2):
            # i pair = pointes extérieures, i impair = pointes intérieures
            r = outer_radius if i % 2 == 0 else inner_radius
            angle = start_angle + i * (np.pi / self.points)
            
            x = center_x + r * np.cos(angle)
            y = center_y - r * np.sin(angle) # Soustraire car l'axe Y est inversé dans les images
            polygon_points.append((x, y))

        shape_draw.polygon(polygon_points, fill=255)
        mask = np.array(shape_img, dtype=np.float32) / 255.0
        return mask

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "star", "size_multiplier": self.size_multiplier, "points": self.points}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StarShape":
        return cls(size_multiplier=d.get("size_multiplier", 1.6), points=d.get("points", 5))


def create_shape(shape_type: str) -> Shape:
    """Crée une forme à partir de son type."""
    if shape_type == "rectangle":
        return RectangleShape()
    elif shape_type == "triangle":
        return TriangleShape()
    elif shape_type == "circle":
        return CircleShape()
    elif shape_type == "diamond":
        return DiamondShape()
    elif shape_type == "star":
        return StarShape()
    else:
        raise ValueError(f"Type de forme inconnu: {shape_type}")


__all__ = ["Shape", "RectangleShape", "TriangleShape", "CircleShape", "DiamondShape", "StarShape", "create_shape"]
