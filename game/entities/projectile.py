from engine.timer_manager import TimerManager
from game.settings import WORLD_WIDTH
from game.colors import YELLOW_COLOR
from game.components.health_component import HealthComponent
from game.components.hitbox_component import HitboxComponent
from game.entities.entity import Entity


class Projectile(Entity):
    """Inherits directly from Entity, not Character."""
    def __init__(self, x: float, z: float, vx: float, vz: float, damage: float):
        super().__init__(x, z)
        self.vx, self.vz = vx, vz
        self.width, self.height = 20, 20
        self.tags.add("projectile")
        # Projectiles have simple health/hitbox logic to deal damage on collision
        self.add_component(HealthComponent(1)) # Dies in 1 hit
        self.add_component(HitboxComponent())  # Acts as a moving hitbox
        hitbox = self.get_component(HitboxComponent)
        hitbox.activate(damage, (100, 0), 20, 20)
        
    def update(self, dt):
        super().update(dt)
        self.x += self.vx * dt
        self.z += self.vz * dt
        # Simple lifetime
        TimerManager.start_timer(2.0, lambda: setattr(self, 'alive', False))