# build.py - Script de construction adapté pour Render
import os
import shutil
import subprocess
from pathlib import Path

def build_for_render():
    """Construit le jeu pour Render"""
    print("🔨 Construction pour Render...")
    
    # Nettoyer le build précédent
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Créer la structure de dossiers
    os.makedirs("build/web", exist_ok=True)
    
    # Copier les fichiers essentiels
    essential_files = [
        "index.html", "pygbag.js", "sw.js", "requirements.txt"
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, f"build/web/{file}")
    
    # Copier les fichiers Python nécessaires
    python_files = [
        "main_web.py", "player.py", "environment.py", 
        "ui.py", "controls.py", "monsters.py", "config.py"
    ]
    
    for file in python_files:
        if os.path.exists(file):
            shutil.copy2(file, f"build/web/{file}")
    
    # Copier les assets
    if os.path.exists("assets"):
        shutil.copytree("assets", "build/web/assets", dirs_exist_ok=True)
    
    # Créer un fichier de configuration Render
    with open("build/web/static.json", "w") as f:
        f.write('''{
  "rewrites": [
    { "source": "**", "destination": "/index.html" }
  ]
}''')
    
    print("✅ Build Render terminé!")
    print("📁 Dossier de build: build/web/")

if __name__ == "__main__":
    build_for_render()