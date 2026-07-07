import pygame
from game.settings import SHOW_COMBAT_BOXES
from game.colors import *
from game.camera import world_to_screen
from game.components.health_component import HealthComponent


class CharacterRenderer:
    HP_BAR_HEIGHT = 12  # gap between the sprite's top edge and the health bar

    def __init__(self, owner, show_health_bar=False):
        self.owner = owner
        self.show_health_bar = show_health_bar

    def get_health_bar_top_z(self):
        """World z whose screen row (at y=0) lines up with the top of this
        character's health bar - see _draw_health_bar, which computes the
        same offset from the sprite's frame. Lets other systems (e.g. a
        floating score popup) anchor to the bar without duplicating the
        sprite-offset math and drifting out of sync with it."""
        owner = self.owner
        frame = owner.animation_manager.get_current_frame()
        offset_y = frame.offset[1] if frame else 0
        return owner.z - owner.y + offset_y - self.HP_BAR_HEIGHT

    def draw(self, screen, camera_x):
        owner = self.owner
        current_frame = owner.animation_manager.get_current_frame()
        if not current_frame:
            raise ValueError(f"Missing frame data for state: {owner.state}")

        image = current_frame.image
        offset_x, offset_y = current_frame.offset

        scale = owner.sprite_scale
        if scale != 1:
            image = pygame.transform.scale(image,
                (int(image.get_width() * scale),
                int(image.get_height() * scale)))

        facing_right = owner.facing >= 0
        if not facing_right:
            image = pygame.transform.flip(image, True, False)

        if facing_right:
            sprite_world_x = owner.x + offset_x
        else:
            sprite_world_x = owner.x - image.get_width() - offset_x

        screen_x, screen_y = world_to_screen(sprite_world_x, owner.y, owner.z, camera_x)
        frame_rect = pygame.Rect(screen_x, screen_y + offset_y, image.get_width(), image.get_height())
        screen.blit(image, frame_rect.topleft)

        if self.show_health_bar:
            self._draw_health_bar(screen, camera_x, frame_rect)
        
        if SHOW_COMBAT_BOXES:
            self._draw_debug_boxes(screen, camera_x)

    def _draw_health_bar(self, screen, camera_x, frame_rect):
        owner = self.owner
        bar_width = 50
        bar_x = int(owner.x - camera_x - bar_width / 2)
        health = owner.get_component(HealthComponent)
        hp_width = int(bar_width * (health.health / health.max_health))

        bar_top = frame_rect.y - self.HP_BAR_HEIGHT
        pygame.draw.rect(screen, (120, 120, 120), (bar_x, bar_top, bar_width, 6))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_top, hp_width, 6))

    def _draw_debug_boxes(self, screen, camera_x, line_width=1):
        collision_rect = self.owner.get_collision_rect()
        hurt_rect = self.owner.get_hurt_rect()
        hit_rect = self.owner.get_hit_rect()
        body_rect = self.owner.get_frame_rect()

        # collision rect
        pygame.draw.rect(screen, BLUE_COLOR, (
            collision_rect.x - camera_x,
            collision_rect.y,
            collision_rect.width,
            collision_rect.height,
        ), line_width)
        pygame.draw.circle(
            screen,
            WHITE_COLOR,
            (int(self.owner.x - camera_x), int(self.owner.y)),
            3,
        )
        # hurt rect
        pygame.draw.rect(screen, GREEN_COLOR, (
            hurt_rect.x - camera_x,
            hurt_rect.y,
            hurt_rect.width,
            hurt_rect.height,
        ), line_width)
        # hit rect
        if hit_rect:
            pygame.draw.rect(screen, RED_COLOR, (
                hit_rect.x - camera_x,
                hit_rect.y,
                hit_rect.width,
                hit_rect.height,
            ), line_width)
        # frame rect
        pygame.draw.rect(screen, WHITE_COLOR, (
            body_rect.x - camera_x,
            body_rect.y,
            body_rect.width,
            body_rect.height,
        ), line_width)

