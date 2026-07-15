from game.colors import BLACK_COLOR
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, NO_IMAGES_FOR_STAGE
from game.world.background_layer import BackgroundLayer

# Layers are listed back-to-front - this is both the draw order for
# draw_background() and the set of names a stage's "background" config can
# use. "ground" is the surface characters actually walk on (what every
# stage had before parallax existed); the rest are optional dressing.
LAYER_NAMES = ("far", "far_mid", "near", "ground", "front")

# Relative scroll speed used when a stage doesn't set its own
# scroll_factor for a layer - farther-away layers move slower than the
# camera, foreground moves faster. "ground" always defaults to 1.0 (it
# has to track gameplay exactly, since characters stand on it).
DEFAULT_SCROLL_FACTORS = {
    "far": 0.2,
    "far_mid": 0.4,
    "near": 0.7,
    "ground": 1.0,
    "front": 1.2,
}


class Background:
    """A stage's background: up to 5 parallax layers (far, far_mid, near,
    ground, front - see LAYER_NAMES/BackgroundLayer). A stage only
    configures the layers it has art for; the rest are simply skipped.

    Expected stage config shape:
        "background": {
            "far":  {"image": "...", "y_offset": 0},                 # optional
            "ground": {"image": "..."},                # or {"tiles": {...}}
            "front": {"image": "...", "scroll_factor": 1.3},  # optional
        }
    """

    def __init__(self, layer_configs, world_width, lane_top=None, lane_bottom=None):
        self.layers = {}
        max_camera_x = max(0, world_width - SCREEN_WIDTH)

        # NO_IMAGES_FOR_STAGE needs no per-stage config at all - draws all 5
        # layers with default scroll factors, so a stage can test parallax/
        # lanes with "background": {} and no art. Otherwise, only the
        # layers a stage actually configures are built.
        if NO_IMAGES_FOR_STAGE:
            layer_names = list(LAYER_NAMES)
        else:
            layer_names = [name for name in LAYER_NAMES if layer_configs.get(name)]

        band_bounds = (
            self._compute_debug_bands(layer_names, lane_top, lane_bottom)
            if NO_IMAGES_FOR_STAGE else {}
        )

        for name in layer_names:
            config = layer_configs.get(name) or {}
            scroll_factor = config.get("scroll_factor", DEFAULT_SCROLL_FACTORS[name])
            # A layer scrolling slower/faster than gameplay needs a
            # correspondingly smaller/larger image to still cover the full
            # camera range - a plain world_width would over-tile a slow
            # layer and leave gaps in a fast one.
            required_width = max_camera_x * scroll_factor + SCREEN_WIDTH
            if NO_IMAGES_FOR_STAGE:
                y_offset, band_height = band_bounds[name]
            else:
                y_offset, band_height = config.get("y_offset", 0), None
            self.layers[name] = BackgroundLayer(
                scroll_factor,
                image=config.get("image"),
                tiles=config.get("tiles"),
                required_width=required_width,
                y_offset=y_offset,
                layer_name=name,
                band_height=band_height,
            )

    @staticmethod
    def _compute_debug_bands(layer_names, lane_top, lane_bottom):
        """"ground" is sized to exactly the stage's walkable lane range
        (not an arbitrary slice), so the lane overlay (see draw.py) lines
        up with it. Layers before "ground" (far/far_mid/near) evenly split
        the space above lane_top - near ends exactly where ground begins;
        layers after it (front) evenly split the space below lane_bottom -
        ground ends exactly where front begins."""
        top = lane_top if lane_top is not None else int(SCREEN_HEIGHT * 0.4)
        bottom = lane_bottom if lane_bottom is not None else int(SCREEN_HEIGHT * 0.75)

        ground_index = layer_names.index("ground") if "ground" in layer_names else len(layer_names)
        before = layer_names[:ground_index]
        after = layer_names[ground_index + 1:]

        bounds = {}
        before_height = top // len(before) if before else 0
        for i, name in enumerate(before):
            bounds[name] = (i * before_height, before_height)
        if "ground" in layer_names:
            bounds["ground"] = (top, bottom - top)
        after_height = (SCREEN_HEIGHT - bottom) // len(after) if after else 0
        for i, name in enumerate(after):
            bounds[name] = (bottom + i * after_height, after_height)
        return bounds

    def draw_background(self, screen, camera_x):
        """far/far_mid/near/ground, in back-to-front order - everything
        that sits behind the characters."""
        screen.fill(BLACK_COLOR)
        for name in ("far", "far_mid", "near", "ground"):
            layer = self.layers.get(name)
            if layer:
                layer.draw(screen, camera_x)

    def draw_front(self, screen, camera_x):
        """Foreground decoration - drawn after characters, so it can pass
        in front of them."""
        front = self.layers.get("front")
        if front:
            front.draw(screen, camera_x)
