# asset_generator.py - Générateur d'assets de fallback
import pygame
import os
import json

class AssetGenerator:
    def __init__(self):
        self.assets_created = 0
    
    def generate_all_assets(self):
        """Génère tous les assets manquants"""
        print("🎨 Génération des assets manquants...")
        
        # Structure de dossiers
        directories = [
            "assets/character",
            "assets/monsters",
            "assets/backgrounds", 
            "assets/ui/icons",
            "assets/maps",
            "assets/tilesets"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Créé: {directory}")
        
        # Générer les assets
        self.generate_backgrounds()
        self.generate_character()
        self.generate_monsters()
        self.generate_ui_icons()
        self.generate_tilesets()
        
        print(f"✅ {self.assets_created} assets générés!")
    
    def generate_backgrounds(self):
        """Génère les arrière-plans"""
        backgrounds = {
            "village": (200, 200, 100),  # Jaune sable
            "forest": (0, 100, 0),       # Vert forêt
            "marsh": (70, 50, 30),       # Marron marais
            "dungeon": (50, 50, 70)      # Bleu sombre
        }
        
        for name, color in backgrounds.items():
            bg = pygame.Surface((800, 600))
            bg.fill(color)
            
            # Ajouter des détails selon le type
            if name == "village":
                self.add_village_details(bg)
            elif name == "forest":
                self.add_forest_details(bg)
            elif name == "marsh":
                self.add_marsh_details(bg)
            elif name == "dungeon":
                self.add_dungeon_details(bg)
            
            pygame.image.save(bg, f"assets/backgrounds/{name}.png")
            self.assets_created += 1
            print(f"🖼️  Généré: assets/backgrounds/{name}.png")
    
    def add_village_details(self, surface):
        """Ajoute des détails au village"""
        # Maisons
        for i in range(3):
            x = 100 + i * 200
            pygame.draw.rect(surface, (150, 100, 50), (x, 200, 80, 60))
            pygame.draw.polygon(surface, (100, 50, 25), 
                              [(x, 200), (x+80, 200), (x+40, 160)])
        
        # Chemin
        pygame.draw.rect(surface, (180, 160, 100), (0, 300, 800, 60))
    
    def add_forest_details(self, surface):
        """Ajoute des détails à la forêt"""
        # Arbres
        for i in range(15):
            x = 50 + (i * 50) % 700
            y = 100 + (i * 70) % 400
            pygame.draw.rect(surface, (100, 50, 0), (x, y, 20, 40))
            pygame.draw.circle(surface, (0, 80, 0), (x+10, y-15), 25)
    
    def add_marsh_details(self, surface):
        """Ajoute des détails au marais"""
        # Zones d'eau
        for i in range(5):
            x = 100 + i * 150
            y = 150 + (i * 50) % 300
            pygame.draw.ellipse(surface, (50, 70, 80), (x, y, 100, 60))
    
    def add_dungeon_details(self, surface):
        """Ajoute des détails au donjon"""
        # Pierres/murs
        for i in range(20):
            x = 50 + (i * 40) % 700
            y = 100 + (i * 30) % 400
            pygame.draw.rect(surface, (70, 70, 90), (x, y, 30, 30))
            pygame.draw.rect(surface, (90, 90, 110), (x+5, y+5, 20, 20))
    
    def generate_character(self):
        """Génère le sprite du joueur"""
        sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Corps
        pygame.draw.rect(sprite, (0, 0, 255), (8, 12, 16, 16))
        
        # Tête
        pygame.draw.circle(sprite, (255, 200, 150), (16, 8), 6)
        
        # Épée
        pygame.draw.rect(sprite, (200, 200, 200), (20, 14, 8, 4))
        
        pygame.image.save(sprite, "assets/character/player.png")
        self.assets_created += 1
        print(f"👤 Généré: assets/character/player.png")
    
    def generate_monsters(self):
        """Génère les sprites de monstres"""
        monsters = {
            "slime": (0, 150, 0),
            "rat": (139, 69, 19),
            "goblin": (0, 100, 0)
        }
        
        for name, color in monsters.items():
            sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
            
            if name == "slime":
                pygame.draw.ellipse(sprite, color, (4, 12, 24, 16))
                pygame.draw.circle(sprite, (0, 100, 0), (16, 8), 6)
            elif name == "rat":
                pygame.draw.ellipse(sprite, color, (8, 12, 20, 10))
                pygame.draw.ellipse(sprite, (100, 50, 10), (4, 8, 8, 6))
            else:
                pygame.draw.rect(sprite, color, (8, 8, 16, 16))
            
            pygame.image.save(sprite, f"assets/monsters/{name}.png")
            self.assets_created += 1
            print(f"🐉 Généré: assets/monsters/{name}.png")
    
    def generate_ui_icons(self):
        """Génère les icônes d'interface"""
        icons = {
            "potion": (255, 0, 0),
            "sword": (200, 200, 200),
            "shield": (150, 100, 50),
            "coin": (255, 215, 0)
        }
        
        for name, color in icons.items():
            icon = pygame.Surface((32, 32), pygame.SRCALPHA)
            
            if name == "potion":
                pygame.draw.rect(icon, color, (12, 8, 8, 20))
                pygame.draw.ellipse(icon, color, (10, 4, 12, 8))
            elif name == "sword":
                pygame.draw.rect(icon, color, (15, 8, 2, 20))
                pygame.draw.polygon(icon, color, [(10, 8), (22, 8), (16, 4)])
            elif name == "shield":
                pygame.draw.rect(icon, color, (10, 8, 12, 16), 0, 5)
                pygame.draw.circle(icon, (100, 100, 100), (16, 16), 4)
            elif name == "coin":
                pygame.draw.circle(icon, color, (16, 16), 10)
                pygame.draw.circle(icon, (200, 150, 0), (16, 16), 8)
            
            pygame.image.save(icon, f"assets/ui/icons/{name}.png")
            self.assets_created += 1
            print(f"🎯 Généré: assets/ui/icons/{name}.png")
    
    def generate_tilesets(self):
        """Génère les tilesets de base"""
        tileset = pygame.Surface((96, 96), pygame.SRCALPHA)  # 3x3 tiles
        
        # Tile 1: Herbe
        pygame.draw.rect(tileset, (100, 200, 100), (0, 0, 32, 32))
        pygame.draw.rect(tileset, (120, 220, 120), (2, 2, 28, 28))
        
        # Tile 2: Chemin
        pygame.draw.rect(tileset, (150, 120, 80), (32, 0, 32, 32))
        pygame.draw.rect(tileset, (170, 140, 100), (34, 2, 28, 28))
        
        # Tile 3: Mur
        pygame.draw.rect(tileset, (120, 100, 80), (64, 0, 32, 32))
        pygame.draw.rect(tileset, (140, 120, 100), (66, 2, 28, 28))
        
        # Tile 4: Eau
        pygame.draw.rect(tileset, (50, 100, 200), (0, 32, 32, 32))
        
        # Tile 5: Sable
        pygame.draw.rect(tileset, (200, 180, 100), (32, 32, 32, 32))
        
        pygame.image.save(tileset, "assets/tilesets/terrain.png")
        self.assets_created += 1
        print(f"🧱 Généré: assets/tilesets/terrain.png")

def main():
    """Fonction principale"""
    pygame.init()
    generator = AssetGenerator()
    generator.generate_all_assets()
    pygame.quit()

if __name__ == "__main__":
    main()
