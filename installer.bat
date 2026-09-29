@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Installation de croquis2dxf ===
echo.
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY (
    echo ERREUR : Python est introuvable.
    echo Installe Python depuis https://www.python.org en cochant "Add python.exe to PATH".
    pause
    exit /b 1
)
%PY% -m venv .venv || (echo ERREUR : création de l'environnement impossible. & pause & exit /b 1)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt || (echo ERREUR : installation des modules impossible. & pause & exit /b 1)
echo.
echo Installation terminée. Tu peux fermer cette fenêtre.
pause
