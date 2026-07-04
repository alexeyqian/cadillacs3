import pygame
from game.components.health_component import HealthComponent
from game.components.hitbox_component import HitboxComponent
from game.components.hurtbox_component import HurtboxComponent

class CombatManager:
    """Resolves collisions between active hitboxes and health components"""
    def __init__(self):
        self.entities = []
    
    def register(self, entity):
        self.entities.append(entity)
    
    def resolve_hits(self):
        for attacker in self.entities:
            if not attacker.alive: continue
            hitbox = attacker.get_component(HitboxComponent)
            if not hitbox or not hitbox.active: continue
            
            for target in self.entities:
                if target == attacker or not target.alive: continue
                if target in hitbox.hits: continue
                health = target.get_component(HealthComponent)
                if not health: continue
                hurtbox = target.get_component(HurtboxComponent)
                if not hurtbox: continue
                
                #AABB colision check
                hitbox_rect = hitbox.get_rect()
                # todo: get target hurtbox
                hurtbox_rect = hurtbox.get_rect()
                if hitbox_rect.colliderect(hurtbox_rect):
                    health.take_damage(hitbox.damage, hitbox.knockback)
                    hitbox.hits.add(target) # prevent multi-hit
                