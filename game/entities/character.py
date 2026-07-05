from dataclasses import dataclass
import pygame
from game.settings import *
from game.colors import *
from game.entities.game_object import GameObject
from game.components.stats_component import StatsComponent
from game.components.health_component import HealthComponent
from game.components.hurtbox_component import HurtboxComponent
from game.components.hitbox_component import HitboxComponent
from game.components.status_effect_component import StatusEffectComponent
from game.controllers.character_state_machine import CharacterStateMachine
from game.entities.attack_data import AttackData, AttackPhase

@dataclass
class Intent:
    move_x: float = 0.0   # -1, 0, or 1
    move_z: float = 0.0   # -1, 0, or 1
    running: bool = False
    wants_jump: bool = False
    wants_attack: bool = False

class Character(GameObject):
    def __init__(self, x, z):
        super().__init__(x, z)
        self.width, self.height = PLAYER_W, PLAYER_H
        self.alive = True
        self.move_speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.attack_data = None
        self.current_attack: AttackData = None
        self.attack_phase = AttackPhase.FINISHED
        self.attack_phase_timer = 0.0
        self.intent = Intent()

        self.add_component(StatsComponent())
        self.add_component(HealthComponent(100))
        self.add_component(HurtboxComponent())
        self.add_component(HitboxComponent())
        self.add_component(StatusEffectComponent())
        self.add_component(CharacterStateMachine()) # The Master State Machine

    def update_intention(self, dt, keys, player_x, player_z):
        raise NotImplementedError

    def update_movement(self, dt):
        state_machine = self.get_component(CharacterStateMachine)
        attacking = self.attack_phase != AttackPhase.FINISHED
        locked = attacking or not state_machine.can_act()

        if not locked:
            speed = self.move_speed * (2 if self.intent.running else 1)
            self.vx = self.intent.move_x * speed
            self.vz = self.intent.move_z * speed
            if self.intent.move_x != 0:
                self.facing = 1 if self.intent.move_x > 0 else -1

            if self.intent.wants_jump and self.y == 0:
                self.vy = self.jump_power

        self.vy -= 1500 * dt
        self.x += self.vx * dt
        self.z += self.vz * dt
        self.y = max(0.0, self.y + self.vy * dt)
        if self.y == 0:
            self.vy = 0

        # Don't stomp "hit"/"dead" with a movement label - those states
        # aren't in can_act()'s list, so this naturally skips them.
        if state_machine.can_act():
            if self.y > 0:
                state_machine.set_state("jump")
            elif self.intent.move_x != 0 or self.intent.move_z != 0:
                state_machine.set_state("walk")
            else:
                state_machine.set_state("idle")

    def start_attack(self, attack: AttackData):
        state_machine = self.get_component(CharacterStateMachine)
        if not state_machine.can_act():
            return
        if self.attack_phase != AttackPhase.FINISHED:
            return

        self.current_attack = attack
        self.attack_phase = AttackPhase.WINDUP
        self.attack_phase_timer = 0.0
        self.vx = 0  # stop moving during attack
        self.vz = 0

    def update_attack(self, dt):
        if self.intent.wants_attack and self.attack_data:
            self.start_attack(self.attack_data)

        if self.attack_phase == AttackPhase.FINISHED:
            return

        self.attack_phase_timer += dt
        if self.attack_phase == AttackPhase.WINDUP and self.attack_phase_timer >= self.current_attack.windup:
            self._enter_attack_phase(AttackPhase.ACTIVE)
        elif self.attack_phase == AttackPhase.ACTIVE and self.attack_phase_timer >= self.current_attack.active:
            self._enter_attack_phase(AttackPhase.RECOVERY)
        elif self.attack_phase == AttackPhase.RECOVERY and self.attack_phase_timer >= self.current_attack.recovery:
            self._enter_attack_phase(AttackPhase.FINISHED)

        if self.attack_phase != AttackPhase.FINISHED:
            self.get_component(CharacterStateMachine).set_state("attack")

    def _enter_attack_phase(self, new_phase):
        self.attack_phase = new_phase
        self.attack_phase_timer = 0.0

        hitbox = self.get_component(HitboxComponent)
        if new_phase == AttackPhase.ACTIVE and hitbox:
            # knockback direction depends on the attacker's current facing,
            # so it's computed here rather than stored statically on AttackData.
            knockback = (self.current_attack.knockback_velocity * self.facing, 0)
            hitbox.activate(
                self.current_attack.damage,
                knockback,
                self.current_attack.hitbox_w,
                self.current_attack.hitbox_h
            )
        elif new_phase != AttackPhase.ACTIVE and hitbox:
            hitbox.deactivate()

        if new_phase == AttackPhase.FINISHED:
            self.current_attack = None

    def update_animation(self, dt):
        self.animation_manager.update(self.get_component(CharacterStateMachine).state)

    def draw(self, screen, camera_x):
        pass

    def get_frame_rect(self):
        pass
    
    def get_collision_rect(self):
        pass
    
    def get_hurt_rect(self):
        pass
    
    def get_hit_rect(self):
        pass
    
    def draw_debug_boxes(self, screen, camera_x, line_width=1):
        body_rect = self.get_frame_rect()
        collision_rect = self.get_collision_rect()
        hurt_rect = self.get_hurt_rect()
        attack_rect = self.get_attack_rect()

        pygame.draw.rect(screen, WHITE_COLOR, (
            body_rect.x - camera_x,
            body_rect.y,
            body_rect.width,
            body_rect.height,
        ), line_width)

        pygame.draw.rect(screen, BLUE_COLOR, (
            collision_rect.x - camera_x,
            collision_rect.y,
            collision_rect.width,
            collision_rect.height,
        ), line_width)
        pygame.draw.circle(
            screen,
            WHITE_COLOR,
            (int(self.x - camera_x), int(self.y)),
            3,
        )
        
        pygame.draw.rect(screen, GREEN_COLOR, (
            hurt_rect.x - camera_x,
            hurt_rect.y,
            hurt_rect.width,
            hurt_rect.height,
        ), line_width)

        if attack_rect:
            pygame.draw.rect(screen, RED_COLOR, (
                attack_rect.x - camera_x,
                attack_rect.y,
                attack_rect.width,
                attack_rect.height,
            ), line_width)

