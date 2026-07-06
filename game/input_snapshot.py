from dataclasses import dataclass
import pygame

from game.settings import RUN_TAP_WINDOW


@dataclass
class InputSnapshot:
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False
    running: bool = False  # active double-tap dash
    jump_pressed: bool = False
    attack_pressed: bool = False


class InputReader:
    """Stateful: tracks key-press edges across frames to detect
    double-tap-to-run, which a single stateless snapshot can't see."""

    def __init__(self):
        self._was_pressed = {"left": False, "right": False}
        self._tap_window = {"left": 0.0, "right": 0.0}
        self._dash_direction = None

    def read(self, raw_keys, dt):
        left = bool(raw_keys[pygame.K_a])
        right = bool(raw_keys[pygame.K_d])

        self._update_dash("left", left, dt)
        self._update_dash("right", right, dt)

        return InputSnapshot(
            left=left,
            right=right,
            up=bool(raw_keys[pygame.K_w]),
            down=bool(raw_keys[pygame.K_s]),
            running=self._dash_direction is not None,
            jump_pressed=bool(raw_keys[pygame.K_k]),
            attack_pressed=bool(raw_keys[pygame.K_j]),
        )

    def _update_dash(self, direction, is_pressed, dt):
        self._tap_window[direction] = max(0.0, self._tap_window[direction] - dt)

        just_pressed = is_pressed and not self._was_pressed[direction]
        if just_pressed:
            if self._tap_window[direction] > 0:
                self._dash_direction = direction
            self._tap_window[direction] = RUN_TAP_WINDOW

        # Dash lasts until the direction key is released.
        if self._dash_direction == direction and not is_pressed:
            self._dash_direction = None

        self._was_pressed[direction] = is_pressed
