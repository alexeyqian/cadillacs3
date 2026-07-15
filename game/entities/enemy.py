import random

from game.entities.character import Character
from game.entities.enemy_config import get_enemy_config
from game.entities.character_renderer import CharacterRenderer

from game.settings import *
from game.components.hurtbox_component import HurtboxComponent
from game.controllers.loot_drop_controller import LootDropController

class Enemy(Character):
    def __init__(self, x, z, enemy_type, animation_data):
        super().__init__(x, z, animation_data)
        self.width, self.height = ENEMY_W, ENEMY_H # todo: load from config
        self.collision_box_w, self.collision_box_h = ENEMY_COLLISION_W, ENEMY_COLLISION_H
        self.hurtbox_w, self.hurtbox_h = ENEMY_HURTBOX_W, ENEMY_HURTBOX_H

        self.tags.add("enemy")
        self.add_component(LootDropController())

        # Set each frame by EnemyAIManager, before update_intention runs -
        # keeps a crowd from instantly mobbing the player (see that class).
        self.has_attack_slot = False
        self.flank_target = (x, z)

        # Random walk/run toggle while closing in - re-rolled on a timer
        # rather than every frame, see update_intention().
        self._run_decision_timer = 0
        self._is_running = False

        # Which close-range attack (normal/jump/run) to use once in range -
        # re-rolled on a timer rather than every frame, see _roll_close_attack().
        self._attack_choice_timer = 0
        self._attack_choice = "normal"

        config = get_enemy_config(enemy_type)
        self._load_from_config(config)
        self.renderer = CharacterRenderer(self, show_health_bar=True)

    def _load_from_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name

        self.move_speed = config.speed
        self.run_speed = config.run_speed
        self.can_run = config.can_run
        self.jump_power = config.jump_power
        self.jump_air_move_speed = config.jump_air_move_speed
        self.can_jump_attack = config.can_jump_attack
        self.jump_attack_data = config.jump_attack
        self.can_run_attack = config.can_run_attack
        self.run_attack_data = config.run_attack
        self.attack_range = config.attack_range
        self.attack_data = config.attack
        self.score_points = config.score_points

        self.sprite_scale = config.sprite_scale

        self.get_component(HurtboxComponent).configure(config.hurt_box_w, config.hurt_box_h)

    def apply_capability_overrides(self, overrides):
        """Per-spawn tuning from a wave's "capability_overrides" (see
        stage_config.py) - overrides individual attributes already set by
        _load_from_config, e.g. {"can_run": True} to let one spawn of an
        otherwise walk-only archetype run, or {"can_run": False} to keep
        a normally-run-capable spawn walking for a calmer early wave."""
        for key, value in overrides.items():
            setattr(self, key, value)

    def update_intention(self, dt, keys, player_x, player_z):
        dx = player_x - self.x
        dz = player_z - self.z
        in_range = (dx * dx + dz * dz) ** 0.5 <= self.attack_range

        if self.has_attack_slot:
            # Cleared to close in and attack directly.
            if in_range:
                choice = self._roll_close_attack(dt)
                if choice == "run":
                    # run_attack_data has keep_moving=True - keep closing
                    # the last bit of distance through the hit instead of
                    # planting first.
                    self.intent.move_x = 1 if dx > 0 else -1
                    self.intent.move_z = 1 if dz > 0 else -1
                    self.intent.running = True
                    self.intent.wants_attack = True
                    self.intent.wants_jump = False
                    return

                self.intent.move_x = 0
                self.intent.move_z = 0
                self.intent.running = False
                self.intent.wants_attack = True
                self.intent.wants_jump = (choice == "jump")
                return
            self.intent.move_x = 1 if dx > 0 else -1
            self.intent.move_z = 1 if dz > 0 else -1
            self.intent.running = self._roll_running(dt)
            self.intent.wants_attack = False
            self.intent.wants_jump = False
            return

        # No attack slot right now - hold a flanking position around the
        # player instead of piling in for a hit.
        target_x, target_z = self.flank_target
        tdx = target_x - self.x
        tdz = target_z - self.z

        self.intent.move_x = 0 if abs(tdx) < 4 else (1 if tdx > 0 else -1)
        self.intent.move_z = 0 if abs(tdz) < ENEMY_FLANK_Z_TOLERANCE else (1 if tdz > 0 else -1)
        self.intent.running = False
        self.intent.wants_attack = False
        self.intent.wants_jump = False

    def _roll_running(self, dt):
        """Re-decide walk vs. run every ENEMY_RUN_DECISION_DURATION frames
        instead of every tick, so an enemy doesn't flicker between the two
        while closing distance. Heavy archetypes with can_run=False always
        walk."""
        if not self.can_run:
            return False

        self._run_decision_timer -= dt
        if self._run_decision_timer <= 0:
            self._run_decision_timer = ENEMY_RUN_DECISION_DURATION / FPS
            self._is_running = random.random() < ENEMY_RUN_CHANCE
        return self._is_running

    def _roll_close_attack(self, dt):
        """Re-decide which close-range attack to use ("normal"/"jump"/"run")
        every ENEMY_ATTACK_CHOICE_DECISION_DURATION frames instead of every
        tick - same reasoning as _roll_running: commit to one choice for a
        beat rather than flickering. Weighted so archetypes without
        jump/run capability always land on "normal" (the only option), and
        capable ones still throw a normal punch most of the time."""
        self._attack_choice_timer -= dt
        if self._attack_choice_timer > 0:
            return self._attack_choice

        self._attack_choice_timer = ENEMY_ATTACK_CHOICE_DECISION_DURATION / FPS

        options = ["normal"]
        weights = [ENEMY_NORMAL_ATTACK_WEIGHT]
        if self.can_jump_attack and self.jump_attack_data is not None:
            options.append("jump")
            weights.append(ENEMY_JUMP_ATTACK_WEIGHT)
        if self.can_run_attack and self.run_attack_data is not None:
            options.append("run")
            weights.append(ENEMY_RUN_ATTACK_WEIGHT)

        self._attack_choice = random.choices(options, weights=weights, k=1)[0]
        return self._attack_choice

    def is_ready_to_remove(self):
        return not self.alive and self.animation_manager.is_finished()
