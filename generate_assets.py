# generate_assets.py - Générateur d'assets de placeholder
import pygame
import os
import sys

def create_directory_structure():
    """Crée la structure de dossiers des assets"""
    directories = [
        "assets/character",
        "assets/monsters", 
        "assets/backgrounds",
        "assets/ui",
        "assets/ui/icons",
        "assets/items"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Créé: {directory}")

def generate_character_assets():
    """Génère les assets du personnage"""
    # Sprite du joueur
    player_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(player_surf, (0, 0, 255), (16, 16), 12)  # Corps bleu
    pygame.draw.circle(player_surf, (255, 200, 150), (16, 10), 6)  # Tête
    # Bras
    pygame.draw.rect(player_surf, (0, 0, 200), (8, 14, 16, 4))
    # Épée
    pygame.draw.rect(player_surf, (200, 200, 200), (20, 12, 8, 2))
    pygame.image.save(player_surf, "assets/character/player.png")
    print("✅ Sprite joueur généré")

def generate_monster_assets():
    """Génère les assets des monstres"""
    # Slime
    slime_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(slime_surf, (0, 200, 0), (4, 12, 24, 16))  # Corps
    pygame.draw.circle(slime_surf, (0, 150, 0), (16, 8), 6)  # Yeux
    pygame.draw.circle(slime_surf, (255, 255, 255), (14, 7), 1)  # Reflet
    pygame.draw.circle(slime_surf, (255, 255, 255), (18, 7), 1)
    pygame.image.save(slime_surf, "assets/monsters/slime.png")
    
    # Rat
    rat_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.ellipse(rat_surf, (139, 69, 19), (8, 12, 20, 10))  # Corps
    pygame.draw.ellipse(rat_surf, (100, 50, 10), (4, 8, 8, 6))  # Tête
    pygame.draw.line(rat_surf, (0, 0, 0), (8, 10), (2, 6), 1)  # Moustache
    pygame.draw.line(rat_surf, (0, 0, 0), (8, 12), (2, 12), 1)
    pygame.draw.line(rat_surf, (0, 0, 0), (8, 14), (2, 18), 1)
    pygame.image.save(rat_surf, "assets/monsters/rat.png")
    
    print("✅ Sprites monstres générés")

def generate_background_assets():
    """Génère les arrière-plans"""
    # Village
    village_surf = pygame.Surface((800, 600))
    village_surf.fill((200, 200, 100))  # Sol
    pygame.draw.rect(village_surf, (150, 100, 50), (0, 400, 800, 200))  # Terre
    
    # Maisons
    for i in range(4):
        x = 100 + i * 180
        pygame.draw.rect(village_surf, (150, 100, 50), (x, 250, 80, 100))  # Mur
        pygame.draw.polygon(village_surf, (100, 50, 25), 
                          [(x, 250), (x+80, 250), (x+40, 200)])  # Toit
        pygame.draw.rect(village_surf, (50, 50, 150), (x+30, 300, 20, 50))  # Porte
    
    # Ciel
    for i in range(20):
        x = random.randint(0, 800)
        y = random.randint(0, 200)
        pygame.draw.circle(village_surf, (255, 255, 255), (x, y), 1)
    
    pygame.image.save(village_surf, "assets/backgrounds/village.png")
    
    # Forêt
    forest_surf = pygame.Surface((800, 600))
    forest_surf.fill((0, 100, 0))  # Sol
    pygame.draw.rect(forest_surf, (50, 70, 20), (0, 400, 800, 200))  # Terre
    
    # Arbres
    for i in range(15):
        x = random.randint(50, 750)
        y = random.randint(200, 400)
        pygame.draw.rect(forest_surf, (100, 50, 0), (x, y, 20, 80))  # Tronc
        pygame.draw.circle(forest_surf, (0, 80, 0), (x+10, y-20), 30)  # Feuillage
    
    pygame.image.save(forest_surf, "assets/backgrounds/forest.png")
    
    print("✅ Arrière-plans générés")

def generate_ui_assets():
    """Génère les assets d'interface"""
    # Icônes d'items
    items = {
        "potion": (255, 0, 0),
        "sword": (200, 200, 200),
        "shield": (150, 100, 50),
        "coin": (255, 215, 0)
    }
    
    for item_name, color in items.items():
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        if item_name == "potion":
            pygame.draw.rect(surf, color, (12, 8, 8, 20))
            pygame.draw.ellipse(surf, color, (10, 4, 12, 8))
        elif item_name == "sword":
            pygame.draw.rect(surf, color, (15, 8, 2, 20))
            pygame.draw.polygon(surf, color, [(10, 8), (22, 8), (16, 4)])
        elif item_name == "shield":
            pygame.draw.rect(surf, color, (10, 8, 12, 16), 0, 5)
            pygame.draw.circle(surf, (100, 100, 100), (16, 16), 4)
        elif item_name == "coin":
            pygame.draw.circle(surf, color, (16, 16), 10)
            pygame.draw.circle(surf, (200, 150, 0), (16, 16), 8)
        
        pygame.image.save(surf, f"assets/ui/icons/{item_name}.png")
    
    print("✅ Icônes UI générées")

def main():
    """Fonction principale"""
    print("🎨 Génération des assets de placeholder...")
    
    # Initialiser pygame
    pygame.init()
    
    try:
        create_directory_structure()
        generate_character_assets()
        generate_monster_assets()
        generate_background_assets()
        generate_ui_assets()
        
        print("\n✅ Tous les assets ont été générés avec succès!")
        print("📁 Dossier assets/ créé avec tous les fichiers nécessaires")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return 1
    
    finally:
        pygame.quit()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())