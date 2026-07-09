import math

from game.managers.asset_manager import AssetManager
from game.settings import SCREEN_WIDTH


class BackgroundLayer:
    """One parallax layer of a stage's background - either a single static
    image, or (for a layer too wide to keep as one image) a tiled set:
    "middle" repeats to fill the layer's width, optionally bracketed by a
    one-off "begin"/"end" for layers with a unique landmark at either end
    (see episode_1_stage_2_hallway's tiles). Plain repeating layers (no
    unique bookends - e.g. a tileable sky or floor texture) can omit
    begin/end entirely. How many times middle repeats is derived from the
    layer's required width, not hand-counted in config.

    scroll_factor controls how fast this layer moves relative to the
    camera: < 1.0 sits farther away and scrolls slower than gameplay,
    1.0 matches gameplay exactly (this is what every layer did before
    parallax existed), > 1.0 sits closer than gameplay and scrolls faster
    (e.g. foreground decoration passing in front of the player).

    y_offset positions the layer vertically (screen pixels from the top) -
    lets a layer be cropped tight to just the band of the scene it covers
    (sky, skyline, floor, ...) instead of needing a full-screen-height
    image with transparent padding around its content.
    """

    def __init__(self, scroll_factor, image=None, tiles=None, required_width=None, y_offset=0):
        self.scroll_factor = scroll_factor
        self.y_offset = y_offset
        self.tiled = tiles is not None
        if self.tiled:
            self.begin = AssetManager.load_image(tiles["begin"], alpha=True) if tiles.get("begin") else None
            self.middle = AssetManager.load_image(tiles["middle"], alpha=True)
            self.end = AssetManager.load_image(tiles["end"], alpha=True) if tiles.get("end") else None
            begin_width = self.begin.get_width() if self.begin else 0
            end_width = self.end.get_width() if self.end else 0
            gap = required_width - begin_width - end_width
            # ceil, not round: undercovering (e.g. round(6.5) -> 6) would
            # leave a black gap at the visible edge for part of the stage.
            self.repeat_count = max(0, math.ceil(gap / self.middle.get_width()))
        else:
            self.image = AssetManager.load_image(image, alpha=True)

    def draw(self, screen, camera_x):
        layer_camera_x = camera_x * self.scroll_factor
        if self.tiled:
            self._draw_tiled(screen, layer_camera_x)
        else:
            screen.blit(self.image, (int(-layer_camera_x), self.y_offset))

    def _draw_tiled(self, screen, camera_x):
        viewport_left = camera_x
        viewport_right = camera_x + SCREEN_WIDTH

        x = 0
        if self.begin:
            x = self._blit_if_visible(screen, self.begin, x, camera_x, viewport_left, viewport_right)
        for _ in range(self.repeat_count):
            x = self._blit_if_visible(screen, self.middle, x, camera_x, viewport_left, viewport_right)
        if self.end:
            self._blit_if_visible(screen, self.end, x, camera_x, viewport_left, viewport_right)

    def _blit_if_visible(self, screen, image, world_x, camera_x, viewport_left, viewport_right):
        width = image.get_width()
        if world_x + width > viewport_left and world_x < viewport_right:
            screen.blit(image, (int(world_x - camera_x), self.y_offset))
        return world_x + width
