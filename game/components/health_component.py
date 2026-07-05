from engine.event_bus import EventBus
from engine.timer_manager import TimerManager
from game.components.stats_component import StatsComponent


class HealthComponent:
    def __init__(self, max_health: float):
        self.max_health = max_health
        self.health = max_health
        self.invuln_timer = None

    def take_damage(self, amount, knockback):
        if self.invuln_timer and self.invuln_timer.is_active:
            return

        stats = self.owner.get_component(StatsComponent)
        actual_damage = max(1, amount - (stats.base_defense if stats else 0))
        self.health -= actual_damage
        EventBus.publish("health_changed", self.owner, self.health, self.max_health)
        EventBus.publish("hit_landed", self.owner, actual_damage, knockback)

        # Apply knockback to owner's physics
        self.owner.vx = knockback[0]
        self.owner.vz = knockback[1]
        self.invuln_timer = TimerManager.start_timer(0.4, lambda: None)
        
        if self.health <= 0:
            self.owner.alive = False
            EventBus.publish("entity_died", self.owner)