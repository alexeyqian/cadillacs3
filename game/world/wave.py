from typing import Optional
from dataclasses import dataclass
from game.settings import SCREEN_WIDTH
from game.factories.enemy_factory import EnemyFactory


@dataclass
class SpawnInstruction:
    enemy_type: str
    side: str = "right"
    capability_overrides: Optional[dict] = None


@dataclass
class PendingSpawn:
    enemy_type: str
    x: int
    y: int = 540
    delay: int = 60
    capability_overrides: Optional[dict] = None


class Wave:
    def __init__(self, stage, trigger_x, spawn_instructions, max_active=4):
        self.stage = stage
        self.trigger_x = trigger_x
        self.started = False
        self.completed = False
        self.max_active = max_active
        self.spawn_instructions = spawn_instructions
        self.pending_spawns = []
        self.spawn_timer = 0

    def start(self, camera_x=0):
        self.started = True
        self.spawn_timer = 0
        self.pending_spawns = []

        viewport_left = camera_x
        viewport_right = camera_x + SCREEN_WIDTH
        spawn_inset = 50  # pixels inside the viewport edge
        for instruction in self.spawn_instructions:
            if instruction.side == "left":
                spawn_x = viewport_left + spawn_inset
            else:
                spawn_x = viewport_right - spawn_inset

            self.pending_spawns.append(PendingSpawn(
                enemy_type=instruction.enemy_type,
                x=spawn_x,
                y=instruction.y if instruction.y is not None else 540,
                delay=instruction.delay if instruction.delay is not None else 60,
                capability_overrides=instruction.capability_overrides,
            ))

        if self.pending_spawns:
            self.spawn_timer = self.pending_spawns[0].delay

    # todo: separate spawn logic from tick logic, so that we can spawn multiple enemies per tick if needed
    def tick(self, active_enemy_count=0):
        """Tick one frame. Returns a list of newly spawned enemies (0 or 1)."""
        if not self.pending_spawns:
            return []
        if active_enemy_count >= self.max_active:
            return []

        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            return []

        pending = self.pending_spawns.pop(0)
        enemy = EnemyFactory.create_enemy(
            pending.enemy_type,
            pending.x,
            pending.y,
            capability_overrides=pending.capability_overrides,
        )
        self.spawn_timer = self.pending_spawns[0].delay if self.pending_spawns else 0
        self.stage.enemies.append(enemy)
        return [enemy]

    def is_spawning_done(self):
        return not self.pending_spawns