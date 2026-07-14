import math
from typing import Optional, List

from game.entities.character import Character
from game.entities.attack_data import AttackPhase, DEFAULT_PLAYER_GRAB_KNEE_DATA
from game.components.health_component import HealthComponent
from game.settings import (
    PLAYER_GRAB_RANGE,
    PLAYER_GRAB_KNEE_HIT_COUNT,
    THROWN_DAMAGE,
    THROWN_KNOCKBACK_X,
    THROWN_KNOCKBACK_Z,
    THROWN_STUN_DURATION,
    PLAYER_THROW_POSE_DURATION,
    FPS,
)
from engine.timer_manager import TimerManager

# How close (x-only) the held target is kept to the player each frame -
# tighter than PLAYER_GRAB_RANGE (the reach used to *start* a grab), just
# enough to read as "held".
_HOLD_OFFSET_X = 40


class GrabController:
    """Auto-grabs the nearest enemy in range, then lets the player knee it
    (reusing Character's normal windup/active/recovery attack machinery)
    for a fixed number of hits before automatically throwing it - the
    Cadillacs & Dinosaurs-style grab combo."""

    def __init__(self):
        self.grabbed_target: Optional[Character] = None
        self.knee_hits_landed = 0
        self._damage_applied_this_swing = False

    def try_grab(self, targets: List[Character]):
        owner = self.owner
        if self.grabbed_target is not None or not owner.can_act():
            return False

        for target in targets:
            if target is owner or not target.alive or target.is_grabbed:
                continue
            # Skip anyone mid hit-stun/attack-recovery from a knockdown or a
            # prior throw - can_act() excludes "hit"/"dead", the same gate
            # normal movement/attacks already respect.
            if not target.can_act():
                continue
            dist = math.hypot(target.x - owner.x, target.z - owner.z)
            if dist <= PLAYER_GRAB_RANGE:
                self._start_grab(target)
                return True
        return False

    def _start_grab(self, target):
        owner = self.owner
        self.grabbed_target = target
        self.knee_hits_landed = 0
        self._damage_applied_this_swing = False

        owner.vx = owner.vz = 0
        owner.set_state("grab")

        target.vx = target.vz = 0
        target.is_grabbed = True
        target.cancel_attack()
        target.set_state("grabbed")

    def update(self, dt, wants_attack):
        """Drives the held target + knee combo. Called from Player.update_attack
        in place of the normal attack flow while a grab is active (or while a
        knee swing it started is still finishing up)."""
        owner = self.owner

        # Another enemy's hit landed on the owner mid-grab (cancel_attack()
        # already reset attack_phase) - drop the target cleanly instead of
        # leaving it frozen in "grabbed" forever with no one driving it.
        if self.grabbed_target is not None and (not owner.alive or owner.state == "hit"):
            self.grabbed_target.set_state("idle")
            self._end_grab()
            return

        if self.grabbed_target is not None:
            target = self.grabbed_target
            target.x = owner.x + _HOLD_OFFSET_X * owner.facing
            target.z = owner.z

        if owner.attack_phase != AttackPhase.FINISHED:
            # A knee swing already in progress - keep ticking it to
            # completion even if the target died/was released mid-swing, so
            # the player's own animation always finishes cleanly rather than
            # freezing on "grab_knee".
            self._tick_knee(dt)
            return

        if self.grabbed_target is None:
            return

        if wants_attack:
            self._start_knee()

    def _start_knee(self):
        owner = self.owner
        self._damage_applied_this_swing = False
        owner.current_attack = DEFAULT_PLAYER_GRAB_KNEE_DATA
        owner.attack_phase = AttackPhase.WINDUP
        owner.attack_timer = 0.0
        owner.set_state("grab_knee")
        self.grabbed_target.set_state("grab_kneed")

    def _tick_knee(self, dt):
        owner = self.owner
        owner._tick_attack_phase(dt)

        if owner.attack_phase == AttackPhase.ACTIVE and not self._damage_applied_this_swing:
            self._damage_applied_this_swing = True
            if self.grabbed_target is not None:
                self._apply_knee_damage()

        if owner.attack_phase == AttackPhase.FINISHED:
            if owner.state == "grab_knee":
                owner.set_state("grab" if self.grabbed_target is not None else "idle")
            # Target may have died/been released mid-swing (see
            # _apply_knee_damage) - only revert its pose if it's still held.
            if self.grabbed_target is not None and self.grabbed_target.state == "grab_kneed":
                self.grabbed_target.set_state("grabbed")
            if self.grabbed_target is not None and self.knee_hits_landed >= PLAYER_GRAB_KNEE_HIT_COUNT:
                self.throw_target()

    def _apply_knee_damage(self):
        target = self.grabbed_target
        health = target.get_component(HealthComponent)
        # ignore_invuln: consecutive knees land closer together than the
        # normal 0.4s post-hit invuln window, which would otherwise eat
        # every knee after the first.
        health.take_damage(DEFAULT_PLAYER_GRAB_KNEE_DATA.damage, (0, 0), ignore_invuln=True)
        self.knee_hits_landed += 1

        if not target.alive:
            target.cancel_attack()
            target.set_state("dead")
            self._award_score(target)
            self._end_grab()

    def throw_target(self):
        owner = self.owner
        target = self.grabbed_target
        if target is None:
            return

        health = target.get_component(HealthComponent)
        # Same invuln concern as the knees - the throw follows the last one
        # within a fraction of a second.
        health.take_damage(
            THROWN_DAMAGE,
            (THROWN_KNOCKBACK_X * owner.facing, THROWN_KNOCKBACK_Z),
            ignore_invuln=True,
        )

        if target.alive:
            target.stun(THROWN_STUN_DURATION / FPS, state="thrown")
        else:
            target.cancel_attack()
            target.set_state("dead")
            self._award_score(target)

        owner.set_state("throw")
        TimerManager.start_timer(
            PLAYER_THROW_POSE_DURATION / FPS,
            lambda: owner.set_state("idle"),
        )

        self._end_grab()

    def _award_score(self, target):
        owner = self.owner
        points = getattr(target, "score_points", 0)
        if points and hasattr(owner, "score"):
            owner.score += points

    def _end_grab(self):
        if self.grabbed_target is not None:
            self.grabbed_target.is_grabbed = False
        self.grabbed_target = None
        self.knee_hits_landed = 0
        self._damage_applied_this_swing = False
