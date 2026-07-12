from game.settings import SCREEN_WIDTH
from game.world.lane import Lane
from game.world.wave import SpawnInstruction, Wave
from game.world.stage_exit import StageExit
from game.world.stage_intro import StageIntro
from game.world.background import Background
from game.entities.breakable_object import BreakableObject
# from game.entities.explosive_barrel import ExplosiveBarrel
from game.entities.weapon import Weapon
from game.managers.floating_text_manager import FloatingTextManager
from game.managers.warning_manager import WarningManager

class Stage:
    def __init__(self, camera, player, stage_data):
        self.camera = camera
        self.player = player
        self.enemies = []
        self.floating_text_manager = FloatingTextManager()
        self.warning_manager = WarningManager()
        # (min_x, max_x) while a wave's arena is locked - camera frozen,
        # player/enemies walled to the current screen. None means no lock;
        # movement falls back to the full stage bounds.
        self.locked_arena_bounds = None
        self._load_from_data(stage_data)
        self.exit = StageExit(self.exit_rect)
        self.intro = StageIntro(player, camera, stage_data.get("intro"))

    def get_all_characters(self):
        return [self.player] + self.enemies

    def get_all_entities(self):
        # Non-character entities (weapons, projectiles, breakables) aren't
        # Characters and don't belong in get_all_characters().
        return self.get_all_characters() + []

    def update(self, dt):
        self._update_waves()
        self.floating_text_manager.update(dt)
        self.warning_manager.update(dt)
        self.exit.update(dt)

        # The exit only responds to being touched once there's nothing
        # left to fight - matches the "clear waves, then leave" flow.
        if self.current_wave is None:
            self.exit.try_open(self.player.get_collision_rect())

    def is_complete(self):
        if self.completion == "clear_waves_then_exit" and self.current_wave is not None:
            return False
        if not self.exit.is_open:
            return False
        return self.player.get_collision_rect().colliderect(self.exit.rect)

    def clamp_characters_to_bounds(self):
        if self.locked_arena_bounds:
            min_x, max_x = self.locked_arena_bounds
        else:
            min_x, max_x = 0, self.world_width

        for character in self.get_all_characters():
            character.x = max(min_x, min(character.x, max_x))
            character.z = max(self.lane_top, min(character.z, self.lane_bottom))

    def _update_waves(self):
        wave = self.current_wave
        if wave is None:
            return  # no wave active - either none configured, or all cleared

        if not wave.started:
            if self.player.x < wave.trigger_x:
                return
            wave.start(self.camera.x)
            self._lock_arena(self.camera.x)
            message = "BOSS AHEAD!" if wave.has_boss else "WAVE OF ENEMIES"
            self.warning_manager.show(message)

        wave.tick(len(self.enemies)) # appends any newly spawned enemy to self.enemies

        if wave.is_cleared():
            wave.completed = True
            self._unlock_arena()
            self._advance_to_next_wave()

    def _advance_to_next_wave(self):
        self.current_wave_index += 1
        self.current_wave = (
            self.waves[self.current_wave_index]
            if self.current_wave_index < len(self.waves)
            else None
        )

    def _lock_arena(self, camera_x):
        self.camera.locked = True
        self.camera.locked_x = camera_x
        self.locked_arena_bounds = (camera_x, camera_x + SCREEN_WIDTH)

    def _unlock_arena(self):
        self.camera.locked = False
        self.locked_arena_bounds = None

    def update_clean(self):
        self.enemies[:] = [e for e in self.enemies if not e.is_ready_to_remove()]
        #self.projectiles[:] = [p for p in self.projectiles if p.active]
        #self.enemy_projectiles[:] = [p for p in self.enemy_projectiles if p.active]
        #self.objects[:] = [o for o in self.objects if o.hp > 0]
        #self.loot_items[:] = [l for l in self.loot_items if l.active]
        #self.hit_sparks[:] = [s for s in self.hit_sparks if s.active]
        #self.floating_texts[:] = [t for t in self.floating_texts if t.active]
        #self.explosions[:] = [e for e in self.explosions if e.active]

    def _load_from_data(self, stage_data):
        self.stage_id = stage_data["id"]
        self.stage_name = stage_data["name"]
        self.world_width = stage_data["world_width"]
        self.world_height = stage_data["world_height"]
        self.exit_rect = stage_data["exit_rect"]
        self.completion = stage_data["completion"]

        self.lane_top = stage_data["lane_top"]
        self.lane_bottom = stage_data["lane_bottom"]
        self.lane_system = Lane(self.lane_top, self.lane_bottom)

        self.waves = self._build_waves(stage_data["waves"])
        self.current_wave_index = 0
        self.current_wave = self.waves[0] if self.waves else None

        self.background = Background(stage_data["background"], self.world_width)

    def _build_waves(self, wave_configs):
        waves = []
        for wave_config in wave_configs:
            spawn_instructions = []
            for spawn_config in wave_config["spawns"]:
                count = spawn_config.get("count", 1)
                for _ in range(count):
                    spawn_instructions.append(SpawnInstruction(
                        enemy_type=spawn_config["enemy_type"],
                        side=spawn_config.get("side", "right"),
                        y=spawn_config.get("y"),
                        delay=spawn_config.get("delay"),
                        capability_overrides=spawn_config.get("capability_overrides"),
                    ))

            waves.append(Wave(
                stage=self,
                trigger_x=wave_config["trigger_x"],
                spawn_instructions=spawn_instructions,
                max_active=wave_config.get("max_active", 4),
                has_boss=wave_config.get("has_boss", False),
            ))
        return waves
    
    def _create_weapons(self, stage_data):
        return [
            Weapon(wc["x"], wc["y"], wc["type"])
            for wc in stage_data["weapons"]
        ]

    def _create_objects(self, stage_data):
        objects = []
        for oc in stage_data["objects"]:
            kind = oc["kind"]
            if kind == "breakable":
                objects.append(BreakableObject(oc["x"], oc["y"], loot_type=oc.get("loot_type")))
            #elif kind == "barrel":
            #    objects.append(ExplosiveBarrel(oc["x"], oc["y"]))
        return objects
