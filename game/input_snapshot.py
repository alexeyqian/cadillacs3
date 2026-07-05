from dataclasses import dataclass
import pygame


@dataclass
class InputSnapshot:
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False
    shift: bool = False
    jump_pressed: bool = False
    attack_pressed: bool = False


def read_input_snapshot(keys):
    return InputSnapshot(
        left=bool(keys[pygame.K_a]),
        right=bool(keys[pygame.K_d]),
        up=bool(keys[pygame.K_w]),
        down=bool(keys[pygame.K_s]),
        shift=bool(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]),
        jump_pressed=bool(keys[pygame.K_SPACE]),
        attack_pressed=bool(keys[pygame.K_j]),
    )
