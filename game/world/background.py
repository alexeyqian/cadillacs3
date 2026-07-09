from game.colors import BLACK_COLOR
from game.settings import SCREEN_WIDTH
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

    def __init__(self, layer_configs, world_width):
        self.layers = {}
        max_camera_x = max(0, world_width - SCREEN_WIDTH)
        for name in LAYER_NAMES:
            config = layer_configs.get(name)
            if not config:
                continue
            scroll_factor = config.get("scroll_factor", DEFAULT_SCROLL_FACTORS[name])
            # A layer scrolling slower/faster than gameplay needs a
            # correspondingly smaller/larger image to still cover the full
            # camera range - a plain world_width would over-tile a slow
            # layer and leave gaps in a fast one.
            required_width = max_camera_x * scroll_factor + SCREEN_WIDTH
            self.layers[name] = BackgroundLayer(
                scroll_factor,
                image=config.get("image"),
                tiles=config.get("tiles"),
                required_width=required_width,
                y_offset=config.get("y_offset", 0),
            )

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
