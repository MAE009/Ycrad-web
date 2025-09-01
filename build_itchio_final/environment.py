# environment.py - Gestion des environnements et collisions
import pygame
import random
import json

class Environment:
    def __init__(self):
        self.zones = {
            "village": {
                "monsters": [],
                "npcs": ["marchand", "forgeron"],
                "background": "village",
                "music": "village_theme",
                "collisions": self.generate_village_collisions()
            },
            "forest": {
                "monsters": [("slime", 1), ("rat", 1)],
                "npcs": ["chasseur"],
                "background": "forest",
                "music": "forest_theme",
                "collisions": self.generate_forest_collisions()
            },
            "marsh": {
                "monsters": [("slime", 2), ("rat", 2)],
                "npcs": ["ermite"],
                "background": "marsh",
                "music": "marsh_theme",
                "collisions": self.generate_marsh_collisions()
            }
        }
        
        self.current_zone = "village"
        self.monster_instances = []
        self.generate_monsters()
        
    def generate_village_collisions(self):
        """Génère les collisions pour le village"""
        collisions = []
        # Maisons
        collisions.extend([(100 + i*120, 200, 60, 80) for i in range(5)])
        # Étage
        collisions.append((300, 100, 200, 50))
        # Arbres
        collisions.extend([(50, 400, 40, 60), (700, 400, 40, 60)])
        return collisions
    
    def generate_forest_collisions(self):
        """Génère les collisions pour la forêt"""
        collisions = []
        # Arbres
        for i in range(8):
            x = random.randint(50, 700)
            y = random.randint(100, 500)
            collisions.append((x, y, 40, 60))
        # Rochers
        for i in range(5):
            x = random.randint(100, 650)
            y = random.randint(150, 550)
            collisions.append((x, y, 30, 30))
        return collisions
    
    def generate_marsh_collisions(self):
        """Génère les collisions pour le marais"""
        collisions = []
        # Zones d'eau
        collisions.extend([(200, 300, 100, 80), (500, 200, 120, 60)])
        # Arbres morts
        collisions.extend([(150, 150, 35, 50), (650, 350, 35, 50)])
        # Rochers
        for i in range(7):
            x = random.randint(80, 720)
            y = random.randint(100, 520)
            collisions.append((x, y, 25, 25))
        return collisions
    
    def generate_monsters(self):
        """Génère les instances de monstres pour la zone actuelle"""
        from monsters import Slime, Rat  # Import circulaire évité
        
        monster_classes = {
            "slime": Slime,
            "rat": Rat
        }
        
        self.monster_instances = []
        zone_data = self.zones[self.current_zone]
        
        for monster_type, level in zone_data["monsters"]:
            # Position aléatoire évitant les collisions
            for _ in range(10):  # 10 tentatives
                x = random.randint(100, 700)
                y = random.randint(100, 500)
                
                if not self.check_collision((x, y)):
                    monster = monster_classes[monster_type](level, [x, y])
                    self.monster_instances.append(monster)
                    break
    
    def check_collision(self, position, size=(20, 20)):
        """Vérifie les collisions à une position donnée"""
        pos_x, pos_y = position
        width, height = size
        
        for collision in self.zones[self.current_zone]["collisions"]:
            col_x, col_y, col_w, col_h = collision
            
            if (pos_x < col_x + col_w and
                pos_x + width > col_x and
                pos_y < col_y + col_h and
                pos_y + height > col_y):
                return True
        
        return False
    
    def get_monsters_in_current_zone(self):
        """Retourne les monstres de la zone actuelle"""
        return self.monster_instances
    
    def get_zone_at_position(self, position):
        """Détermine la zone basée sur la position"""
        x, y = position
        
        # Zones simples pour la démo
        if y < 200:
            return "forest"
        elif x > 600:
            return "marsh"
        else:
            return "village"
    
    def load_zone_monsters(self, zone_name):
        """Charge les monstres d'une zone spécifique"""
        if zone_name in self.zones:
            self.current_zone = zone_name
            self.generate_monsters()
    
    def get_zone_background(self):
        """Retourne le nom du background de la zone actuelle"""
        return self.zones[self.current_zone]["background"]
    
    def get_zone_music(self):
        """Retourne la musique de la zone actuelle"""
        return self.zones[self.current_zone]["music"]
    
    def save_state(self):
        """Sauvegarde l'état de l'environnement"""
        return {
            "current_zone": self.current_zone,
            "monsters": [
                {
                    "type": monster.type,
                    "level": monster.level,
                    "position": monster.position,
                    "hp": monster.hp
                }
                for monster in self.monster_instances
            ]
        }
    
    def load_state(self, data):
        """Charge l'état de l'environnement"""
        from monsters import Slime, Rat
        
        monster_classes = {
            "slime": Slime,
            "rat": Rat
        }
        
        self.current_zone = data.get("current_zone", "village")
        self.monster_instances = []
        
        for monster_data in data.get("monsters", []):
            monster_type = monster_data["type"]
            if monster_type in monster_classes:
                monster = monster_classes[monster_type](
                    monster_data["level"],
                    monster_data["position"]
                )
                monster.hp = monster_data["hp"]
                self.monster_instances.append(monster)
