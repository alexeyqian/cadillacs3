class GameObject:
    def __init__(self, x: float, z: float):
        self.name = "unknown"
        self.x = x # left/right
        self.z = z # depth (up/down)
        self.y = 0.0 # jump height
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.facing = 1

        self.tags = set()
        self.active = True
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
