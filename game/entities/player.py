from game.settings import *

from game.entities.character import Character
from game.entities.player_config import get_player_config
from game.entities.character_state import PlayerState
from game.entities.player_renderer import PlayerRenderer
from game.entities.attack_data import AttackData

from game.components.interaction_component import InteractionComponent
from game.components.inventory_component import InventoryComponent
from game.controllers.input_controller import InputController
from game.controllers.movement_controller import MovementController
from game.controllers.attack_controller import AttackController
from game.controllers.grab_controller import GrabController
from game.controllers.animation_controller import AnimationController

from game.animation.animation_manager import AnimationManager


class Player(Character):
    def __init__(self, x, z, player_type, animation_data):
        super().__init__(x, z)
        self.color = (0, 150, 255)
        self.width = PLAYER_W
        self.height = PLAYER_H
        self.tags.add("Player")
        self.add_component(InteractionComponent())
        self.add_component(InventoryComponent())

        self.add_component(InputController())
        self.add_component(MovementController())
        self.add_component(AttackController())
        self.add_component(GrabController())
        self.add_component(AnimationController())

        config = get_player_config(player_type)
        self._load_from_config(config)
        self.state = PlayerState.IDLE
        self.animation_manager = AnimationManager(animation_data)
        self.renderer = PlayerRenderer(self)
        
    def _load_from_config(self, config):
        self.player_id = config.player_id
        self.display_name = config.display_name

        self.speed = config.speed
        self.run_speed = config.run_speed
        self.jump_power = config.jump_power
        self.air_move_speed = config.air_move_speed

        self.sprite_scale = config.sprite_scale

    def update(self, game_state):
        super().update()
        self.update_movement(game_state.keys)
        # ...
        self.animation_manager.update(self.state)

    def draw(self, screen, camera_x):
        super().draw(screen)
        self.renderer.draw(screen, camera_x)

    def update_movement(self, game_state):
        player_input = game_state.player_input

        self.state = PlayerState.WALK

        if player_input.left:
            self.move_left()
        elif player_input.right:
            self.move_right()
        elif player_input.up:
            self.move_up()
        elif player_input.down:
            self.move_down()
        elif player_input.jump:
            self.jump()
            self.state = PlayerState.JUMP
        elif player_input.attack:
            self.attack()
            self.state = PlayerState.ATTACK
        else:
            self.stop_moving()
            self.state = PlayerState.IDLE

    def move_left(self):
        self.x -= self.speed
        self.facing_right = False
        
    def move_right(self):
        self.x += self.speed
        self.facing_right = True
    
    def move_up(self):
        self.y -= self.speed
    
    def move_down(self):
        self.y += self.speed

    def jump(self):
        pass

    def stop_moving(self):
        pass
    
    def attack(self):
        pass
    
    def take_damage(self, amount):
        return super().take_damage(amount)
