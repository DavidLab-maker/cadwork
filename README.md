# croquis2dxf — du croquis main levée au DXF pour cadwork 2D

Prototype : un croquis (photo JPG/PNG ou scan PDF) est lu par Claude, retranscrit
en géométrie cotée (JSON), contrôlé, puis converti en DXF à importer dans cadwork 2D.

```
croquis.jpg ──lire──▶ croquis.json + croquis_apercu.png ──(relecture humaine)──▶ dxf ──▶ croquis.dxf
```

**Débutant ? Suis le [guide pas à pas](GUIDE_DEBUTANT.md)** (installation par
double-clic, croquis par glisser-déposer).

> **La relecture n'est pas optionnelle.** Un chiffre manuscrit mal lu donne une
> géométrie fausse mais propre. L'outil fait gagner le temps de saisie, pas la
> vérification.

## Installation (Windows, une fois)

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
setx ANTHROPIC_API_KEY "sk-ant-..."
```

Clé API : https://console.anthropic.com (compter quelques centimes par croquis).

## Utilisation

```bat
:: 1. Lecture du croquis
python -m croquis2dxf lire C:\croquis\plancher.jpg -p "plan de solivage, cotes en cm"

:: 2. Comparer sorties\plancher_apercu.png au croquis.
::    Lire la liste « À VÉRIFIER ». Corriger sorties\plancher.json si besoin.

:: 3. Génération du DXF (bloquée si une cote ne correspond pas à la géométrie)
python -m croquis2dxf dxf sorties\plancher.json
```

Puis dans cadwork 2D : import DXF de `sorties\plancher.dxf` (unités : mm).

## Ce que fait l'outil

- **Les cotes écrites font foi**, pas les proportions du tracé.
- Redresse les traits (horizontaux, verticaux, angles droits).
- Calques DXF : `CONTOUR`, `AXE` (mixte), `CACHE` (pointillé), `DETAIL`, `COTES`, `TEXTES`.
- Les cotes du DXF affichent la **mesure réelle** de la géométrie : un écart avec
  le croquis se voit immédiatement.
- Contrôle automatique : chaque cote lue est comparée à la géométrie (tolérance 1 mm).
  En cas d'écart, le DXF n'est pas généré (sauf `--forcer`).
- Tout ce qui est supposé ou illisible est listé dans `incertitudes`.

## Limites connues

- Croquis très chargés : découper en plusieurs vues (une vue = un fichier).
- Cotes d'angle, arcs et courbes : peu fiables à ce stade.
- Pas d'import direct dans cadwork : passage obligatoire par l'import DXF.

## Structure

| Fichier | Rôle |
|---|---|
| `croquis2dxf/modele.py` | Format du JSON (géométrie en mm) |
| `croquis2dxf/extraction.py` | Lecture du croquis par Claude |
| `croquis2dxf/verification.py` | Contrôles cotes / géométrie |
| `croquis2dxf/dxf.py` | Écriture DXF + aperçu PNG |
| `exemples/solivage.json` | Exemple : plancher 4,50 m, 5 solives e=50 cm |

Tests : `python -m pytest`
