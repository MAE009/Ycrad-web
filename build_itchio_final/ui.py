# ui.py - Interface utilisateur pour la version web
import pygame
import math

class UI:
    def __init__(self, player, inventory, quest_manager, config, game):
        self.player = player
        self.inventory = inventory
        self.quest_manager = quest_manager
        self.config = config
        self.menu_options = ["Nouvelle Partie", "Charger", "Options", "Quitter"]
        self.menu_rects = []  # stockera les zones cliquables
        self.selected_menu = 0
        self.selected_option = None
        self.game = game
        
        # Polices
        self.fonts = {
            "small": pygame.font.SysFont("Arial", 14),
            "medium": pygame.font.SysFont("Arial", 18),
            "large": pygame.font.SysFont("Arial", 24),
            "title": pygame.font.SysFont("Arial", 32, bold=True)
        }
        
        # Couleurs
        self.colors = {
            "health": (255, 50, 50),
            "mana": (50, 100, 255),
            "xp": (50, 200, 50),
            "background": (0, 0, 0, 180),
            "text": (255, 255, 255),
            "highlight": (255, 215, 0),
            "warning": (255, 100, 100)
        }
        
        # État de l'UI
        self.show_inventory = False
        self.show_quests = False
        self.show_skills = False
        self.messages = []
        self.combat_messages = []
        self.message_timeout = 5000  # 5 secondes
        self.last_message_time = 0
        
        # Animation
        self.animation_time = 0
        self.ui_scale = self.config.get("interface", "ui_scale", 1.0)
    
    def add_message(self, message):
        """Ajoute un message à l'interface"""
        self.messages.append({
            "text": message,
            "time": pygame.time.get_ticks(),
            "color": self.colors["text"]
        })
        # Garder seulement les 5 derniers messages
        if len(self.messages) > 5:
            self.messages.pop(0)
    
    def add_combat_message(self, message, is_critical=False):
        """Ajoute un message de combat"""
        color = self.colors["highlight"] if is_critical else self.colors["text"]
        self.combat_messages.append({
            "text": message,
            "time": pygame.time.get_ticks(),
            "color": color
        })
        if len(self.combat_messages) > 3:
            self.combat_messages.pop(0)
    
    def draw(self, screen, game_state):
        """Dessine l'interface selon l'état du jeu"""
        current_time = pygame.time.get_ticks()
        self.animation_time = current_time
        
        # Nettoyer les messages anciens
        self.messages = [msg for msg in self.messages 
                        if current_time - msg["time"] < self.message_timeout]
        
        if game_state == "playing":
            self.draw_hud(screen)
            self.draw_messages(screen)
            
        elif game_state == "combat":
            self.draw_combat_ui(screen)
            self.draw_combat_messages(screen)
            
        elif game_state == "inventory":
            self.draw_inventory(screen)
            
        elif game_state == "dialogue":
            self.draw_dialogue(screen)
            
        elif game_state == "menu":
            self.draw_main_menu(screen)
            
        elif game_state == "game_over":
            self.draw_game_over(screen)
    
    def draw_hud(self, screen):
        """Dessine le HUD (Heads-Up Display)"""
        # Barre de vie
        self.draw_bar(screen, 20, 20, 200, 20, 
                     self.player.hp / self.player.max_hp, 
                     self.colors["health"], "PV")
        
        # Barre de mana
        self.draw_bar(screen, 20, 50, 200, 20,
                     self.player.mp / self.player.max_mp,
                     self.colors["mana"], "MP")
        
        # Barre d'XP
        xp_percent = self.player.xp / self.player.xp_to_next_level
        self.draw_bar(screen, 20, 80, 200, 15,
                     xp_percent, self.colors["xp"], "XP")
        
        # Informations du joueur
        info_text = [
            f"Niveau: {self.player.level}",
            f"Classe: {self.player.current_class.name}",
            f"Or: {self.player.gold}",
            f"Zone: {getattr(self.player, 'current_zone', 'Inconnue')}"
        ]
        
        for i, text in enumerate(info_text):
            text_surface = self.fonts["small"].render(text, True, self.colors["text"])
            screen.blit(text_surface, (250, 25 + i * 20))
        
        # Compétences rapides
        if len(self.player.skills) > 0:
            self.draw_quick_skills(screen)
    
    def draw_bar(self, screen, x, y, width, height, ratio, color, label):
        """Dessine une barre de progression"""
        # Fond de la barre
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        
        # Barre de remplissage
        fill_width = max(5, int(width * ratio))
        pygame.draw.rect(screen, color, (x, y, fill_width, height))
        
        # Bordure
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2)
        
        # Texte
        if label:
            text = self.fonts["small"].render(f"{label}: {int(ratio * 100)}%", True, self.colors["text"])
            screen.blit(text, (x + 5, y + 2))
    
    def draw_quick_skills(self, screen):
        """Dessine les compétences rapides"""
        skills = self.player.skills[:4]  # 4 premières compétences
        
        for i, skill in enumerate(skills):
            x = 600 + i * 70
            y = 20
            
            # Fond du bouton de compétence
            color = (100, 100, 100) if skill.name in self.player.skill_cooldowns else (50, 50, 150)
            pygame.draw.rect(screen, color, (x, y, 60, 60))
            pygame.draw.rect(screen, (200, 200, 200), (x, y, 60, 60), 2)
            
            # Icône/texte de la compétence
            text = self.fonts["small"].render(str(i+1), True, (255, 255, 255))
            screen.blit(text, (x + 25, y + 20))
            
            # Nom abrégé
            name_text = self.fonts["small"].render(skill.name[:8], True, (255, 255, 255))
            screen.blit(name_text, (x, y + 40))
            
            # Cooldown
            if skill.name in self.player.skill_cooldowns:
                cooldown = self.player.skill_cooldowns[skill.name]
                if cooldown > 0:
                    # Overlay de cooldown
                    s = pygame.Surface((60, 60), pygame.SRCALPHA)
                    s.fill((0, 0, 0, 150))
                    screen.blit(s, (x, y))
                    
                    # Texte de cooldown
                    cd_text = self.fonts["medium"].render(str(int(cooldown)), True, (255, 0, 0))
                    screen.blit(cd_text, (x + 20, y + 20))
    
    def draw_messages(self, screen):
        """Dessine les messages système"""
        for i, message in enumerate(self.messages):
            alpha = 255 - (pygame.time.get_ticks() - message["time"]) / self.message_timeout * 255
            alpha = max(0, min(255, alpha))
            
            text_surface = self.fonts["small"].render(message["text"], True, message["color"])
            text_surface.set_alpha(alpha)
            
            screen.blit(text_surface, (20, 120 + i * 20))
    
    def draw_combat_ui(self, screen):
        """Dessine l'interface de combat"""
        # Fond semi-transparent
        s = pygame.Surface((800, 200), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        screen.blit(s, (0, 400))
        
        # Actions de combat
        actions = ["1. Attaquer", "2. Compétence", "3. Objet", "4. Fuir"]
        for i, action in enumerate(actions):
            text = self.fonts["medium"].render(action, True, self.colors["text"])
            screen.blit(text, (600, 410 + i * 30))
    
    def draw_combat_messages(self, screen):
        """Dessine les messages de combat"""
        for i, message in enumerate(self.combat_messages):
            text = self.fonts["medium"].render(message["text"], True, message["color"])
            screen.blit(text, (50, 410 + i * 25))
    
    def draw_inventory(self, screen):
        """Dessine l'interface d'inventaire"""
        # Fond semi-transparent
        s = pygame.Surface((600, 400), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (100, 100))
        
        # Titre
        title = self.fonts["large"].render("INVENTAIRE", True, self.colors["highlight"])
        screen.blit(title, (400 - title.get_width() // 2, 110))
        
        # Équipement
        equip_title = self.fonts["medium"].render("ÉQUIPÉ:", True, self.colors["text"])
        screen.blit(equip_title, (120, 140))
        
        y_pos = 170
        for slot, item in self.player.equipment.items():
            item_name = item.name if item else "Aucun"
            text = self.fonts["small"].render(f"{slot}: {item_name}", True, self.colors["text"])
            screen.blit(text, (120, y_pos))
            y_pos += 25
        
        # Inventaire
        inv_title = self.fonts["medium"].render("SAC:", True, self.colors["text"])
        screen.blit(inv_title, (350, 140))
        
        for i, item in enumerate(self.player.inventory[:12]):  # 12 premiers items
            text = self.fonts["small"].render(f"{i+1}. {item.name}", True, self.colors["text"])
            screen.blit(text, (350, 170 + i * 20))
    
    def draw_dialogue(self, screen):
        """Dessine l'interface de dialogue"""
        # Boîte de dialogue
        s = pygame.Surface((700, 150), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (50, 400))
        
        # Texte (simulé)
        text = self.fonts["medium"].render("Dialogue avec le PNJ...", True, self.colors["text"])
        screen.blit(text, (70, 420))
        
        # Indicateur de continuation
        if int(self.animation_time / 500) % 2 == 0:  # Clignotement
            continue_text = self.fonts["small"].render("Appuyez sur ENTREE", True, self.colors["highlight"])
            screen.blit(continue_text, (70, 470))
            
            
    def draw_main_menu(self, screen):
        # Fond
        screen.fill((0, 0, 50))
    
        # Titre
        title = self.fonts["title"].render("YCRAD L'AVENTURIER", True, self.colors["highlight"])
        screen.blit(title, (400 - title.get_width() // 2, 100))
    
        # Options du menu
        self.menu_rects = []
        y = 200
        
        for option in self.menu_options:
            text_surface = self.fonts["large"].render(option, True, (225, 225, 225))
            rect = text_surface.get_rect(center=(400, y))
            screen.blit(text_surface, rect)
            self.menu_rects.append((rect, option))
            
            # Détecter clic ici
            if pygame.mouse.get_pressed()[0]:  # bouton gauche
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.selected_option = option
                    if option == "Nouvelle Partie":
                        self.game.start_new_game()
                    elif option == "Quitter":
                        pygame.quit()
                        sys.exit()
        
            y += 50

    
        # Copyright
        copyright = self.fonts["small"].render("© 2024 Votre Studio - Version Web ui", True, self.colors["text"])
        screen.blit(copyright, (400 - copyright.get_width() // 2, 500))
    
    
    def draw_game_over(self, screen):
        """Dessine l'écran de game over"""
        screen.fill((0, 0, 0))
        
        # Message
        game_over = self.fonts["title"].render("GAME OVER", True, self.colors["warning"])
        screen.blit(game_over, (400 - game_over.get_width() // 2, 200))
        
        # Score
        score_text = self.fonts["large"].render(f"Niveau atteint: {self.player.level}", True, self.colors["text"])
        screen.blit(score_text, (400 - score_text.get_width() // 2, 270))
        
        # Instructions
        restart = self.fonts["medium"].render("Appuyez sur R pour recommencer", True, self.colors["highlight"])
        screen.blit(restart, (400 - restart.get_width() // 2, 330))
    
    # ui.py - Modifications dans la méthode handle_event
def handle_event(self, event, game):
    """Gère les événements de l'interface"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_i and game.game_state == "playing":
            game.game_state = "inventory"
        elif event.key == pygame.K_i and game.game_state == "inventory":
            game.game_state = "playing"
        elif event.key == pygame.K_q:
            self.show_quests = not self.show_quests
        elif event.key == pygame.K_ESCAPE:
            if game.game_state == "inventory":
                game.game_state = "playing"
                
    # elif event.type == pygame.MOUSEBUTTONDOWN:
    #     if self.game.game_state == "menu":  # <-- ONLY handle clicks in menu state
            
    #         pos = pygame.mouse.get_pos()
    #         for rect, option in self.menu_rects:
    #             if rect.collidepoint(pos):
    #                 self.selected_option = option
    #                 print(f"Option sélectionnée: {option}")  # Debug
                    
    #                 # Appeler les méthodes appropriées sur l'instance de jeu
    #                 if option == "Nouvelle Partie":
    #                     game.start_new_game()
    #                 elif option == "Charger":
    #                     game.load_game()
    #                 elif option == "Options":
    #                     game.open_options()
    #                 elif option == "Quitter":
    #                     pygame.quit()
    #                     sys.exit()
    #                 break  # Sortir après avoir trouvé l'option cliquée       
