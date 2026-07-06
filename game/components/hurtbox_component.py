import pygame


class HurtboxComponent:
    def __init__(self,  width, height):
        self.width = width
        self.height = height
        
    def get_rect(self):
        return pygame.Rect(
            self.owner.x - self.width//2,
            # -y for jumping when needed
            self.owner.z - self.owner.y - self.height,
            self.width, self.height)