# main_web.py - Version navigateur de Ycrad l'Aventurier
import pygame
import sys
import asyncio
import json
import os
from pathlib import Path

# Configuration spéciale pour le web
class WebConfig:
    def __init__(self):
        self.is_web = True
        self.assets_path = "assets/"
        self.save_path = "/idb/ycrad_saves/"
        
        # Configuration par défaut adaptée au web
        self.settings = {
            "graphics": {
                "resolution": [800, 600],
                "fullscreen": False,
                "vsync": True,
                "framerate": 60
            },
            "audio": {
                "music_volume": 0.6,
                "sound_volume": 0.7,
                "mute": False
            },
            "controls": {
                "touch_enabled": True,
                "keyboard_enabled": True
            }
        }
    
    def get(self, category, key, default=None):
        return self.settings.get(category, {}).get(key, default)

# Gestionnaire d'assets pour le web
class WebAssetManager:
    def __init__(self):
        self.assets = {}
        self.loaded = False
    
    async def load_assets(self):
        """Charge les assets de manière asynchrone"""
        if self.loaded:
            return
        
        # Créer des assets de base programmatiquement pour le web
        self.assets = {
            "player": self.create_surface((32, 32), (0, 0, 255)),
            "monsters": {
                "slime": self.create_surface((32, 32), (0, 255, 0)),
                "rat": self.create_surface((32, 32), (139, 69, 19)),
            },
            "environments": {
                "village": self.create_surface((800, 600), (200, 200, 100)),
                "forest": self.create_surface((800, 600), (0, 100, 0)),
                "marsh": self.create_surface((800, 600), (70, 50, 30)),
            },
            "npcs": {
                "merchant": self.create_surface((32, 32), (255, 0, 0)),
                "blacksmith": self.create_surface((32, 32), (100, 100, 100)),
            }
        }
        
        # Essayer de charger les vrais assets si disponibles
        try:
            await self.load_real_assets()
        except Exception as e:
            print(f"Impossible de charger les assets: {e}")
        
        self.loaded = True
    
    def create_surface(self, size, color):
        """Crée une surface avec une couleur unie"""
        surf = pygame.Surface(size)
        surf.fill(color)
        return surf
    
    async def load_real_assets(self):
        """Tente de charger les vrais assets"""
        # Cette fonction essaie de charger les images réelles
        asset_files = {
            "player": "character/player.png",
            "monsters/slime": "monsters/slime.png",
            "monsters/rat": "monsters/rat.png",
            "environments/village": "backgrounds/village.png",
            "environments/forest": "backgrounds/forest.png",
            "environments/marsh": "backgrounds/marsh.png",
        }
        
        for key, path in asset_files.items():
            try:
                full_path = self.config.assets_path + path
                if await self.file_exists(full_path):
                    if "/" in key:
                        # Gestion des sous-dossiers
                        parts = key.split("/")
                        category = parts[0]
                        subkey = parts[1]
                        
                        if category not in self.assets:
                            self.assets[category] = {}
                        
                        self.assets[category][subkey] = await self.load_image(full_path)
                    else:
                        self.assets[key] = await self.load_image(full_path)
            except Exception as e:
                print(f"Erreur chargement {path}: {e}")
    
    async def file_exists(self, path):
        """Vérifie si un fichier existe (simulation pour le web)"""
        # En réalité, on utiliserait des requêtes HTTP ou IndexedDB
        return False  # Pour l'instant, on retourne toujours faux
    
    async def load_image(self, path):
        """Charge une image (simulation pour le web)"""
        # Dans une vraie implémentation, on utiliserait pygame.image.load
        # avec des appels asynchrones ou des workers web
        return self.create_surface((32, 32), (255, 0, 0))

