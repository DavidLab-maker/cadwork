@echo off
chcp 65001 >nul
cd /d "%~dp0"
if "%~1"=="" (
    echo Glisse-dépose le fichier .json produit par 1_lire_croquis sur ce fichier.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat
python -m croquis2dxf dxf "%~1"
if errorlevel 1 (
    echo.
    echo Relance 1_lire_croquis avec des précisions, ou corrige le .json.
    pause
    exit /b 1
)
echo.
echo Le fichier %~n1.dxf est dans le dossier : %~dp1
start "" "%~dpn1_apercu.png"
pause
