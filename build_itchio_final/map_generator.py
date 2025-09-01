# map_generator.py - Générateur de maps de fallback
import pygame
import json
import os

class MapGenerator:
    def __init__(self):
        self.tile_size = 32
        
    def generate_all_maps(self):
        """Génère toutes les maps de fallback"""
        os.makedirs("assets/maps", exist_ok=True)
        os.makedirs("assets/tilesets", exist_ok=True)
        
        zones = ["village", "forest", "marsh", "dungeon"]
        
        for zone in zones:
            if zone == "village":
                self.generate_village_map()
            elif zone == "forest":
                self.generate_forest_map()
            elif zone == "marsh":
                self.generate_marsh_map()
            elif zone == "dungeon":
                self.generate_dungeon_map()
        
        print("✅ Toutes les maps générées!")
    
    def generate_village_map(self):
        """Génère une map de village"""
        map_data = {
            "width": 25,
            "height": 19,
            "tilewidth": 32,
            "tileheight": 32,
            "layers": [
                {
                    "name": "background",
                    "type": "tilelayer",
                    "data": self.generate_village_background()
                },
                {
                    "name": "collision", 
                    "type": "tilelayer",
                    "data": self.generate_village_collision()
                },
                {
                    "name": "decorations",
                    "type": "tilelayer", 
                    "data": self.generate_village_decorations()
                }
            ],
            "tilesets": [
                {
                    "firstgid": 1,
                    "image": "terrain.png",
                    "tilecount": 9,
                    "columns": 3,
                    "tilewidth": 32,
                    "tileheight": 32
                }
            ]
        }
        
        with open("assets/maps/village.json", "w") as f:
            json.dump(map_data, f, indent=2)
    
    def generate_village_background(self):
        """Génère le calque d'arrière-plan du village"""
        layer = []
        for y in range(19):
            for x in range(25):
                # Herbe partout
                tile_id = 1
                
                # Chemins
                if (x == 12 and 5 <= y <= 15) or (y == 10 and 8 <= x <= 16):
                    tile_id = 2
                
                # Places devant les maisons
                if (7 <= x <= 11 and 4 <= y <= 4) or (14 <= x <= 18 and 4 <= y <= 4):
                    tile_id = 2
                
                layer.append(tile_id)
        return layer
    
    def generate_village_collision(self):
        """Génère le calque de collision du village"""
        layer = [0] * (25 * 19)
        
        # Bordures
        for y in range(19):
            for x in range(25):
                if x == 0 or x == 24 or y == 0 or y == 18:
                    layer[y * 25 + x] = 3
                
                # Maisons
                if (8 <= x <= 10 and 5 <= y <= 7) or (15 <= x <= 17 and 5 <= y <= 7):
                    layer[y * 25 + x] = 3
                
                # Arbres
                if (x == 5 and y == 5) or (x == 20 and y == 5) or (x == 5 and y == 15) or (x == 20 and y == 15):
                    layer[y * 25 + x] = 3
        
        return layer
    
    def generate_village_decorations(self):
        """Génère le calque de décorations du village"""
        layer = [0] * (25 * 19)
        
        # Fleurs et décorations
        decorations = [
            (6, 6, 4), (7, 6, 4), (18, 6, 4), (19, 6, 4),
            (6, 16, 4), (7, 16, 4), (18, 16, 4), (19, 16, 4),
            (12, 4, 5), (12, 16, 5)
        ]
        
        for x, y, tile_id in decorations:
            if 0 <= x < 25 and 0 <= y < 19:
                layer[y * 25 + x] = tile_id
        
        return layer
    
    def generate_forest_map(self):
        """Génère une map de forêt"""
        map_data = {
            "width": 25,
            "height": 19,
            "tilewidth": 32,
            "tileheight": 32,
            "layers": [
                {
                    "name": "background",
                    "type": "tilelayer",
                    "data": [6] * (25 * 19)  # Herbe forestière
                },
                {
                    "name": "collision",
                    "type": "tilelayer",
                    "data": self.generate_forest_collision()
                }
            ],
            "tilesets": [
                {
                    "firstgid": 1,
                    "image": "terrain.png",
                    "tilecount": 9,
                    "columns": 3,
                    "tilewidth": 32,
                    "tileheight": 32
                }
            ]
        }
        
        with open("assets/maps/forest.json", "w") as f:
            json.dump(map_data, f, indent=2)
    
    def generate_forest_collision(self):
        """Génère le calque de collision de la forêt"""
        layer = [0] * (25 * 19)
        
        # Bordures
        for y in range(19):
            for x in range(25):
                if x == 0 or x == 24 or y == 0 or y == 18:
                    layer[y * 25 + x] = 3
                
                # Arbres aléatoires
                if (x % 4 == 0 and y % 3 == 0) and (x > 3 and x < 21 and y > 3 and y < 15):
                    layer[y * 25 + x] = 3
        
        return layer
    
    def generate_marsh_map(self):
        """Génère une map de marais"""
        # Similaire aux autres, avec des tiles de marais
        pass
    
    def generate_dungeon_map(self):
        """Génère une map de donjon"""
        # Similaire aux autres, avec des tiles de donjon
        pass
    
    def create_terrain_tileset(self):
        """Crée le tileset de terrain"""
        tileset = pygame.Surface((96, 96), pygame.SRCALPHA)  # 3x3 tiles
        
        # Tile 1: Herbe normale
        pygame.draw.rect(tileset, (100, 200, 100), (0, 0, 32, 32))
        pygame.draw.rect(tileset, (120, 220, 120), (2, 2, 28, 28))
        
        # Tile 2: Chemin terre
        pygame.draw.rect(tileset, (150, 120, 80), (32, 0, 32, 32))
        pygame.draw.rect(tileset, (170, 140, 100), (34, 2, 28, 28))
        
        # Tile 3: Mur/Rocher
        pygame.draw.rect(tileset, (120, 100, 80), (64, 0, 32, 32))
        pygame.draw.rect(tileset, (140, 120, 100), (66, 2, 28, 28))
        
        # Tile 4: Fleurs
        pygame.draw.rect(tileset, (100, 200, 100), (0, 32, 32, 32))
        pygame.draw.circle(tileset, (255, 100, 100), (16, 20), 4)
        pygame.draw.circle(tileset, (255, 200, 100), (10, 25), 3)
        
        # Tile 5: Pierre centrale
        pygame.draw.rect(tileset, (100, 200, 100), (32, 32, 32, 32))
        pygame.draw.circle(tileset, (150, 150, 150), (16, 16), 8)
        
        # Tile 6: Herbe forestière
        pygame.draw.rect(tileset, (80, 160, 80), (64, 32, 32, 32))
        pygame.draw.rect(tileset, (90, 180, 90), (66, 34, 28, 28))
        
        pygame.image.save(tileset, "assets/tilesets/terrain.png")

if __name__ == "__main__":
    pygame.init()
    generator = MapGenerator()
    generator.create_terrain_tileset()
    generator.generate_all_maps()
    pygame.quit()