"""Écriture du `Dessin` en DXF (à importer dans cadwork 2D) et aperçu PNG."""

from pathlib import Path

import ezdxf
from ezdxf import units
from ezdxf.addons.drawing import matplotlib as rendu

from .modele import Dessin

# nom : (couleur ACI, type de ligne)
CALQUES = {
    "CONTOUR": (7, "Continuous"),
    "AXE": (1, "DASHDOT"),
    "CACHE": (3, "DASHED"),
    "DETAIL": (8, "Continuous"),
    "COTES": (4, "Continuous"),
    "TEXTES": (7, "Continuous"),
}


def construire(dessin: Dessin) -> ezdxf.document.Drawing:
    doc = ezdxf.new("R2010", setup=True)
    doc.units = units.MM
    doc.header["$LTSCALE"] = 20  # pointillés visibles à l'échelle du mm
    for nom, (couleur, type_ligne) in CALQUES.items():
        doc.layers.add(nom, color=couleur, linetype=type_ligne)

    msp = doc.modelspace()

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
                "dimtxt": 80, "dimasz": 60, "dimexe": 30, "dimexo": 30,
            },
            dxfattribs={"layer": "COTES"},
        ).render()

    for t in dessin.textes:
        msp.add_text(
            t.contenu, height=t.hauteur, dxfattribs={"layer": "TEXTES"}
        ).set_placement((t.x, t.y))

    return doc


def ecrire_dxf(dessin: Dessin, chemin: Path) -> None:
    construire(dessin).saveas(chemin)


def ecrire_apercu(dessin: Dessin, chemin: Path) -> None:
    rendu.qsave(construire(dessin).modelspace(), str(chemin), bg="#FFFFFF", dpi=150)
