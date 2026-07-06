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
    name: str = 'unknown' # also doubles as the animation/state name while this attack plays
    delay: float = 0 #deprecated
    windup: float = 0
    active: float = 0
    recovery: float = 0
    cooldown: float = 0 # deprecated
    combo_window: float = 0 # how long after finishing this attack a repeat press continues the combo
    damage: float = 10
    knockback: tuple = ()
    # some attack is special, such as mustapha's run attack is flying attack, which is airborne
    # other player's run attack might be not airborne,
    launch_power: float = 0 # initial upward velocity applied to the attacker on start
    keep_moving: bool = False # if True, intent-driven movement keeps applying during this attack

    hitbox_offset_x: int = 0 # deprecated
    hitbox_offset_y: int = 0 # deprecated
    hitbox_w: int = 50
    hitbox_h: int = 60

    hit_stun_duration: float = 0 # deprecated
    knockback_velocity: float = 0 # deprecated
    lane_reach: int = 0 # deprecated
    max_targets: int = 0 # deprecated


DEFAULT_PLAYER_ATTACK_1_DATA = AttackData(
    name="attack",
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
    cooldown=ATTACK_1_COOLDOWN / FPS,
    combo_window=ATTACK_1_COMBO_WINDOW / FPS,
    hit_stun_duration=ATTACK_1_HIT_STUN_DURATION,
    knockback_velocity=ATTACK_1_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)


DEFAULT_PLAYER_ATTACK_2_DATA = AttackData(
    name="attack2",
    hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
    hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
    hitbox_w=PLAYER_HITBOX_W,
    hitbox_h=PLAYER_HITBOX_H,

    delay=0,
    damage=ATTACK_2_DAMAGE,
    windup=ATTACK_2_WINDUP_DURATION / FPS,
    active=ATTACK_2_ACTIVE_DURATION / FPS,
    recovery=ATTACK_2_RECOVERY_DURATION / FPS,
    cooldown=ATTACK_2_COOLDOWN / FPS,
    combo_window=ATTACK_2_COMBO_WINDOW / FPS,
    hit_stun_duration=ATTACK_2_HIT_STUN_DURATION,
    knockback_velocity=ATTACK_2_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)


DEFAULT_PLAYER_ATTACK_3_DATA = AttackData(
    name="attack3",
    hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
    hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
    hitbox_w=PLAYER_HITBOX_W,
    hitbox_h=PLAYER_HITBOX_H,

    delay=0,
    damage=ATTACK_3_DAMAGE,
    windup=ATTACK_3_WINDUP_DURATION / FPS,
    active=ATTACK_3_ACTIVE_DURATION / FPS,
    recovery=ATTACK_3_RECOVERY_DURATION / FPS,
    cooldown=ATTACK_3_COOLDOWN / FPS,
    combo_window=0, # finisher - never chains into anything, always resets to hit 1
    hit_stun_duration=ATTACK_3_HIT_STUN_DURATION,
    knockback_velocity=ATTACK_3_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)

# The 3-hit punch combo, in order. Character.combo_index walks through this
# list; ATTACK_3's combo_window=0 means there's nothing after it to chain into.
DEFAULT_PLAYER_COMBO_ATTACKS = [
    DEFAULT_PLAYER_ATTACK_1_DATA,
    DEFAULT_PLAYER_ATTACK_2_DATA,
    DEFAULT_PLAYER_ATTACK_3_DATA,
]

DEFAULT_PLAYER_RUN_ATTACK_DATA = AttackData(
    name="run_attack",
    delay=0,
    damage=RUN_ATTACK_DAMAGE,
    launch_power=RUN_ATTACK_LAUNCH_POWER,
    keep_moving=True,
    windup=RUN_ATTACK_WINDUP_DURATION / FPS,
    active=RUN_ATTACK_ACTIVE_DURATION / FPS,
    recovery=RUN_ATTACK_RECOVERY_DURATION / FPS,
    cooldown=RUN_ATTACK_COOLDOWN / FPS,
    hit_stun_duration=RUN_ATTACK_HIT_STUN_DURATION,
    knockback_velocity=RUN_ATTACK_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)


DEFAULT_ENEMY_ATTACK_DATA = AttackData(
    name="attack",
    hitbox_offset_x=ENEMY_HITBOX_OFFSET_X,
    hitbox_offset_y=ENEMY_HITBOX_OFFSET_Y,
    hitbox_w=ENEMY_HITBOX_W,
    hitbox_h=ENEMY_HITBOX_H,
    delay=ENEMY_ATTACK_DELAY,
    damage=ENEMY_ATTACK_DAMAGE,
    windup=ENEMY_ATTACK_WINDUP / FPS,
    active=ENEMY_ATTACK_ACTIVE / FPS,
    recovery=ENEMY_ATTACK_RECOVERY / FPS,
    cooldown=ENEMY_ATTACK_COOLDOWN / FPS,
    hit_stun_duration=ENEMY_ATTACK_HIT_STUN_DURATION,
    knockback_velocity=ENEMY_ATTACK_KNOCKBACK_VELOCITY,
    lane_reach=0,
    max_targets=1,
)
