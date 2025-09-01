# create_thumbnails.py - Crée des miniatures pour itch.io
from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnails():
    """Crée des miniatures pour itch.io"""
    # Créer le dossier thumbnails
    os.makedirs("thumbnails", exist_ok=True)
    
    # Dimensions standard itch.io
    sizes = {
        "cover": (600, 450),      # Image de couverture
        "thumbnail": (280, 210),  # Miniature
        "screenshot": (800, 600)  # Capture d'écran
    }
    
    # Créer des images de placeholder
    for name, size in sizes.items():
        img = Image.new('RGB', size, color=(40, 40, 60))
        draw = ImageDraw.Draw(img)
        
        # Ajouter du texte
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = "Ycrad l'Aventurier"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) / 2
        y = (size[1] - text_height) / 2
        
        draw.text((x, y), text, font=font, fill=(255, 215, 0))
        draw.text((x, y + 30), name, font=font, fill=(200, 200, 200))
        
        img.save(f"thumbnails/{name}.jpg")
        print(f"✅ Miniature créée: thumbnails/{name}.jpg")

if __name__ == "__main__":
    create_thumbnails()