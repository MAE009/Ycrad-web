# inventory.py - Système d'inventaire simplifié
class Item:
    def __init__(self, item_id, name, item_type, description, value=0, **kwargs):
        self.id = item_id
        self.name = name
        self.type = item_type  # weapon, armor, consumable, material, quest
        self.description = description
        self.value = value
        
        # Propriétés spécifiques
        self.equipable = item_type in ["weapon", "armor", "accessory"]
        self.consumable = item_type == "consumable"
        
        # Stats d'équipement
        if item_type == "weapon":
            self.damage = kwargs.get('damage', 0)
        elif item_type == "armor":
            self.defense = kwargs.get('defense', 0)
        
        # Effets de consommable
        if item_type == "consumable":
            self.health_restore = kwargs.get('health_restore', 0)
            self.mana_restore = kwargs.get('mana_restore', 0)

class Inventory:
    def __init__(self, max_size=20):
        self.max_size = max_size
        self.items = []
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.gold = 50  # Or de départ
        
        # Initialiser avec quelques items de base
        self.initialize_starting_items()
    
    def initialize_starting_items(self):
        """Initialise l'inventaire avec des items de départ"""
        starting_items = [
            Item("sword_001", "Épée Rouillée", "weapon", "Une vieille épée usée", 15, damage=5),
            Item("armor_001", "Tunique en Cuir", "armor", "Armure basique en cuir", 20, defense=3),
            Item("potion_001", "Potion de Santé", "consumable", "Restaure 20 points de vie", 10, health_restore=20),
            Item("potion_002", "Potion de Mana", "consumable", "Restaure 15 points de mana", 12, mana_restore=15),
            Item("material_001", "Peau de Slime", "material", "Peau gluante de slime", 5),
            Item("material_002", "Queue de Rat", "material", "Queue de rat séchée", 3)
        ]
        
        for item in starting_items:
            self.add_item(item)
        
        # Équiper les items de départ
        self.equip_item(self.get_item_by_id("sword_001"))
        self.equip_item(self.get_item_by_id("armor_001"))
    
    def add_item(self, item, quantity=1):
        """Ajoute un item à l'inventaire"""
        if len(self.items) < self.max_size:
            # Vérifier si l'item existe déjà
            for existing_item in self.items:
                if existing_item.id == item.id:
                    # Pour les items stackables, on pourrait ajouter une quantité
                    break
            else:
                self.items.append(item)
            return True
        return False
    
    def remove_item(self, item):
        """Retire un item de l'inventaire"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def get_item_by_id(self, item_id):
        """Trouve un item par son ID"""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def equip_item(self, item):
        """Équipe un item"""
        if item and item.equipable and item in self.items:
            slot = self.get_equipment_slot(item.type)
            if slot:
                # Déséquiper l'item actuel s'il y en a un
                if self.equipment[slot]:
                    self.unequip_item(slot)
                
                # Équiper le nouvel item
                self.equipment[slot] = item
                self.items.remove(item)
                return True
        return False
    
    def unequip_item(self, slot):
        """Déséquipe un item"""
        if self.equipment[slot]:
            self.items.append(self.equipment[slot])
            self.equipment[slot] = None
            return True
        return False
    
    def get_equipment_slot(self, item_type):
        """Retourne le slot d'équipement approprié"""
        equipment_slots = {
            "weapon": "weapon",
            "armor": "armor", 
            "accessory": "accessory"
        }
        return equipment_slots.get(item_type)
    
    def use_consumable(self, item):
        """Utilise un objet consommable"""
        if item and item.consumable and item in self.items:
            # Appliquer les effets (sera géré par le Player)
            effects = {}
            if hasattr(item, 'health_restore'):
                effects['health'] = item.health_restore
            if hasattr(item, 'mana_restore'):
                effects['mana'] = item.mana_restore
            
            self.remove_item(item)
            return effects
        return None
    
    def get_equipment_bonuses(self):
        """Retourne les bonus de l'équipement"""
        bonuses = {"damage": 0, "defense": 0}
        
        for slot, item in self.equipment.items():
            if item:
                if hasattr(item, 'damage'):
                    bonuses["damage"] += item.damage
                if hasattr(item, 'defense'):
                    bonuses["defense"] += item.defense
        
        return bonuses
    
    def add_gold(self, amount):
        """Ajoute de l'or"""
        self.gold += amount
        return self.gold
    
    def remove_gold(self, amount):
        """Retire de l'or"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def is_full(self):
        """Vérifie si l'inventaire est plein"""
        return len(self.items) >= self.max_size
    
    def get_items_by_type(self, item_type):
        """Retourne tous les items d'un type spécifique"""
        return [item for item in self.items if item.type == item_type]