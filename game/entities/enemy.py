from game.entities.character import Character
from game.entities.enemy_config import get_enemy_config
from game.entities.character_renderer import CharacterRenderer

from game.settings import *
from game.components.hurtbox_component import HurtboxComponent
from game.controllers.loot_drop_controller import LootDropController

class Enemy(Character):
    def __init__(self, x, z, enemy_type, animation_data):
        super().__init__(x, z, animation_data)
        self.width, self.height = ENEMY_W, ENEMY_H # todo: load from config
        self.collision_box_w, self.collision_box_h = ENEMY_COLLISION_W, ENEMY_COLLISION_H
        self.hurtbox_w, self.hurtbox_h = ENEMY_HURTBOX_W, ENEMY_HURTBOX_H

        self.tags.add("enemy")
        self.add_component(LootDropController())

        config = get_enemy_config(enemy_type)
        self._load_from_config(config)
        self.renderer = CharacterRenderer(self, show_health_bar=True)

    def _load_from_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name

        self.move_speed = config.speed
        self.run_speed = config.run_speed
        self.attack_range = config.attack_range
        self.attack_data = config.attack
        self.score_points = config.score_points

        self.sprite_scale = config.sprite_scale

        self.get_component(HurtboxComponent).configure(config.hurt_box_w, config.hurt_box_h)

    def update_intention(self, dt, keys, player_x, player_z):
        dx = player_x - self.x
        dz = player_z - self.z
        in_range = (dx * dx + dz * dz) ** 0.5 <= self.attack_range

        self.intent.move_x = 0 if in_range else (1 if dx > 0 else -1)
        self.intent.move_z = 0 if in_range else (1 if dz > 0 else -1)
        self.intent.wants_attack = in_range

    def is_ready_to_remove(self):
        return not self.alive and self.animation_manager.is_finished()
