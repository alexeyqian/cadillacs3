import pygame
from game.components.interaction_component import InteractionComponent
from game.controllers.character_controller import CharacterController
from game.controllers.movement_controller import MovementController
from game.controllers.attack_controller import AttackController


class InputController:
    """Reads raw hardware input and translates to game commands."""
    def __init__(self):
        self.input_buffer = [] # Stores recent inputs for buffering
    
    # todo: deprecated
    # update intention
    def handle_input(self, keys):
        char_ctrl = self.owner.get_component(CharacterController)
        if not char_ctrl.can_act(): return
        
        # Movement
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dz = keys[pygame.K_s] - keys[pygame.K_w]
        move_ctrl = self.owner.get_component(MovementController)
        if move_ctrl:
            move_ctrl.move(dx, dz)
            if dx != 0 or dz != 0:
                char_ctrl.set_state("walk")
            else:
                char_ctrl.set_state("idle")
                
        # Jump
        if keys[pygame.K_SPACE]:
            if move_ctrl: move_ctrl.jump()
            
        # Attack
        if keys[pygame.K_j]:
            atk_ctrl = self.owner.get_component(AttackController)
            if atk_ctrl: atk_ctrl.start_attack()
            
        # Interact - auto pickup loot
        if keys[pygame.K_e]:
            interact_comp = self.owner.get_component(InteractionComponent)
            if interact_comp: interact_comp.try_interact([]) # Pass interactables list here
