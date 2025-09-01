# build.py - Script de construction pour itch.io
import os
import shutil
import zipfile
from pathlib import Path

def build_itchio():
    """Construit le jeu pour itch.io"""
    print("🔨 Construction pour itch.io...")
    
    build_dir = "build_itchio"
    
    # Nettoyer le build précédent
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print("🧹 Build précédent nettoyé")
    
    os.makedirs(build_dir, exist_ok=True)
    
    # Fichiers HTML
    copy_essential_files(build_dir)
    
    # Fichiers Python
    copy_python_files(build_dir)
    
    # Assets
    copy_assets(build_dir)
    
    # Fichiers de configuration
    copy_config_files(build_dir)
    
    # Créer un fichier README
    create_readme(build_dir)
    
    # Créer un zip
    create_zip_file(build_dir)
    
    print(f"✅ Build terminé! Dossier: {build_dir}/")
    print("🚀 Uploader le contenu sur itch.io")

def copy_essential_files(build_dir):
    """Copie les fichiers essentiels"""
    essential_files = [
        'index.html',
        'pygbag.js',
        'sw.js',
        'requirements.txt',
        'README.md'
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(build_dir, file))
            print(f"📄 Copié: {file}")
        else:
            print(f"⚠️  Manquant: {file}")

def copy_python_files(build_dir):
    """Copie les fichiers Python"""
    python_files = [
        'main_web.py',
        'player.py',
        'environment.py',
        'ui.py',
        'controls.py',
        'monsters.py',
        'config.py',
        'quests.py',
        'inventory.py',
        'animation.py',
        'tilemap.py',
        'map_generator.py',
        'asset_generator.py'
    ]
    
    for file in python_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(build_dir, file))
            print(f"🐍 Copié: {file}")
        else:
            print(f"⚠️  Manquant: {file}")

def copy_assets(build_dir):
    """Copie les assets"""
    assets_dirs = [
        'assets/character',
        'assets/monsters',
        'assets/backgrounds',
        'assets/ui',
        'assets/maps',
        'assets/tilesets'
    ]
    
    for asset_dir in assets_dirs:
        if os.path.exists(asset_dir):
            dest_dir = os.path.join(build_dir, asset_dir)
            shutil.copytree(asset_dir, dest_dir, dirs_exist_ok=True)
            print(f"🎨 Copié: {asset_dir}/")
        else:
            print(f"⚠️  Manquant: {asset_dir}/")

def copy_config_files(build_dir):
    """Copie les fichiers de configuration"""
    config_files = [
        'pyproject.toml',
        'runtime.txt'
    ]
    
    for file in config_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(build_dir, file))
            print(f"⚙️  Copié: {file}")
        else:
            print(f"⚠️  Manquant: {file}")

def create_readme(build_dir):
    """Crée un fichier README"""
    readme_content = """Ycrad l'Aventurier - Build pour itch.io
========================================

📦 Contenu du build:
- index.html : Page principale
- *.py : Code source du jeu
- assets/ : Ressources graphiques
- pyproject.toml : Configuration Pygbag

🚀 Comment uploader sur itch.io:
1. Aller sur https://itch.io/dashboard
2. Créer un nouveau projet
3. Uploader le contenu de ce dossier
4. Configurer:
   - Type: HTML
   - File: index.html  
   - Viewport: 800x600
   - Compression: Activée

🎮 Contrôles:
- ZQSD/Flèches : Déplacement
- E : Interagir
- Espace : Attaquer
- I : Inventaire
- Échap : Pause

📝 Notes:
- Le jeu utilise Pyodide pour exécuter Python dans le navigateur
- Le chargement peut prendre quelques secondes
- Compatible desktop et mobile

© 2024 Votre Studio - Version Web
"""
    
    with open(os.path.join(build_dir, "README_ITCHIO.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("📝 Fichier README créé")

def create_zip_file(build_dir):
    """Crée un fichier zip pour l'upload"""
    zip_path = "ycrad-adventurer-itchio.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, build_dir)
                zipf.write(file_path, arcname)
    
    print(f"📦 Fichier zip créé: {zip_path}")

def check_dependencies():
    """Vérifie les dépendances nécessaires"""
    print("🔍 Vérification des dépendances...")
    
    # Vérifier que Python est installé
    try:
        import pygame
        print("✅ PyGame installé")
    except ImportError:
        print("❌ PyGame non installé. Installez avec: pip install pygame")
        return False
    
    return True

if __name__ == "__main__":
    print("🎮 Construction de Ycrad l'Aventurier")
    print("=" * 50)
    
    if check_dependencies():
        build_itchio()
        print("\n✅ Build terminé avec succès!")
        print("\n📋 Prochaines étapes:")
        print("1. Uploader le fichier ycrad-adventurer-itchio.zip sur itch.io")
        print("2. Ou uploader le dossier build_itchio/")
        print("3. Configurer comme projet HTML")
        print("4. Partager le lien avec vos amis! 🎉")
    else:
        print("❌ Build échoué à cause de dépendances manquantes")
