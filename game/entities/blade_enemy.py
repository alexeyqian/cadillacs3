from game.animation.blade_data import BLADE_ANIMATIONS
from game.entities.enemy import Enemy

class BladeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="blade",
                animation_data=BLADE_ANIMATIONS,
                sprite_scale=1)
