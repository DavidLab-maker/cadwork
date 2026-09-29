"""Écriture du `Dessin` en DXF (à importer dans cadwork 2D) et aperçu PNG."""

from pathlib import Path

import ezdxf
from ezdxf import units
from ezdxf.addons.drawing import matplotlib as rendu

from .modele import Dessin

# motif du modèle : (motif DXF, échelle)
MOTIFS = {"MACONNERIE": ("ANSI31", 20), "BETON": ("AR-CONC", 1), "ISOLANT": ("ANSI37", 20)}

# nom : (couleur ACI, type de ligne)
CALQUES = {
    "CONTOUR": (7, "Continuous"),
    "AXE": (1, "DASHDOT"),
    "CACHE": (3, "DASHED"),
    "DETAIL": (8, "Continuous"),
    "HACHURES": (8, "Continuous"),
    "COTES": (4, "Continuous"),
    "TEXTES": (7, "Continuous"),
}


def _etendue(dessin: Dessin) -> float:
    """Plus grande dimension du dessin, pour dimensionner le texte des cotes."""
    xs, ys = [], []
    for l in dessin.lignes:
        xs += [l.x1, l.x2]
        ys += [l.y1, l.y2]
    for p in dessin.polylignes:
        xs += [pt.x for pt in p.points]
        ys += [pt.y for pt in p.points]
    if not xs:
        return 0.0
    return max(max(xs) - min(xs), max(ys) - min(ys))


def construire(dessin: Dessin) -> ezdxf.document.Drawing:
    doc = ezdxf.new("R2010", setup=True)
    doc.units = units.MM
    doc.header["$LTSCALE"] = 20  # pointillés visibles à l'échelle du mm
    for nom, (couleur, type_ligne) in CALQUES.items():
        doc.layers.add(nom, color=couleur, linetype=type_ligne)

    msp = doc.modelspace()
    hauteur_cote = max(80.0, _etendue(dessin) / 60)

    for l in dessin.lignes:
        msp.add_line((l.x1, l.y1), (l.x2, l.y2), dxfattribs={"layer": l.calque})

    for p in dessin.polylignes:
        msp.add_lwpolyline(
            [(pt.x, pt.y) for pt in p.points], close=p.fermee, dxfattribs={"layer": p.calque}
        )

    for c in dessin.cercles:
        msp.add_circle((c.cx, c.cy), c.rayon, dxfattribs={"layer": c.calque})

    for c in dessin.cotes:
        # Le texte affiché est la mesure réelle : un écart avec le croquis saute aux yeux.
        msp.add_aligned_dim(
            p1=(c.x1, c.y1),
            p2=(c.x2, c.y2),
            distance=c.decalage,
            dimstyle="EZDXF",
            override={
                "dimlfac": 1, "dimdec": 0,
                "dimtxt": hauteur_cote, "dimasz": hauteur_cote * 0.75,
                "dimexe": hauteur_cote * 0.4, "dimexo": hauteur_cote * 0.4,
            },
            dxfattribs={"layer": "COTES"},
        ).render()

    for h in dessin.hachures:
        motif, echelle = MOTIFS[h.motif]
        hachure = msp.add_hatch(dxfattribs={"layer": "HACHURES"})
        hachure.set_pattern_fill(motif, scale=echelle)
        hachure.paths.add_polyline_path([(pt.x, pt.y) for pt in h.contour], is_closed=True)

    for t in dessin.textes:
        msp.add_text(
            t.contenu, height=t.hauteur, dxfattribs={"layer": "TEXTES"}
        ).set_placement((t.x, t.y))

    return doc


def ecrire_dxf(dessin: Dessin, chemin: Path) -> None:
    construire(dessin).saveas(chemin)


def ecrire_apercu(dessin: Dessin, chemin: Path) -> None:
    rendu.qsave(construire(dessin).modelspace(), str(chemin), bg="#FFFFFF", dpi=150)
