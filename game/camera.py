from game.settings import SCREEN_WIDTH


def world_to_screen(x, y, z, camera_x):
    # world y (jump height) subtracts from world z (depth/lane position)
    # because both collapse onto pygame's single vertical pixel axis.
    # So z - y isn't an arithmetic curiosity — it's "start at the depth row, 
    # then lift up by however much you've jumped."
    screen_x = x - camera_x
    screen_y = z - y
    return screen_x, screen_y


class Camera:
    def __init__(self):
        self.x = 0
        self.locked = False
        self.locked_x = 0

    def update(self, player, world_width=None):
        if self.locked:
            self.x = self.locked_x
            return

        # follow player
        self.x = max(0, player.x - SCREEN_WIDTH // 2)
        if world_width is not None:
            # Don't scroll past the right edge of the stage. (Only x is
            # clamped - the camera has no vertical/z scroll to bound; the
            # lane_top/lane_bottom depth range is fixed within the screen
            # height and is enforced on the player directly, not the camera.)
            self.x = min(self.x, max(0, world_width - SCREEN_WIDTH))