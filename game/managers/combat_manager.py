from game.components.health_component import HealthComponent
from game.components.hitbox_component import HitboxComponent
from game.components.hurtbox_component import HurtboxComponent


class CombatManager:
    """Resolves collisions between active hitboxes and hurtboxes each frame."""

    def __init__(self, stage=None):
        self.stage = stage

    def resolve(self, characters):
        for attacker in characters:
            if not attacker.alive:
                continue
            hitbox = attacker.get_component(HitboxComponent)
            if not hitbox or not hitbox.active:
                continue

            for target in characters:
                if target is attacker or not target.alive:
                    continue
                if target in hitbox.hits:
                    continue
                health = target.get_component(HealthComponent)
                hurtbox = target.get_component(HurtboxComponent)
                if not health or not hurtbox:
                    continue

                if hitbox.get_rect().colliderect(hurtbox.get_rect()):
                    health.take_damage(hitbox.damage, hitbox.knockback)
                    hitbox.hits.add(target)
                    self._react_to_hit(attacker, target)

    def _react_to_hit(self, attacker, target):
        if not target.alive:
            target.cancel_attack()
            target.set_state("dead")
            self._award_score(attacker, target)
        else:
            target.stun(attacker.current_attack.hit_stun_duration)

    def _award_score(self, attacker, target):
        points = getattr(target, "score_points", 0)
        if not points or not hasattr(attacker, "score"):
            return

        attacker.score += points
        if self.stage.floating_text_manager:
            spawn_z = target.renderer.get_health_bar_top_z()
            self.stage.floating_text_manager.spawn(f"+{points}", target.x, spawn_z)
