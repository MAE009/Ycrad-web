# build_itchio.py - Script de construction pour itch.io
import os
import shutil
import zipfile
from pathlib import Path

def build_for_itchio():
    """Construit le jeu pour itch.io"""
    print("🔨 Construction pour itch.io...")
    
    # Nettoyer les builds précédents
    if os.path.exists("build_itchio"):
        shutil.rmtree("build_itchio")
    
    os.makedirs("build_itchio", exist_ok=True)
    
    # Fichiers nécessaires pour itch.io
    files_to_copy = [
        'index.html',
        'pygbag.js', 
        'sw.js',
        'pyproject.toml'
    ]
    
    # Copier les fichiers
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, f"build_itchio/{file}")
    
    # Copier le dossier assets
    if os.path.exists("assets"):
        shutil.copytree("assets", "build_itchio/assets")
    
    # Créer un fichier README pour itch.io
    with open("build_itchio/README.txt", "w", encoding="utf-8") as f:
        f.write("Ycrad l'Aventurier - RPG Pixel Art\n")
        f.write("==================================\n\n")
        f.write("Comment jouer :\n")
        f.write("- ZQSD/Flèches : Se déplacer\n")
        f.write("- E : Interagir\n")
        f.write("- Espace : Attaquer\n")
        f.write("- I : Inventaire\n\n")
        f.write("Le jeu peut prendre quelques secondes à charger.\n")
    
    print("✅ Build itch.io terminé!")
    print("📁 Dossier : build_itchio/")
    
    # Créer un zip pour upload facile
    create_zip_file()

def create_zip_file():
    """Crée un fichier zip pour l'upload"""
    zip_path = "ycrad-adventurer-itchio.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("build_itchio"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "build_itchio")
                zipf.write(file_path, arcname)
    
    print(f"📦 Fichier zip créé : {zip_path}")

if __name__ == "__main__":
    build_for_itchio()