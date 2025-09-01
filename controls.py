# controls.py - Système de contrôle pour clavier et tactile
import pygame

class ControlSystem:
    def __init__(self):
        # États de contrôle
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.interact = False
        self.attack = False
        self.inventory = False
        self.pause = False
        
        # Contrôles tactiles
        self.touch_controls = []
        self.virtual_joystick = (0, 0)
        self.create_touch_controls()
        
        # Configuration des touches
        self.key_bindings = {
            "move_up": [pygame.K_UP, pygame.K_w, pygame.K_z],
            "move_down": [pygame.K_DOWN, pygame.K_s],
            "move_left": [pygame.K_LEFT, pygame.K_a, pygame.K_q],
            "move_right": [pygame.K_RIGHT, pygame.K_d],
            "interact": [pygame.K_e],
            "attack": [pygame.K_SPACE],
            "inventory": [pygame.K_i],
            "pause": [pygame.K_ESCAPE]
        }
    
    def create_touch_controls(self):
        """Crée les contrôles tactiles virtuels"""
        # Joystick virtuel pour le mouvement
        self.touch_controls.append({
            "type": "joystick",
            "rect": pygame.Rect(50, 450, 120, 120),
            "active": False,
            "center": (110, 510),
            "max_distance": 40
        })
        
        # Boutons d'action
        actions = [
            {"action": "interact", "rect": pygame.Rect(700, 450, 80, 80), "icon": "E"},
            {"action": "attack", "rect": pygame.Rect(600, 450, 80, 80), "icon": "⚔️"},
            {"action": "inventory", "rect": pygame.Rect(500, 450, 80, 80), "icon": "🎒"}
        ]
        
        for action_info in actions:
            self.touch_controls.append({
                "type": "button",
                "action": action_info["action"],
                "rect": action_info["rect"],
                "icon": action_info["icon"],
                "pressed": False
            })
    
    def handle_event(self, event):
        """Gère les événements d'entrée"""
        # Réinitialiser les états temporaires
        self.interact = False
        self.attack = False
        self.inventory = False
        self.pause = False
        
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.KEYUP:
            self.handle_keyup(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button(event.pos, True)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button(event.pos, False)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event.pos)
    
    def handle_keydown(self, event):
        """Gère les appuis de touches"""
        if event.key in self.key_bindings["move_up"]:
            self.move_up = True
        elif event.key in self.key_bindings["move_down"]:
            self.move_down = True
        elif event.key in self.key_bindings["move_left"]:
            self.move_left = True
        elif event.key in self.key_bindings["move_right"]:
            self.move_right = True
        elif event.key in self.key_bindings["interact"]:
            self.interact = True
        elif event.key in self.key_bindings["attack"]:
            self.attack = True
        elif event.key in self.key_bindings["inventory"]:
            self.inventory = True
        elif event.key in self.key_bindings["pause"]:
            self.pause = True
    
    def handle_keyup(self, event):
        """Gère les relâchements de touches"""
        if event.key in self.key_bindings["move_up"]:
            self.move_up = False
        elif event.key in self.key_bindings["move_down"]:
            self.move_down = False
        elif event.key in self.key_bindings["move_left"]:
            self.move_left = False
        elif event.key in self.key_bindings["move_right"]:
            self.move_right = False
    
    def handle_mouse_button(self, pos, pressed):
        """Gère les clics souris/tactiles"""
        for control in self.touch_controls:
            if control["rect"].collidepoint(pos):
                if control["type"] == "joystick" and pressed:
                    control["active"] = True
                    self.update_joystick_position(pos, control)
                elif control["type"] == "button" and pressed:
                    setattr(self, control["action"], True)
                    control["pressed"] = True
                elif control["type"] == "joystick" and not pressed:
                    control["active"] = False
                    self.virtual_joystick = (0, 0)
    
    def handle_mouse_motion(self, pos):
        """Gère le mouvement de souris/glissement tactile"""
        for control in self.touch_controls:
            if control["type"] == "joystick" and control["active"]:
                self.update_joystick_position(pos, control)
    
    def update_joystick_position(self, pos, joystick):
        """Met à jour la position du joystick virtuel"""
        center_x, center_y = joystick["center"]
        dx = pos[0] - center_x
        dy = pos[1] - center_y
        
        # Limiter la distance
        distance = (dx**2 + dy**2)**0.5
        if distance > joystick["max_distance"]:
            dx = dx / distance * joystick["max_distance"]
            dy = dy / distance * joystick["max_distance"]
        
        # Normaliser et stocker
        norm_dx = dx / joystick["max_distance"]
        norm_dy = dy / joystick["max_distance"]
        
        self.virtual_joystick = (norm_dx, norm_dy)
        
        # Convertir en directions booléennes
        self.move_left = norm_dx < -0.3
        self.move_right = norm_dx > 0.3
        self.move_up = norm_dy < -0.3
        self.move_down = norm_dy > 0.3
    
    def get_movement_vector(self):
        """Retourne le vecteur de mouvement normalisé"""
        dx, dy = 0, 0
        
        # Contrôles clavier
        if self.move_up: dy -= 1
        if self.move_down: dy += 1
        if self.move_left: dx -= 1
        if self.move_right: dx += 1
        
        # Contrôles virtuels (prioritaires)
        joy_dx, joy_dy = self.virtual_joystick
        if abs(joy_dx) > 0.1 or abs(joy_dy) > 0.1:
            dx, dy = joy_dx, joy_dy
        
        # Normaliser pour les déplacements diagonaux
        if dx != 0 and dy != 0:
            magnitude = (dx**2 + dy**2)**0.5
            dx /= magnitude
            dy /= magnitude
        
        return dx, dy
    
    def draw_touch_controls(self, screen):
        """Dessine les contrôles tactiles à l'écran"""
        for control in self.touch_controls:
            if control["type"] == "joystick":
                self.draw_joystick(screen, control)
            elif control["type"] == "button":
                self.draw_button(screen, control)
    
    def draw_joystick(self, screen, joystick):
        """Dessine un joystick virtuel"""
        # Zone de fond
        s = pygame.Surface((joystick["rect"].width, joystick["rect"].height), pygame.SRCALPHA)
        pygame.draw.circle(s, (100, 100, 100, 100), 
                          (joystick["rect"].width//2, joystick["rect"].height//2),
                          joystick["rect"].width//2)
        screen.blit(s, joystick["rect"])
        
        # Stick
        joy_x, joy_y = self.virtual_joystick
        stick_pos = (
            joystick["center"][0] + joy_x * joystick["max_distance"],
            joystick["center"][1] + joy_y * joystick["max_distance"]
        )
        pygame.draw.circle(screen, (200, 200, 200, 200), stick_pos, 20)
    
    def draw_button(self, screen, button):
        """Dessine un bouton tactile"""
        # Fond
        color = (100, 100, 100, 150) if not button["pressed"] else (150, 150, 150, 200)
        s = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
        pygame.draw.circle(s, color, 
                          (button["rect"].width//2, button["rect"].height//2),
                          button["rect"].width//2)
        screen.blit(s, button["rect"])
        
        # Icône
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(button["icon"], True, (255, 255, 255))
        text_rect = text.get_rect(center=button["rect"].center)
        screen.blit(text, text_rect)
    
    def update(self):
        """Met à jour l'état des contrôles"""
        # Réinitialiser l'état pressé des boutons
        for control in self.touch_controls:
            if control["type"] == "button":
                control["pressed"] = False