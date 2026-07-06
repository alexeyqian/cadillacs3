from dataclasses import dataclass
import pygame
from game.settings import *
from game.colors import *
from engine.timer_manager import TimerManager
from game.entities.entity import Entity
from game.components.stats_component import StatsComponent
from game.components.health_component import HealthComponent
from game.components.collision_box_component import CollisionBoxComponent
from game.components.hurtbox_component import HurtboxComponent
from game.components.hitbox_component import HitboxComponent
from game.components.status_effect_component import StatusEffectComponent
from game.entities.attack_data import AttackData, AttackPhase
from game.animation.animation_manager import AnimationManager


@dataclass
class Intent:
    """What this entity wants to do this frame - written by update_intention(),
    consumed by update_movement()/update_attack(). Keeping this a separate
    snapshot (rather than mutating physics/attack state directly) is what lets
    every entity's update_intention() run before anyone's update_movement()."""
    move_x: float = 0.0   # -1, 0, or 1
    move_z: float = 0.0   # -1, 0, or 1
    running: bool = False
    wants_jump: bool = False
    wants_attack: bool = False


class Character(Entity):
    """Base for Player/Enemy. Each frame, the main loop drives these phases
    in order: update_intention -> update_movement -> update_attack -> update_animation.
    """

    # States in which the character still responds to intent-driven
    # movement/attack. "hit" and "dead" are deliberately excluded, so a
    # stun or death naturally overrides whatever the player/AI is asking for.
    ACTIONABLE_STATES = {"idle", "walk", "run", "jump", "attack", "attack2", "attack3", "run_attack", "chase"}

    def __init__(self, x, z, animation_data):
        super().__init__(x, z)
        # default values, real values load from player or enemy's config
        self.width, self.height = PLAYER_W, PLAYER_H
        self.collision_box_w, self.collision_box_h = PLAYER_COLLISION_W, PLAYER_COLLISION_H
        self.hurtbox_w, self.hurtbox_h = PLAYER_HURTBOX_W, PLAYER_HURTBOX_H

        self.sprite_scale = 1.0
        self.alive = True

        # State machine: gates which actions are currently allowed.
        self.state = "idle"
        self.hit_stun_timer = None

        # Physics tuning, overridden per character type in _load_from_config.
        self.move_speed = 0
        self.run_speed = 0
        self.jump_power = 0
        self.jump_air_move_speed = 0

        self.intent = Intent()

        # Attack phase state machine: WINDUP -> ACTIVE -> RECOVERY -> FINISHED.
        self.attack_data = None # single basic attack, used when combo_attacks is empty
        self.run_attack_data = None # used instead of attack_data while intent.running
        self.combo_attacks = [] # e.g. [attack1, attack2, attack3]; empty means no combo chain
        self.combo_index = 0 # index into combo_attacks that the next press will start
        self.combo_window_timer = 0.0 # time left to continue the combo before it resets to hit 1
        self.current_attack: AttackData = None
        self.attack_phase = AttackPhase.FINISHED
        self.attack_timer = 0.0
        self.attack_cooldown_timer = 0.0

        self.add_component(StatsComponent())
        self.add_component(HealthComponent(100))
        self.add_component(CollisionBoxComponent(self.collision_box_w, self.collision_box_h))
        self.add_component(HurtboxComponent(self.hurtbox_w, self.hurtbox_h))
        self.add_component(HitboxComponent())
        self.add_component(StatusEffectComponent())
        self.animation_manager = AnimationManager(animation_data)

    # --- State machine -----------------------------------------------------

    def can_act(self):
        return self.state in self.ACTIONABLE_STATES

    def set_state(self, new_state: str):
        if self.state == "dead":
            return
        self.state = new_state

    def stun(self, duration):
        if self.hit_stun_timer:
            self.hit_stun_timer.cancel()
        self.cancel_attack()
        self.set_state("hit")
        self.hit_stun_timer = TimerManager.start_timer(duration, lambda: self.set_state("idle"))

    def cancel_attack(self):
        """Interrupts any in-progress attack. Without this, a hit landing
        mid-windup would leave attack_phase ticking toward ACTIVE while the
        animation has already switched to "hit" - which has no hitbox data
        to read, crashing _enter_attack_phase."""
        hitbox = self.get_component(HitboxComponent)
        if hitbox:
            hitbox.deactivate()
        self.attack_phase = AttackPhase.FINISHED
        self.current_attack = None
        self.combo_index = 0

    # --- Per-frame phases, called by the main loop in this order -----------

    def update_intention(self, dt, keys, player_x, player_z):
        raise NotImplementedError

    def update_movement(self, dt):
        if not self._is_action_locked():
            self._apply_intent_to_velocity()

        self._apply_move_and_gravity(dt)
        self._refresh_movement_state()

    def update_attack(self, dt):
        self.attack_cooldown_timer = max(0.0, self.attack_cooldown_timer - dt)
        self.combo_window_timer = max(0.0, self.combo_window_timer - dt)

        if self.intent.wants_attack:
            self._try_start_next_attack()

        if self.attack_phase == AttackPhase.FINISHED:
            return

        self._tick_attack_phase(dt)
        # Phase timing/hitbox keep ticking regardless, but don't let this
        # stomp "hit"/"dead" - set_state() only guards "dead", not "hit".
        if self.attack_phase != AttackPhase.FINISHED and self.can_act():
            self.set_state(self.current_attack.name)

    def _try_start_next_attack(self):
        if self.intent.running and self.run_attack_data:
            self._try_start_attack(self.run_attack_data)
            return

        if not self.combo_attacks:
            if self.attack_data:
                self._try_start_attack(self.attack_data)
            return

        # Window expired (or this is the first press, or the last hit just
        # finished with no window at all) - next press starts a fresh chain.
        if self.combo_window_timer <= 0:
            self.combo_index = 0

        if self._try_start_attack(self.combo_attacks[self.combo_index]):
            self.combo_index = min(self.combo_index + 1, len(self.combo_attacks) - 1)

    def update_animation(self, dt):
        self.animation_manager.update(self.state)

    def draw(self, screen, camera_x):
        self.renderer.draw(screen, camera_x)

    # --- Movement helpers ---------------------------------------------------

    def _is_action_locked(self):
        """True while mid-attack or otherwise unable to act (hit/dead) -
        intent-driven velocity/state changes are suppressed in that case,
        though any existing velocity (e.g. knockback) keeps integrating.
        Attacks with keep_moving (e.g. a run attack) are the exception -
        intent still drives movement while they're in progress."""
        is_attacking = self.attack_phase != AttackPhase.FINISHED
        moves_during_attack = is_attacking and self.current_attack and self.current_attack.keep_moving
        return (is_attacking and not moves_during_attack) or not self.can_act()

    def _apply_intent_to_velocity(self):
        airborne = self.y > 0
        if airborne:
            speed = self.jump_air_move_speed
        else:
            speed = self.run_speed if self.intent.running else self.move_speed

        self.vx = self.intent.move_x * speed
        self.vz = self.intent.move_z * speed
        if self.intent.move_x != 0:
            self.facing = 1 if self.intent.move_x > 0 else -1

        if self.intent.wants_jump and self.y == 0:
            self.vy = self.jump_power

    def _apply_move_and_gravity(self, dt):
        self.x += self.vx * dt
        self.z += self.vz * dt

        self.vy -= GRAVITY * dt
        self.y = max(0.0, self.y + self.vy * dt)
        if self.y == 0:
            self.vy = 0

    def _refresh_movement_state(self):
        # Skipped while "hit"/"dead" (not in ACTIONABLE_STATES), so a
        # movement label can't stomp those over the frames they last.
        if not self.can_act():
            return
        if self.y > 0:
            self.set_state("jump")
        elif self.intent.move_x != 0 or self.intent.move_z != 0:
            self.set_state("run" if self.intent.running else "walk")
        else:
            self.set_state("idle")

    # --- Attack helpers ------------------------------------------------------

    def _try_start_attack(self, attack: AttackData) -> bool:
        if not self.can_act() or self.attack_phase != AttackPhase.FINISHED:
            return False
        if self.attack_cooldown_timer > 0:
            return False

        self.current_attack = attack
        self.attack_phase = AttackPhase.WINDUP
        self.attack_timer = 0.0
        if not attack.keep_moving:
            self.vx = 0  # stop moving during attack
            self.vz = 0
        return True

    def _tick_attack_phase(self, dt):
        self.attack_timer += dt
        attack = self.current_attack
        if self.attack_phase == AttackPhase.WINDUP and self.attack_timer >= attack.windup:
            self._enter_attack_phase(AttackPhase.ACTIVE)
        elif self.attack_phase == AttackPhase.ACTIVE and self.attack_timer >= attack.active:
            self._enter_attack_phase(AttackPhase.RECOVERY)
        elif self.attack_phase == AttackPhase.RECOVERY and self.attack_timer >= attack.recovery:
            self._enter_attack_phase(AttackPhase.FINISHED)

    def _enter_attack_phase(self, new_phase):
        self.attack_phase = new_phase
        self.attack_timer = 0.0

        hitbox = self.get_component(HitboxComponent)
        if new_phase == AttackPhase.ACTIVE and hitbox:
            # Knockback direction depends on the attacker's current facing,
            # so it's computed here rather than stored statically on AttackData.
            knockback = (self.current_attack.knockback_velocity * self.facing, 0)

            # todo: use hitbox in attack data instead of animation config
            frame = self.animation_manager.get_current_frame()
            animation_hitbox = getattr(frame, "hitbox", None)

            hitbox.activate(
                self.current_attack.damage,
                knockback,
                animation_hitbox[0], # offset_x
                animation_hitbox[1], # offset_z
                animation_hitbox[2], # hitbox_w
                animation_hitbox[3]  # hitbox_h
                #self.current_attack.hitbox_w,
                #self.current_attack.hitbox_h
            )
        elif new_phase != AttackPhase.ACTIVE and hitbox:
            hitbox.deactivate()

        if new_phase == AttackPhase.FINISHED:
            self.attack_cooldown_timer = self.current_attack.cooldown
            self.combo_window_timer = self.current_attack.combo_window
            self.current_attack = None

    def get_collision_rect(self):
        return self.get_component(CollisionBoxComponent).get_rect()

    def get_hurt_rect(self):
        return self.get_component(HurtboxComponent).get_rect()
    
    def get_hit_rect(self):
        hitbox = self.get_component(HitboxComponent)
        if hitbox and hitbox.active:
            return hitbox.get_rect()
        return None

    def get_frame_rect(self):
        frame = self.animation_manager.get_current_frame()
        scale = self.sprite_scale
        offset_x, offset_y = frame.offset

        frame_w = frame.image.get_width() * scale
        frame_h = frame.image.get_height() * scale
        offset_x *= scale
        offset_y *= scale

        if self.facing:
            world_x = self.x + offset_x
        else:
            world_x = self.x - frame_w - offset_x

        # -y for jumping when needed
        world_y = self.z - self.y + offset_y

        return pygame.Rect(
            int(world_x),
            int(world_y),
            int(frame_w),
            int(frame_h),
        )

    # todo: deprecated
    def _convert_box_to_world_rect(self, box):
        anchor_x = self.x
        anchor_z = self.z # todo: update anchor_z if jumping
        facing_right = self.facing

        if facing_right:
            world_x = anchor_x + box.x
        else:
            world_x = anchor_x - box.x - box.width

        return pygame.Rect(
            int(world_x),
            int(anchor_z + box.y),
            int(box.width),
            int(box.height)
        )