"""Modèle de données du dessin extrait d'un croquis.

Conventions : unités en millimètres, origine en bas à gauche, X vers la droite,
Y vers le haut. C'est ce JSON que l'utilisateur relit et corrige avant la
génération du DXF.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

Calque = Literal["CONTOUR", "AXE", "CACHE", "DETAIL"]


class Point(BaseModel):
    x: float
    y: float


class Ligne(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    calque: Calque


class Polyligne(BaseModel):
    points: List[Point]
    fermee: bool
    calque: Calque


class Cercle(BaseModel):
    cx: float
    cy: float
    rayon: float
    calque: Calque


class Cote(BaseModel):
    """Cote linéaire entre deux points, avec la valeur lue sur le croquis."""

    x1: float
    y1: float
    x2: float
    y2: float
    valeur_lue: float = Field(description="Valeur manuscrite lue, en mm")
    texte_lu: str = Field(description="Texte exact tel qu'écrit sur le croquis")
    decalage: float = Field(description="Distance de la ligne de cote à l'élément, en mm")


class Texte(BaseModel):
    x: float
    y: float
    hauteur: float
    contenu: str


class Dessin(BaseModel):
    titre: str
    echelle_notee: Optional[str]
    lignes: List[Ligne]
    polylignes: List[Polyligne]
    cercles: List[Cercle]
    cotes: List[Cote]
    textes: List[Texte]
    incertitudes: List[str] = Field(
        description="Tout ce qui est illisible, ambigu ou supposé : à vérifier par l'humain"
    )
