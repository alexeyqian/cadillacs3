from dataclasses import dataclass, replace
from game.settings import *
from game.animation.mustapha_data import MUSTAPHA_ANIMATIONS
from game.entities.attack_data import (
    DEFAULT_PLAYER_ATTACK_1_DATA,
    DEFAULT_PLAYER_ATTACK_2_DATA,
    DEFAULT_PLAYER_ATTACK_3_DATA,
    DEFAULT_PLAYER_RUN_ATTACK_DATA,
    DEFAULT_PLAYER_GRAB_KNEE_DATA,
)

@dataclass(frozen=True)
class PlayerConfig:
    player_id: str
    display_name: str

    speed: float = PLAYER_SPEED
    run_speed: float = PLAYER_RUN_SPEED
    jump_power: float = PLAYER_JUMP_POWER
    jump_air_move_speed: float = PLAYER_JUMP_AIR_MOVE_SPEED

    animation_data: dict = None
    sprite_scale: int = 1
    combo_attacks: list = None
    run_attack_data: object = None
    grab_knee_data: object = None


# Hitbox geometry is gameplay tuning (per punch, per character), not
# animation data - it lives here rather than on mustapha_data.py's "attack"/
# "attack2"/"attack3" entries, layered onto the generic timing/damage
# templates from attack_data.py.
MUSTAPHA_COMBO_ATTACKS = [
    replace(DEFAULT_PLAYER_ATTACK_1_DATA,
        hitbox_offset_x=64, hitbox_offset_y=-256, hitbox_w=128, hitbox_h=100),
    replace(DEFAULT_PLAYER_ATTACK_2_DATA,
        hitbox_offset_x=64, hitbox_offset_y=-192, hitbox_w=128, hitbox_h=100),
    replace(DEFAULT_PLAYER_ATTACK_3_DATA,
        hitbox_offset_x=64, hitbox_offset_y=-192, hitbox_w=128, hitbox_h=100),
]

MUSTAPHA_RUN_ATTACK_DATA = replace(DEFAULT_PLAYER_RUN_ATTACK_DATA,
    hitbox_offset_x=50, hitbox_offset_y=-230, hitbox_w=128, hitbox_h=100)

MUSTAPHA_GRAB_KNEE_DATA = replace(DEFAULT_PLAYER_GRAB_KNEE_DATA,
    hitbox_offset_x=64, hitbox_offset_y=-180, hitbox_w=128, hitbox_h=100)


PLAYER_CONFIGS = {
    "mustapha": PlayerConfig(
        player_id="mustapha",
        display_name="Mustapha",
        animation_data=MUSTAPHA_ANIMATIONS,
        combo_attacks=MUSTAPHA_COMBO_ATTACKS,
        run_attack_data=MUSTAPHA_RUN_ATTACK_DATA,
        grab_knee_data=MUSTAPHA_GRAB_KNEE_DATA,
    ),
}

def get_player_config(player_type):
    return PLAYER_CONFIGS.get(player_type, PLAYER_CONFIGS["mustapha"])
