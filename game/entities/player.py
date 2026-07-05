from game.settings import *

from game.entities.character import Character
from game.entities.player_config import get_player_config
from game.entities.player_renderer import PlayerRenderer
from game.entities.attack_data import DEFAULT_PLAYER_ATTACK_DATA

from game.components.interaction_component import InteractionComponent
from game.components.inventory_component import InventoryComponent
from game.controllers.attack_controller import AttackController
from game.controllers.grab_controller import GrabController
from game.controllers.animation_controller import AnimationController

from game.animation.animation_manager import AnimationManager


class Player(Character):
    def __init__(self, x, z, player_type, animation_data):
        super().__init__(x, z)

        self.width = PLAYER_W
        self.height = PLAYER_H
        self.tags.add("player")
        self.add_component(InteractionComponent())
        self.add_component(InventoryComponent())

        self.add_component(AttackController())
        self.add_component(GrabController())
        self.add_component(AnimationController())

        config = get_player_config(player_type)
        self._load_from_config(config)
        self.animation_manager = AnimationManager(animation_data)
        self.renderer = PlayerRenderer(self)

    def _load_from_config(self, config):
        self.player_id = config.player_id
        self.display_name = config.display_name

        self.move_speed = config.speed
        self.run_speed = config.run_speed
        self.jump_power = config.jump_power
        self.air_move_speed = config.air_move_speed
        self.attack_data = DEFAULT_PLAYER_ATTACK_DATA

        self.sprite_scale = config.sprite_scale

    def update_intention(self, dt, input, player_x, player_z):
        self.intent.move_x = input.right - input.left
        self.intent.move_z = input.down - input.up
        self.intent.running = input.shift
        self.intent.wants_jump = input.jump_pressed
        self.intent.wants_attack = input.attack_pressed

    def draw(self, screen, camera_x):
        self.renderer.draw(screen, camera_x)

