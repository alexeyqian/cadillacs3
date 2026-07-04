from game.entities.character import Character
from game.entities.enemy_config import get_enemy_config
from game.entities.character_state import EnemyState
from game.entities.enemy_renderer import EnemyRenderer
from game.entities.attack_data import AttackData

from game.settings import *
from game.components.health_component import HealthComponent
from game.components.hitbox_component import HitboxComponent
from game.controllers.movement_controller import MovementController
from game.controllers.attack_controller import AttackController
from game.controllers.ai_controller import AIController
from game.controllers.loot_drop_controller import LootDropController
from game.animation.animation_manager import AnimationManager

class Enemy(Character):
    def __init__(self, x, z, enemy_type, animation_data, target): # target is Player
        super().__init__(x, z)
        self.color = (200, 50, 50)
        self.width = 40
        self.height = 80
        self.tags.add("enemy")
        self.add_component(AIController(target))
        self.add_component(MovementController(move_speed=120))
        self.add_component(AttackController())
        self.add_component(LootDropController())

        config = get_enemy_config(enemy_type)
        self._load_from_config(config)
        self.state = EnemyState.IDLE
        self.animation_manager = AnimationManager(animation_data)
        self.renderer = EnemyRenderer(self)
        
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

        self.state = EnemyState.WALK

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
            self.state = EnemyState.JUMP
        elif player_input.attack:
            self.attack()
            self.state = EnemyState.ATTACK
        else:
            self.stop_moving()
            self.state = EnemyState.IDLE

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


