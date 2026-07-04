from engine.timer_manager import TimerManager
from game.controllers.character_controller import CharacterController
from game.controllers.movement_controller import MovementController
from game.controllers.attack_controller import AttackController
from game.entities.attack_data import AttackPhase


class AIController:
    """Active component: Basic enemy AI brain."""
    def __init__(self, target):
        self.target = target
        self.attack_range = 60
        self.attack_cooldown = None
    
    def update(self, dt):
        if not self.target or not self.target.alive: return

        char_ctrl = self.owner.get_component(CharacterController)
        if not char_ctrl.can_act(): return
        move_ctrl = self.owner.get_component(MovementController)
        attack_ctrl = self.owner.get_component(AttackController)
        # cannot use intent and movement during attack
        if attack_ctrl.phase != AttackPhase.FINISHED: return

        dist_x = self.target.x - self.owner.x
        dist_z = self.target.z - self.owner.z
        if abs(dist_x) < self.attack_range and abs(dist_z) < 30:
            # Attack intent
            if not self.attack_cooldown or not self.attack_cooldown.is_active:
                attack_ctrl.start_attack(EnemySlash)
                self.attack_cooldown = TimerManager.start_timer(1.5, lambda: None)
            move_ctrl.move(0,0)
        else:
            #Chase intent
            dx = 1 if dist_x > 10 else (-1 if dist_x < -10 else 0)
            dz = 1 if dist_z > 10 else (-1 if dist_z < -10 else 0)
            move_ctrl.move(dx, dz)