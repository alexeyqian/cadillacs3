from dataclasses import dataclass, replace
from game.settings import *
from game.animation.mustapha_data import MUSTAPHA_ANIMATIONS

@dataclass(frozen=True)
class PlayerConfig:
    player_id: str
    display_name: str

    speed: float = PLAYER_SPEED
    run_speed: float = PLAYER_RUN_SPEED
    jump_power: float = PLAYER_JUMP_POWER
    jump_air_move_speed: float = PLAYER_JUMP_AIR_MOVE_SPEED
    run_air_move_speed: float = PLAYER_RUN_AIR_MOVE_SPEED

    animation_data: dict = None
    sprite_scale: int = 1


PLAYER_CONFIGS = {
    "mustapha": PlayerConfig(
        player_id="mustapha",
        display_name="Mustapha",
        animation_data=MUSTAPHA_ANIMATIONS,
    ),
}

def get_player_config(player_type):
    return PLAYER_CONFIGS.get(player_type, PLAYER_CONFIGS["mustapha"])
