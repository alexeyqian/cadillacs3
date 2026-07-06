import pygame


class CollisionBoxComponent:
    def __init__(self,  width, height):
        self.width = width
        self.height = height
        
    def get_rect(self):
        return pygame.Rect(
            self.owner.x - self.width//2, 
            self.owner.z - self.height, 
            self.width, self.height)