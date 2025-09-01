# monsters.py - Classes de monstres et système de combat
import pygame
import random

class Monster:
    def __init__(self, monster_type, level, position):
        self.type = monster_type
        self.name = monster_type.capitalize()
        self.level = level
        self.position = list(position)
        self.hp = self.max_hp = 20 + (level * 8)
        self.damage = 5 + level
        self.defense = 2 + level
        self.xp_reward = 10 + (level * 5)
        self.gold_reward = 3 + level
        self.speed = 1.0
        self.attack_cooldown = 0
        self.loot_table = self.get_loot_table()
    
    def get_loot_table(self):
        """Retourne la table de butin selon le type de monstre"""
        if self.type == "slime":
            return [
                ("Gelée visqueuse", 0.7, 1, 3),
                ("Petite potion", 0.3, 1, 1),
                ("Pièce d'or", 0.8, 1, 5)
            ]
        elif self.type == "rat":
            return [
                ("Queue de rat", 0.5, 1, 2),
                ("Fromage", 0.2, 1, 1),
                ("Pièce d'or", 0.6, 1, 3)
            ]
        return []
    
    def take_damage(self, damage):
        """Reçoit des dégâts avec réduction par la défense"""
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
    
    def attack(self, target):
        """Attaque une cible"""
        if self.attack_cooldown <= 0:
            damage = self.damage
            actual_damage = target.take_damage(damage)
            self.attack_cooldown = 30  # Cooldown d'attaque
            return actual_damage
        return 0
    
    def update(self, dt, player_position):
        """Met à jour le monstre"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt * 60
        
        # Mouvement simple vers le joueur
        if self.should_chase_player(player_position):
            self.move_towards_player(player_position, dt)
    
    def should_chase_player(self, player_position):
        """Détermine si le monstre doit poursuivre le joueur"""
        distance = ((self.position[0] - player_position[0])**2 + 
                   (self.position[1] - player_position[1])**2)**0.5
        return distance < 200  # Distance de détection
    
    def move_towards_player(self, player_position, dt):
        """Se déplace vers le joueur"""
        dx = player_position[0] - self.position[0]
        dy = player_position[1] - self.position[1]
        
        # Normaliser la direction
        distance = max(1, (dx**2 + dy**2)**0.5)
        dx /= distance
        dy /= distance
        
        # Appliquer le mouvement
        self.position[0] += dx * self.speed * dt * 60
        self.position[1] += dy * self.speed * dt * 60
    
    def generate_loot(self):
        """Génère le butin du monstre"""
        loot = []
        for item_name, chance, min_qty, max_qty in self.loot_table:
            if random.random() < chance:
                quantity = random.randint(min_qty, max_qty)
                loot.append({"name": item_name, "quantity": quantity})
        return loot
    
    def is_alive(self):
        """Vérifie si le monstre est en vie"""
        return self.hp > 0
    
    def draw(self, screen, camera_offset=(0, 0)):
        """Dessine le monstre"""
        # Cette méthode serait normalement gérée par le renderer
        pass

class Slime(Monster):
    def __init__(self, level, position):
        super().__init__("slime", level, position)
        self.hp = self.max_hp = 15 + (level * 6)
        self.damage = 4 + level
        self.defense = 1 + level
        self.speed = 0.8
        self.xp_reward = 8 + (level * 4)
    
    def attack(self, target):
        """Attaque avec chance d'empoisonnement"""
        damage = super().attack(target)
        if damage > 0 and random.random() < 0.2:  # 20% chance
            # Appliquer un effet de poison
            if hasattr(target, 'add_status_effect'):
                target.add_status_effect("poison", 3, 2)  # 3 tours, 2 dégâts par tour
        return damage

class Rat(Monster):
    def __init__(self, level, position):
        super().__init__("rat", level, position)
        self.hp = self.max_hp = 12 + (level * 5)
        self.damage = 3 + level
        self.defense = 0 + level
        self.speed = 1.2
        self.xp_reward = 6 + (level * 3)
        self.critical_chance = 0.1
    
    def attack(self, target):
        """Attaque avec chance de coup critique"""
        damage = super().attack(target)
        if damage > 0 and random.random() < self.critical_chance:
            damage *= 2  # Coup critique
        return damage

class Boss(Monster):
    def __init__(self, boss_type, level, position):
        super().__init__(boss_type, level, position)
        self.hp = self.max_hp = 100 + (level * 30)
        self.damage = 15 + (level * 2)
        self.defense = 10 + level
        self.xp_reward = 50 + (level * 20)
        self.gold_reward = 25 + (level * 10)
        self.special_attacks = []
    
    def add_special_attack(self, attack_name, cooldown, damage_multiplier):
        """Ajoute une attaque spéciale"""
        self.special_attacks.append({
            "name": attack_name,
            "cooldown": cooldown,
            "current_cooldown": 0,
            "damage_multiplier": damage_multiplier
        })
    
    def update(self, dt, player_position):
        """Met à jour le boss avec ses attaques spéciales"""
        super().update(dt, player_position)
        
        # Mettre à jour les cooldowns des attaques spéciales
        for attack in self.special_attacks:
            if attack["current_cooldown"] > 0:
                attack["current_cooldown"] -= dt * 60

# Factory pour créer des monstres
class MonsterFactory:
    @staticmethod
    def create_monster(monster_type, level, position):
        if monster_type == "slime":
            return Slime(level, position)
        elif monster_type == "rat":
            return Rat(level, position)
        elif monster_type == "boss":
            return Boss("boss", level, position)
        else:
            return Monster(monster_type, level, position)
