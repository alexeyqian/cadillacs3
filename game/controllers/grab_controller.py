import math
from typing import Optional, List
from game.entities.character import Character
from game.components.status_effect_component import StatusEffectComponent
from game.controllers.character_state_machine import CharacterStateMachine

class GrabController:
    def __init__(self):
        self.grabbed_target: Optional[Character] = None
        
    def try_grab(self, targets: List[Character]):
        char_ctrl = self.owner.get_component(CharacterStateMachine)
        if not char_ctrl.can_act(): return
        
        for target in targets:
            if target == self.owner: continue
            dist = math.hypot(target.x - self.owner.x, target.z - self.owner.z)
            if dist < 50:
                self.grabbed_target = target
                target.get_component(StatusEffectComponent).add_effect("grabbed", 2.0)
                target.get_component(CharacterStateMachine).set_state("stunned")
                char_ctrl.set_state("grabbing")
                print(f"{self.owner.__class__.__name__} grabbed {target.__class__.__name__}!")
                return True
        return False

    def throw_target(self):
        if self.grabbed_target:
            self.grabbed_target.vx = 500 * self.owner.facing
            self.grabbed_target.vz = -200
            self.grabbed_target.get_component(CharacterStateMachine).set_state("idle")
            self.grabbed_target = None

            self.owner.get_component(CharacterStateMachine).set_state("idle")
