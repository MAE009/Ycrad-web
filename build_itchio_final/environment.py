# environment.py - Version avec tilemaps
import pygame
from tilemap import TileMap

class Environment:
    def __init__(self):
        self.tilemaps = {}
        self.current_zone = "village"
        self.camera_offset = [0, 0]
        
        # Charger les tilemaps
        self.load_tilemaps()
        
        # Monstres et PNJs
        self.monster_instances = []
        self.npcs = []
    
    def load_tilemaps(self):
        """Charge les tilemaps pour chaque zone"""
        zones = ["village", "forest", "marsh", "dungeon"]
        
        for zone in zones:
            try:
                self.tilemaps[zone] = TileMap(f"assets/maps/{zone}.json")
                print(f"✅ Tilemap chargée: {zone}")
            except:
                print(f"⚠️  Tilemap manquante: {zone}")
                # Créer une tilemap de fallback
                self.tilemaps[zone] = TileMap(None)  # Cela créera une fallback
    
    def update_camera(self, player_position, screen_width, screen_height):
        """Met à jour la position de la caméra"""
        map_width = self.tilemaps[self.current_zone].width * 32
        map_height = self.tilemaps[self.current_zone].height * 32
        
        # Centrer la caméra sur le joueur, mais ne pas dépasser les bords
        self.camera_offset[0] = max(0, min(
            player_position[0] - screen_width // 2,
            map_width - screen_width
        ))
        
        self.camera_offset[1] = max(0, min(
            player_position[1] - screen_height // 2,
            map_height - screen_height
        ))
    
    def render(self, screen, player_position):
        """Dessine l'environnement"""
        # Mettre à jour la caméra
        self.update_camera(player_position, screen.get_width(), screen.get_height())
        
        # Dessiner les calques de la tilemap
        current_map = self.tilemaps[self.current_zone]
        
        # Calque d'arrière-plan
        current_map.render_layer(screen, "background", 
                               self.camera_offset[0], self.camera_offset[1])
        
        # Calque de décoration
        if "decorations" in current_map.layers:
            current_map.render_layer(screen, "decorations",
                                   self.camera_offset[0], self.camera_offset[1])
    
    def check_collision(self, position, size=(20, 20)):
        """Vérifie les collisions avec l'environnement"""
        current_map = self.tilemaps[self.current_zone]
        
        # Vérifier les 4 coins du rectangle de collision
        points = [
            (position[0], position[1]),  # Haut gauche
            (position[0] + size[0], position[1]),  # Haut droite
            (position[0], position[1] + size[1]),  # Bas gauche
            (position[0] + size[0], position[1] + size[1])  # Bas droite
        ]
        
        for point in points:
            if current_map.check_collision(point[0], point[1], "collision"):
                return True
        
        return False
    
    def get_zone_at_position(self, position):
        """Détermine la zone basée sur la position"""
        # Vérifier les zones de transition dans la tilemap
        current_map = self.tilemaps[self.current_zone]
        tile_x = position[0] // 32
        tile_y = position[1] // 32
        
        if 0 <= tile_x < current_map.width and 0 <= tile_y < current_map.height:
            index = tile_y * current_map.width + tile_x
            if "transitions" in current_map.layers:
                transition_id = current_map.layers["transitions"][index]
                if transition_id > 0:
                    # Mapping des IDs de transition vers les noms de zones
                    transition_map = {
                        1: "forest",
                        2: "marsh",
                        3: "dungeon",
                        4: "village"
                    }
                    return transition_map.get(transition_id, self.current_zone)
        
        return self.current_zone