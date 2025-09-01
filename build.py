#!/usr/bin/env python3
# build.py - Script de construction pour itch.io
import os
import shutil
import subprocess
from pathlib import Path

def build_for_itch():
    """Construit le jeu pour itch.io"""
    print("🔨 Construction pour itch.io...")
    
    # Nettoyer le build précédent
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Créer la structure de dossiers
    os.makedirs("build/web", exist_ok=True)
    os.makedirs("build/assets", exist_ok=True)
    
    # Copier les assets
    if os.path.exists("assets"):
        print("📦 Copie des assets...")
        shutil.copytree("assets", "build/assets", dirs_exist_ok=True)
    
    # Copier les fichiers Python
    print("🐍 Copie des fichiers Python...")
    python_files = [
        "main_web.py", "player.py", "environment.py", 
        "ui.py", "controls.py", "config.py"
    ]
    
    for file in python_files:
        if os.path.exists(file):
            shutil.copy2(file, "build/")
    
    # Copier les fichiers web
    print("🌐 Copie des fichiers web...")
    web_files = ["index.html", "pygbag.js", "pyproject.toml"]
    for file in web_files:
        if os.path.exists(file):
            shutil.copy2(file, "build/web/")
    
    # Créer un fichier README pour itch.io
    with open("build/README_itch.txt", "w", encoding="utf-8") as f:
        f.write("Ycrad l'Aventurier - Build pour itch.io\n")
        f.write("========================================\n\n")
        f.write("Pour uploader sur itch.io:\n")
        f.write("1. Aller dans https://itch.io/dashboard\n")
        f.write("2. Créer un nouveau projet\n")
        f.write("3. Uploader le contenu du dossier 'build/web/'\n")
        f.write("4. Configurer comme projet HTML5\n\n")
        f.write("Options recommandées:\n")
        f.write("- Embed: File\n")
        f.write("- File: index.html\n")
        f.write("- Viewport: 800x600\n")
        f.write("- Compression: Activée\n")
    
    print("✅ Build terminé!")
    print("📁 Dossier de build: build/web/")
    print("🚀 Uploader le contenu de build/web/ sur itch.io")

if __name__ == "__main__":
    build_for_itch()