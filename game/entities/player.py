from game.entities.character import Character
from game.entities.player_config import get_player_config

class Player(Character):
    def __init__(self, player_type, animation_data):
        super().__init__()
        config = get_player_config(player_type)
        self._load_from_config(config, animation_data)
        
    def _load_from_config(self, config, animation_data):
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
        # Additional player-specific update logic can be added here
        
    def draw(self, surface):
        super().draw(surface)
        # Additional player-specific drawing logic can be added here

    def update_movement(self, game_state):
        player_input = game_state.player_input

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
        elif player_input.attack:
            self.attack()
        else:
            self.stop_moving()

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

