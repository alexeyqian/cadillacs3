import pygame
import game.settings as settings

class PlayerRenderer:
    def draw(self, owner, screen, camera_x):
        frame = owner.animation_controller.get_current_frame()
        image = owner.animation_controller.get_image()
        scale = frame.get_scale(owner.sprite_scale)
        image = pygame.transform.scale(
            image,
            (int(image.get_width() * scale), int(image.get_height() * scale))
        )

        if not owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        offset_x, offset_y = frame.offset
        offset_x *= scale
        offset_y *= scale

        if owner.facing_right:
            sprite_world_x = owner.x + offset_x
        else:
            sprite_world_x = owner.x - image.get_width() - offset_x

        visual_y = owner.movement.air.get_visual_y(owner.y) if owner.movement.air else owner.y
        sprite_y = visual_y + offset_y
        screen.blit(image, (sprite_world_x - camera_x, sprite_y))

        if settings.SHOW_COMBAT_BOXES:
            self.draw_debug_boxes(screen, camera_x)