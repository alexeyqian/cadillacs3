import pygame


class HurtboxComponent:
    def __init__(self):
        # In a real game, this might be a list of rects (head, body, legs)
        self.width = 40
        self.height = 80
        
    def get_rect(self):
        return pygame.Rect(
            self.owner.x - self.width//2, 
            self.owner.z - self.height, 
            self.width, self.height)