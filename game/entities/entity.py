from game.entities.game_object import GameObject


class Entity(GameObject):
    """A GameObject that takes part in the per-frame update/draw loop
    (players, enemies, projectiles, breakables - not scenery/camera)."""
    def __init__(self, x, z):
        super().__init__(x, z)
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.facing = 1
        self.components = []

    def add_component(self, comp):
        comp.owner = self
        self.components.append(comp)
        return comp

    def get_component(self, comp_type):
        for c in self.components:
            if isinstance(c, comp_type):
                return c
        return None

    def update(self, dt):
        for c in self.components:
            c.update(dt)

    def draw(self, screen, camera_x):
        pass
