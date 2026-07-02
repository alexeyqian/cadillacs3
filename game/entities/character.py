import pygame
from game.colors import *
class Character:
    def __init__(self):
        self.name = "unknown"

        self.hp = 100
        self.speed = 5
        self.attack_power = 10
        
        self.x = 0
        self.y = 0
        self.facing_right = True
        self.state = None

        self.sprite_scale = 1.0

    def update(self):
        pass

    def draw(self, screen, camera_x):
        pass

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        pass

    def attack(self, target):
        pass
    
    def get_frame_rect(self):
        pass
    
    def get_collision_rect(self):
        pass
    
    def get_hurt_rect(self):
        pass
    
    def get_hit_rect(self):
        pass
    
    def draw_debug_boxes(self, screen, camera_x, line_width=1):
        body_rect = self.get_frame_rect()
        collision_rect = self.get_collision_rect()
        hurt_rect = self.get_hurt_rect()
        attack_rect = self.get_attack_rect()

        pygame.draw.rect(screen, WHITE_COLOR, (
            body_rect.x - camera_x,
            body_rect.y,
            body_rect.width,
            body_rect.height,
        ), line_width)

        pygame.draw.rect(screen, BLUE_COLOR, (
            collision_rect.x - camera_x,
            collision_rect.y,
            collision_rect.width,
            collision_rect.height,
        ), line_width)
        pygame.draw.circle(
            screen,
            WHITE_COLOR,
            (int(self.x - camera_x), int(self.y)),
            3,
        )
        
        pygame.draw.rect(screen, GREEN_COLOR, (
            hurt_rect.x - camera_x,
            hurt_rect.y,
            hurt_rect.width,
            hurt_rect.height,
        ), line_width)

        if attack_rect:
            pygame.draw.rect(screen, RED_COLOR, (
                attack_rect.x - camera_x,
                attack_rect.y,
                attack_rect.width,
                attack_rect.height,
            ), line_width)

