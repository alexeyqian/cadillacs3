from game.controllers.character_state_machine import CharacterStateMachine
from game.controllers.attack_controller import AttackController


class AnimationController:
    def __init__(self):
        self.current_animation = "Idle"
        self.current_frame = 0
        
    def update(self, dt):
        char_ctrl = self.owner.get_component(CharacterStateMachine)
        atk_ctrl = self.owner.get_component(AttackController)
        
        # Sync logic state to animation string
        if char_ctrl.state == "dead":
            self.current_animation = "death"
        elif atk_ctrl.phase != "finished":
            self.current_animation = f"attack_{atk_ctrl.phase}"
        elif self.owner.y > 0:
            self.current_animation = "jump"
        elif abs(self.owner.vx) > 10 or abs(self.owner.vz) > 10:
            self.current_animation = "walk"
        else:
            self.current_animation = "idle"
            
        # Frame calculation logic would go here based on dt