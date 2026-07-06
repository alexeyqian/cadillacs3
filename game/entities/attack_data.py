from dataclasses import dataclass
from enum import Enum
from game.settings import *


class AttackPhase(Enum):
    WINDUP = 1
    ACTIVE = 2
    RECOVERY = 3
    FINISHED = 4


@dataclass
class AttackData:
    name: str = 'unknown'
    delay: float = 0 #deprecated
    windup: float = 0
    active: float = 0
    recovery: float = 0
    cooldown: float = 0 # deprecated
    combo_window: float = 0
    damage: float = 10
    knockback: tuple = ()
    # some attack is special, such as mustapha's run attack is flying attack, which is airborne
    # other player's run attack might be not airborne,
    launch_power: float = 0 # initial upward velocity applied to the attacker on start

    hitbox_offset_x: int = 0 # deprecated
    hitbox_offset_y: int = 0 # deprecated
    hitbox_w: int = 50
    hitbox_h: int = 60
    
    hit_stun_duration: float = 0 # deprecated
    knockback_velocity: float = 0 # deprecated
    lane_reach: int = 0 # deprecated
    max_targets: int = 0 # deprecated
    combo_window: int = 0 # deprecated


DEFAULT_PLAYER_ATTACK_DATA = AttackData(
    hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
    hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
    hitbox_w=PLAYER_HITBOX_W,
    hitbox_h=PLAYER_HITBOX_H,

    delay=0,
    damage=ATTACK_1_DAMAGE,
    # *_DURATION constants are frame counts (fighting-game style frame data);
    # Character.update_attack ticks phase_timer in real seconds, so convert here.
    windup=ATTACK_1_WINDUP_DURATION / FPS,
    active=ATTACK_1_ACTIVE_DURATION / FPS,
    recovery=ATTACK_1_RECOVERY_DURATION / FPS,
    cooldown=0,
    hit_stun_duration=ATTACK_1_HIT_STUN_DURATION,
    knockback_velocity=ATTACK_1_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
    combo_window=0,
)


DEFAULT_PLAYER_RUN_ATTACK_DATA = AttackData(
    delay=0,
    damage=RUN_ATTACK_DAMAGE,
    launch_power=RUN_ATTACK_LAUNCH_POWER,
    windup=RUN_ATTACK_WINDUP_DURATION / FPS,
    active=RUN_ATTACK_ACTIVE_DURATION / FPS,
    recovery=RUN_ATTACK_RECOVERY_DURATION / FPS,
    cooldown=0,
    hit_stun_duration=RUN_ATTACK_HIT_STUN_DURATION,
    knockback_velocity=RUN_ATTACK_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
    combo_window=0,
)


DEFAULT_ENEMY_ATTACK_DATA = AttackData(
    hitbox_offset_x=ENEMY_HITBOX_OFFSET_X,
    hitbox_offset_y=ENEMY_HITBOX_OFFSET_Y,
    hitbox_w=ENEMY_HITBOX_W,
    hitbox_h=ENEMY_HITBOX_H,
    delay=ENEMY_ATTACK_DELAY,
    damage=ENEMY_ATTACK_DAMAGE,
    windup=ENEMY_ATTACK_WINDUP / FPS,
    active=ENEMY_ATTACK_ACTIVE / FPS,
    recovery=ENEMY_ATTACK_RECOVERY / FPS,
    cooldown=ENEMY_ATTACK_COOLDOWN,
    hit_stun_duration=ENEMY_ATTACK_HIT_STUN_DURATION,
    knockback_velocity=ENEMY_ATTACK_KNOCKBACK_VELOCITY,
    lane_reach=0,
    max_targets=1,
    combo_window=0,
)
