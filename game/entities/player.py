import pygame
from game.settings import *

from game.entities.character import Character
from game.entities.player_config import get_player_config
from game.entities.character_renderer import CharacterRenderer
from game.entities.attack_data import (
    DEFAULT_PLAYER_COMBO_ATTACKS,
    DEFAULT_PLAYER_RUN_ATTACK_DATA,
)

from game.components.interaction_component import InteractionComponent
from game.components.inventory_component import InventoryComponent
from game.components.hurtbox_component import HurtboxComponent
from game.controllers.grab_controller import GrabController


class Player(Character):
    def __init__(self, x, z, player_type, animation_data):
        super().__init__(x, z, animation_data)

        self.width, self.height = PLAYER_W, PLAYER_H
        self.collision_box_w, self.collision_box_h = PLAYER_COLLISION_W, PLAYER_COLLISION_H
        self.hurtbox_w, self.hurtbox_h = PLAYER_HURTBOX_W, PLAYER_HURTBOX_H

        self.tags.add("player")
        self.score = 0
        self.lives = PLAYER_LIVES
        self.add_component(InteractionComponent())
        self.add_component(InventoryComponent())
        self.add_component(GrabController())

        config = get_player_config(player_type)
        self._load_from_config(config)
        self.renderer = CharacterRenderer(self)

    def _load_from_config(self, config):
        self.player_id = config.player_id
        self.display_name = config.display_name

        self.move_speed = config.speed
        self.run_speed = config.run_speed
        self.jump_power = config.jump_power
        self.jump_air_move_speed = config.jump_air_move_speed
        self.combo_attacks = DEFAULT_PLAYER_COMBO_ATTACKS
        self.run_attack_data = DEFAULT_PLAYER_RUN_ATTACK_DATA

        self.sprite_scale = config.sprite_scale

        self.get_component(HurtboxComponent).configure(
            PLAYER_HURTBOX_W, PLAYER_HURTBOX_H, PLAYER_HURTBOX_AIRBORNE_H)

    def update_intention(self, dt, input, player_x, player_z):
        self.intent.move_x = input.right - input.left
        self.intent.move_z = input.down - input.up
        self.intent.running = input.running
        self.intent.wants_jump = input.jump_pressed
        self.intent.wants_attack = input.attack_pressed




