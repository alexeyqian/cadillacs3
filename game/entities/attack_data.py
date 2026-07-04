from dataclasses import dataclass
from enum import Enum


class AttackPhase(Enum):
    WINDUP = 1
    ACTIVE = 2
    RECOVERY = 3
    FINISHED = 4


@dataclass
class AttackData:
    name: str
    windup_dur: float
    active_dur: float
    recovery_dur: float
    damage: float
    knockback: tuple
    hitbox_offset_x: int = 0 # deprecated
    hitbox_offset_y: int = 0 # deprecated
    hitbox_width: int = 50
    hitbox_height: int = 60