# build_itchio_final.py - Build final pour itch.io
import os
import shutil
import zipfile

def build_final():
    print("🔨 Construction finale pour itch.io...")
    
    build_dir = "build_itchio_final"
    
    # Nettoyer le build précédent
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    os.makedirs(build_dir, exist_ok=True)
    
    # Fichiers HTML essentiels
    html_files = ['index.html', 'game.html']
    for file in html_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(build_dir, file))
        else:
            print(f"⚠️  Fichier manquant: {file}")
    
    # Fichiers Python essentiels
    python_files = [
        'main_web.py',
        'player.py', 
        'environment.py',
        'ui.py',
        'controls.py',
        'monsters.py',
        'config.py'
    ]
    
    for file in python_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(build_dir, file))
        else:
            print(f"⚠️  Fichier Python manquant: {file}")
    
    # Copier les assets
    if os.path.exists("assets"):
        shutil.copytree("assets", os.path.join(build_dir, "assets"))
        print("✅ Assets copiés")
    else:
        print("⚠️  Dossier assets manquant")
    
    # Créer un fichier README
    readme_content = """Ycrad l'Aventurier - Build pour itch.io
========================================

Fichiers inclus:
- index.html : Page d'accueil avec iframe
- game.html : Page du jeu principal
- *.py : Code source Python du jeu
- assets/ : Graphismes et ressources

Comment uploader sur itch.io:
1. Aller sur https://itch.io/dashboard
2. Créer un nouveau projet
3. Uploader tout le contenu de ce dossier
4. Configurer: Type=HTML, File=index.html
"""
    
    with open(os.path.join(build_dir, "README_ITCHIO.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Créer un zip
    create_zip_file(build_dir)
    
    print(f"✅ Build final terminé! Dossier: {build_dir}/")

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

if __name__ == "__main__":
    build_final()