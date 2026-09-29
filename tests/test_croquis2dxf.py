import json
from pathlib import Path

import ezdxf

from croquis2dxf.__main__ import main
from croquis2dxf.dxf import ecrire_dxf
from croquis2dxf.modele import Dessin
from croquis2dxf.verification import verifier

EXEMPLE = Path(__file__).parent.parent / "exemples" / "solivage.json"


def charger():
    return Dessin.model_validate_json(EXEMPLE.read_text(encoding="utf-8"))


def test_exemple_sans_incoherence():
    assert verifier(charger()) == []


def test_cote_incoherente_detectee():
    dessin = charger()
    dessin.cotes[0].valeur_lue = 4800
    alertes = verifier(dessin)
    assert len(alertes) == 1 and "4800" in alertes[0]


def test_dxf_contient_la_geometrie(tmp_path):
    dessin = charger()
    chemin = tmp_path / "s.dxf"
    ecrire_dxf(dessin, chemin)
    msp = ezdxf.readfile(chemin).modelspace()
    assert len(msp.query("LWPOLYLINE")) == len(dessin.polylignes)
    assert len(msp.query("DIMENSION")) == len(dessin.cotes)
    assert {e.dxf.layer for e in msp.query("LINE")} == {"AXE"}


def test_cli_refuse_si_incoherence(tmp_path):
    d = json.loads(EXEMPLE.read_text(encoding="utf-8"))
    d["cotes"][0]["valeur_lue"] = 4800
    chemin = tmp_path / "faux.json"
    chemin.write_text(json.dumps(d), encoding="utf-8")
    assert main(["dxf", str(chemin)]) == 1
    assert not chemin.with_suffix(".dxf").exists()
    assert main(["dxf", str(chemin), "--forcer"]) == 0
    assert chemin.with_suffix(".dxf").exists()


def test_croquis_reel_plancher_poutre(tmp_path):
    chemin = EXEMPLE.with_name("plancher_poutre_LC.json")
    dessin = Dessin.model_validate_json(chemin.read_text(encoding="utf-8"))
    assert verifier(dessin) == []
    ecrire_dxf(dessin, tmp_path / "p.dxf")
    msp = ezdxf.readfile(tmp_path / "p.dxf").modelspace()
    assert len(msp.query("HATCH")) == 4  # 4 murs maçonnés
    assert len(msp.query("LWPOLYLINE")) == 4 + 1 + 32  # murs, poutre, 2 x 16 solives
