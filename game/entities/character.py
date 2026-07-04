import pygame
from game.colors import *
from game.entities.game_object import GameObject
from game.components.stats_component import StatsComponent
from game.components.health_component import HealthComponent
from game.components.hurtbox_component import HurtboxComponent
from game.components.status_effect_component import StatusEffectComponent
from game.controllers.character_controller import CharacterController

class Character(GameObject):
    def __init__(self, x, z):
        super().__init__(x, z)
        self.width, self.height = 40, 80
        self.alive = True
        self.add_component(StatsComponent())
        self.add_component(HealthComponent(100))
        self.add_component(HurtboxComponent())
        self.add_component(StatusEffectComponent())
        self.add_component(CharacterController()) # The Master State Machine

    def update(self):
        pass

    def draw(self, screen, camera_x):
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

