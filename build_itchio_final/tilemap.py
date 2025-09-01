# tilemap.py - Système de gestion des tilemaps
import pygame
import json
import os

class TileMap:
    def __init__(self, filename=None):
        self.tile_size = 32
        self.layers = {}
        self.tilesets = []
        
        if filename:
            self.load_map(filename)
        else:
            self.create_fallback_map()
    
    def load_map(self, filename):
        """Charge une tilemap depuis un fichier JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                map_data = json.load(f)
            
            self.width = map_data['width']
            self.height = map_data['height']
            self.tile_width = map_data['tilewidth']
            self.tile_height = map_data['tileheight']
            
            # Charger les calques
            for layer in map_data['layers']:
                if layer['type'] == 'tilelayer':
                    self.layers[layer['name']] = layer['data']
            
            # Charger les tilesets
            for tileset_data in map_data['tilesets']:
                tileset = {
                    'firstgid': tileset_data['firstgid'],
                    'image': tileset_data['image'],
                    'tile_count': tileset_data['tilecount'],
                    'columns': tileset_data['columns'],
                    'tile_width': tileset_data['tilewidth'],
                    'tile_height': tileset_data['tileheight']
                }
                
                # Charger l'image du tileset
                try:
                    image_path = f"assets/tilesets/{tileset_data['image']}"
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
        """Crée une map de fallback"""
        self.width = 25
        self.height = 19
        self.tile_width = 32
        self.tile_height = 32
        
        # Calque d'arrière-plan (herbe partout)
        background = [1] * (self.width * self.height)
        
        # Calque de collision (bordures seulement)
        collision = [0] * (self.width * self.height)
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    collision[y * self.width + x] = 1
        
        self.layers = {
            'background': background,
            'collision': collision
        }
        
        # Tileset de fallback
        self.tilesets = [{
            'firstgid': 1,
            'image_surface': self.create_fallback_tileset(),
            'tile_count': 3,
            'columns': 3,
            'tile_width': 32,
            'tile_height': 32
        }]
    
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
    
    def get_tile_at(self, x, y, layer_name='collision'):
        """Retourne le tile à une position donnée"""
        if layer_name not in self.layers:
            return 0
            
        tile_x = x // self.tile_width
        tile_y = y // self.tile_height
        
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            index = tile_y * self.width + tile_x
            return self.layers[layer_name][index]
        
        return 1  # Collision hors map
    
    def check_collision(self, x, y, layer_name='collision'):
        """Vérifie s'il y a une collision"""
        tile_id = self.get_tile_at(x, y, layer_name)
        return tile_id > 0