# Système de sauvegarde pour le web (IndexedDB)
class WebSaveSystem:
    def __init__(self):
        self.ready = False
    
    async def initialize(self):
        """Initialise le système de sauvegarde"""
        try:
            # Ici on initialiserait la connexion à IndexedDB
            self.ready = True
        except Exception as e:
            print(f"Erreur initialisation sauvegarde: {e}")
            self.ready = False
    
    async def save_game(self, data, slot=0):
        """Sauvegarde la partie"""
        if not self.ready:
            return False
        
        try:
            # Simulation de sauvegarde dans le localStorage
            if hasattr(window, 'localStorage'):
                window.localStorage.setItem(f'ycrad_save_{slot}', json.dumps(data))
            return True
        except Exception as e:
            print(f"Erreur sauvegarde: {e}")
            return False
    
    async def load_game(self, slot=0):
        """Charge une partie"""
        if not self.ready:
            return None
        
        try:
            if hasattr(window, 'localStorage'):
                data = window.localStorage.getItem(f'ycrad_save_{slot}')
                if data:
                    return json.loads(data)
            return None
        except Exception as e:
            print(f"Erreur chargement: {e}")
            return None

# Version web du jeu principal
class WebGame:
    def __init__(self):
        # Initialisation de base
        pygame.init()
        pygame.font.init()
        
        # Configuration web
        self.config = WebConfig()
        
        # Fenêtre
        self.screen = pygame.display.set_mode(
            self.config.get("graphics", "resolution")
        )
        pygame.display.set_caption("Ycrad l'Aventurier")
        
        # Timing
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps = self.config.get("graphics", "framerate")
        self.running = True
        
        # États
        self.game_state = "loading"
        self.loading_progress = 0
        
        # Systèmes
        self.asset_manager = WebAssetManager()
        self.save_system = WebSaveSystem()
        
        # Initialisation différée
        self.player = None
        self.environment = None
        self.ui = None
        
        # Contrôles web
        self.setup_web_controls()
    
    def setup_web_controls(self):
        """Configure les contrôles spécifiques au web"""
        # Écouteurs d'événements pour les contrôles tactiles
        try:
            import js
            js.document.addEventListener('joystickMove', self.handle_joystick)
            js.document.addEventListener('gameButton', self.handle_game_button)
        except ImportError:
            print("Mode navigateur non détecté, contrôles web désactivés")
    
    def handle_joystick(self, event):
        """Gère les mouvements du joystick virtuel"""
        if hasattr(event, 'detail'):
            dx, dy = event.detail['x'], event.detail['y']
            # Convertir en entrées de contrôle
            self.virtual_joystick = (dx, dy)
    
    def handle_game_button(self, event):
        """Gère les boutons de jeu virtuels"""
        if hasattr(event, 'detail'):
            button = event.detail
            if button == 'interact':
                self.virtual_button_interact = True
            elif button == 'attack':
                self.virtual_button_attack = True
            elif button == 'inventory':
                self.virtual_button_inventory = True
    
    async def load_game_assets(self):
        """Charge les assets du jeu de manière asynchrone"""
        self.game_state = "loading"
        self.loading_progress = 0
        
        # Initialiser le système de sauvegarde
        await self.save_system.initialize()
        self.loading_progress = 20
        
        # Charger les assets
        await self.asset_manager.load_assets()
        self.loading_progress = 70
        
        # Initialiser les systèmes de jeu
        await self.initialize_game_systems()
        self.loading_progress = 100
        
        self.game_state = "menu"
    
    async def initialize_game_systems(self):
        """Initialise les systèmes de jeu"""
        # Ici on initialiserait le joueur, l'environnement, etc.
        # Pour l'instant, on crée des placeholders
        from player import Player
        from environment import Environment
        from ui import UI
        
        self.player = Player("Ycrad", "warrior")
        self.environment = Environment()
        self.ui = UI(self.player, None, None, self.config)
    
    async def run(self):
        """Boucle principale asynchrone"""
        # Chargement initial
        await self.load_game_assets()
        
        # Boucle de jeu principale
        while self.running:
            await self.handle_events()
            self.update()
            self.render()
            await asyncio.sleep(0)  # Yield to event loop
            self.dt = self.clock.tick(self.fps) / 1000.0
    
    async def handle_events(self):
        """Gère les événements de manière asynchrone"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Gestion des états
            if self.game_state == "menu":
                await self.handle_menu_events(event)
            elif self.game_state == "playing":
                await self.handle_playing_events(event)
    
    async def handle_menu_events(self, event):
        """Gère les événements du menu"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            await self.start_new_game()
    
    async def handle_playing_events(self, event):
        """Gère les événements de jeu"""
        pass
    
    async def start_new_game(self):
        """Démarre une nouvelle partie"""
        self.game_state = "playing"
        # Initialisation de la nouvelle partie...
    
    def update(self):
        """Met à jour la logique du jeu"""
        if self.game_state == "loading":
            # Animation de chargement
            pass
        
        elif self.game_state == "playing" and self.player:
            # Mettre à jour le jeu
            self.update_game_state()
    
    def update_game_state(self):
        """Met à jour l'état de jeu"""
        # Gérer les entrées virtuelles
        if hasattr(self, 'virtual_joystick'):
            dx, dy = self.virtual_joystick
            # Appliquer le mouvement au joueur...
        
        # Réinitialiser les boutons virtuels
        if hasattr(self, 'virtual_button_interact'):
            self.virtual_button_interact = False
        if hasattr(self, 'virtual_button_attack'):
            self.virtual_button_attack = False
        if hasattr(self, 'virtual_button_inventory'):
            self.virtual_button_inventory = False
    
    def render(self):
        """Affiche le jeu"""
        self.screen.fill((0, 0, 0))
        
        if self.game_state == "loading":
            self.render_loading_screen()
        elif self.game_state == "menu":
            self.render_menu()
        elif self.game_state == "playing":
            self.render_game()
        
        pygame.display.flip()
    
    def render_loading_screen(self):
        """Affiche l'écran de chargement"""
        font = pygame.font.SysFont("Arial", 24)
        
        # Barre de progression
        bar_width = 400
        bar_height = 30
        bar_x = (800 - bar_width) // 2
        bar_y = 300
        
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 255), 
                        (bar_x, bar_y, bar_width * self.loading_progress / 100, bar_height))
        
        # Texte
        text = font.render(f"Chargement... {self.loading_progress}%", True, (255, 255, 255))
        self.screen.blit(text, (400 - text.get_width() // 2, 250))
        
        # Conseils de chargement
        tips = [
            "Astuce: Utilisez ZQSD pour vous déplacer",
            "Astuce: Appuyez sur E pour interagir",
            "Astuce: Espace pour attaquer les ennemis"
        ]
        tip = tips[int(pygame.time.get_ticks() / 3000) % len(tips)]
        tip_text = font.render(tip, True, (200, 200, 200))
        self.screen.blit(tip_text, (400 - tip_text.get_width() // 2, 350))
    
    def render_menu(self):
        """Affiche le menu principal"""
        font = pygame.font.SysFont("Arial", 36)
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        
        # Titre
        title = title_font.render("YCRAD L'AVENTURIER", True, (255, 215, 0))
        self.screen.blit(title, (400 - title.get_width() // 2, 100))
        
        # Options
        options = ["Nouvelle Partie", "Charger", "Options", "Quitter"]
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == 0 else (150, 150, 150)
            text = font.render(option, True, color)
            self.screen.blit(text, (400 - text.get_width() // 2, 200 + i * 60))
        
        # Copyright
        copyright_font = pygame.font.SysFont("Arial", 16)
        copyright = copyright_font.render("© 2024 Votre Studio - Version Web", True, (100, 100, 100))
        self.screen.blit(copyright, (400 - copyright.get_width() // 2, 500))
    
    def render_game(self):
        """Affiche le jeu"""
        if not self.player:
            return
        
        # Environnement
        env = self.asset_manager.assets["environments"]["village"]
        self.screen.blit(env, (0, 0))
        
        # Joueur
        player_sprite = self.asset_manager.assets["player"]
        self.screen.blit(player_sprite, self.player.position)
        
        # UI
        if self.ui:
            self.ui.draw(self.screen, self.game_state)
        
        # Indicateur de contrôles tactiles
        if hasattr(self, 'virtual_joystick'):
            control_font = pygame.font.SysFont("Arial", 14)
            control_text = control_font.render("Contrôles tactiles actifs", True, (0, 255, 255))
            self.screen.blit(control_text, (10, 10))

# Point d'entrée asynchrone pour le web
async def main():
    game = WebGame()
    await game.run()
    pygame.quit()

# Lancement du jeu
if __name__ == "__main__":
    asyncio.run(main())