import pygame


class HitboxComponent:
    def __init__(self):
        self.offset_x = 0
        self.offset_z = 0
        self.width = 50
        self.height = 50
        self.damage = 0
        self.knockback = (0, 0)
        self.active = False

        self.hits = set()
    
    def activate(self, damage, knockback, offset_x, offset_z, width, height):
        self.offset_x = offset_x
        self.offset_z = offset_z
        self.width = width
        self.height = height

        self.damage = damage
        self.knockback = knockback
        self.active = True

        self.hits.clear()

    def deactivate(self):
        self.active = False
    
    def get_rect(self):
        x = self.owner.x + (self.offset_x if self.owner.facing == 1 else -self.offset_x - self.width)
        y = self.owner.z + self.offset_z
        return pygame.Rect(x, y, self.width, self.height)

    def update(self, dt):
        pass # Logic is driven by Character.update_attack
