from dataclasses import dataclass, replace
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


# Fields ticked against real-second timers (Character._tick_attack_phase,
# attack_cooldown_timer, combo_window_timer, HealthComponent's stun) but
# authored as frame counts - the genre's standard way to express/tune
# frame data. make_attack_data() is the one place the /FPS conversion
# happens, so no call site does that math itself (and risks forgetting it -
# see enemy_config.py's gneiss/blade/black_elmer/walther attacks, which did).
_FRAME_DURATION_FIELDS = (
    "windup", "active", "recovery", "cooldown", "combo_window", "hit_stun_duration",
)


def make_attack_data(base: AttackData = None, **kwargs) -> AttackData:
    """Builds a fresh AttackData (base=None), or overrides one (base=<an
    existing AttackData>, e.g. a per-character variant in player_config.py/
    enemy_config.py). windup/active/recovery/cooldown/combo_window/
    hit_stun_duration are given in frame counts here, not seconds."""
    converted = {
        key: (value / FPS if key in _FRAME_DURATION_FIELDS else value)
        for key, value in kwargs.items()
    }
    if base is None:
        return AttackData(**converted)
    return replace(base, **converted)


DEFAULT_PLAYER_ATTACK_1_DATA = make_attack_data(
    name="attack",
    damage=ATTACK_1_DAMAGE,
    windup=ATTACK_1_WINDUP_DURATION,
    active=ATTACK_1_ACTIVE_DURATION,
    recovery=ATTACK_1_RECOVERY_DURATION,
    cooldown=ATTACK_1_COOLDOWN,
    combo_window=ATTACK_1_COMBO_WINDOW,
    hit_stun_duration=ATTACK_1_HIT_STUN_DURATION,
    knockback_velocity=ATTACK_1_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)


DEFAULT_PLAYER_ATTACK_2_DATA = make_attack_data(
    name="attack2",
    damage=ATTACK_2_DAMAGE,
    windup=ATTACK_2_WINDUP_DURATION,
    active=ATTACK_2_ACTIVE_DURATION,
    recovery=ATTACK_2_RECOVERY_DURATION,
    cooldown=ATTACK_2_COOLDOWN,
    combo_window=ATTACK_2_COMBO_WINDOW,
    hit_stun_duration=ATTACK_2_HIT_STUN_DURATION,
    knockback_velocity=ATTACK_2_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)


DEFAULT_PLAYER_ATTACK_3_DATA = make_attack_data(
    name="attack3",
    damage=ATTACK_3_DAMAGE,
    windup=ATTACK_3_WINDUP_DURATION,
    active=ATTACK_3_ACTIVE_DURATION,
    recovery=ATTACK_3_RECOVERY_DURATION,
    cooldown=ATTACK_3_COOLDOWN,
    combo_window=0, # finisher - never chains into anything, always resets to hit 1
    hit_stun_duration=ATTACK_3_HIT_STUN_DURATION,
    knockback_velocity=ATTACK_3_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)

DEFAULT_PLAYER_GRAB_KNEE_DATA = make_attack_data(
    name="grab_knee",
    damage=PLAYER_GRAB_KNEE_DAMAGE,
    # the "grab_knee" clip's own frame_durations (see mustapha_data.py) are
    # tuned 1:1 with these so the windup/active/recovery pose lines up with
    # the animation frame shown.
    windup=PLAYER_GRAB_KNEE_WINDUP_DURATION,
    active=PLAYER_GRAB_KNEE_ACTIVE_DURATION,
    recovery=PLAYER_GRAB_KNEE_RECOVERY_DURATION,
)


DEFAULT_PLAYER_RUN_ATTACK_DATA = make_attack_data(
    name="run_attack",
    damage=RUN_ATTACK_DAMAGE,
    keep_moving=True,
    windup=RUN_ATTACK_WINDUP_DURATION,
    active=RUN_ATTACK_ACTIVE_DURATION,
    recovery=RUN_ATTACK_RECOVERY_DURATION,
    cooldown=RUN_ATTACK_COOLDOWN,
    hit_stun_duration=RUN_ATTACK_HIT_STUN_DURATION,
    knockback_velocity=RUN_ATTACK_KNOCKBACK_VELOCITY,
    lane_reach=1,
    max_targets=1,
)


DEFAULT_ENEMY_ATTACK_DATA = make_attack_data(
    name="attack",
    damage=ENEMY_ATTACK_DAMAGE,
    windup=ENEMY_ATTACK_WINDUP,
    active=ENEMY_ATTACK_ACTIVE,
    recovery=ENEMY_ATTACK_RECOVERY,
    cooldown=ENEMY_ATTACK_COOLDOWN,
    hit_stun_duration=ENEMY_ATTACK_HIT_STUN_DURATION,
    knockback_velocity=ENEMY_ATTACK_KNOCKBACK_VELOCITY,
    lane_reach=0,
    max_targets=1,
)
