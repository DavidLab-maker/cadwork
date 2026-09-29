"""Contrôles automatiques avant génération : la géométrie respecte-t-elle les cotes lues ?"""

import math
from typing import List

from .modele import Dessin

TOLERANCE_MM = 1.0


def verifier(dessin: Dessin) -> List[str]:
    """Renvoie la liste des alertes. Vide = rien de suspect détecté automatiquement."""
    alertes = []

    for i, cote in enumerate(dessin.cotes, start=1):
        mesure = math.hypot(cote.x2 - cote.x1, cote.y2 - cote.y1)
        if abs(mesure - cote.valeur_lue) > TOLERANCE_MM:
            alertes.append(
                f"Cote {i} (« {cote.texte_lu} ») : écrit {cote.valeur_lue:g} mm, "
                f"géométrie {mesure:.1f} mm"
            )
        if cote.valeur_lue <= 0:
            alertes.append(f"Cote {i} (« {cote.texte_lu} ») : valeur nulle ou négative")

    for i, ligne in enumerate(dessin.lignes, start=1):
        if math.hypot(ligne.x2 - ligne.x1, ligne.y2 - ligne.y1) < TOLERANCE_MM:
            alertes.append(f"Ligne {i} : longueur nulle")

    for i, poly in enumerate(dessin.polylignes, start=1):
        if len(poly.points) < 2:
            alertes.append(f"Polyligne {i} : moins de 2 points")

    for i, cercle in enumerate(dessin.cercles, start=1):
        if cercle.rayon <= 0:
            alertes.append(f"Cercle {i} : rayon nul ou négatif")

    if not (dessin.lignes or dessin.polylignes or dessin.cercles):
        alertes.append("Aucune géométrie extraite")

    return alertes
