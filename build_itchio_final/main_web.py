# main_web.py - Point d'entrée principal avec toutes les améliorations
import pygame
import sys
import os
import asyncio
from player import Player
from environment import Environment
from quests import QuestManager
from inventory import Inventory
from ui import UI
from monsters import MonsterFactory
from config import game_config
from animation import AnimationManager
from tilemap import TileMap
from map_generator import MapGenerator

class WebGame:
    def __init__(self):
        # Initialisation de base
        pygame.init()
        pygame.font.init()
        
        # Configuration
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ycrad l'Aventurier")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.fps = game_config.get("graphics", "framerate", 60)
        
        # États du jeu
        self.game_state = "loading"  # loading, menu, playing, combat, inventory, game_over
        self.loading_progress = 0
        self.loading_message = "Initialisation..."
        
        # Systèmes principaux
        self.player = None
        self.environment = Environment()
        self.quest_manager = QuestManager()
        self.inventory = None
        self.ui = None
        self.animation_manager = AnimationManager()
        
        # Assets
        self.assets = {}
        
        # Contrôles
        self.keys_pressed = {}
        
        # Initialisation différée
        self.initialize_game()
    
    def initialize_game(self):
        """Initialise les systèmes de jeu"""
        # Dans main_web.py - Modifiez initialize_game

        # Vérifier et générer les assets
        self.check_and_generate_assets()
    
        # Créer le joueur
        self.player = Player("Ycrad", "warrior")
    
        # Créer l'inventaire
        self.inventory = Inventory(self.player)
    
        # Créer l'UI
        self.ui = UI(self.player, self.inventory, self.quest_manager, game_config)
    
        # Charger les assets
        self.load_assets()
    
    def check_assets(self):
        """Vérifie et génère les assets si nécessaire"""
        if not os.path.exists("assets/maps/village.json"):
            self.loading_message = "Génération des maps..."
            generator = MapGenerator()
            generator.generate_all_maps()
        
        # Charger les tilemaps
        self.environment.load_tilemaps()
    
    async def load_assets_async(self):
        """Charge les assets de manière asynchrone"""
        self.game_state = "loading"
        
        steps = [
            ("Chargement des configurations...", 10),
            ("Génération des maps...", 30),
            ("Chargement des tilemaps...", 50),
            ("Chargement des sprites...", 70),
            ("Initialisation des systèmes...", 90),
            ("Démarrage du jeu...", 100)
        ]
        
        for message, progress in steps:
            self.loading_message = message
            self.loading_progress = progress
            await asyncio.sleep(0.1)  # Simuler le chargement
        
        self.game_state = "menu"
    
    def handle_events(self):
        """Gère tous les événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Gestion des touches
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed[event.key] = True
                self.handle_keydown(event)
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed[event.key] = False
            
            # Gestion de l'UI
            if self.ui:
                self.ui.handle_event(event, self)
    
    

    def load_assets(self):
        """Charge les assets dans un dictionnaire"""
        self.assets = {}
        
        try:
            # Backgrounds
            self.assets["backgrounds"] = {
                "village": pygame.image.load("assets/backgrounds/village.png").convert(),
                "forest": pygame.image.load("assets/backgrounds/forest.png").convert(),
                "marsh": pygame.image.load("assets/backgrounds/marsh.png").convert()
            }
            
            # Character
            #self.assets["player"] = pygame.image.load("assets/character/player.png").convert_alpha()
            
            # Monsters
           # self.assets["monsters"] = {
              #  "slime": pygame.image.load("assets/monsters/slime.png").convert_alpha(),
             #   "rat": pygame.image.load("assets/monsters/rat.png").convert_alpha()
            #}
            
            print("✅ Assets chargés avec succès")
            
        except Exception as e:
            print(f"❌ Erreur chargement assets: {e}")
            self.create_fallback_assets()

    
    def create_fallback_assets(self):
        """Crée des assets de fallback programmatiquement"""
        self.assets = {
            "backgrounds": {
                "village": pygame.Surface((800, 600)),
                "forest": pygame.Surface((800, 600)),
                "marsh": pygame.Surface((800, 600))
            },
            "player": pygame.Surface((32, 32), pygame.SRCALPHA),
            "monsters": {
                "slime": pygame.Surface((32, 32), pygame.SRCALPHA),
                "rat": pygame.Surface((32, 32), pygame.SRCALPHA)
            }
        }
        
        # Couleurs de fallback
        self.assets["backgrounds"]["village"].fill((200, 200, 100))
        self.assets["backgrounds"]["forest"].fill((0, 100, 0))
        self.assets["backgrounds"]["marsh"].fill((70, 50, 30))
        
        # Joueur fallback (carré bleu)
        self.assets["player"].fill((0, 0, 255))
        
        # Monstres fallback
        self.assets["monsters"]["slime"].fill((0, 255, 0))
        self.assets["monsters"]["rat"].fill((139, 69, 19))
        
        print("✅ Assets de fallback créés")
    

    
    def handle_keydown(self, event):
        """Gère les appuis de touches"""
        key_actions = {
            pygame.K_ESCAPE: self.toggle_pause,
            pygame.K_i: self.toggle_inventory,
            pygame.K_q: self.toggle_quests,
            pygame.K_e: self.handle_interaction,
            pygame.K_SPACE: self.handle_attack,
            pygame.K_r: self.restart_game if self.game_state == "game_over" else None,
            pygame.K_F5: self.quick_save,
            pygame.K_F9: self.quick_load
        }
        
        action = key_actions.get(event.key)
        if action:
            action()
    
    def toggle_pause(self):
        """Met en pause/reprend le jeu"""
        if self.game_state == "playing":
            self.game_state = "pause"
        elif self.game_state == "pause":
            self.game_state = "playing"
    
    def toggle_inventory(self):
        """Ouvre/ferme l'inventaire"""
        if self.game_state == "playing":
            self.game_state = "inventory"
        elif self.game_state == "inventory":
            self.game_state = "playing"
    
    def toggle_quests(self):
        """Affiche/cache les quêtes"""
        if self.ui:
            self.ui.show_quests = not self.ui.show_quests
    
    def handle_interaction(self):
        """Gère l'interaction avec l'environnement"""
        if self.game_state == "playing":
            # Logique d'interaction avec les PNJs
            pass
    
    def handle_attack(self):
        """Gère l'attaque"""
        if self.game_state == "playing":
            self.player.is_attacking = True
    
    def update(self):
        """Met à jour la logique du jeu"""
        self.dt = self.clock.get_time() / 1000.0  # Convertir en secondes
        
        if self.game_state == "playing":
            self.update_playing_state()
        elif self.game_state == "combat":
            self.update_combat_state()
        
        # Mettre à jour les animations
        self.animation_manager.update(self.dt)
    
    def update_playing_state(self):
        """Met à jour l'état de jeu normal"""
        # Gestion des entrées de mouvement
        dx, dy = 0, 0
        if self.keys_pressed.get(pygame.K_LEFT) or self.keys_pressed.get(pygame.K_a) or self.keys_pressed.get(pygame.K_q):
            dx = -1
            self.player.direction = "left"
        if self.keys_pressed.get(pygame.K_RIGHT) or self.keys_pressed.get(pygame.K_d):
            dx = 1
            self.player.direction = "right"
        if self.keys_pressed.get(pygame.K_UP) or self.keys_pressed.get(pygame.K_w) or self.keys_pressed.get(pygame.K_z):
            dy = -1
            self.player.direction = "up"
        if self.keys_pressed.get(pygame.K_DOWN) or self.keys_pressed.get(pygame.K_s):
            dy = 1
            self.player.direction = "down"
        
        # Déplacement du joueur
        if dx != 0 or dy != 0:
            self.player.is_moving = True
            new_x = self.player.position[0] + dx * self.player.speed
            new_y = self.player.position[1] + dy * self.player.speed
            
            # Vérifier les collisions
            if not self.environment.check_collision([new_x, new_y]):
                self.player.position[0] = new_x
                self.player.position[1] = new_y
        else:
            self.player.is_moving = False
        
        # Vérifier les changements de zone
        new_zone = self.environment.get_zone_at_position(self.player.position)
        if new_zone != self.environment.current_zone:
            new_pos = self.environment.change_zone(new_zone, self.player.position)
            self.player.position = list(new_pos)
        
        # Mettre à jour les animations
        self.update_animations()
        
        # Vérifier les quêtes
        self.quest_manager.check_triggers(self.player.position)
    
    def update_combat_state(self):
        """Met à jour l'état de combat"""
        # Logique de combat tour par tour
        pass
    
    def update_animations(self):
        """Met à jour les animations"""
        # Animation du joueur
        if self.player.is_attacking:
            animation_name = f"attack_{self.player.direction}"
            self.player.is_attacking = False
        elif self.player.is_moving:
            animation_name = f"walk_{self.player.direction}"
        else:
            animation_name = f"idle_{self.player.direction}"
        
        self.animation_manager.play_animation("player", animation_name)
    
    def render(self):
        """Affiche le jeu"""
        self.screen.fill((0, 0, 0))  # Clear screen
        
        if self.game_state == "loading":
            self.render_loading_screen()
        elif self.game_state == "menu":
            self.render_menu()
        elif self.game_state in ["playing", "combat", "inventory"]:
            self.render_game()
        elif self.game_state == "game_over":
            self.render_game_over()
        elif self.game_state == "pause":
            self.render_pause()
        
        pygame.display.flip()
    
    def render_loading_screen(self):
        """Affiche l'écran de chargement"""
        # Fond
        self.screen.fill((0, 0, 50))
        
        # Titre
        font = pygame.font.SysFont("Arial", 36)
        title = font.render("Ycrad l'Aventurier", True, (255, 215, 0))
        self.screen.blit(title, (400 - title.get_width() // 2, 150))
        
        # Barre de progression
        bar_width = 400
        bar_height = 30
        bar_x = 400 - bar_width // 2
        bar_y = 250
        
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 255), 
                        (bar_x, bar_y, bar_width * self.loading_progress / 100, bar_height))
        
        # Texte de chargement
        loading_font = pygame.font.SysFont("Arial", 20)
        loading_text = loading_font.render(self.loading_message, True, (255, 255, 255))
        self.screen.blit(loading_text, (400 - loading_text.get_width() // 2, 220))
        
        # Pourcentage
        percent_text = loading_font.render(f"{self.loading_progress}%", True, (255, 255, 255))
        self.screen.blit(percent_text, (400 - percent_text.get_width() // 2, 290))
        
        # Conseils
        tips = [
            "Astuce: Utilisez ZQSD pour vous déplacer",
            "Astuce: Appuyez sur E pour interagir",
            "Astuce: Espace pour attaquer les ennemis",
            "Astuce: I pour ouvrir l'inventaire"
        ]
        tip_index = int(pygame.time.get_ticks() / 4000) % len(tips)
        tip_text = loading_font.render(tips[tip_index], True, (200, 200, 200))
        self.screen.blit(tip_text, (400 - tip_text.get_width() // 2, 330))
    
    def render_menu(self):
        """Affiche le menu principal"""
        self.screen.fill((0, 0, 50))
        
        # Titre
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title = title_font.render("YCRAD L'AVENTURIER", True, (255, 215, 0))
        self.screen.blit(title, (400 - title.get_width() // 2, 100))
        
        # Sous-titre
        subtitle_font = pygame.font.SysFont("Arial", 24)
        subtitle = subtitle_font.render("RPG Pixel Art Épique", True, (200, 200, 200))
        self.screen.blit(subtitle, (400 - subtitle.get_width() // 2, 160))
        
        # Options du menu
        options = ["Nouvelle Partie", "Charger Partie", "Options", "Quitter"]
        option_font = pygame.font.SysFont("Arial", 32)
        
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == 0 else (150, 150, 150)
            text = option_font.render(option, True, color)
            self.screen.blit(text, (400 - text.get_width() // 2, 250 + i * 60))
        
        # Copyright
        copyright_font = pygame.font.SysFont("Arial", 16)
        copyright = copyright_font.render("© 2024 Votre Studio - Version Web", True, (100, 100, 100))
        self.screen.blit(copyright, (400 - copyright.get_width() // 2, 500))
    
    def render_game(self):
        """Affiche le jeu en cours"""
        # Dessiner l'environnement
        self.environment.render(self.screen, self.player.position)
        
        # Dessiner le joueur
        player_frame = self.animation_manager.get_current_frame()
        if player_frame:
            # Convertir les coordonnées monde vers écran
            screen_x = self.player.position[0] - self.environment.camera_offset[0]
            screen_y = self.player.position[1] - self.environment.camera_offset[1]
            self.screen.blit(player_frame, (screen_x, screen_y))
        else:
            # Fallback
            pygame.draw.rect(self.screen, (0, 0, 255), 
                           (self.player.position[0] - 16, self.player.position[1] - 16, 32, 32))
        
        # Dessiner l'UI
        if self.ui:
            self.ui.draw(self.screen, self.game_state)
        
        # Mode pause
        if self.game_state == "pause":
            self.render_pause_overlay()
    
    def render_game_over(self):
        """Affiche l'écran de game over"""
        self.screen.fill((0, 0, 0))
        
        # Message
        font = pygame.font.SysFont("Arial", 48)
        game_over = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over, (400 - game_over.get_width() // 2, 200))
        
        # Score
        score_font = pygame.font.SysFont("Arial", 24)
        if self.player:
            score_text = score_font.render(f"Niveau atteint: {self.player.level}", True, (255, 255, 255))
            self.screen.blit(score_text, (400 - score_text.get_width() // 2, 270))
        
        # Instructions
        instruct_font = pygame.font.SysFont("Arial", 20)
        instruct = instruct_font.render("Appuyez sur R pour recommencer", True, (255, 215, 0))
        self.screen.blit(instruct, (400 - instruct.get_width() // 2, 320))
    
    def render_pause(self):
        """Affiche l'écran de pause"""
        self.render_game()
        self.render_pause_overlay()
    
    def render_pause_overlay(self):
        """Affiche l'overlay de pause"""
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("PAUSE", True, (255, 255, 255))
        self.screen.blit(text, (400 - text.get_width() // 2, 250))
        
        instruct_font = pygame.font.SysFont("Arial", 20)
        instruct = instruct_font.render("Appuyez sur Échap pour continuer", True, (200, 200, 200))
        self.screen.blit(instruct, (400 - instruct.get_width() // 2, 320))
    
    def quick_save(self):
        """Sauvegarde rapide"""
        print("💾 Sauvegarde rapide")
        # Implémentation de la sauvegarde
    
    def quick_load(self):
        """Chargement rapide"""
        print("📂 Chargement rapide")
        # Implémentation du chargement
    
    
    # ✅ Vérifie et génère les assets manquants
    def check_and_generate_assets(self):
        """Vérifie et génère les assets manquants"""
        required_assets = [
            "assets/backgrounds/village.png",
            "assets/backgrounds/forest.png",
            "assets/backgrounds/marsh.png",
            "assets/character/player.png",
            "assets/monsters/slime.png",
            "assets/monsters/rat.png",
            "assets/ui/icons/potion.png",
            "assets/ui/icons/sword.png",
            "assets/tilesets/terrain.png"
        ]

        missing_assets = []

        for asset in required_assets:
            if not os.path.exists(asset):
                missing_assets.append(asset)

        if missing_assets:
            print(f"⚠️  Assets manquants détectés: {len(missing_assets)}")
            print("🔄 Génération des assets de fallback...")

            try:
                from asset_generator import AssetGenerator
                generator = AssetGenerator()
                generator.generate_all_assets()
                print("✅ Assets générés avec succès!")
            except Exception as e:
                print(f"❌ Erreur lors de la génération des assets: {e}")
                # Créer des placeholders minimalistes
                self.create_minimal_assets()

    # ✅ Création d’assets minimalistes en cas d’erreur
    def create_minimal_assets(self):
        """Crée des assets minimalistes en cas d'erreur"""
        os.makedirs("assets/backgrounds", exist_ok=True)

        # Créer un background minimal
        bg = pygame.Surface((800, 600))
        bg.fill((50, 50, 100))  # Fond bleu foncé
        pygame.image.save(bg, "assets/backgrounds/village.png")

        print("✅ Assets minimalistes créés")


    
    
    def restart_game(self):
        """Redémarre le jeu"""
        self.initialize_game()
        self.game_state = "playing"
    
    async def run(self):
        """Boucle principale asynchrone"""
        # Chargement initial
        await self.load_assets_async()
        
        # Boucle de jeu
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            
            await asyncio.sleep(0)  # Yield to event loop
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

# Point d'entrée asynchrone
async def main():
    game = WebGame()
    await game.run()

# Lancement du jeu
if __name__ == "__main__":
    asyncio.run(main())
