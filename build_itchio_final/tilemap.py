# tilemap.py - Système de gestion des tilemaps
import pygame
import json

class TileMap:
    def __init__(self, filename):
        self.tile_size = 32  # Taille des tiles en pixels
        self.load_map(filename)
    
    def load_map(self, filename):
        """Charge une tilemap depuis un fichier JSON"""
        try:
            with open(filename, 'r') as f:
                map_data = json.load(f)
            
            # Extraire les données de la map
            self.width = map_data['width']
            self.height = map_data['height']
            self.tile_width = map_data['tilewidth']
            self.tile_height = map_data['tileheight']
            
            # Charger les calques
            self.layers = {}
            for layer in map_data['layers']:
                if layer['type'] == 'tilelayer':
                    self.layers[layer['name']] = layer['data']
            
            # Charger les tilesets
            self.tilesets = []
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
                tileset['image_surface'] = pygame.image.load(
                    f"assets/tilesets/{tileset_data['image']}"
                ).convert_alpha()
                self.tilesets.append(tileset)
                
        except Exception as e:
            print(f"Erreur chargement tilemap: {e}")
            self.create_fallback_map()
    
    def create_fallback_map(self):
        """Crée une map de fallback si le chargement échoue"""
        self.width = 25  # 25 tiles de large (800px / 32)
        self.height = 19  # 19 tiles de haut (600px / 32)
        self.tile_width = 32
        self.tile_height = 32
        
        # Créer un calque simple
        self.layers = {
            'background': [1] * (self.width * self.height)
        }
        
        # Créer un tileset de fallback
        self.tilesets = [{
            'firstgid': 1,
            'image_surface': self.create_fallback_tileset(),
            'tile_count': 1,
            'columns': 1,
            'tile_width': 32,
            'tile_height': 32
        }]
    
    def create_fallback_tileset(self):
        """Crée un tileset de fallback"""
        tileset = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(tileset, (100, 100, 100), (0, 0, 32, 32))
        pygame.draw.rect(tileset, (150, 150, 150), (2, 2, 28, 28))
        return tileset
    
    def get_tile_image(self, gid):
        """Retourne l'image d'un tile spécifique"""
        for tileset in self.tilesets:
            if gid >= tileset['firstgid'] and gid < tileset['firstgid'] + tileset['tile_count']:
                # Calculer la position dans le tileset
                local_id = gid - tileset['firstgid']
                x = (local_id % tileset['columns']) * tileset['tile_width']
                y = (local_id // tileset['columns']) * tileset['tile_height']
                
                # Extraire le tile
                tile_rect = pygame.Rect(x, y, tileset['tile_width'], tileset['tile_height'])
                tile_surface = pygame.Surface((tileset['tile_width'], tileset['tile_height']), pygame.SRCALPHA)
                tile_surface.blit(tileset['image_surface'], (0, 0), tile_rect)
                
                return tile_surface
        
        return None
    
    def render_layer(self, screen, layer_name, offset_x=0, offset_y=0):
        """Dessine un calque de la map"""
        if layer_name not in self.layers:
            return
        
        layer_data = self.layers[layer_name]
        
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x
                gid = layer_data[index]
                
                if gid > 0:  # 0 = tile vide
                    tile_image = self.get_tile_image(gid)
                    if tile_image:
                        screen.blit(
                            tile_image,
                            (x * self.tile_width - offset_x, y * self.tile_height - offset_y)
                        )
    
    def get_tile_at(self, x, y, layer_name='collision'):
        """Retourne le tile à une position donnée"""
        if layer_name not in self.layers:
            return 0
        
        tile_x = x // self.tile_width
        tile_y = y // self.tile_height
        
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            index = tile_y * self.width + tile_x
            return self.layers[layer_name][index]
        
        return 0
    
    def check_collision(self, x, y, layer_name='collision'):
        """Vérifie s'il y a une collision à une position"""
        tile_id = self.get_tile_at(x, y, layer_name)
        return tile_id > 0  # Suppose que tous les tiles > 0 sont des collisions