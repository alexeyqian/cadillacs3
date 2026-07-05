import pygame


class HitboxComponent:
    def __init__(self):
        self.active = False
        self.damage = 0
        self.knockback = (0, 0)

        self.width = 50
        self.height = 50
        self.hits = set()
    
    def activate(self, damage, knockback, width, height):
        self.active = True
        self.damage = damage
        self.knockback = knockback
        self.width = width
        self.height = height
        self.hits.clear()
    
    def deactivate(self):
        self.active = False
    
    def get_rect(self):
        x = self.owner.x + (30 if self.owner.facing == 1 else -30 - self.width)
        y = self.owner.z - self.height // 2
        return pygame.Rect(x, y, self.width, self.height)

    def update(self, dt):
        pass # Logic is driven by Character.update_attack
