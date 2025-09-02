# tilemap.py - Version corrigée
import pygame
import json
import os
import random

class TileMap:
    def __init__(self, filename=None, map_type="village"):
        self.tile_size = 32
        self.layers = {}
        self.tilesets = []
        self.map_type = map_type
        
        if filename and os.path.exists(filename):
            self.load_map(filename)
        else:
            self.create_fallback_map()
    
    def load_map(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                map_data = json.load(f)
            
            self.width = map_data.get('width', 25)
            self.height = map_data.get('height', 19)
            self.tile_width = map_data.get('tilewidth', 32)
            self.tile_height = map_data.get('tileheight', 32)
            
            # Charger les calques
            for layer in map_data.get('layers', []):
                if layer.get('type') == 'tilelayer':
                    self.layers[layer['name']] = layer.get('data', [])
            
            # Charger les tilesets
            for tileset_data in map_data.get('tilesets', []):
                tileset = {
                    'firstgid': tileset_data.get('firstgid', 1),
                    'image': tileset_data.get('image', 'terrain.png'),
                    'tile_count': tileset_data.get('tilecount', 9),
                    'columns': tileset_data.get('columns', 3),
                    'tile_width': tileset_data.get('tilewidth', 32),
                    'tile_height': tileset_data.get('tileheight', 32)
                }
                
                # Charger l'image du tileset
                try:
                    image_path = f"assets/tilesets/{tileset['image']}"
                    if os.path.exists(image_path):
                        tileset['image_surface'] = pygame.image.load(image_path).convert_alpha()
                    else:
                        tileset['image_surface'] = self.create_fallback_tileset()
                except:
                    tileset['image_surface'] = self.create_fallback_tileset()
                
                self.tilesets.append(tileset)
                
        except Exception as e:
            print(f"❌ Erreur chargement tilemap: {e}")
            self.create_fallback_map()
    
    def create_fallback_map(self):
        """Crée une map de fallback selon le type"""
        self.width = 25
        self.height = 19
        self.tile_width = 32
        self.tile_height = 32
        
        # Calque d'arrière-plan
        background = []
        collision = []
        
        if self.map_type == "village":
            background, collision = self.create_village_map()
        elif self.map_type == "forest":
            background, collision = self.create_forest_map()
        elif self.map_type == "marsh":
            background, collision = self.create_marsh_map()
        else:
            background, collision = self.create_generic_map()
        
        self.layers = {
            'background': background,
            'collision': collision
        }
        
        # Tileset de fallback
        self.tilesets = [{
            'firstgid': 1,
            'image_surface': self.create_fallback_tileset(),
            'tile_count': 9,
            'columns': 3,
            'tile_width': 32,
            'tile_height': 32
        }]
    
    def create_village_map(self):
        """Crée une map de village"""
        background = [1] * (self.width * self.height)
        collision = [0] * (self.width * self.height)
        
        # Bordures
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    collision[y * self.width + x] = 3
                
                # Maisons
                if (8 <= x <= 10 and 5 <= y <= 7) or (15 <= x <= 17 and 5 <= y <= 7):
                    collision[y * self.width + x] = 3
                    background[y * self.width + x] = 3
        
        return background, collision
    
    def create_forest_map(self):
        """Crée une map de forêt"""
        background = [6] * (self.width * self.height)  # Herbe forestière
        collision = [0] * (self.width * self.height)
        
        # Bordures et arbres
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    collision[y * self.width + x] = 3
                
                # Arbres aléatoires
                if random.random() < 0.1 and 3 < x < self.width - 3 and 3 < y < self.height - 3:
                    collision[y * self.width + x] = 3
                    background[y * self.width + x] = 3
        
        return background, collision
    
    def create_marsh_map(self):
        """Crée une map de marais"""
        background = [1] * (self.width * self.height)
        collision = [0] * (self.width * self.height)
        
        # Eau et obstacles
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    collision[y * self.width + x] = 3
                
                # Zones d'eau
                if (x + y) % 4 == 0 and 2 < x < self.width - 2 and 2 < y < self.height - 2:
                    background[y * self.width + x] = 4
                    collision[y * self.width + x] = 3
        
        return background, collision
    
    def create_generic_map(self):
        """Crée une map générique"""
        background = [1] * (self.width * self.height)
        collision = [0] * (self.width * self.height)
        
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    collision[y * self.width + x] = 3
        
        return background, collision
    
    def create_fallback_tileset(self):
        """Crée un tileset de fallback"""
        tileset = pygame.Surface((96, 96), pygame.SRCALPHA)  # 3x3 tiles
        
        # Tile 1: Herbe
        pygame.draw.rect(tileset, (100, 200, 100), (0, 0, 32, 32))
        pygame.draw.rect(tileset, (120, 220, 120), (2, 2, 28, 28))
        
        # Tile 2: Chemin
        pygame.draw.rect(tileset, (150, 120, 80), (32, 0, 32, 32))
        pygame.draw.rect(tileset, (170, 140, 100), (34, 2, 28, 28))
        
        # Tile 3: Mur/Rocher
        pygame.draw.rect(tileset, (120, 100, 80), (64, 0, 32, 32))
        pygame.draw.rect(tileset, (140, 120, 100), (66, 2, 28, 28))
        
        # Tile 4: Eau
        pygame.draw.rect(tileset, (50, 100, 200), (0, 32, 32, 32))
        
        # Tile 5: Sable
        pygame.draw.rect(tileset, (200, 180, 100), (32, 32, 32, 32))
        
        # Tile 6: Herbe forestière
        pygame.draw.rect(tileset, (80, 160, 80), (64, 32, 32, 32))
        
        return tileset
    
    def get_tile_image(self, gid):
        """Retourne l'image d'un tile spécifique"""
        if gid == 0:  # Tile vide
            return None
            
        for tileset in self.tilesets:
            if gid >= tileset['firstgid'] and gid < tileset['firstgid'] + tileset['tile_count']:
                local_id = gid - tileset['firstgid']
                x = (local_id % tileset['columns']) * tileset['tile_width']
                y = (local_id // tileset['columns']) * tileset['tile_height']
                
                tile_rect = pygame.Rect(x, y, tileset['tile_width'], tileset['tile_height'])
                tile_surface = pygame.Surface((tileset['tile_width'], tileset['tile_height']), pygame.SRCALPHA)
                tile_surface.blit(tileset['image_surface'], (0, 0), tile_rect)
                
                return tile_surface
        
        return None
    
    def render_layer(self, screen, layer_name, offset_x=0, offset_y=0):
        """Dessine un calque de la map"""
        if layer_name not in self.layers:
            return False
            
        layer_data = self.layers[layer_name]
        
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x
                gid = layer_data[index]
                
                if gid > 0:
                    tile_image = self.get_tile_image(gid)
                    if tile_image:
                        screen.blit(
                            tile_image,
                            (x * self.tile_width - offset_x, y * self.tile_height - offset_y)
                        )
        return True
        
    # Dans tilemap.py - Correction de check_collision
    def check_collision(self, x, y, layer_name='collision'):
        """Vérifie s'il y a une collision - VERSION CORRIGÉE"""
        # CONVERTIR EN ENTIERS
        tile_x = int(x) // self.tile_width
        tile_y = int(y) // self.tile_height
        
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            index = tile_y * self.width + tile_x
            return self.layers.get(layer_name, [])[index] > 0
        
        return True  # Collision hors de la map