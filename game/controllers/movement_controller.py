from engine.timer_manager import TimerManager
from game.components.stats_component import StatsComponent
from game.components.status_effect_component import StatusEffectComponent
from game.entities.attack_data import AttackPhase
from game.controllers.character_controller import CharacterController
from game.controllers.attack_controller import AttackController


class MovementController:
    """
    Active component: Handles input/AI translation to physics velocity.
    """
    def __init__(self, move_speed=250, jump_power=600):
        self.move_speed = move_speed
        self.jump_power = jump_power
        self.is_jumping = False

    def move(self, dx, dz):
        char_ctrl = self.owner.get_component(CharacterController)
        if not char_ctrl.can_act: return

        status_ctrl = self.owner.get_component(StatusEffectComponent)
        if status_ctrl and status_ctrl.has_effect("stun"): return
        
        stats = self.owner.get_component(StatsComponent)
        speed = self.move_speed * (stats.move_speed_mult if stats else 1.0)
        # dx: is -1, 0 or 1
        # vx: speed and direction the character travels per frame or per second
        self.owner.vx = dx * speed
        self.owner.vz = dz * speed
        if dx != 0: self.owner.facing = 1 if dx > 0 else -1

    def jump(self):
        if self.owner.y == 0:
            self.owner.vy = self.jump_power
            self.is_jumping = True

    def update(self, dt):
        # Apply gravity for jumping
        if self.owner.y > 0 or self.owner.vy > 0:
            # constantly slowing down the character's upward speed.
            self.owner.vy -= 1500 * dt
            self.owner.y += self.owner.vy * dt
            if self.owner.y <= 0:
                self.owner.y = 0
                self.owner.vy = 0
                self.is_jumping = False
        
        # Apply X/Z movement for working
        self.owner.x += self.owner.vx * dt
        self.owner.z += self.owner.vz * dt
        
        # Friction
        if not self.is_jumping:
            self.owner.vx *= 0.8
            self.owner.vz *= 0.8
    
    def is_locked(self):
        attack_ctrl = self.owner.get_component(AttackController)
        return attack_ctrl and attack_ctrl.phase != AttackPhase.FINISHED