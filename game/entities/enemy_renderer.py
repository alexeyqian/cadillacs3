import pygame
import game.settings as settings
from game.colors import WHITE_COLOR, YELLOW_COLOR
from game.camera import world_to_screen
from game.components.health_component import HealthComponent
#from game.components.debug_renderer import CharacterDebugRenderer

class EnemyRenderer:
    def draw(self, owner, screen, camera_x):
        current_frame = owner.animation_manager.get_current_frame()
        if not current_frame:
            raise ValueError(f"Missing frame data for enemy state: {owner.state}")

        image = current_frame.image
        offset_x, offset_y = current_frame.offset
        scale = (
            current_frame.get_scale(owner.sprite_scale)
            if hasattr(current_frame, "get_scale")
            else owner.sprite_scale
        )
        image = pygame.transform.scale(image,
            (int(image.get_width() * scale),
            int(image.get_height() * scale)))
        if not owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        if owner.facing_right:
            sprite_world_x = owner.x + offset_x
        else:
            sprite_world_x = owner.x - image.get_width() - offset_x

        screen_x, screen_y = world_to_screen(sprite_world_x, owner.y, owner.z, camera_x)
        frame_rect = pygame.Rect(screen_x, screen_y + offset_y, image.get_width(), image.get_height())
        screen.blit(image, frame_rect.topleft)
        self.draw_health_bar(owner, screen, camera_x, frame_rect)

    def draw_health_bar(self, owner, screen, camera_x, frame_rect):
        bar_width = 50
        bar_x = int(owner.x - camera_x - bar_width / 2)
        health = owner.get_component(HealthComponent)
        hp_width = int(bar_width * (health.health / health.max_health))
        hp_height = 12

        pygame.draw.rect(screen,(120, 120, 120),
            (bar_x, frame_rect.y - hp_height, bar_width, 6)
        )
        pygame.draw.rect(screen,(255, 0, 0),
            (bar_x, frame_rect.y - hp_height, hp_width, 6))
