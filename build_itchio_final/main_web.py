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
        asset_files = {
            "player": "character/player.png",
            "monsters/slime": "monsters/slime.png",
            "monsters/rat": "monsters/rat.png",
        }
            
        for key, path in asset_files.items():
            try:
                full_path = "assets/" + path
                if await self.file_exists(full_path):
                    if "/" in key:
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
        return False  # Simulation
    
    async def load_image(self, path):
        """Charge une image (simulation pour le web)"""
        return self.create_surface((32, 32), (255, 0, 0))

# Système de sauvegarde pour le web (IndexedDB)
class WebSaveSystem:
    def __init__(self):
        self.ready = False
        
    async def initialize(self):
        """Initialise le système de sauvegarde"""
        try:
            self.ready = True
        except Exception as e:
            print(f"Erreur initialisation sauvegarde: {e}")
            self.ready = False
        
    async def save_game(self, data, slot=0):
        """Sauvegarde la partie"""
        if not self.ready:
            return False
        return True
        
    async def load_game(self, slot=0):
        """Charge une partie"""
        if not self.ready:
            return None
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
        from environment import Environment
        self.environment = Environment()
        self.ui = None
            
        # Contrôles web
        self.setup_web_controls()
        
    def setup_web_controls(self):
        """Configure les contrôles spécifiques au web"""
        try:
            import js
            js.document.addEventListener('joystickMove', self.handle_joystick)
            js.document.addEventListener('gameButton', self.handle_game_button)
        except ImportError:
            print("Mode navigateur non détecté, contrôles web désactivés")
        
    def handle_joystick(self, event):
        if hasattr(event, 'detail'):
            dx, dy = event.detail['x'], event.detail['y']
            self.virtual_joystick = (dx, dy)
        
    def handle_game_button(self, event):
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
        self.loading_progress = 50

        # Vérifier/générer les maps
        if not os.path.exists("assets/maps/village.json"):
            print("🔄 Génération des maps de fallback...")
            from map_generator import MapGenerator
            generator = MapGenerator()
            generator.generate_all_maps()

        # Charger les tilemaps
        self.environment.load_tilemaps()
        self.loading_progress = 80
            
        # Initialiser les systèmes de jeu
        await self.initialize_game_systems()
        self.loading_progress = 100
        self.game_state = "menu"
        
    async def initialize_game_systems(self):
        from player import Player
        from ui import UI
        self.player = Player("Ycrad", "warrior")
        self.ui = UI(self.player, None, None, self.config)
        
    async def run(self):
        await self.load_game_assets()
        while self.running:
            await self.handle_events()
            self.update()
            self.render()
            await asyncio.sleep(0)
            self.dt = self.clock.tick(self.fps) / 1000.0
        
    async def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.game_state == "menu":
                await self.handle_menu_events(event)
            elif self.game_state == "playing":
                await self.handle_playing_events(event)
        
    async def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            await self.start_new_game()
        
    async def handle_playing_events(self, event):
        pass
        
    async def start_new_game(self):
        self.game_state = "playing"
        
    def update(self):
        if self.game_state == "playing" and self.player:
            self.update_game_state()
        
    def update_game_state(self):
        if hasattr(self, 'virtual_joystick'):
            dx, dy = self.virtual_joystick
            new_pos = (self.player.position[0] + dx, self.player.position[1] + dy)
            if not self.environment.check_collision(new_pos):
                self.player.position = new_pos
        if hasattr(self, 'virtual_button_interact'):
            self.virtual_button_interact = False
        if hasattr(self, 'virtual_button_attack'):
            self.virtual_button_attack = False
        if hasattr(self, 'virtual_button_inventory'):
            self.virtual_button_inventory = False
        
    def render(self):
        self.screen.fill((0, 0, 0))
        if self.game_state == "loading":
            self.render_loading_screen()
        elif self.game_state == "menu":
            self.render_menu()
        elif self.game_state == "playing":
            self.render_game()
        pygame.display.flip()
        
    def render_loading_screen(self):
        font = pygame.font.SysFont("Arial", 24)
        bar_width, bar_height = 400, 30
        bar_x, bar_y = (800 - bar_width) // 2, 300
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 255),
                         (bar_x, bar_y, bar_width * self.loading_progress / 100, bar_height))
        text = font.render(f"Chargement... {self.loading_progress}%", True, (255, 255, 255))
        self.screen.blit(text, (400 - text.get_width() // 2, 250))
        
    def render_menu(self):
        font = pygame.font.SysFont("Arial", 36)
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title = title_font.render("YCRAD L'AVENTURIER", True, (255, 215, 0))
        self.screen.blit(title, (400 - title.get_width() // 2, 100))
        options = ["Nouvelle Partie", "Charger", "Options", "Quitter"]
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == 0 else (150, 150, 150)
            text = font.render(option, True, color)
            self.screen.blit(text, (400 - text.get_width() // 2, 200 + i * 60))
        
    def render_game(self):
        if not self.player:
            return
        # Dessiner la tilemap
        self.environment.render(self.screen, self.player.position)
        # Joueur
        player_sprite = self.asset_manager.assets["player"]
        screen_x = self.player.position[0] - self.environment.camera_offset[0]
        screen_y = self.player.position[1] - self.environment.camera_offset[1]
        self.screen.blit(player_sprite, (screen_x, screen_y))
        # UI
        if self.ui:
            self.ui.draw(self.screen, self.game_state)

# Point d'entrée asynchrone pour le web
async def main():
    game = WebGame()
    await game.run()
    pygame.quit()
    
if __name__ == "__main__":
    asyncio.run(main())
