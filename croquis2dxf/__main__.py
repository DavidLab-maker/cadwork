"""Ligne de commande.

    python -m croquis2dxf lire croquis.jpg        -> croquis.json + croquis_apercu.png
    (relire le JSON et l'aperçu, corriger le JSON si besoin)
    python -m croquis2dxf dxf sorties/croquis.json -> croquis.dxf à importer dans cadwork 2D
"""

import argparse
import sys
from pathlib import Path

from .dxf import ecrire_apercu, ecrire_dxf
from .modele import Dessin
from .verification import verifier


def _afficher_controles(dessin: Dessin) -> int:
    alertes = verifier(dessin)
    if dessin.incertitudes:
        print("\nÀ VÉRIFIER (signalé par la lecture du croquis) :")
        for texte in dessin.incertitudes:
            print(f"  - {texte}")
    if alertes:
        print("\nINCOHÉRENCES DÉTECTÉES :")
        for texte in alertes:
            print(f"  - {texte}")
    if not dessin.incertitudes and not alertes:
        print("\nAucune alerte. Contrôle visuel de l'aperçu quand même obligatoire.")
    return len(alertes)


def cmd_lire(args) -> int:
    from .extraction import lire_croquis  # import tardif : `dxf` marche sans clé API

    source = Path(args.croquis)
    sortie = Path(args.sortie)
    sortie.mkdir(parents=True, exist_ok=True)

    print(f"Lecture de {source.name}…")
    dessin = lire_croquis(source, args.precisions)

    json_path = sortie / f"{source.stem}.json"
    json_path.write_text(dessin.model_dump_json(indent=2), encoding="utf-8")
    apercu = sortie / f"{source.stem}_apercu.png"
    ecrire_apercu(dessin, apercu)

    print(f"Géométrie : {json_path}")
    print(f"Aperçu    : {apercu}  <- à comparer au croquis")
    _afficher_controles(dessin)
    print(f"\nEnsuite : python -m croquis2dxf dxf {json_path}")
    return 0


def cmd_dxf(args) -> int:
    json_path = Path(args.json)
    dessin = Dessin.model_validate_json(json_path.read_text(encoding="utf-8"))

    nb_alertes = _afficher_controles(dessin)
    if nb_alertes and not args.forcer:
        print("\nDXF non généré : corrige le JSON ou relance avec --forcer.")
        return 1

    dxf_path = json_path.with_suffix(".dxf")
    ecrire_dxf(dessin, dxf_path)
    ecrire_apercu(dessin, json_path.with_name(f"{json_path.stem}_apercu.png"))
    print(f"\nDXF : {dxf_path}  -> cadwork 2D : Fichier > Importer > DXF")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="croquis2dxf", description="Croquis main levée -> DXF")
    sous = parser.add_subparsers(dest="commande", required=True)

    p_lire = sous.add_parser("lire", help="Lire un croquis (jpg, png, pdf) et produire le JSON")
    p_lire.add_argument("croquis")
    p_lire.add_argument("-o", "--sortie", default="sorties")
    p_lire.add_argument("-p", "--precisions", default="",
                        help="Contexte utile, ex. « plan de solivage, cotes en cm »")
    p_lire.set_defaults(fonction=cmd_lire)

    p_dxf = sous.add_parser("dxf", help="Générer le DXF à partir du JSON validé")
    p_dxf.add_argument("json")
    p_dxf.add_argument("--forcer", action="store_true", help="Générer malgré les incohérences")
    p_dxf.set_defaults(fonction=cmd_dxf)

    args = parser.parse_args(argv)
    return args.fonction(args)


if __name__ == "__main__":
    sys.exit(main())
