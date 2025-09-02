class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.current_animations = {}
    
    def add_animation(self, name, frames, speed=0.1):
        self.animations[name] = {"frames": frames, "speed": speed}
    
    def play_animation(self, target, animation_name):
        if animation_name in self.animations:
            self.current_animations[target] = {
                "name": animation_name,
                "index": 0,
                "timer": 0
            }
    
    def update(self, dt):
        for target, anim in self.current_animations.items():
            anim["timer"] += dt
            if anim["timer"] >= self.animations[anim["name"]]["speed"]:
                anim["timer"] = 0
                anim["index"] = (anim["index"] + 1) % len(self.animations[anim["name"]]["frames"])
    
    def get_current_frame(self, target):
        if target in self.current_animations:
            anim_name = self.current_animations[target]["name"]
            frame_index = self.current_animations[target]["index"]
            return self.animations[anim_name]["frames"][frame_index]
        return None