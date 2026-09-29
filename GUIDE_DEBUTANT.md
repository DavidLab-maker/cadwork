# Guide pas à pas : du croquis au plan cadwork 2D

Durée de la première installation : environ 30 minutes. Ensuite : 2 minutes par croquis.

Ordre conseillé : on vérifie d'abord que l'import dans cadwork fonctionne avec
l'exemple fourni (étapes 1 à 3, **gratuit**), et seulement ensuite on crée la
clé API payante (étape 4).

---

## Étape 1 — Installer Python (une seule fois par poste)

1. Va sur https://www.python.org/downloads/ et clique sur le gros bouton jaune
   **Download Python 3.12.x** (ou plus récent).
2. Lance le fichier téléchargé.
3. **IMPORTANT** : en bas de la première fenêtre, coche **« Add python.exe to PATH »**.
   Sans cette case, rien ne marchera.
4. Clique sur **Install Now**, attends, puis **Close**.

Vérification : touche Windows, tape `cmd`, Entrée. Dans la fenêtre noire, tape
`py --version` puis Entrée. Tu dois voir `Python 3.12.x`. Ferme la fenêtre.

## Étape 2 — Récupérer l'outil et l'installer

1. Va sur la page GitHub du dépôt `davidlab-maker/cadwork` (connecte-toi).
2. En haut à gauche, clique sur le menu des branches (il affiche `main`) et
   choisis **`claude/cadwork-plugin-creation-c34z45`**.
3. Clique sur le bouton vert **Code** → **Download ZIP**.
4. Dans tes Téléchargements, clic droit sur le ZIP → **Extraire tout…** →
   choisis par exemple `C:\Outils\croquis2dxf` → **Extraire**.
5. Ouvre ce dossier. Tu dois y voir `installer.bat`, `1_lire_croquis.bat`,
   `2_generer_dxf.bat`, et les dossiers `croquis2dxf` et `exemples`.
6. **Double-clique sur `installer.bat`.** Une fenêtre noire s'ouvre et télécharge
   les modules (2 à 5 minutes). Attends le message **« Installation terminée »**.

Si Windows affiche « Windows a protégé votre ordinateur » : clique sur
**Informations complémentaires** → **Exécuter quand même** (c'est ton propre fichier).

## Étape 3 — Tester l'import dans cadwork 2D avec l'exemple (gratuit)

Le fichier `exemples\plancher_poutre_LC.dxf` est déjà généré à partir de ton croquis.

1. Ouvre cadwork 2D, crée un nouveau dessin.
2. Menu d'import DXF/DWG (en général **Fichier → Importer → DXF/DWG** ; le libellé
   exact dépend de ta version de cadwork).
3. Choisis `exemples\plancher_poutre_LC.dxf`.
4. Dans les options d'import, si on te demande l'unité : **millimètre**
   (1 unité du fichier = 1 mm).
5. Contrôle : mesure avec l'outil de mesure de cadwork la distance entre les
   nus intérieurs des murs. Tu dois trouver **8000 mm**.
   - Si tu trouves 800 ou 80 000 : le réglage d'unité à l'import est faux,
     recommence en changeant l'unité.
6. Regarde les calques (ou couches) importés : `CONTOUR`, `AXE`, `HACHURES`,
   `COTES`, `TEXTES`.

**Si l'import échoue ou donne un résultat bizarre, arrête-toi là** et envoie-moi
une capture d'écran : inutile de payer l'API tant que cette étape ne marche pas.

## Étape 4 — Créer la clé API (une seule fois)

La clé permet à l'outil d'envoyer le croquis à Claude pour qu'il le lise.
Coût : quelques centimes par croquis.

1. Va sur https://console.anthropic.com et crée un compte (idéalement avec
   l'adresse de l'entreprise).
2. Menu **Billing** (Facturation) : ajoute un moyen de paiement et achète des
   crédits (le minimum, 5 $, suffit pour des dizaines de croquis).
3. Menu **Limits** : fixe une **limite de dépense mensuelle** (par ex. 20 $).
   C'est ton garde-fou si la clé fuit.
4. Menu **API Keys** → **Create Key** → nomme-la `croquis2dxf-poste-XX` →
   **copie la clé** (elle commence par `sk-ant-`). Elle ne s'affiche qu'une fois.
