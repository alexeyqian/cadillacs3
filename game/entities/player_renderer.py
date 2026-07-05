import pygame
import game.settings as settings
from game.camera import world_to_screen

class PlayerRenderer:
    def __init__(self, owner):
        self.owner = owner

    def draw(self, screen, camera_x):
        current_frame = self.owner.animation_manager.get_current_frame()
        image = current_frame.image
        offset_x, offset_y = current_frame.offset

        if not self.owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        if self.owner.facing_right:
            sprite_world_x = self.owner.x + offset_x
        else:
            sprite_world_x = self.owner.x - image.get_width() - offset_x

        screen_x, screen_y = world_to_screen(sprite_world_x, self.owner.y, self.owner.z, camera_x)
        screen.blit(image, (screen_x, screen_y + offset_y))

        #if settings.SHOW_COMBAT_BOXES:
        #    self.draw_debug_boxes(screen, camera_x)