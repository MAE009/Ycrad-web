# generate_assets.py - Génère des assets de placeholder
import pygame
import os

def generate_placeholder_assets():
    """Génère des assets de base pour le jeu"""
    assets_dir = "assets"
    directories = [
        "character",
        "monsters", 
        "backgrounds",
        "ui",
        "items"
    ]
    
    # Créer les dossiers
    for directory in directories:
        os.makedirs(f"{assets_dir}/{directory}", exist_ok=True)
    
    # Générer le sprite du joueur
    player_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(player_surf, (0, 0, 255), (16, 16), 12)  # Corps bleu
    pygame.draw.circle(player_surf, (255, 200, 150), (16, 10), 6)  # Tête
    pygame.image.save(player_surf, f"{assets_dir}/character/player.png")
    
    # Générer des monstres
    monsters = {
        "slime": ((0, 255, 0), (0, 200, 0)),
        "rat": ((139, 69, 19), (100, 50, 10)),
        "goblin": ((0, 100, 0), (0, 150, 0))
    }
    
    for name, (color1, color2) in monsters.items():
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, color1, (4, 8, 24, 20))  # Corps
        pygame.draw.circle(surf, color2, (16, 6), 8)  # Tête
        pygame.image.save(surf, f"{assets_dir}/monsters/{name}.png")
    
    # Générer des backgrounds
    backgrounds = {
        "village": (200, 200, 100),
        "forest": (0, 100, 0), 
        "marsh": (70, 50, 30),
        "dungeon": (50, 50, 70)
    }
    
    for name, color in backgrounds.items():
        surf = pygame.Surface((800, 600))
        surf.fill(color)
        # Ajouter quelques détails
        if name == "village":
            for i in range(5):
                pygame.draw.rect(surf, (150, 100, 50), (100 + i*120, 200, 60, 80))
        elif name == "forest":
            for i in range(10):
                pygame.draw.circle(surf, (0, 70, 0), (100 + i*80, 150), 30)
        pygame.image.save(surf, f"{assets_dir}/backgrounds/{name}.png")
    
    print("✅ Assets de placeholder générés!")

if __name__ == "__main__":
    generate_placeholder_assets()