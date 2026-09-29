"""Lecture d'un croquis (JPG, PNG, PDF) par Claude et extraction en `Dessin`."""

import base64
import io
from pathlib import Path

import anthropic
from PIL import Image

from .modele import Dessin

MODELE = "claude-opus-5-5"
COTE_MAX_PX = 2000  # les photos de téléphone sont réduites avant envoi

CONSIGNES = """\
Tu es dessinateur dans un bureau d'études structure bois. On te donne un croquis \
fait à la main (plan, coupe ou détail). Tu dois le retranscrire en géométrie 2D \
exacte, prête à être importée dans un logiciel de CAO.

Règles :
- Unités : millimètres. Origine (0,0) en bas à gauche du dessin, X vers la droite, Y vers le haut.
- Les COTES ÉCRITES font foi, pas les proportions du tracé : un croquis n'est jamais à l'échelle. \
Positionne la géométrie pour que chaque cote dessinée corresponde exactement à la valeur écrite.
- Redresse les traits : un trait quasi horizontal ou vertical est horizontal ou vertical, \
un angle quasi droit est droit, sauf cote d'angle ou pente indiquée.
- Si une cote est en cm ou en m (ex. « 4,50 » ou « 450 » pour une portée), convertis en mm \
et signale l'hypothèse dans `incertitudes`.
- N'invente rien : si une dimension manque ou est illisible, choisis une valeur plausible, \
et écris-le explicitement dans `incertitudes` (quel élément, quelle valeur supposée, pourquoi).
- Calques : CONTOUR pour les traits vus, AXE pour les axes/entraxes (traits mixtes), \
CACHE pour les traits cachés (pointillés), DETAIL pour le reste (hachures, repères).
- Pièces rectangulaires (solives, poutres, montants) : polyligne fermée, largeur = section vue en plan.
- Une flèche annotée « solive 10x30 entraxe 50 » indique le sens de portée d'un solivage : \
dessine CHAQUE solive individuellement sur toute la zone, à l'entraxe indiqué. \
Position de la première solive : 25 cm de l'appui si rien n'est indiqué (le signaler).
- Les couleurs du croquis distinguent souvent les éléments (ex. poutre en vert, solives en rouge).
- Zones hachurées (murs maçonnés, béton) : un `Hachure` par zone rectangulaire, \
plus les polylignes de contour sur le calque CONTOUR.
- Longueurs d'appui des poutres et solives dans les murs : si non cotées, suppose-les et signale-le.
- Une cote sans unité sur un croquis où d'autres cotes sont en cm est probablement en cm.
- Chaque cote du croquis donne une `Cote` : points mesurés, `valeur_lue` en mm, \
`texte_lu` exactement comme écrit, `decalage` ≈ 300 mm.
- Textes et annotations (sections, essences, repères) : `Texte` avec hauteur ≈ 100 mm.
"""


def _bloc_fichier(chemin: Path) -> dict:
    ext = chemin.suffix.lower()
    if ext == ".pdf":
        donnees = base64.standard_b64encode(chemin.read_bytes()).decode()
        return {
            "type": "document",
            "source": {"type": "base64", "media_type": "application/pdf", "data": donnees},
        }
    if ext not in (".jpg", ".jpeg", ".png"):
        raise ValueError(f"Format non géré : {ext} (attendu : .jpg, .jpeg, .png, .pdf)")

    image = Image.open(chemin)
    image = image.convert("RGB")
    image.thumbnail((COTE_MAX_PX, COTE_MAX_PX))
    tampon = io.BytesIO()
    image.save(tampon, format="JPEG", quality=90)
    donnees = base64.standard_b64encode(tampon.getvalue()).decode()
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": "image/jpeg", "data": donnees},
    }


def lire_croquis(chemin: Path, precisions: str = "") -> Dessin:
    """Envoie le croquis à Claude et renvoie la géométrie structurée."""
    client = anthropic.Anthropic()
    consigne = "Retranscris ce croquis."
    if precisions:
        consigne += f"\nPrécisions de l'utilisateur : {precisions}"

    reponse = client.beta.messages.parse(
        model=MODELE,
        max_tokens=16000,
        output_config={"effort": "high"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=CONSIGNES,
        messages=[{
            "role": "user",
            "content": [_bloc_fichier(chemin), {"type": "text", "text": consigne}],
        }],
        output_format=Dessin,
    )

    if reponse.stop_reason == "refusal":
        raise RuntimeError("Le modèle a refusé de traiter ce fichier.")
    if reponse.stop_reason == "max_tokens":
        raise RuntimeError("Réponse tronquée : croquis trop chargé, découpe-le en plusieurs vues.")
    if reponse.parsed_output is None:
        raise RuntimeError("Réponse illisible : aucune géométrie extraite.")
    return reponse.parsed_output
