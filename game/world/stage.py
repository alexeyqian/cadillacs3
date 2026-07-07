from game.world.lane import Lane
from game.world.wave import SpawnInstruction, Wave
from game.world.background import Background
from game.entities.breakable_object import BreakableObject
# from game.entities.explosive_barrel import ExplosiveBarrel
from game.entities.weapon import Weapon
from game.managers.floating_text_manager import FloatingTextManager

class Stage:
    def __init__(self, camera, player, stage_data):
        self.camera = camera
        self.player = player
        self.enemies = []
        self.floating_text_manager = FloatingTextManager()
        self._load_from_data(stage_data)

    def get_all_characters(self):
        return [self.player] + self.enemies

    def get_all_entities(self):
        # Non-character entities (weapons, projectiles, breakables) aren't
        # Characters and don't belong in get_all_characters().
        return self.get_all_characters() + []

    def update(self, dt):
        self._update_waves()
        self.floating_text_manager.update(dt)

    def _update_waves(self):
        for wave in self.waves:
            if wave.completed:
                continue

            if not wave.started:
                if self.player.x < wave.trigger_x:
                    continue
                wave.start(self.camera.x)

            wave.tick(len(self.enemies)) # appends any newly spawned enemy to self.enemies

            if wave.is_spawning_done():
                wave.completed = True

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

        far = stage_data.get("background_far", stage_data["background"])
        mid = stage_data.get("background_mid", stage_data["background"])
        self.background = Background(
            far,
            mid_file=mid,
            front_file=stage_data.get("background_front"),
        )

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
