from game.components.health_component import HealthComponent
from game.components.hitbox_component import HitboxComponent
from game.components.hurtbox_component import HurtboxComponent

HIT_STUN_DURATION = 0.4  # seconds; matches HealthComponent's invulnerability window


class CombatManager:
    """Resolves collisions between active hitboxes and hurtboxes each frame."""

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
                    self._react_to_hit(target)

    def _react_to_hit(self, target):
        if not target.alive:
            target.set_state("dead")
        else:
            target.stun(HIT_STUN_DURATION)
