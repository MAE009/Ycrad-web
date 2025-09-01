# environment.py - Gestion de l'environnement avec tilemaps
import pygame
import os
from tilemap import TileMap

class Environment:
    def __init__(self):
        self.tilemaps = {}
        self.current_zone = "village"
        self.camera_offset = [0, 0]
        self.monster_instances = []
        self.npcs = []
        
        self.load_tilemaps()
    
    def load_tilemaps(self):
        """Charge les tilemaps pour chaque zone"""
        #zones = ["village", "forest", "marsh", "dungeon"]
        zones = ["village"]
        
        for zone in zones:
            map_path = f"assets/maps/{zone}.json"
            if os.path.exists(map_path):
                self.tilemaps[zone] = TileMap(map_path)
                print(f"✅ Tilemap chargée: {zone}")
            else:
                print(f"⚠️  Tilemap manquante, création fallback: {zone}")
                self.tilemaps[zone] = TileMap()  # Fallback
    
    def update_camera(self, player_position, screen_width, screen_height):
        """Met à jour la position de la caméra"""
        current_map = self.tilemaps[self.current_zone]
        map_width = current_map.width * current_map.tile_width
        map_height = current_map.height * current_map.tile_height
        
        # Centrer sur le joueur
        target_x = player_position[0] - screen_width // 2
        target_y = player_position[1] - screen_height // 2
        
        # Limiter aux bords de la map
        self.camera_offset[0] = max(0, min(target_x, map_width - screen_width))
        self.camera_offset[1] = max(0, min(target_y, map_height - screen_height))
    
    def render(self, screen, player_position):
        """Dessine l'environnement"""
        self.update_camera(player_position, screen.get_width(), screen.get_height())
        current_map = self.tilemaps[self.current_zone]
        
        # Dessiner les calques
        current_map.render_layer(screen, "background", 
                               self.camera_offset[0], self.camera_offset[1])
        
        # Dessiner les calques supplémentaires
        for layer_name in ["ground", "decorations", "details"]:
            current_map.render_layer(screen, layer_name,
                                   self.camera_offset[0], self.camera_offset[1])
    
    def check_collision(self, position, size=(20, 20)):
        """Vérifie les collisions avec l'environnement"""
        current_map = self.tilemaps[self.current_zone]
        
        # Vérifier les 4 coins du rectangle de collision
        points = [
            (position[0], position[1]),
            (position[0] + size[0], position[1]),
            (position[0], position[1] + size[1]),
            (position[0] + size[0], position[1] + size[1])
        ]
        
        for point in points:
            if current_map.check_collision(point[0], point[1]):
                return True
        
        return False
    
    def get_zone_at_position(self, position):
        """Détermine la zone basée sur la position"""
        current_map = self.tilemaps[self.current_zone]
        
        # Vérifier les zones de transition
        if "transitions" in current_map.layers:
            tile_x = position[0] // current_map.tile_width
            tile_y = position[1] // current_map.tile_height
            
            if 0 <= tile_x < current_map.width and 0 <= tile_y < current_map.height:
                index = tile_y * current_map.width + tile_x
                transition_id = current_map.layers["transitions"][index]
                
                if transition_id > 0:
                    transition_zones = {
                        1: "forest",
                        2: "marsh", 
                        3: "dungeon",
                        4: "village"
                    }
                    return transition_zones.get(transition_id, self.current_zone)
        
        return self.current_zone
    
    def change_zone(self, new_zone, player_position):
        """Change de zone"""
        if new_zone in self.tilemaps and new_zone != self.current_zone:
            print(f"🚪 Transition: {self.current_zone} → {new_zone}")
            
            # Déterminer le point d'apparition
            spawn_point = self.get_spawn_point(self.current_zone, new_zone, player_position)
            self.current_zone = new_zone
            
            return spawn_point
        
        return player_position
    
    def get_spawn_point(self, from_zone, to_zone, old_position):
        """Détermine le point d'apparition"""
        spawn_points = {
            "village_forest": (400, 50),
            "village_marsh": (750, 300),
            "forest_village": (400, 550),
            "marsh_village": (50, 300),
            "forest_dungeon": (700, 150),
            "dungeon_forest": (100, 500)
        }
        
        key = f"{from_zone}_{to_zone}"
        return spawn_points.get(key, (400, 300))
