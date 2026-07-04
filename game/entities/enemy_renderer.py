import pygame
import game.settings as settings
from game.colors import WHITE_COLOR, YELLOW_COLOR
#from game.components.debug_renderer import CharacterDebugRenderer

class EnemyRenderer:
    def draw(self, owner, screen, camera_x):
        frame = owner.animation_controller.get_current_frame()
        if not frame:
            raise ValueError(f"Missing frame data for enemy state: {owner.state}")

        image = owner.animation_controller.get_image()
        scale = (
            frame.get_scale(owner.sprite_scale)
            if hasattr(frame, "get_scale")
            else owner.sprite_scale
        )
        image = pygame.transform.scale(image,
            (int(image.get_width() * scale),
            int(image.get_height() * scale)))
        if not owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        frame_rect = owner.get_frame_rect()
        screen.blit(image, (frame_rect.x - camera_x, frame_rect.y))
        self.draw_health_bar(owner, screen, camera_x, frame_rect)

    def draw_health_bar(self, owner, screen, camera_x, frame_rect):
        bar_width = 50
        bar_x = int(owner.x - camera_x - bar_width / 2)
        hp_width = int(bar_width * (owner.health.hp / owner.health.max_hp))
        hp_height = 12

        pygame.draw.rect(screen,(120, 120, 120),
            (bar_x, frame_rect.y - hp_height, bar_width, 6)
        )
        pygame.draw.rect(screen,(255, 0, 0),
            (bar_x, frame_rect.y - hp_height, hp_width, 6))
