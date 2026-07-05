from game.entities.character import Character
from game.entities.enemy_config import get_enemy_config
from game.entities.enemy_renderer import EnemyRenderer

from game.settings import *
from game.controllers.loot_drop_controller import LootDropController
from game.animation.animation_manager import AnimationManager

class Enemy(Character):
    def __init__(self, x, z, enemy_type, animation_data, target): # target is Player
        super().__init__(x, z)
        self.width = 40
        self.height = 80
        self.tags.add("enemy")

        self.add_component(LootDropController())

        config = get_enemy_config(enemy_type)
        self._load_from_config(config)
        self.animation_manager = AnimationManager(animation_data)
        self.renderer = EnemyRenderer(self)

    def _load_from_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name

        self.move_speed = config.speed
        self.run_speed = config.run_speed
        self.attack_range = config.attack_range
        self.attack_data = config.attack

        self.sprite_scale = config.sprite_scale

    def update_intention(self, dt, keys, player_x, player_z):
        dx = player_x - self.x
        dz = player_z - self.z
        in_range = (dx * dx + dz * dz) ** 0.5 <= self.attack_range

        self.intent.move_x = 0 if in_range else (1 if dx > 0 else -1)
        self.intent.move_z = 0 if in_range else (1 if dz > 0 else -1)
        self.intent.wants_attack = in_range

    def draw(self, screen, camera_x):
        self.renderer.draw(screen, camera_x)
