from game.colors import BLACK_COLOR
from game.managers.asset_manager import AssetManager
from game.settings import SCREEN_WIDTH


class TiledBackground:
    """A background built from 3 small pieces instead of one image spanning
    the whole stage: `begin` and `end` are drawn once at each end, and
    `middle` is repeated to fill the gap between them - so a long stage
    never needs one giant background image in memory. How many times
    `middle` repeats is derived from `total_width`, not hand-counted in
    stage config.

    Exposes the same draw_far_and_mid()/draw_front() interface as
    Background, so Stage/draw.py don't need to know or care which one a
    given stage is using.

    `middle_file`'s art must tile seamlessly against its own copy (its
    right edge continuing into its left edge) - episode_1_stage_2_hallway's
    tiles were cropped at repeating column positions for exactly this.
    """

    def __init__(self, begin_file, middle_file, end_file, total_width, front_file=None):
        self.begin = AssetManager.load_image(begin_file)
        self.middle = AssetManager.load_image(middle_file)
        self.end = AssetManager.load_image(end_file)
        self.front = AssetManager.load_image(front_file, alpha=True) if front_file else None

        gap = total_width - self.begin.get_width() - self.end.get_width()
        self.repeat_count = max(0, round(gap / self.middle.get_width()))

    def draw_far_and_mid(self, screen, camera_x):
        screen.fill(BLACK_COLOR)
        self._draw_tiles(screen, camera_x)

    def draw_front(self, screen, camera_x):
        if self.front:
            screen.blit(self.front, (-camera_x, 0))

    def _draw_tiles(self, screen, camera_x):
        viewport_left = camera_x
        viewport_right = camera_x + SCREEN_WIDTH

        x = self._blit_if_visible(screen, self.begin, 0, camera_x, viewport_left, viewport_right)
        for _ in range(self.repeat_count):
            x = self._blit_if_visible(screen, self.middle, x, camera_x, viewport_left, viewport_right)
        self._blit_if_visible(screen, self.end, x, camera_x, viewport_left, viewport_right)

    def _blit_if_visible(self, screen, image, world_x, camera_x, viewport_left, viewport_right):
        width = image.get_width()
        if world_x + width > viewport_left and world_x < viewport_right:
            screen.blit(image, (world_x - camera_x, 0))
        return world_x + width
