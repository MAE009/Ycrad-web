# quests.py - Système de quêtes basique
class Quest:
    def __init__(self, quest_id, title, description, objectives, rewards):
        self.id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives  # [("kill", "slime", 5), ("collect", "item", 3)]
        self.rewards = rewards        # {"xp": 100, "gold": 50, "items": ["sword"]}
        self.completed = False
        self.progress = {}
        
        # Initialiser la progression
        for obj_type, target, quantity in objectives:
            self.progress[target] = 0
    
    def update_progress(self, objective_type, target, amount=1):
        """Met à jour la progression d'un objectif"""
        if self.completed:
            return False
            
        for obj_type, obj_target, quantity in self.objectives:
            if obj_type == objective_type and obj_target == target:
                self.progress[target] = min(self.progress[target] + amount, quantity)
                
                # Vérifier si tous les objectifs sont complétés
                if all(self.progress[obj[1]] >= obj[2] for obj in self.objectives):
                    self.completed = True
                    return True
        return False

class QuestManager:
    def __init__(self, quests=[]):
        self.active_quests = []
        self.completed_quests = []
        self.available_quests = self.initialize_quests()
        self.quests = quests
    
    def initialize_quests(self):
        """Initialise les quêtes disponibles"""
        return [
            Quest(
                "quest_001",
                "Chasse aux Slimes",
                "Les slimes envahissent le village. Éliminez 5 slimes.",
                [("kill", "slime", 5)],
                {"xp": 100, "gold": 50, "items": ["basic_sword"]}
            ),
            Quest(
                "quest_002", 
                "Problème de Rats",
                "Les rats volent nos provisions. Tuez 3 rats.",
                [("kill", "rat", 3)],
                {"xp": 80, "gold": 30, "items": ["health_potion"]}
            ),
            Quest(
                "quest_003",
                "Exploration Forestière",
                "Explorez la forêt et revenez au village.",
                [("explore", "forest", 1)],
                {"xp": 150, "gold": 75, "items": ["leather_armor"]}
            )
        ]
    
    def start_quest(self, quest_id):
        """Démarre une quête"""
        for quest in self.available_quests:
            if quest.id == quest_id and quest not in self.active_quests:
                self.active_quests.append(quest)
                return quest
        return None
    
    # nouvelle méthode
    def check_triggers(self, player_position):
        """
        Vérifie si une quête se déclenche selon la position du joueur.
        """
        for quest in self.quests:
            if hasattr(quest, "trigger_position") and quest.trigger_position == player_position:
                print(f"Quête déclenchée: {quest.name}")
                # ici tu peux lancer la quête, afficher dialogue, etc.
    
    def complete_quest(self, quest):
        """Termine une quête et donne les récompenses"""
        if quest in self.active_quests and quest.completed:
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)
            return quest.rewards
        return None
    
    def on_monster_killed(self, monster_type):
        """Appelé quand un monstre est tué"""
        for quest in self.active_quests:
            quest.update_progress("kill", monster_type)
    
    def on_item_collected(self, item_type):
        """Appelé quand un item est collecté"""
        for quest in self.active_quests:
            quest.update_progress("collect", item_type)
    
    def on_zone_entered(self, zone_name):
        """Appelé quand une zone est explorée"""
        for quest in self.active_quests:
            quest.update_progress("explore", zone_name)
    
    def get_available_quests(self):
        """Retourne les quêtes disponibles"""
        return [q for q in self.available_quests if q not in self.active_quests and q not in self.completed_quests]
    
    def has_completed_quests(self):
        """Vérifie s'il y a des quêtes complétées non réclamées"""
        return any(quest.completed for quest in self.active_quests)
