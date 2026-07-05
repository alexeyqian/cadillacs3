class GameObject:
    """Anything placed in the world: just a position and a name/tag identity.
    No components, no per-frame behavior - see Entity for both."""
    def __init__(self, x: float, z: float):
        self.name = "unknown"
        self.x = x # left/right
        self.z = z # depth (up/down)
        self.y = 0.0 # jump height

        self.tags = set()
        self.active = True
