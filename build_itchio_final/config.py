# config.py - Configuration de base pour Ycrad l'Aventurier
class Config:
    def __init__(self):
        # Configuration graphique
        self.resolution = [800, 600]
        self.fullscreen = False
        self.framerate = 60
        
        # Configuration audio
        self.music_volume = 0.7
        self.sound_volume = 0.8
        self.mute = False
        
        # Configuration gameplay
        self.difficulty = "normal"
        self.language = "french"
        self.autosave = True
        
        # Contrôles clavier
        self.controls = {
            "move_up": ["up", "w", "z"],
            "move_down": ["down", "s"], 
            "move_left": ["left", "a", "q"],
            "move_right": ["right", "d"],
            "interact": ["e"],
            "attack": ["space"],
            "inventory": ["i"],
            "pause": ["escape"]
        }
        
        # Paramètres du joueur
        self.player_settings = {
            "starting_class": "warrior",
            "difficulty_multiplier": 1.0
        }
    
    def get(self, category, key, default=None):
        """Récupère une valeur de configuration"""
        try:
            if hasattr(self, category):
                category_obj = getattr(self, category)
                if isinstance(category_obj, dict) and key in category_obj:
                    return category_obj[key]
            return default
        except:
            return default
    
    def set(self, category, key, value):
        """Définit une valeur de configuration"""
        try:
            if not hasattr(self, category):
                setattr(self, category, {})
            getattr(self, category)[key] = value
        except:
            pass

# Instance globale de configuration
game_config = Config()