5. Enregistre-la dans Windows :
   - touche Windows, tape **« variables d'environnement »**, choisis
     **« Modifier les variables d'environnement pour votre compte »** ;
   - dans le cadre du haut, clique **Nouvelle…** ;
   - Nom de la variable : `ANTHROPIC_API_KEY`
   - Valeur de la variable : colle ta clé ;
   - **OK**, puis **OK**.
6. Ferme toutes les fenêtres noires ouvertes (la clé n'est prise en compte que
   dans les nouvelles fenêtres).

Sécurité : cette clé est un moyen de paiement. Ne l'envoie pas par mail, ne la
mets pas dans un fichier partagé. Une clé par poste : si un poste est compromis,
tu supprimes sa clé sans toucher aux autres.

## Étape 5 — Transformer un vrai croquis

### 5.1 Préparer le croquis
- Photo prise **bien à plat, au-dessus de la feuille**, sans ombre, feuille entière
  dans le cadre ; ou scan en PDF.
- Une seule vue par feuille.
- **Écris les unités** (cm) et **cote les appuis** : chaque cote manquante devient
  une hypothèse à vérifier.
- Mets le fichier dans le dossier du projet, par ex. `C:\Projets\2026-042\croquis.jpg`.

### 5.2 Lire le croquis
1. **Glisse-dépose** le fichier du croquis **sur `1_lire_croquis.bat`**.
2. La fenêtre te demande des **précisions**. Tape ce que tu sais et qui n'est pas
   évident sur le croquis, par exemple :
   `mur ép. 40 cm, cotes en cm, appui poutre 20 cm`
   puis Entrée (ou juste Entrée si rien à ajouter).
3. Attends 30 s à 2 min. L'aperçu `croquis_apercu.png` s'ouvre tout seul.
4. Dans la fenêtre noire, lis les deux listes :
   - **À VÉRIFIER** : ce que l'IA a supposé ou n'a pas pu lire ;
   - **INCOHÉRENCES DÉTECTÉES** : cotes qui ne correspondent pas à la géométrie.

### 5.3 Vérifier (obligatoire)
Compare l'aperçu à ton croquis, élément par élément : murs, poutres, nombre de
solives, chaque cote.

- **Tout est bon** → étape 5.4.
- **Une erreur de lecture** (ex. mur lu à 140 cm au lieu de 40) → le plus simple
  est de **relancer l'étape 5.2** en l'écrivant dans les précisions :
  `le mur fait 40 cm d'épaisseur, pas 140`.
- **Petite retouche** (une solive en trop, un texte mal placé) → ne perds pas de
  temps : génère le DXF et corrige directement dans cadwork 2D.

### 5.4 Générer le DXF
1. Dans le dossier du croquis, un fichier `croquis.json` est apparu.
2. **Glisse-dépose `croquis.json` sur `2_generer_dxf.bat`.**
3. Si une incohérence est détectée, le DXF n'est pas créé : relance l'étape 5.2
   avec des précisions.
4. Sinon, `croquis.dxf` est créé dans le même dossier.

### 5.5 Importer dans cadwork 2D
Comme à l'étape 3 : import DXF, unité millimètre, puis **mesure une cote de
contrôle** avant de continuer ton plan.

---

## En cas de problème

| Message | Cause | Solution |
|---|---|---|
| `Python est introuvable` | Case « Add to PATH » non cochée | Relance l'installateur Python → **Modify** ou désinstalle/réinstalle en cochant la case |
| `Lance d'abord installer.bat` | Installation pas faite | Double-clic sur `installer.bat` |
| `clé API absente` | Variable non créée, ou fenêtre ouverte avant | Refais l'étape 4.5, ferme et rouvre |
| `AuthenticationError` / `401` | Clé mal copiée | Recrée une clé, recolle-la |
| `credit balance is too low` | Plus de crédits | Console Anthropic → Billing |
| `Réponse tronquée` | Croquis trop chargé | Une vue par feuille |
| Import cadwork : dessin minuscule ou géant | Mauvaise unité à l'import | Choisir millimètre |

Dans tous les autres cas : fais une capture de la fenêtre noire et envoie-la.
