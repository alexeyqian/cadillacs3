import pygame
import game.settings as settings

class PlayerRenderer:
    def __init__(self, owner):
        self.owner = owner

    def draw(self, screen, camera_x):
        current_frame = self.owner.animation_manager.get_current_frame()
        image = current_frame.image
        offset_x, offset_y = current_frame.offset

        if not self.owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        player_x = self.owner.x
        player_y = self.owner.y

        if self.owner.facing_right:
            sprite_world_x = player_x + offset_x
        else:
            sprite_world_x = player_x - image.get_width() - offset_x

        #visual_y = self.owner.movement.air.get_visual_y(owner.y) if owner.movement.air else owner.y
        visual_y = player_y
        sprite_y = visual_y + offset_y
        screen.blit(image, (sprite_world_x - camera_x, sprite_y))

        if settings.SHOW_COMBAT_BOXES:
            self.draw_debug_boxes(screen, camera_x)