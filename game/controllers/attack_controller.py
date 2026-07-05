from game.entities.attack_data import AttackData, AttackPhase
from game.components.hitbox_component import HitboxComponent
from game.controllers.character_controller import CharacterController


class AttackController:
    """Active component: state machine managing attack phases and animations."""
    def __init__(self):
        self.current_attack: AttackData = None
        self.phase = AttackPhase.FINISHED
        self.phase_timer = 0.0
    
    def start_attack(self, attack: AttackData):
        char_ctrl = self.owner.get_component(CharacterController)
        if not char_ctrl.can_act(): return

        if self.phase != AttackPhase.FINISHED:
            return
        self.current_attack = attack
        self.phase = AttackPhase.WINDUP
        self.phase_timer = 0.0
        self.owner.vx = 0 # stop moving during attack
        self.owner.vz = 0
    
    def update(self, dt):
        if self.phase == AttackPhase.FINISHED:
            return
        self.phase_timer += dt
        if self.phase == AttackPhase.WINDUP and self.phase_timer >= self.current_attack.windup:
            self._enter_phase(AttackPhase.ACTIVE)
        elif self.phase == AttackPhase.ACTIVE and self.phase_timer >= self.current_attack.active:
            self._enter_phase(AttackPhase.RECOVERY)
        elif self.phase == AttackPhase.RECOVERY and self.phase_timer >= self.current_attack.recovery:
            self._enter_phase(AttackPhase.FINISHED)

    def _enter_phase(self, new_phase):
        self.phase = new_phase
        self.phase_timer = 0.0

        hitbox = self.owner.get_component(HitboxComponent)
        if new_phase == AttackPhase.ACTIVE and hitbox:
            # knockback direction depends on the attacker's current facing,
            # so it's computed here rather than stored statically on AttackData.
            knockback = (self.current_attack.knockback_velocity * self.owner.facing, 0)
            hitbox.activate(
                self.current_attack.damage,
                knockback,
                self.current_attack.hitbox_w,
                self.current_attack.hitbox_h
            )
        elif new_phase != AttackPhase.ACTIVE and hitbox:
            hitbox.deactivate()

        if new_phase == AttackPhase.FINISHED:
            self.current_attack = None
        