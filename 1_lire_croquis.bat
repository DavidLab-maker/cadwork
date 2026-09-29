@echo off
chcp 65001 >nul
cd /d "%~dp0"
if "%~1"=="" (
    echo Glisse-dépose un croquis ^(jpg, png ou pdf^) sur ce fichier.
    pause
    exit /b 1
)
if not exist .venv\Scripts\activate.bat (
    echo Lance d'abord installer.bat
    pause
    exit /b 1
)
if "%ANTHROPIC_API_KEY%"=="" (
    echo ERREUR : clé API absente. Voir le guide, étape 4.
    pause
    exit /b 1
)
echo Croquis : %~nx1
echo.
echo Précisions utiles pour la lecture, par exemple :
echo    mur ép. 40 cm, cotes en cm, première solive à 10 cm du mur
set "PRECISIONS="
set /p "PRECISIONS=Précisions (ou Entrée pour aucune) : "
echo.
call .venv\Scripts\activate.bat
python -m croquis2dxf lire "%~1" -o "%~dp1." -p "%PRECISIONS%"
if errorlevel 1 (pause & exit /b 1)
start "" "%~dpn1_apercu.png"
pause
