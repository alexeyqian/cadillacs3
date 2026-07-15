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
    keep_moving: bool = False # if True, intent-driven movement keeps applying during this attack

    hitbox_offset_x: int = 0 # deprecated
    hitbox_offset_y: int = 0 # deprecated
    hitbox_w: int = 50
    hitbox_h: int = 60

    hit_stun_duration: float = 0 # how long this attack stuns the target on hit, in seconds
    knockback_velocity: float = 0 # deprecated
    lane_reach: int = 0 # deprecated
    max_targets: int = 0 # deprecated


DEFAULT_PLAYER_ATTACK_1_DATA = AttackData(
    name="attack",
    delay=0,
    damage=ATTACK_1_DAMAGE,
    # *_DURATION constants are frame counts (fighting-game style frame data);
    # Character.update_attack ticks phase_timer in real seconds, so convert here.
    windup=ATTACK_1_WINDUP_DURATION / FPS,
    active=ATTACK_1_ACTIVE_DURATION / FPS,
    recovery=ATTACK_1_RECOVERY_DURATION / FPS,
    cooldown=ATTACK_1_COOLDOWN / FPS,
    combo_window=ATTACK_1_COMBO_WINDOW / FPS,
    hit_stun_duration=ATTACK_1_HIT_STUN_DURATION / FPS,
    knockback_velocity=ATTACK_1_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)


DEFAULT_PLAYER_ATTACK_2_DATA = AttackData(
    name="attack2",
    delay=0,
    damage=ATTACK_2_DAMAGE,
    windup=ATTACK_2_WINDUP_DURATION / FPS,
    active=ATTACK_2_ACTIVE_DURATION / FPS,
    recovery=ATTACK_2_RECOVERY_DURATION / FPS,
    cooldown=ATTACK_2_COOLDOWN / FPS,
    combo_window=ATTACK_2_COMBO_WINDOW / FPS,
    hit_stun_duration=ATTACK_2_HIT_STUN_DURATION / FPS,
    knockback_velocity=ATTACK_2_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)


DEFAULT_PLAYER_ATTACK_3_DATA = AttackData(
    name="attack3",
    delay=0,
    damage=ATTACK_3_DAMAGE,
    windup=ATTACK_3_WINDUP_DURATION / FPS,
    active=ATTACK_3_ACTIVE_DURATION / FPS,
    recovery=ATTACK_3_RECOVERY_DURATION / FPS,
    cooldown=ATTACK_3_COOLDOWN / FPS,
    combo_window=0, # finisher - never chains into anything, always resets to hit 1
    hit_stun_duration=ATTACK_3_HIT_STUN_DURATION / FPS,
    knockback_velocity=ATTACK_3_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)

DEFAULT_PLAYER_GRAB_KNEE_DATA = AttackData(
    name="grab_knee",
    damage=PLAYER_GRAB_KNEE_DAMAGE,
    # *_DURATION constants are frame counts; the "grab_knee" clip's own
    # frame_durations (see mustapha_data.py) are tuned 1:1 with these so the
    # windup/active/recovery pose lines up with the animation frame shown.
    windup=PLAYER_GRAB_KNEE_WINDUP_DURATION / FPS,
    active=PLAYER_GRAB_KNEE_ACTIVE_DURATION / FPS,
    recovery=PLAYER_GRAB_KNEE_RECOVERY_DURATION / FPS,
)


DEFAULT_PLAYER_RUN_ATTACK_DATA = AttackData(
    name="run_attack",
    delay=0,
    damage=RUN_ATTACK_DAMAGE,
    keep_moving=True,
    windup=RUN_ATTACK_WINDUP_DURATION / FPS,
    active=RUN_ATTACK_ACTIVE_DURATION / FPS,
    recovery=RUN_ATTACK_RECOVERY_DURATION / FPS,
    cooldown=RUN_ATTACK_COOLDOWN / FPS,
    hit_stun_duration=RUN_ATTACK_HIT_STUN_DURATION / FPS,
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
    hit_stun_duration=ENEMY_ATTACK_HIT_STUN_DURATION / FPS,
    knockback_velocity=ENEMY_ATTACK_KNOCKBACK_VELOCITY,
    lane_reach=0,
    max_targets=1,
)
