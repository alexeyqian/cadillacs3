import pygame
from game.camera import world_to_screen
from game.components.health_component import HealthComponent


class CharacterRenderer:
    def __init__(self, owner, show_health_bar=False):
        self.owner = owner
        self.show_health_bar = show_health_bar

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

    def _draw_health_bar(self, screen, camera_x, frame_rect):
        owner = self.owner
        bar_width = 50
        bar_x = int(owner.x - camera_x - bar_width / 2)
        health = owner.get_component(HealthComponent)
        hp_width = int(bar_width * (health.health / health.max_health))
        hp_height = 12

        pygame.draw.rect(screen, (120, 120, 120), (bar_x, frame_rect.y - hp_height, bar_width, 6))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, frame_rect.y - hp_height, hp_width, 6))
